# Puppet Manifest: File Resource Management
#
# Purpose: Demonstrate declarative file creation with specific ownership and permissions
#
# Resource Type: file
# Title: /tmp/school (unique identifier and target path)
#
# Key Concepts:
#   - Idempotency: Running this manifest multiple times produces same result
#   - Declarative: Describes desired state, not steps to achieve it
#   - Self-healing: If file is modified/deleted, Puppet corrects it on next run
#
# Production Use Cases:
#   - Creating configuration files with correct permissions
#   - Ensuring critical files exist with proper ownership
#   - Managing application-specific files for web services
#
# Security Note: Mode 0744 = Owner: RWX, Group: R, Others: R
#   - Owner (www-data) can read, write, execute
#   - Group (www-data) can read only
#   - Others can read only
#   - Follows least-privilege principle

file { '/tmp/school':
    # Ensure this is a regular file (not directory, symlink, etc.)
    ensure  => 'file',
    
    # Set file owner to www-data (common web server user)
    # www-data typically runs Apache/Nginx processes
    owner   => 'www-data',
    
    # Set group ownership to www-data
    # Allows multiple processes running as www-data to access
    group   => 'www-data',
    
    # Set file permissions: 0744 (octal notation)
    # 0 = no special bits (no setuid/setgid/sticky)
    # 7 = owner: read(4) + write(2) + execute(1)
    # 4 = group: read(4)
    # 4 = others: read(4)
    mode    => '0744',
    
    # Static file content
    # In production, use 'source' for external files or 'content => template()'
    # for dynamic content with variables
    content => 'I love Puppet',
}
