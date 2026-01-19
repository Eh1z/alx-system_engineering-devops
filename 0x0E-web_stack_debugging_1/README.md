# Web Stack Debugging 1 - Port Configuration & Service Management

## Scenario Overview

This debugging scenario focuses on Nginx port binding issues and service configuration - common problems in production web stacks that require systematic troubleshooting.

## Problem Context

Web servers must bind to network ports to accept incoming connections. When port binding fails, the service cannot start, resulting in connection refused errors for clients. This represents a critical production outage scenario.

## Common Causes

### 1. Port Already in Use
Another process is already listening on the desired port (typically 80 or 443).

**Diagnosis:**
```bash
netstat -tulpn | grep :80
lsof -i :80
ss -tulpn | grep :80
```

**Resolution:**
- Identify conflicting process
- Stop conflicting service or change port
- Update configuration accordingly

### 2. Configuration Error
Nginx configuration has syntax errors or invalid directives preventing startup.

**Diagnosis:**
```bash
nginx -t  # Test configuration
journalctl -u nginx -n 50  # Check service logs
```

**Resolution:**
- Fix configuration syntax
- Validate with `nginx -t`
- Reload service

### 3. Permission Issues
Nginx process lacks permission to bind to privileged ports (<1024).

**Diagnosis:**
```bash
ps aux | grep nginx  # Check user nginx runs as
cat /etc/nginx/nginx.conf | grep user
```

**Resolution:**
- Ensure nginx master runs as root
- Workers can run as www-data/nginx user
- Check file permissions for config files

### 4. Service Not Enabled
Service configured but not enabled for automatic startup.

**Diagnosis:**
```bash
systemctl status nginx
systemctl is-enabled nginx
```

**Resolution:**
```bash
systemctl enable nginx  # Enable auto-start
systemctl start nginx   # Start service
```

## Debugging Methodology

### 1. Check Service Status
```bash
systemctl status nginx
# Output shows: active, inactive, failed
```

### 2. Examine Logs
```bash
journalctl -u nginx -n 100 --no-pager
tail -f /var/log/nginx/error.log
```

### 3. Validate Configuration
```bash
nginx -t
# Outputs: syntax is ok, test is successful
```

### 4. Check Port Availability
```bash
netstat -tulpn | grep :80
# Empty output = port available
# Output with PID = port in use
```

### 5. Test Connectivity
```bash
curl -I http://localhost
# 200 OK = working
# Connection refused = service not running
```

## Systematic Resolution Steps

1. **Gather information** - Status, logs, configuration
2. **Identify root cause** - Which component is failing?
3. **Implement fix** - Address the specific issue
4. **Verify resolution** - Test that service works
5. **Document** - Record issue and solution

## Production Considerations

### Monitoring
- Service health checks every 30 seconds
- Alert on service down > 1 minute
- Track restart frequency (high = underlying issue)

### High Availability
- Multiple web servers behind load balancer
- Graceful restarts (zero-downtime deployments)
- Automated failover on service failure

### Prevention
- Configuration validation in CI/CD pipeline
- Canary deployments (test on subset first)
- Automated testing before production
- Infrastructure as code for consistency

## Related Concepts

- **systemd** - Modern Linux service manager
- **Port binding** - Network socket operations
- **Process management** - Start, stop, reload services
- **Configuration management** - Maintaining consistent configs
- **Service discovery** - How services find each other

## Key Learnings

1. **Test configurations before applying** - Catch errors early
2. **Check logs first** - They usually tell you the problem
3. **Understand service dependencies** - What must start first?
4. **Know your debugging tools** - systemctl, journalctl, netstat
5. **Document solutions** - Build knowledge base for team

---

*This debugging scenario demonstrates systematic troubleshooting approach essential for maintaining production web infrastructure.*
