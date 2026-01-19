# Regular Expressions - Pattern Matching Mastery

## Overview

Regular expressions (regex) are the Swiss Army knife of text processing. Essential for log analysis, data validation, text extraction, and automation, regex is a fundamental DevOps and systems engineering skill.

## What Are Regular Expressions?

**Definition:** A formal language for describing text patterns.

**Use Cases:**
- **Log parsing** - Extract specific information from logs
- **Data validation** - Verify email formats, phone numbers, IPs
- **Text transformation** - Search and replace operations
- **Security** - Input sanitization, pattern-based filtering
- **Monitoring** - Alert on specific log patterns

## Key Concepts

### 1. Literal Matching
```regex
hello       # Matches exactly "hello"
192.168     # Matches IP prefix "192.168"
```

### 2. Metacharacters
```regex
.       # Any single character
^       # Start of line
$       # End of line
*       # Zero or more repetitions
+       # One or more repetitions
?       # Zero or one repetition
[]      # Character class
()      # Grouping
|       # Alternation (OR)
\       # Escape special character
```

### 3. Character Classes
```regex
[abc]       # Matches a, b, or c
[a-z]       # Any lowercase letter
[A-Z]       # Any uppercase letter
[0-9]       # Any digit
[^0-9]      # Any non-digit
\d          # Digit [0-9]
\w          # Word character [a-zA-Z0-9_]
\s          # Whitespace
```

### 4. Quantifiers
```regex
a*          # Zero or more 'a'
a+          # One or more 'a'
a?          # Zero or one 'a'
a{3}        # Exactly 3 'a's
a{3,}       # 3 or more 'a's
a{3,5}      # Between 3 and 5 'a's
```

### 5. Anchors
```regex
^start      # Line starts with "start"
end$        # Line ends with "end"
\bword\b    # Word boundary (whole word)
```

## Production Examples

### 1. Log Analysis - Extract IPs
```bash
# Match IPv4 addresses
grep -E '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' access.log

# Better version (validates ranges)
grep -E '\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b' access.log
```

### 2. Email Validation
```regex
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

# Breakdown:
# [a-zA-Z0-9._%+-]+  : Local part (before @)
# @                  : Literal @
# [a-zA-Z0-9.-]+     : Domain name
# \.                 : Literal dot
# [a-zA-Z]{2,}       : TLD (at least 2 letters)
```

### 3. Extract HTTP Status Codes
```bash
# From Apache/Nginx logs
awk '{print $9}' access.log | grep -E '^[45][0-9]{2}$'

# 4xx and 5xx errors only
grep -E ' (4[0-9]{2}|5[0-9]{2}) ' access.log
```

### 4. Phone Number Validation
```regex
# US phone: (123) 456-7890 or 123-456-7890
^\(?[0-9]{3}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}$

# International: +1 234 567 8900
^\+?[1-9]\d{1,14}$  # E.164 format
```

### 5. Security - Detect SQL Injection Attempts
```bash
# Look for SQL keywords in input
grep -iE '(union|select|insert|update|delete|drop|exec).*from' logs.txt

# OR patterns
grep -iE 'or 1=1|or true|' logs.txt
```

## Regex in Different Tools

### grep (Basic & Extended)
```bash
# Basic regex (BRE)
grep 'pattern' file.txt

# Extended regex (ERE)
grep -E 'pattern|alternative' file.txt
egrep 'pattern' file.txt  # Same as grep -E

# Perl-compatible (PCRE)
grep -P '(?<=prefix)pattern' file.txt
```

### sed (Stream Editor)
```bash
# Substitute
sed 's/old/new/g' file.txt

# Delete lines matching pattern
sed '/pattern/d' file.txt

# Extract matches
sed -n 's/.*\(pattern\).*/\1/p' file.txt
```

### awk (Pattern Scanning)
```bash
# Print lines matching regex
awk '/pattern/ {print}' file.txt

# Field extraction with regex
awk '$3 ~ /^ERROR/ {print $1, $3}' log.txt
```

### Python
```python
import re

# Search
match = re.search(r'pattern', text)

# Find all
matches = re.findall(r'pattern', text)

# Replace
result = re.sub(r'old', 'new', text)

# Compile for reuse
pattern = re.compile(r'pattern')
pattern.search(text)
```

## Common Patterns Library

### IPv4 Address
```regex
\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b
```

### Email Address
```regex
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
```

### URL
```regex
https?://[^\s]+
```

### Date (YYYY-MM-DD)
```regex
\d{4}-\d{2}-\d{2}
```

### Time (HH:MM:SS)
```regex
\d{2}:\d{2}:\d{2}
```

### Hex Color Code
```regex
#[0-9A-Fa-f]{6}
```

### Credit Card (Visa)
```regex
4[0-9]{12}(?:[0-9]{3})?
```

## Best Practices

### 1. Be Specific
```regex
# Bad: Too greedy
.*log.*

# Good: More specific
\b\w+\.log\b
```

### 2. Use Non-Capturing Groups
```regex
# Capturing (stores match)
(https?)://(.+)

# Non-capturing (better performance)
(?:https?)://(.+)
```

### 3. Escape Metacharacters
```regex
# Literal dot
192\.168\.1\.1

# Literal dollar sign
\$100
```

### 4. Test Performance
```bash
# Measure regex performance
time grep -E 'complex.*regex.*pattern' large_file.txt

# Optimize by ordering
# Better: common patterns first
(error|warn|info)
# Not: (info|warn|error)  # Most logs are info
```

### 5. Document Complex Regex
```python
# Python verbose regex
pattern = re.compile(r"""
    ^                   # Start of line
    (?P<ip>\d{1,3}\.){3}\d{1,3}  # IP address
    \s+                 # Whitespace
    \[(?P<date>[^\]]+)\]  # Date in brackets
    \s+                 # Whitespace
    "(?P<request>[^"]+)"  # Request in quotes
    \s+                 # Whitespace
    (?P<status>\d{3})   # Status code
""", re.VERBOSE)
```

## Debugging Regex

### Online Tools
- **regex101.com** - Interactive testing with explanation
- **regexr.com** - Visual regex builder
- **debuggex.com** - Visualize regex structure

### Testing Strategy
1. Start simple, add complexity gradually
2. Test with real data samples
3. Check edge cases
4. Validate performance on large datasets

## Common Pitfalls

### 1. Catastrophic Backtracking
```regex
# Bad: Can hang on certain inputs
(a+)+b

# Good: More efficient
a+b
```

### 2. Overuse of Wildcards
```regex
# Bad: Too greedy, matches too much
<.*>

# Good: Non-greedy
<.*?>

# Better: More specific
<[^>]+>
```

### 3. Forgetting to Escape
```regex
# Wrong: Matches any character
192.168.1.1

# Right: Literal dots
192\.168\.1\.1
```

## Performance Considerations

**Fast:**
- Literal strings
- Character classes
- Anchors

**Slow:**
- Backreferences
- Lookaheads/lookbehinds (especially in long text)
- Nested quantifiers

**Optimization Tips:**
1. Anchor when possible (`^` and `$`)
2. Use character classes over alternation: `[abc]` not `(a|b|c)`
3. Order alternations by frequency: common patterns first
4. Avoid unnecessary capture groups

## Key Learnings

1. **Regex is powerful but complex** - Start simple, build up
2. **Test thoroughly** - Edge cases will surprise you
3. **Performance matters** - Inefficient regex can DoS your system
4. **Document complex patterns** - Future you will thank you
5. **Know your flavor** - PCRE, POSIX, Python all differ slightly

---

*Regular expressions are an essential DevOps skill for log analysis, data validation, and text processing automation.*
