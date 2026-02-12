# Make.com Scheduling Configurations

This reference explains how to configure scenario scheduling in Make.com.

## Scheduling Types

Make.com supports three scheduling types:

1. **Interval** - Run at fixed time intervals
2. **Cron** - Run based on cron expressions
3. **Instant** - Trigger-based (webhooks, app events)

## Interval Scheduling

Run scenarios at regular intervals (minutes).

### Supported Intervals
- `1` - Every 1 minute
- `5` - Every 5 minutes
- `15` - Every 15 minutes (default)
- `30` - Every 30 minutes
- `60` - Every 60 minutes (1 hour)

### Configuration
```json
{
  "scheduling": {
    "type": "interval",
    "interval": 15
  }
}
```

### Use Cases
- **1 minute**: Real-time monitoring, high-frequency data sync
- **5 minutes**: Frequent API polling, stock price updates
- **15 minutes**: Standard data sync, email checking
- **30 minutes**: Moderate-frequency updates
- **60 minutes**: Hourly reports, low-frequency sync

### Example: Run Every 15 Minutes
```json
{
  "name": "Check New Orders",
  "scheduling": {
    "type": "interval",
    "interval": 15
  },
  "flow": [
    {
      "id": 1,
      "module": "http:Get",
      "mapper": {
        "url": "https://api.example.com/orders/new"
      }
    }
  ]
}
```

## Cron Scheduling

Advanced scheduling using cron expressions for specific times/days.

### Cron Expression Format
```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sunday=0)
│ │ │ │ │
* * * * *
```

### Configuration
```json
{
  "scheduling": {
    "type": "cron",
    "cron": "0 9 * * 1-5"
  }
}
```

### Common Cron Patterns

#### Daily at 9:00 AM
```json
{
  "scheduling": {
    "type": "cron",
    "cron": "0 9 * * *"
  }
}
```

#### Weekdays at 9:00 AM
```json
{
  "scheduling": {
    "type": "cron",
    "cron": "0 9 * * 1-5"
  }
}
```

#### Every Monday at 8:00 AM
```json
{
  "scheduling": {
    "type": "cron",
    "cron": "0 8 * * 1"
  }
}
```

#### First day of every month at 6:00 AM
```json
{
  "scheduling": {
    "type": "cron",
    "cron": "0 6 1 * *"
  }
}
```

#### Every 6 hours
```json
{
  "scheduling": {
    "type": "cron",
    "cron": "0 */6 * * *"
  }
}
```

#### Every hour on weekdays
```json
{
  "scheduling": {
    "type": "cron",
    "cron": "0 * * * 1-5"
  }
}
```

#### Midnight every day
```json
{
  "scheduling": {
    "type": "cron",
    "cron": "0 0 * * *"
  }
}
```

#### Every 15 minutes (using cron)
```json
{
  "scheduling": {
    "type": "cron",
    "cron": "*/15 * * * *"
  }
}
```

### Cron Special Characters
- `*` - Any value
- `,` - Value list separator (e.g., `1,3,5`)
- `-` - Range (e.g., `1-5` for Monday-Friday)
- `/` - Step values (e.g., `*/15` for every 15)

### Use Cases
- **Daily reports**: Run at specific time each day
- **Weekly summaries**: Run once per week
- **Monthly billing**: Run on first of month
- **Business hours only**: Run during 9-5 on weekdays
- **Custom schedules**: Any specific timing requirements

## Instant/Webhook Scheduling

For scenarios triggered by external events or webhooks.

### Configuration
```json
{
  "scheduling": {
    "type": "instant"
  }
}
```

### When to Use
- Webhook-triggered scenarios
- Real-time event processing
- On-demand execution
- User-initiated flows
- App event triggers (e.g., Shopify new order, Gmail new email)

### Example: Webhook-Triggered
```json
{
  "name": "Process Incoming Webhook",
  "scheduling": {
    "type": "instant"
  },
  "flow": [
    {
      "id": 1,
      "module": "webhook:CustomWebhook",
      "parameters": {
        "hook": "webhook-id-here"
      }
    },
    {
      "id": 2,
      "module": "http:Post",
      "mapper": {
        "url": "https://api.example.com/process",
        "body": "{{1}}"
      }
    }
  ]
}
```

### Example: App Event Trigger
```json
{
  "name": "New Gmail Email",
  "scheduling": {
    "type": "instant"
  },
  "flow": [
    {
      "id": 1,
      "module": "gmail:WatchEmails",
      "parameters": {
        "connection": "gmail-connection-id"
      }
    },
    {
      "id": 2,
      "module": "slack:SendMessage",
      "mapper": {
        "text": "New email from {{1.from}}"
      }
    }
  ]
}
```

## Choosing the Right Scheduling Type

| Use Case | Recommended Type | Example |
|----------|------------------|---------|
| Real-time webhook processing | Instant | Payment notifications |
| High-frequency polling | Interval (1-5 min) | Stock price updates |
| Standard data sync | Interval (15-30 min) | CRM data sync |
| Daily reports | Cron (specific time) | 9 AM daily summary |
| Weekly backups | Cron (weekly) | Sunday midnight backup |
| Business hours only | Cron (weekday hours) | 9-5 weekdays |
| Monthly billing | Cron (monthly) | 1st of month |
| Event-driven flows | Instant | New order in Shopify |

## Advanced Patterns

### Time Zone Considerations
Cron expressions run in the account's configured timezone. To handle different timezones:

```json
{
  "scheduling": {
    "type": "cron",
    "cron": "0 14 * * *"  // 2 PM in account timezone
  }
}
```

### Rate Limiting
To avoid hitting API rate limits:
- Use longer intervals (30-60 min)
- Use cron for specific off-peak times
- Add delay modules between API calls

### Combining with Filters
Even with scheduling, use filters to control when modules execute:

```json
{
  "flow": [
    {
      "id": 1,
      "module": "http:Get",
      "mapper": {"url": "https://api.example.com/data"}
    }
  ],
  "connections": [
    {
      "sourceModuleId": 1,
      "targetModuleId": 2,
      "filter": {
        "name": "Only if new data",
        "conditions": [
          [{"a": "{{1.data.length}}", "o": "greater", "b": "0"}]
        ]
      }
    }
  ]
}
```

## Best Practices

### 1. **Start with Longer Intervals**
Begin with 15-30 minute intervals and decrease only if needed.

### 2. **Use Cron for Specific Times**
If you need a scenario to run at 9 AM daily, use cron instead of interval.

### 3. **Monitor Execution Frequency**
Check scenario execution logs to ensure schedules are appropriate.

### 4. **Consider API Limits**
Respect third-party API rate limits when setting intervals.

### 5. **Use Instant for Real-Time Needs**
Webhooks and app events are more efficient than polling.

### 6. **Test Before Activating**
Run scenarios manually before enabling scheduling to verify correctness.

## MCP Tools for Scheduling

Use these MCP tools to manage scenario scheduling:

- **`scenarios_activate`**: Enable scenario scheduling
- **`scenarios_deactivate`**: Disable scenario scheduling
- **`scenarios_update`**: Change scheduling configuration
- **`scenarios_run`**: Manually trigger a scenario (ignores schedule)

## Examples

### Example 1: Daily Morning Report
```json
{
  "name": "Daily Sales Report",
  "scheduling": {
    "type": "cron",
    "cron": "0 8 * * 1-5"  // 8 AM weekdays
  },
  "flow": [...]
}
```

### Example 2: Frequent Data Sync
```json
{
  "name": "Sync CRM Contacts",
  "scheduling": {
    "type": "interval",
    "interval": 15
  },
  "flow": [...]
}
```

### Example 3: Real-Time Order Processing
```json
{
  "name": "Process Orders",
  "scheduling": {
    "type": "instant"
  },
  "flow": [
    {
      "id": 1,
      "module": "webhook:CustomWebhook"
    }
  ]
}
```
