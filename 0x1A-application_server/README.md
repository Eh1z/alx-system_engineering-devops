# Application Server Configuration & Deployment

## Problem Statement

Web applications need more than just a web server. Static file serving (Nginx, Apache) is insufficient for dynamic applications. You need an application server to:
- Execute application code (Python, Ruby, Node.js, etc.)
- Manage application processes and resources
- Handle application-level logic and business rules
- Connect to databases and external services

## Architecture Overview

### Modern Web Application Stack

```
Internet Traffic
    ↓
Nginx (Reverse Proxy / Web Server)
    ↓ (proxy_pass)
Gunicorn (WSGI Application Server)
    ↓
Python Application (Flask/Django)
    ↓
Database / External Services
```

**Why This Architecture:**

**Nginx (Frontend):**
- Handles SSL/TLS termination
- Serves static files efficiently (images, CSS, JS)
- Acts as reverse proxy to application server
- Load balancing across multiple application instances
- Request buffering and rate limiting

**Gunicorn (Application Server):**
- Manages Python application processes (workers)
- Handles concurrent requests
- Process management (restart failed workers)
- Resource isolation per worker

**Python Application:**
- Business logic
- Dynamic content generation
- Database interactions
- API endpoints

## Key Concepts

### 1. WSGI (Web Server Gateway Interface)

**What is WSGI?**
- Standard interface between web servers and Python applications
- Allows any WSGI-compliant server to run any WSGI-compliant application
- Defined in PEP 3333

**Why WSGI Matters:**
- **Portability:** Switch between Gunicorn, uWSGI, mod_wsgi without app changes
- **Standardization:** Common interface across Python frameworks
- **Ecosystem:** Rich tooling and middleware

**WSGI Flow:**
```python
# Simplest WSGI application
def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)
    return [b'Hello World']
```

### 2. Application Server vs Web Server

**Web Server (Nginx, Apache):**
- Optimized for static content
- Handles HTTP protocol efficiently
- SSL/TLS termination
- Connection management
- Not designed for running application code

**Application Server (Gunicorn, uWSGI):**
- Executes application code
- Process/thread management
- Application-specific protocol (WSGI, ASGI)
- Resource management for workers
- Not optimized for static content

**Why Both?**
- Nginx: Fast at what it does (static files, SSL, proxying)
- Gunicorn: Fast at what it does (Python execution)
- Separation of concerns
- Each component optimized for its role

### 3. Process Management with systemd

**Why systemd?**
- Start services automatically on boot
- Restart failed services
- Manage service dependencies
- Centralized logging (journalctl)
- Resource limits and isolation

**Service Unit File Structure:**
```ini
[Unit]
Description=Gunicorn application server
After=network.target  # Start after network is available

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/app
ExecStart=/usr/bin/gunicorn app:app
Restart=always  # Auto-restart on failure

[Install]
WantedBy=multi-user.target  # Enable on boot
```

### 4. Reverse Proxy Pattern

**What is a Reverse Proxy?**
- Server that forwards client requests to backend servers
- Client thinks it's talking directly to the proxy
- Backend servers are hidden from clients

**Benefits:**
- **SSL Termination:** Handle HTTPS at proxy, HTTP to backend
- **Load Balancing:** Distribute across multiple backends
- **Caching:** Serve cached content without hitting backend
- **Security:** Hide internal architecture, add firewall rules
- **Static Content:** Serve directly from proxy (faster)

**Nginx Reverse Proxy Config:**
```nginx
location / {
    proxy_pass http://127.0.0.1:8000;  # Forward to Gunicorn
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

## Gunicorn Configuration

### Worker Types

**Sync Workers (Default):**
- One request per worker at a time
- Blocking I/O
- Simple and stable
- Good for CPU-bound tasks

**Async Workers (gevent, eventlet):**
- Handle multiple requests per worker
- Non-blocking I/O
- Good for I/O-bound tasks (API calls, database queries)
- More complex, harder to debug

**Worker Calculation:**
```
# Rule of thumb: (2 x CPU cores) + 1
# Example: 4-core server = (2 x 4) + 1 = 9 workers

# Why this formula?
# - 2 workers per core: Keep cores busy during I/O
# - +1: Handle incoming requests while others process
```

### Gunicorn Command Line
```bash
# Basic usage
gunicorn app:app

# Production configuration
gunicorn \
    --workers 9 \
    --worker-class gevent \
    --bind 127.0.0.1:8000 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    --log-level info \
    --timeout 30 \
    --graceful-timeout 30 \
    app:app
```

**Key Options:**

| Option | Purpose | Production Value |
|--------|---------|------------------|
| `--workers` | Number of worker processes | (2 x CPUs) + 1 |
| `--worker-class` | Worker type (sync/async) | gevent for I/O-bound |
| `--bind` | Listen address:port | 127.0.0.1:8000 (behind proxy) |
| `--timeout` | Worker silence timeout | 30-60 seconds |
| `--graceful-timeout` | Graceful shutdown time | 30 seconds |
| `--max-requests` | Restart worker after N requests | 1000 (prevent memory leaks) |
| `--preload` | Load app before forking | True (save memory) |

## Nginx Configuration for Application Server

### Basic Reverse Proxy
```nginx
server {
    listen 80;
    server_name example.com;

    # Static files served directly by Nginx
    location /static/ {
        alias /var/www/app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Application requests proxied to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        
        # Preserve client information
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout configuration
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }
}
```

### Production Enhancements
```nginx
# SSL/TLS configuration
server {
    listen 443 ssl http2;
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=app:10m rate=10r/s;
    limit_req zone=app burst=20 nodelay;
    
    # Rest of configuration...
}
```

## Deployment Workflow

### 1. Deploy Application Code
```bash
# Clone/update application
cd /var/www
git pull origin main

# Install dependencies
pip install -r requirements.txt

# Run migrations (if applicable)
python manage.py migrate
```

### 2. Configure Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/myapp.service

# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable myapp

# Start service
sudo systemctl start myapp

# Check status
sudo systemctl status myapp
```

### 3. Configure Nginx
```bash
# Create site configuration
sudo nano /etc/nginx/sites-available/myapp

# Enable site
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### 4. Verify Deployment
```bash
# Check Gunicorn is running
ps aux | grep gunicorn

# Check listening ports
netstat -tlnp | grep :8000

# Check Nginx status
sudo systemctl status nginx

# Test application
curl http://localhost
curl https://example.com
```

## Production Considerations

### High Availability
- **Multiple Workers:** Handle concurrent requests
- **Worker Restarts:** Graceful rolling restarts
- **Health Checks:** Nginx checks backend health
- **Process Supervision:** systemd auto-restarts failures

### Performance Optimization
- **Connection Pooling:** Reuse database connections
- **Caching:** Redis/Memcached for frequently accessed data
- **Static Files:** Serve from Nginx, not application
- **CDN:** Offload static assets to CDN
- **Compression:** Gzip/Brotli at Nginx level

### Security
- **Process Isolation:** Run as non-root user (www-data)
- **Firewall:** Only expose Nginx, not Gunicorn
- **SSL/TLS:** HTTPS everywhere, redirect HTTP
- **Security Headers:** HSTS, CSP, X-Frame-Options
- **Rate Limiting:** Prevent abuse/DoS

### Monitoring
- **Application Logs:** Gunicorn access/error logs
- **Web Server Logs:** Nginx access/error logs
- **System Logs:** journalctl for systemd services
- **Metrics:** Response times, error rates, worker status
- **Health Endpoints:** /health for load balancer checks

## Common Issues & Solutions

### 1. "502 Bad Gateway"
**Cause:** Nginx can't reach Gunicorn
**Debug:**
```bash
# Is Gunicorn running?
systemctl status myapp

# Is it listening?
netstat -tlnp | grep :8000

# Check Gunicorn logs
journalctl -u myapp -n 50
```

### 2. High Memory Usage
**Cause:** Memory leaks in application
**Solution:**
```python
# Restart workers periodically
gunicorn --max-requests 1000 app:app
```

### 3. Slow Response Times
**Cause:** Too few workers or slow code
**Debug:**
```bash
# Check worker count
ps aux | grep gunicorn | wc -l

# Monitor resource usage
top -p $(pgrep -d, gunicorn)

# Profile application
# Use Python profilers (cProfile, line_profiler)
```

### 4. Workers Timing Out
**Cause:** Long-running requests
**Solution:**
```python
# Increase timeout
gunicorn --timeout 120 app:app

# Or move long tasks to background queue (Celery)
```

## Key Learnings

1. **Separation of concerns** - Web server vs application server
2. **Process management matters** - systemd provides reliability
3. **Reverse proxy pattern** - Security, performance, flexibility
4. **Worker tuning critical** - Right worker count/type for workload
5. **Monitoring essential** - Logs, metrics, health checks

## Proposed Improvements

**Short-term:**
1. Add health check endpoint
2. Implement graceful shutdown handling
3. Set up log rotation
4. Configure automated SSL renewal

**Long-term:**
1. Containerize application (Docker)
2. Implement blue-green deployments
3. Add application performance monitoring
4. Auto-scaling based on load
5. Multi-region deployment

## Related Projects

- `0x0F-load_balancer`: Load balance across multiple app servers
- `0x18-webstack_monitoring`: Monitor application server health
- `0x0A-configuration_management`: Automate deployment with Puppet

---

*This implementation demonstrates understanding of production application deployment, process management, and modern web architecture patterns.*
