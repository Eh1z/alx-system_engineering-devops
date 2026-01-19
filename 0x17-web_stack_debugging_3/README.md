# Web Stack Debugging 3 - Automated Debugging with Puppet

## Scenario Overview

This debugging scenario demonstrates **Infrastructure as Code (IaC) for incident remediation** - automating the fix for recurring production issues using Puppet configuration management.

## The Problem

Manual fixes don't scale. When the same issue affects multiple servers or recurs frequently, manually SSH-ing into each server is:
- Time-consuming
- Error-prone
- Not auditable
- Doesn't prevent recurrence

## The Solution: Automated Remediation

Instead of manually fixing each occurrence:
1. **Diagnose** the issue once
2. **Write Puppet manifest** to implement fix
3. **Apply declaratively** across all affected servers
4. **Prevent recurrence** through configuration management

## Benefits of IaC for Debugging

### 1. Repeatability
- Same fix applied consistently everywhere
- No human error in execution
- Reproducible across environments

### 2. Speed
- Fix hundreds of servers in minutes
- No manual SSH required
- Parallel execution across fleet

### 3. Auditability
- Fixes version controlled in Git
- Who changed what, when, why
- Can review before applying

### 4. Prevention
- Fix persists across server reboots
- Prevents configuration drift
- Self-healing infrastructure

### 5. Documentation
- Puppet manifest IS the documentation
- Code explains exactly what's done
- Easier than maintaining wiki pages

## Common Web Stack Issues Automated

### 1. PHP-FPM Configuration Errors
**Problem:** Typo in php.ini causes 500 errors

**Manual Fix:** Edit file, restart service

**Puppet Fix:**
```puppet
file_line { 'fix-php-typo':
    path  => '/etc/php/7.0/fpm/php.ini',
    match => '^phpp_admin_value',
    line  => 'php_admin_value[error_log] = /var/log/fpm-php.www.log',
}

service { 'php7.0-fpm':
    ensure    => running,
    subscribe => File_line['fix-php-typo'],  # Auto-restart on change
}
```

### 2. Apache/Nginx Misconfigurations
**Problem:** Wrong DocumentRoot or server_name

**Puppet Fix:**
```puppet
file { '/etc/nginx/sites-available/default':
    ensure  => file,
    content => template('nginx/default.conf.erb'),
    notify  => Service['nginx'],  # Reload nginx
}
```

### 3. File Permission Issues
**Problem:** 403 errors due to wrong ownership

**Puppet Fix:**
```puppet
file { '/var/www/html':
    ensure  => directory,
    owner   => 'www-data',
    group   => 'www-data',
    mode    => '0755',
    recurse => true,  # Fix all files inside
}
```

### 4. Service Not Running
**Problem:** Service stopped, needs restart

**Puppet Fix:**
```puppet
service { 'nginx':
    ensure => running,
    enable => true,  # Start on boot
}
```

## Debugging Workflow with Puppet

### 1. Manual Investigation
```bash
# Find the problem
systemctl status apache2
tail -f /var/log/apache2/error.log
apache2ctl configtest

# Identify root cause
# Example: typo in config file
```

### 2. Manual Fix First
```bash
# Fix on one server
sudo vim /etc/apache2/apache2.conf
# Correct the typo
sudo systemctl restart apache2

# Verify fix works
curl http://localhost
# Returns 200 OK
```

### 3. Automate with Puppet
```puppet
# Create manifest: fix_apache_typo.pp
exec { 'fix-apache-config':
    command => '/bin/sed -i "s/ServerNam/ServerName/g" /etc/apache2/apache2.conf',
    onlyif  => '/bin/grep -q ServerNam /etc/apache2/apache2.conf',
}

service { 'apache2':
    ensure    => running,
    subscribe => Exec['fix-apache-config'],
}
```

### 4. Test Manifest
```bash
# Dry run (no changes)
puppet apply --noop fix_apache_typo.pp

# Apply for real
puppet apply fix_apache_typo.pp
```

### 5. Deploy to All Servers
```bash
# Via Puppet Master-Agent
# Manifest checked into version control
# Agents pull and apply automatically

# Or via orchestration
for server in $(cat servers.txt); do
    scp fix_apache_typo.pp $server:/tmp/
    ssh $server 'puppet apply /tmp/fix_apache_typo.pp'
done
```

## Best Practices

### 1. Idempotency
```puppet
# Bad: Not idempotent (appends every time)
exec { 'add-line':
    command => 'echo "config" >> /etc/file',
}

# Good: Idempotent (only adds if missing)
file_line { 'add-line':
    path => '/etc/file',
    line => 'config',
}
```

### 2. Validation
```puppet
# Validate before restarting service
exec { 'nginx-configtest':
    command     => '/usr/sbin/nginx -t',
    refreshonly => true,  # Only run when config changes
}

file { '/etc/nginx/nginx.conf':
    notify => Exec['nginx-configtest'],
}
```

### 3. Dependencies
```puppet
# Ensure order of operations
File['/etc/app/config']
  -> Service['app']  # Configure before starting
```

### 4. Error Handling
```puppet
# Handle failure gracefully
exec { 'risky-operation':
    command => '/usr/local/bin/risky',
    onlyif  => '/usr/local/bin/should-i-run',  # Precondition
    timeout => 30,  # Don't hang forever
}
```

## Testing Puppet Manifests

### Syntax Check
```bash
puppet parser validate manifest.pp
```

### Dry Run
```bash
puppet apply --noop manifest.pp
# Shows what WOULD change, doesn't apply
```

### Linting
```bash
puppet-lint manifest.pp
# Checks style and best practices
```

### Unit Testing
```bash
# Using rspec-puppet
rspec spec/classes/myclass_spec.rb
```

## Production Deployment Pattern

1. **Write manifest** in development environment
2. **Test in staging** - verify fix works
3. **Code review** - peer review manifest
4. **Deploy gradually** - canary rollout
5. **Monitor results** - check for errors
6. **Full rollout** once validated

## When NOT to Use Puppet for Debugging

**One-time fixes:**
- Unique server issue
- Server being decommissioned
- Faster to manually fix

**Urgent incidents:**
- Mitigate manually first (restore service)
- Automate fix later (prevent recurrence)
- Don't delay incident response to write Puppet

**Exploratory debugging:**
- Still investigating root cause
- Don't know fix yet
- Manual debugging phase

## Key Learnings

1. **Automate recurring fixes** - Don't repeat manual work
2. **IaC for incident response** - Fixes as code
3. **Test before deploying** - Dry run prevents mistakes
4. **Gradual rollout** - Validate on subset first
5. **Document with code** - Puppet manifest = documentation

## Related Concepts

- **Configuration Management** - Puppet, Ansible, Chef
- **Infrastructure as Code** - Declarative infrastructure
- **Idempotency** - Safe to run repeatedly
- **Declarative vs Imperative** - Describe state vs steps
- **GitOps** - Version control for infrastructure

---

*This approach demonstrates using configuration management for automated incident remediation, enabling self-healing infrastructure and consistent fixes across server fleets.*
