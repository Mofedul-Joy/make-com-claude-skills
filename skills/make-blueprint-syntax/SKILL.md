---
name: make-blueprint-syntax
description: Deep dive into Make.com's Blueprint JSON structure, manipulation techniques, and import/export workflows
---

# Make.com Blueprint Syntax

## Overview

Blueprints are Make.com's JSON representation of scenarios. This skill teaches how to read, write, and manipulate Blueprint JSON to build scenarios programmatically or import/export scenario configurations.

## When to Use This Skill

Use this skill when:
- Creating scenarios from scratch in JSON format
- Importing/exporting scenario configurations
- Manipulating scenario structure programmatically
- Understanding scenario JSON responses from MCP tools
- Converting templates or existing scenarios

## Blueprint Structure

A complete Make.com Blueprint has this top-level structure:

```json
{
  "name": "Scenario Name",
  "flow": [...],
  "connections": [...],
  "metadata": {...},
  "scheduling": {...},
  "settings": {...}
}
```

### Top-Level Fields

#### `name` (string, required)
The scenario's display name.

```json
{
  "name": "Daily User Sync"
}
```

#### `flow` (array, required)
Array of modules representing the scenario's logic.

```json
{
  "flow": [
    {
      "id": 1,
      "module": "webhook:CustomWebhook",
      ...
    },
    {
      "id": 2,
      "module": "http:ActionSendData",
      ...
    }
  ]
}
```

#### `connections` (array, required)
Defines how modules connect to each other.

```json
{
  "connections": [
    {
      "sourceModuleId": 1,
      "targetModuleId": 2
    }
  ]
}
```

#### `scheduling` (object, optional)
When and how the scenario runs.

```json
{
  "scheduling": {
    "type": "interval",
    "interval": 15
  }
}
```

#### `metadata` (object, optional)
Additional scenario information (folder, tags, etc.).

```json
{
  "metadata": {
    "folder": "folder-id",
    "tags": ["production", "urgent"]
  }
}
```

#### `settings` (object, optional)
Scenario execution settings.

```json
{
  "settings": {
    "sequential": false,
    "maxErrors": 3
  }
}
```

## Module Structure (Flow Items)

Each module in the `flow` array follows this structure:

```json
{
  "id": 1,
  "module": "app-name:ActionName",
  "version": 1,
  "parameters": {...},
  "mapper": {...},
  "metadata": {...}
}
```

### Module Fields

#### `id` (number, required)
Unique sequential identifier. Start from 1.

```json
{"id": 1}
```

#### `module` (string, required)
Module identifier in `app-name:ActionName` format.

```json
{"module": "gmail:SendEmail"}
```

Common module formats:
- `webhook:CustomWebhook`
- `http:ActionSendData`
- `gmail:SendEmail`
- `slack:ActionPostMessage`
- `router:Router`
- `iterator:Iterator`
- `aggregator:NumericAggregator`

#### `version` (number, optional)
Module version, typically `1`.

```json
{"version": 1}
```

#### `parameters` (object, required)
Static configuration values that don't change between executions.

```json
{
  "parameters": {
    "handleErrors": false,
    "connection": "connection-id"
  }
}
```

#### `mapper` (object, required)
Dynamic field mappings that can reference previous modules.

```json
{
  "mapper": {
    "to": "{{1.email}}",
    "subject": "Welcome!",
    "body": "Hello {{1.name}}"
  }
}
```

#### `metadata` (object, optional)
Visual designer info and module name.

```json
{
  "metadata": {
    "designer": {
      "x": 300,
      "y": 0,
      "name": "Send Welcome Email"
    }
  }
}
```

## Connection Structure

Connections link modules together to define data flow.

### Simple Connection
```json
{
  "sourceModuleId": 1,
  "targetModuleId": 2
}
```

### Connection with Filter
```json
{
  "sourceModuleId": 1,
  "targetModuleId": 2,
  "filter": {
    "name": "Only Active Users",
    "conditions": [
      [
        {
          "a": "{{1.status}}",
          "o": "equal",
          "b": "active"
        }
      ]
    ]
  }
}
```

### Router Connection
```json
{
  "sourceModuleId": 1,
  "targetModuleId": null,  // Router has no single target
  "routes": [
    {
      "filter": {...},
      "flow": [...]
    }
  ]
}
```

## Data Mapping Syntax

### Referencing Previous Modules

Use `{{moduleId.field}}` syntax:

```json
{
  "mapper": {
    "email": "{{1.email}}",
    "name": "{{1.firstName}} {{1.lastName}}",
    "timestamp": "{{now}}"
  }
}
```

### Nested Fields
```json
{
  "mapper": {
    "userId": "{{1.data.user.id}}",
    "address": "{{1.data.address.street}}"
  }
}
```

### Array References
```json
{
  "mapper": {
    "firstItem": "{{1.items[0]}}",
    "allItems": "{{1.items}}"
  }
}
```

### Functions
Make.com supports built-in functions:

```json
{
  "mapper": {
    "uppercaseName": "{{upper(1.name)}}",
    "formattedDate": "{{formatDate(now, 'YYYY-MM-DD')}}",
    "jsonString": "{{toJSON(1)}}"
  }
}
```

Common functions:
- `upper()`, `lower()`, `trim()`
- `formatDate()`, `now`, `addDays()`
- `toJSON()`, `parseJSON()`
- `length()`, `join()`, `split()`

## Special Module Types

### Router Module

```json
{
  "id": 2,
  "module": "router:Router",
  "metadata": {
    "designer": {"x": 300, "y": 0}
  },
  "routes": [
    {
      "filter": {
        "name": "Route 1",
        "conditions": [[...]]
      },
      "flow": [
        {"id": 3, "module": "..."}
      ]
    }
  ]
}
```

### Iterator Module

```json
{
  "id": 2,
  "module": "iterator:Iterator",
  "mapper": {
    "array": "{{1.items}}"
  }
}
```

### Aggregator Module

```json
{
  "id": 4,
  "module": "aggregator:NumericAggregator",
  "mapper": {
    "source": 2,  // Iterator module ID
    "target": 3,  // Last module in iteration
    "aggregateFunction": "sum",
    "value": "{{3.amount}}"
  }
}
```

### Error Handler

```json
{
  "id": 5,
  "module": "error-handler:Resume",
  "mapper": {},
  "metadata": {
    "errorHandler": {
      "moduleId": 3,  // Module this handles errors for
      "strategy": "resume"
    }
  }
}
```

## Complete Blueprint Example

```json
{
  "name": "User Registration Flow",
  "scheduling": {
    "type": "instant"
  },
  "flow": [
    {
      "id": 1,
      "module": "webhook:CustomWebhook",
      "version": 1,
      "parameters": {
        "hook": "webhook-id"
      },
      "metadata": {
        "designer": {"x": 0, "y": 0, "name": "Receive Registration"}
      }
    },
    {
      "id": 2,
      "module": "router:Router",
      "metadata": {
        "designer": {"x": 300, "y": 0}
      },
      "routes": [
        {
          "filter": {
            "name": "Premium Users",
            "conditions": [
              [{"a": "{{1.plan}}", "o": "equal", "b": "premium"}]
            ]
          },
          "flow": [
            {
              "id": 3,
              "module": "slack:ActionPostMessage",
              "mapper": {
                "channel": "premium-signups",
                "text": "New premium user: {{1.email}}"
              }
            }
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
            {
              "id": 4,
              "module": "gmail:SendEmail",
              "mapper": {
                "to": "{{1.email}}",
                "subject": "Welcome!",
                "body": "Thanks for signing up!"
              }
            }
          ]
        }
      ]
    }
  ],
  "connections": [
    {
      "sourceModuleId": 1,
      "targetModuleId": 2
    }
  ],
  "metadata": {
    "folder": "production",
    "tags": ["users", "automation"]
  }
}
```

## Blueprint Manipulation

### Adding a Module
1. Choose next available ID
2. Add to `flow` array
3. Update `connections` to wire it in

```json
// Before
{"flow": [{"id": 1, ...}, {"id": 2, ...}]}

// After (adding module 3)
{"flow": [
  {"id": 1, ...},
  {"id": 2, ...},
  {"id": 3, "module": "gmail:SendEmail", ...}
]}

// Update connections
{"connections": [
  {"sourceModuleId": 1, "targetModuleId": 2},
  {"sourceModuleId": 2, "targetModuleId": 3}  // New connection
]}
```

### Removing a Module
1. Remove from `flow` array
2. Remove related connections
3. Update any module references in mappers

### Updating Module Configuration
Locate module by ID and update `parameters` or `mapper`:

```json
{
  "flow": [
    {
      "id": 2,
      "module": "http:ActionSendData",
      "mapper": {
        "url": "https://new-api.example.com"  // Updated
      }
    }
  ]
}
```

## Best Practices

### 1. **Sequential IDs**
Always use sequential IDs starting from 1. Don't skip numbers.

### 2. **Valid Module References**
Ensure `{{moduleId.field}}` references only exist for modules with lower IDs.

### 3. **Complete Connections**
Every module (except triggers and routers) should have an incoming connection.

### 4. **Designer Coordinates**
Set logical `x` and `y` values for visual clarity (e.g., increment by 300 per module).

### 5. **Name Modules**
Use `metadata.designer.name` to document what each module does.

### 6. **Validate JSON**
Always validate JSON syntax before sending to MCP tools.

## Import/Export Workflow

### Export Scenario
Use `scenarios_get` MCP tool to retrieve Blueprint JSON:

```typescript
// MCP tool call
{
  "tool": "scenarios_get",
  "parameters": {
    "scenarioId": "123456"
  }
}

// Response contains complete Blueprint
```

### Import Scenario
Use `scenarios_create` with Blueprint JSON:

```typescript
{
  "tool": "scenarios_create",
  "parameters": {
    "name": "Imported Scenario",
    "flow": [...],
    "connections": [...]
  }
}
```

### Modify and Re-import
1. Export with `scenarios_get`
2. Modify Blueprint JSON
3. Update with `scenarios_update`

## References

- [Blueprint Structure Reference](references/blueprint-structure.md)
- **make-scenario-builder**: Module and connection patterns
- **make-mcp-tools-expert**: Using MCP tools with Blueprints
