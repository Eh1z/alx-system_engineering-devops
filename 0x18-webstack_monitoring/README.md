# Web Stack Monitoring with Datadog

## Problem Statement

"You can't fix what you can't see." Without monitoring, infrastructure problems go undetected until users complain. By then, you're losing money, users, and reputation.

Effective monitoring provides:
- **Early warning** - Detect issues before they impact users
- **Root cause analysis** - Metrics to understand what went wrong
- **Capacity planning** - Data to predict when to scale
- **Performance optimization** - Insights into bottlenecks

## Solution: Datadog Integration

Datadog is a comprehensive observability platform providing:
- Infrastructure monitoring (CPU, memory, disk, network)
- Application Performance Monitoring (APM)
- Log aggregation and analysis
- Custom metrics and dashboards
- Alerting and incident management

## Implementation Overview

### Monitoring Architecture

```
Your Infrastructure
    ↓ (Datadog Agent)
    ↓ (Metrics Collection)
    ↓
Datadog Platform
    ↓
Dashboards, Alerts, Analytics
    ↓
Operations Team
```

### Datadog Agent

**What it does:**
- Runs on each server as a lightweight daemon
- Collects system metrics every 15 seconds
- Sends metrics to Datadog platform via HTTPS
- Minimal resource overhead (~1% CPU, ~200MB RAM)

**What it monitors automatically:**
- CPU usage (per core, system, user, iowait)
- Memory utilization (free, used, cached, swap)
- Disk I/O (read/write throughput, latency)
- Network traffic (bytes in/out, packets, errors)
- Process metrics (count, state, resource usage)

## Key Monitoring Concepts

### 1. Metrics vs Logs vs Traces

**Metrics:**
- Numerical measurements over time (CPU: 45%, requests: 1000/sec)
- Aggregated and efficient for long-term storage
- Best for: Resource usage, performance trends, alerting

**Logs:**
- Discrete event records (timestamps, messages, context)
- Detailed but storage-intensive
- Best for: Debugging, audit trails, error investigation

**Traces:**
- Request paths through distributed systems
- Shows timing and dependencies between services
- Best for: Performance bottlenecks, latency analysis

### 2. Monitoring Dashboards

**Purpose:** Visual representation of system health at a glance

**Essential Dashboard Elements:**
- **Golden Signals** (Google SRE methodology):
  - Latency: How long requests take
  - Traffic: How much demand on the system
  - Errors: Rate of failed requests
  - Saturation: How full the system is (CPU, memory, disk)

**Dashboard Design Principles:**
- Most important metrics at the top
- Color coding: green (good), yellow (warning), red (critical)
- Time range selectors for trend analysis
- Drill-down capability from overview to details

### 3. Alerting Strategy

**Alert on Symptoms, Not Causes:**
- ❌ Bad: "Disk usage > 80%" (cause)
- ✅ Good: "API response time > 2s" (symptom)

**Alert Fatigue Prevention:**
- Set appropriate thresholds (not too sensitive)
- Use alert aggregation (don't alert on every instance)
- Implement escalation policies
- Regular alert tuning based on false positive rate

**Alert Severity Levels:**

| Level | Response Time | Example |
|-------|--------------|---------|
| **Critical** | Immediate (24/7) | Service down, data loss |
| **Warning** | Business hours | High resource usage, elevated errors |
| **Info** | No action needed | Deployments, scheduled maintenance |

### 4. Baseline and Anomaly Detection

**Baseline:** Normal operating range for a metric
- Example: CPU normally 20-40% during business hours

**Anomaly:** Significant deviation from baseline
- Example: CPU suddenly spikes to 95%

**Machine Learning Alerting:**
- Datadog can learn normal patterns
- Alert on deviations, not static thresholds
- Adapts to daily/weekly patterns
- Reduces false positives

## Datadog Features Demonstrated

### Infrastructure Monitoring
```
# View all hosts
Hosts: web-01, web-02, lb-01
Status: ✓ All reporting metrics

# System metrics
CPU: 35% avg across fleet
Memory: 60% utilization
Disk: 45% used, no I/O bottlenecks
Network: 50 Mbps inbound, 200 Mbps outbound
```

### Custom Metrics
```python
# Application-level metrics
from datadog import statsd

# Increment counters
statsd.increment('web.requests')
statsd.increment('web.errors', tags=['status:500'])

# Record timing
statsd.timing('web.response_time', 150)  # milliseconds

# Set gauges
statsd.gauge('database.connections', 45)
```

### Dashboard Creation
- **Host Map:** Visualize entire infrastructure
- **Timeseries Graphs:** Trend analysis over time
- **Heatmaps:** Distribution of latencies/errors
- **Top Lists:** Highest resource consumers

## Production Best Practices

### 1. Metric Naming Convention
```
<namespace>.<metric_name>.<aggregation>

Examples:
web.requests.count
web.response_time.avg
db.connections.gauge
cache.hit_ratio.percent
```

Benefits:
- Organized metric hierarchy
- Easy filtering and querying
- Clear semantic meaning

### 2. Tagging Strategy
```
Tags: env:prod, service:api, region:us-east-1, version:v2.3

# Enable queries like:
# "Show me API errors in production, US-East region"
# "Compare performance between v2.2 and v2.3"
```

**Tag Categories:**
- Environment: prod, staging, dev
- Service: web, api, database
- Region: us-east-1, eu-west-1
- Version: v1.0, v2.0

### 3. SLA/SLO Monitoring

**SLA (Service Level Agreement):** Contract with users
- "99.9% uptime" = max 43 minutes downtime/month

**SLO (Service Level Objective):** Internal target
- "95th percentile latency < 200ms"

**SLI (Service Level Indicator):** Actual measurement
- "Current 95th percentile: 180ms" ✓

**Monitor SLOs with Datadog:**
```
# Create SLO dashboard
Target: 99.9% of requests < 500ms response time
Current: 99.95% (meeting target)
Error budget remaining: 0.05% = 22 minutes this month
```

### 4. Capacity Planning

**Use historical data to predict:**
- When will disk fill up? (trend line)
- How many users until CPU saturates?
- When to add more servers?

**Example Analysis:**
```
Current: 1000 requests/sec @ 40% CPU
Projected: 2500 requests/sec in 3 months
Saturation point: ~2200 requests/sec @ 80% CPU
Action: Add 1-2 servers within 2 months
```

## Monitoring Anti-Patterns to Avoid

### 1. Monitor Everything
❌ Too many metrics, unclear signal
✅ Focus on what matters (SLIs, golden signals)

### 2. Alert on Everything
❌ Alert fatigue, ignored notifications
✅ Alert on actionable symptoms, not informational events

### 3. Dashboard Sprawl
❌ 50 dashboards, no one knows which to use
✅ 3-5 well-designed dashboards for different audiences

### 4. No Documentation
❌ "What does this metric mean?" → No one remembers
✅ Document metrics, alert runbooks, dashboard purposes

## Observability Maturity Model

### Level 1: Basic Monitoring
- System metrics (CPU, memory, disk)
- Service up/down checks
- Manual dashboard checking

### Level 2: Proactive Monitoring
- Automated alerting
- Log aggregation
- Dashboards for common issues

### Level 3: Full Observability
- Distributed tracing
- Custom application metrics
- Anomaly detection
- Predictive alerting

### Level 4: Advanced Observability
- AIOps (AI-powered operations)
- Auto-remediation
- Chaos engineering integration
- Continuous profiling

## Related Monitoring Tools

| Tool | Strength | Best For |
|------|----------|----------|
| **Datadog** | All-in-one platform | Companies wanting single vendor |
| **Prometheus** | Time-series database | Kubernetes, open-source stacks |
| **Grafana** | Visualization | Multi-source dashboards |
| **New Relic** | APM focus | Application performance |
| **ELK Stack** | Log analysis | Centralized logging |

**Why Datadog:**
- Comprehensive out-of-box integrations (500+)
- Low setup overhead
- Great UI/UX
- Strong community and documentation

## Key Learnings

1. **Monitoring is not optional** - Production systems need observability
2. **Alert on symptoms** - Focus on user impact, not internal metrics
3. **Dashboards tell stories** - Design for your audience
4. **Tagging enables analysis** - Good tags = powerful queries
5. **Baselines matter** - Know what "normal" looks like

## Proposed Improvements

**Short-term:**
1. Set up alerting for critical services
2. Create runbooks for common alerts
3. Add custom application metrics
4. Configure log forwarding to Datadog

**Long-term:**
1. Implement distributed tracing (APM)
2. Set up SLO monitoring
3. Build anomaly detection models
4. Integrate with incident management (PagerDuty)
5. Automate common remediation actions

## Related Projects

- `0x0F-load_balancer`: Monitor load distribution and health
- `0x1A-application_server`: Application-level metrics and APM
- `0x0D-0x1B-web_stack_debugging`: Faster debugging with metrics/logs

---

*This implementation demonstrates understanding of observability principles, monitoring strategies, and production operations essential for reliable service delivery.*
