# Advanced Shell Scripting - Loops, Conditions & Text Processing

## Overview

This collection demonstrates advanced Bash scripting capabilities including control structures, file processing, and text manipulation. These are foundational DevOps skills for automation, log analysis, and system administration.

## Key Concepts Demonstrated

### 1. Control Flow Structures
- **For loops** - Iterating over sequences and ranges
- **While loops** - Condition-based iteration
- **Until loops** - Loop until condition is true
- **If/elif/else** - Conditional branching
- **Case statements** - Multi-way branching

### 2. Text Processing Pipeline
- **AWK** - Pattern scanning and text processing
- **sed** - Stream editing
- **cut** - Field extraction
- **sort/uniq** - Data aggregation
- **grep** - Pattern matching

### 3. Advanced Bash Features
- **Arithmetic expressions** - `(( ))` for calculations
- **String manipulation** - Variable expansion and substitution
- **File descriptors** - Input/output redirection
- **Process substitution** - `<()` for command output as files

## Featured Scripts

### FizzBuzz (10-fizzbuzz)
Classic algorithm demonstration showing conditional logic precedence and modulo operations.

**Skills:** Loop control, conditional logic, mathematical operations

### Apache Log Parser (102-lets_parse_apache_logs)
Extract IP addresses and HTTP status codes from Apache access logs.

**Skills:** Field extraction, AWK, log analysis

### Apache Log Analytics (103-dig_the-data)
Advanced log aggregation - count occurrences by IP and status, sorted by frequency.

**Skills:** Pipeline composition, sort/uniq patterns, data aggregation

### /etc/passwd Parser (101-tell_the_story_of_passwd)
Parse and format system user information from /etc/passwd in human-readable narrative.

**Skills:** File parsing, field extraction, string interpolation, system knowledge

## Production Applications

These scripting techniques are essential for:

**Operations:**
- Log analysis and monitoring
- Automated reporting
- System auditing
- Batch processing

**DevOps:**
- CI/CD pipeline scripts
- Deployment automation
- Health check scripts
- Data migration

**Security:**
- User enumeration
- Access log analysis
- Security auditing
- Incident response

## Best Practices Demonstrated

1. **Proper shebang** - `#!/usr/bin/env bash` for portability
2. **Meaningful variable names** - Self-documenting code
3. **Input validation** - Defensive programming
4. **Error handling** - Exit codes and error messages
5. **Comments** - Explain intent and complex logic
6. **Idempotency** - Safe to run multiple times

## Related Skills

- Regular expressions (pattern matching)
- Process management (signals, job control)
- System administration (users, permissions)
- Performance analysis (profiling scripts)

---

*These scripts demonstrate practical shell scripting expertise essential for DevOps automation and system administration.*
