# Web Stack Debugging - Systematic Troubleshooting

## Problem Statement

Production systems fail. Services crash, configurations break, resources exhaust. The difference between junior and senior engineers isn't whether they encounter problems—it's how systematically they debug them.

This project demonstrates methodical debugging approaches, root cause analysis, and production incident response patterns.

## Debugging Methodology

### The Systematic Approach

1. **Identify the symptom** - What's actually broken?
2. **Gather information** - Logs, metrics, process state
3. **Form hypothesis** - What could cause this?
4. **Test hypothesis** - Verify each theory
5. **Implement fix** - Resolve root cause, not symptoms
6. **Verify resolution** - Confirm problem is solved
7. **Document** - Record issue and solution

## Scenario Breakdown

### Scenario: Apache Not Responding (0x0D-web_stack_debugging_0)

**Symptom:** HTTP requests to server return no response

**Investigation Process:**

```bash
# Check if Apache is running
ps aux | grep apache2
# Result: No Apache processes found

# Check Apache service status
service apache2 status
# Result: Service is stopped

# Check if port 80 is in use
netstat -tulpn | grep :80
# Result: Nothing listening on port 80
```

**Root Cause:** Apache service not started

**Solution:**
```bash
#!/usr/bin/env bash
# Start Apache service to serve web requests
sudo service apache2 start
```

**Why This Works:**
- Addresses root cause (service not running)
- Simple, direct solution
- Idempotent (can run multiple times safely)

**Production Considerations:**
- Why did service stop? Check logs
- Should service auto-start on boot?
- Need monitoring/alerting for service status
- Consider using systemd for better service management

### Advanced Debugging Scenarios

#### Web Stack Debugging 1 (0x0E)
**Typical Issues:**
- Port binding conflicts
- Permission problems
- Configuration file errors
- Process management failures

**Debugging Tools:**
```bash
# Service status
systemctl status nginx
journalctl -u nginx

# Port usage
netstat -tulpn | grep :80
ss -tulpn | grep :80

# Process information
ps aux | grep nginx
pstree -p

# Configuration validation
nginx -t

# Log analysis
tail -f /var/log/nginx/error.log
```

#### Web Stack Debugging 3 (0x17)
**Focus:** Automated debugging with Puppet

**Problem:** Manual fixes don't scale

**Solution:** 
- Diagnose issue
- Write Puppet manifest to fix
- Automated, repeatable resolution

**Benefits:**
- Consistent across all servers
- Version controlled
- Auditable
- Self-documenting

#### Web Stack Debugging 4 (0x1B)
**Focus:** Performance optimization

**Common Issues:**
- Too many connections
- Resource limits (file descriptors, processes)
- Slow queries/responses
- Memory leaks

**Investigation:**
```bash
# System limits
ulimit -a

# File descriptor usage
lsof | wc -l
cat /proc/sys/fs/file-nr

# Connection states
netstat -an | awk '/tcp/ {print $6}' | sort | uniq -c

# Resource usage
top
htop
vmstat 1
iostat -x 1
```

## Debugging Tools Reference

### Process Management
```bash
ps aux                    # List all processes
pgrep <name>             # Find process by name
pidof <name>             # Get PID of process
kill -9 <pid>            # Force kill process
systemctl status <svc>   # Service status
journalctl -u <svc>      # Service logs
```

### Network Debugging
```bash
netstat -tulpn           # Listening ports
ss -tulpn                # Socket statistics (modern)
lsof -i :80              # What's using port 80
tcpdump -i eth0          # Packet capture
curl -I http://localhost # Test HTTP
telnet localhost 80      # Test TCP connection
```

### Log Analysis
```bash
tail -f /var/log/syslog              # Follow system log
grep -r "error" /var/log/            # Search all logs
journalctl -n 100 --no-pager         # Last 100 journal entries
dmesg | tail                         # Kernel ring buffer
```

### System Resources
```bash
free -h                  # Memory usage
df -h                    # Disk usage
du -sh /var/log/*       # Directory sizes
top                      # Process monitor
htop                     # Interactive process viewer
iostat                   # I/O statistics
vmstat                   # Virtual memory stats
```

### Configuration Testing
```bash
nginx -t                 # Test Nginx config
apache2ctl configtest    # Test Apache config
puppet parser validate   # Validate Puppet manifest
```

## Common Web Stack Issues

### 1. Service Not Running
**Symptoms:** Connection refused, no response
**Debug:**
```bash
systemctl status service_name
journalctl -u service_name -n 50
```
**Common Causes:**
- Configuration error
- Port already in use
- Insufficient permissions
- Missing dependencies

### 2. Port Binding Issues
**Symptoms:** "Address already in use"
**Debug:**
```bash
netstat -tulpn | grep :80
lsof -i :80
```
**Solutions:**
- Kill process using port
- Change application port
- Fix configuration conflict

### 3. Permission Denied
**Symptoms:** 403 errors, "Permission denied" in logs
**Debug:**
```bash
ls -la /path/to/file
namei -l /path/to/file
ps aux | grep process_name  # Check user/group
```
**Solutions:**
- Fix file permissions: `chmod`
- Fix file ownership: `chown`
- Check parent directory permissions
- Verify SELinux/AppArmor policies

### 4. Resource Exhaustion
**Symptoms:** Slow performance, connection timeouts, OOM errors
**Debug:**
```bash
free -h                          # Memory
df -h                            # Disk
ulimit -a                        # Process limits
cat /proc/sys/fs/file-max        # File descriptor limit
```
**Solutions:**
- Increase system limits
- Optimize resource usage
- Scale horizontally
- Add caching layer

### 5. Configuration Errors
**Symptoms:** Service fails to start, unexpected behavior
**Debug:**
```bash
# Test configuration before restart
nginx -t
apache2ctl configtest

# Check for syntax errors
puppet parser validate manifest.pp

# Review recent config changes
git diff HEAD~1 config_file
```
**Solutions:**
- Validate before applying
- Use version control
- Implement configuration testing
- Staged rollouts

## Production Incident Response

### Incident Workflow

1. **Detection** - Alert fires, user reports issue
2. **Triage** - Assess severity, impact, urgency
3. **Investigation** - Gather data, form hypotheses
4. **Mitigation** - Stop the bleeding (may not fix root cause)
5. **Resolution** - Fix root cause
6. **Verification** - Confirm fix works
7. **Post-Mortem** - Document and learn

### Mitigation vs Resolution

**Mitigation (Stop the Bleeding):**
- Restart failed service
- Failover to backup
- Disable problematic feature
- Scale up resources

**Resolution (Fix Root Cause):**
- Patch bug
- Fix configuration
- Optimize query
- Upgrade infrastructure

**Why Both Matter:**
- Mitigation: Restore service quickly (minutes)
- Resolution: Prevent recurrence (hours/days)
- Don't skip resolution after mitigating!

### Debugging Under Pressure

**Do:**
- Stay calm and systematic
- Document steps as you go
- Share information with team
- Focus on impact reduction first
- Take breaks if incident is long

**Don't:**
- Make random changes hoping something works
- Skip verification steps
- Forget to communicate status
- Assume you know the cause without evidence
- Panic or blame

## Advanced Debugging Techniques

### 1. Binary Search Debugging
When did it break?
- Test midpoint of timeline
- Narrow down to specific change
- Review that change for issues

### 2. Divide and Conquer
Complex system not working?
- Test each component individually
- Find which component fails
- Debug that specific component

### 3. Rubber Duck Debugging
Stuck on a problem?
- Explain the issue out loud
- Often reveals solution while explaining
- Forces logical thinking

### 4. Diff-Based Debugging
Was it working before?
```bash
git diff working_commit current_commit
diff working_config current_config
```

## Monitoring & Prevention

**Don't Just Fix - Prevent Future Issues:**

1. **Add Monitoring**
   - Service health checks
   - Resource usage alerts
   - Error rate tracking

2. **Improve Logging**
   - Structured logs
   - Appropriate log levels
   - Useful context in messages

3. **Automate Recovery**
   - Service auto-restart
   - Health check-based failover
   - Resource limit increases

4. **Document Issues**
   - Known issues wiki
   - Runbooks for common problems
   - Post-mortem documents

## Key Learnings

1. **Systematic beats random** - Following a process is faster than guessing
2. **Logs are truth** - Trust logs over assumptions
3. **Change one thing at a time** - Multiple changes obscure root cause
4. **Verify your hypothesis** - Don't assume, test
5. **Document everything** - Future you will thank present you

## Proposed Improvements

**Better Debugging:**
1. Add comprehensive logging to all services
2. Implement distributed tracing (Jaeger, Zipkin)
3. Set up centralized log aggregation (ELK stack)
4. Create debugging runbooks

**Better Prevention:**
1. Automated health checks
2. Proactive monitoring and alerting
3. Chaos engineering (intentional failures to test resilience)
4. Automated remediation for common issues

**Better Process:**
1. Incident response procedures
2. Post-mortem template and process
3. On-call rotation and escalation
4. Incident retrospectives

## Related Projects

- `0x18-webstack_monitoring`: Monitoring setup (detect issues faster)
- `0x0F-load_balancer`: High availability (reduce impact of failures)
- `0x0A-configuration_management`: Automated fixes (consistent resolution)

---

*This work demonstrates systematic debugging methodology, understanding of web stack architecture, and production incident response capabilities essential for reliable operations.*
