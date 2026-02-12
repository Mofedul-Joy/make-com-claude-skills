---
name: make-scenario-builder
description: Core skill for building Make.com scenarios including modules, routers, filters, aggregators, iterators, and scheduling configurations
---

# Make.com Scenario Builder

## Overview

This skill teaches Claude how to construct complete Make.com scenarios from natural language descriptions. It covers the fundamental building blocks: modules (trigger and action apps), routers for conditional logic, filters for data control, aggregators/iterators for data transformation, and scheduling configurations.

## When to Use This Skill

Use this skill when:
- Building a new Make.com scenario from scratch
- Adding modules, routers, or filters to existing scenarios
- Configuring scenario scheduling (intervals, cron expressions)
- Setting up aggregators or iterators for batch processing
- Wiring module connections and data flow

## Key Concepts

### Scenarios
A **scenario** is a complete automation workflow in Make.com. Each scenario has:
- **Name**: Descriptive identifier
- **Scheduling**: When/how the scenario runs (interval, webhook, instant)
- **Flow**: A sequence of modules connected in a specific order

### Modules
**Modules** are the building blocks of scenarios. Each module represents an action or trigger:
- **Trigger modules**: Start the scenario (webhooks, scheduled triggers, app events)
- **Action modules**: Perform operations (create record, send email, API request)
- **Special modules**: Routers, filters, aggregators, iterators, error handlers

### Routers
**Routers** enable conditional branching. A single input splits into multiple parallel routes, each with optional filter conditions.

### Filters
**Filters** control data flow between modules. Only items matching filter conditions pass through.

### Aggregators & Iterators
- **Aggregators**: Combine multiple items into a single bundle (e.g., sum values, merge arrays)
- **Iterators**: Split a single bundle containing an array into multiple individual bundles

## Module Configuration Structure

Each module in a Make.com scenario has this structure:

```json
{
  "id": 1,
  "module": "app-name:ActionName",
  "version": 1,
  "parameters": {
    // App-specific configuration
  },
  "mapper": {
    // Field mappings (often references to previous modules)
  },
  "metadata": {
    "designer": {
      "x": 0,
      "y": 0
    }
  }
}
```

### Key Fields
- **id**: Unique numeric identifier (sequential)
- **module**: Format is `app-name:TriggerName` or `app-name:ActionName`
- **version**: Module version (usually 1)
- **parameters**: Fixed configuration values
- **mapper**: Dynamic field mappings (can reference `{{1.field}}` from module 1)
- **metadata.designer**: Visual positioning in the UI

## Connection Structure

Connections define how data flows between modules:

```json
{
  "sourceModuleId": 1,
  "targetModuleId": 2
}
```

For routers, use `routes` to define conditional branching:

```json
{
  "sourceModuleId": 2,
  "targetModuleId": null,
  "routes": [
    {
      "flow": [
        {
          "id": 3,
          "module": "...",
          ...
        }
      ],
      "filter": {
        "name": "Route 1",
        "conditions": [
          [
            {
              "a": "{{2.status}}",
              "o": "equal",
              "b": "active"
            }
          ]
        ]
      }
    }
  ]
}
```

## Scheduling Patterns

### Interval Scheduling
Run scenario at regular intervals:

```json
{
  "scheduling": {
    "type": "interval",
    "interval": 15
  }
}
```

Interval values: 1, 5, 15, 30, 60 (minutes)

### Cron Scheduling
Advanced scheduling with cron expressions:

```json
{
  "scheduling": {
    "type": "cron",
    "cron": "0 9 * * 1-5"
  }
}
```

### Instant/Webhook
Scenarios triggered by webhooks or app events:

```json
{
  "scheduling": {
    "type": "instant"
  }
}
```

## Best Practices

### 1. **Use Sequential Module IDs**
Always assign sequential IDs starting from 1. This makes module references (`{{1.field}}`) predictable.

### 2. **Set Descriptive Module Names**
Use the `name` field in module metadata to clarify what each module does:

```json
{
  "metadata": {
    "designer": {
      "x": 0,
      "y": 0,
      "name": "Get User from Database"
    }
  }
}
```

### 3. **Position Modules Logically**
Set `x` and `y` coordinates to create a clear visual flow (left-to-right or top-to-bottom).

### 4. **Validate Filter Conditions**
Ensure filter conditions reference valid module fields. Common operators:
- `equal`, `notEqual`
- `greater`, `less`, `greaterOrEqual`, `lessOrEqual`
- `contains`, `notContains`
- `exists`, `notExists`

### 5. **Use Routers for Multiple Outcomes**
When a scenario needs to handle different data types or conditions, use a router rather than nested filters.

### 6. **Handle Empty Results**
Add error handlers or fallback routes to manage cases where a module returns no data.

## Common Patterns

### Pattern 1: Simple Linear Flow
Trigger → Action → Action

```json
{
  "name": "Send Welcome Email",
  "flow": [
    {
      "id": 1,
      "module": "webhook:CustomWebhook"
    },
    {
      "id": 2,
      "module": "gmail:SendEmail",
      "mapper": {
        "to": "{{1.email}}",
        "subject": "Welcome!",
        "body": "Hello {{1.name}}"
      }
    }
  ]
}
```

### Pattern 2: Router with Conditional Routes
Trigger → Router → [Route A | Route B]

```json
{
  "id": 2,
  "module": "router:Router",
  "routes": [
    {
      "filter": {
        "name": "Premium Users",
        "conditions": [
          [{"a": "{{1.plan}}", "o": "equal", "b": "premium"}]
        ]
      },
      "flow": [
        {"id": 3, "module": "slack:SendMessage"}
      ]
    },
    {
      "filter": {
        "name": "Free Users",
        "conditions": [
          [{"a": "{{1.plan}}", "o": "equal", "b": "free"}]
        ]
      },
      "flow": [
        {"id": 4, "module": "gmail:SendEmail"}
      ]
    }
  ]
}
```

### Pattern 3: Aggregator for Batch Processing
Trigger → Iterator → Actions → Aggregator → Summary Action

```json
{
  "flow": [
    {
      "id": 1,
      "module": "http:Get",
      "mapper": {"url": "https://api.example.com/users"}
    },
    {
      "id": 2,
      "module": "iterator:Iterator",
      "mapper": {"array": "{{1.data.users}}"}
    },
    {
      "id": 3,
      "module": "database:UpdateRecord"
    },
    {
      "id": 4,
      "module": "aggregator:NumericAggregator",
      "mapper": {
        "source": 2,
        "target": 3,
        "aggregateFunction": "count"
      }
    },
    {
      "id": 5,
      "module": "slack:SendMessage",
      "mapper": {
        "text": "Processed {{4.value}} users"
      }
    }
  ]
}
```

## MCP Tools for Scenario Building

When building scenarios, use these Make.com MCP tools:

- **`scenarios_create`**: Create a new scenario
- **`scenarios_update`**: Update existing scenario
- **`scenarios_get`**: Fetch scenario details
- **`scenarios_list`**: List all scenarios
- **`scenarios_delete`**: Remove a scenario
- **`scenarios_run`**: Trigger immediate execution
- **`scenarios_activate`**: Enable scenario scheduling
- **`scenarios_deactivate`**: Disable scenario

Refer to **make-mcp-tools-expert** skill for detailed tool usage.

## Examples

See `references/modules.md` for module examples, `references/routers-filters.md` for routing patterns, and `references/scheduling.md` for scheduling configurations.

## Workflow

1. **Plan the scenario flow**: Identify trigger, actions, and decision points
2. **Create modules**: Build each module with proper ID, module name, and configuration
3. **Wire connections**: Link modules in the correct sequence
4. **Add routers/filters**: Implement conditional logic where needed
5. **Configure scheduling**: Set when/how the scenario runs
6. **Use MCP tools**: Push scenario to Make.com via `scenarios_create` or `scenarios_update`
7. **Test and iterate**: Run the scenario, check execution logs, fix errors

## References

- [modules.md](references/modules.md) - Common module configurations
- [routers-filters.md](references/routers-filters.md) - Router and filter patterns
- [scheduling.md](references/scheduling.md) - Scheduling configurations
