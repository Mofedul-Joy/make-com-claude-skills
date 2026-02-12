# Blueprint Structure Reference

Quick reference for Make.com Blueprint JSON structure.

## Minimal Blueprint

```json
{
  "name": "Minimal Scenario",
  "flow": [
    {
      "id": 1,
      "module": "webhook:CustomWebhook",
      "parameters": {}
    }
  ],
  "connections": []
}
```

## Complete Blueprint Template

```json
{
  "name": "Complete Scenario Template",
  "scheduling": {
    "type": "interval",
    "interval": 15
  },
  "flow": [
    {
      "id": 1,
      "module": "app:TriggerName",
      "version": 1,
      "parameters": {
        "key": "value"
      },
      "mapper": {},
      "metadata": {
        "designer": {
          "x": 0,
          "y": 0,
          "name": "Module Display Name"
        }
      }
    }
  ],
  "connections": [
    {
      "sourceModuleId": 1,
      "targetModuleId": 2
    }
  ],
  "metadata": {
    "folder": "folder-id",
    "tags": ["tag1", "tag2"]
  },
  "settings": {
    "sequential": false,
    "maxErrors": 3,
    "autoCommit": true
  }
}
```

## Field Descriptions

### Root Level

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Scenario display name |
| `flow` | array | Yes | Array of modules |
| `connections` | array | Yes | Module connections |
| `scheduling` | object | No | When scenario runs |
| `metadata` | object | No | Folder, tags, etc. |
| `settings` | object | No | Execution settings |

### Module (Flow Item)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | number | Yes | Unique module ID (sequential) |
| `module` | string | Yes | Module type (`app:ActionName`) |
| `version` | number | No | Module version (default: 1) |
| `parameters` | object | Yes | Static configuration |
| `mapper` | object | Yes | Dynamic field mappings |
| `metadata` | object | No | Designer info and name |

### Connection

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sourceModuleId` | number | Yes | Source module ID |
| `targetModuleId` | number | Yes (or null for router) | Target module ID |
| `filter` | object | No | Optional filter conditions |
| `routes` | array | No | Router routes (routers only) |

### Scheduling

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"interval"`, `"cron"`, or `"instant"` |
| `interval` | number | For interval | Minutes: 1, 5, 15, 30, 60 |
| `cron` | string | For cron | Cron expression |

### Metadata (Root)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `folder` | string | No | Folder ID |
| `tags` | array | No | Array of tag strings |

### Metadata (Module)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `designer` | object | No | Visual positioning |
| `designer.x` | number | No | X coordinate |
| `designer.y` | number | No | Y coordinate |
| `designer.name` | string | No | Module display name |

### Settings

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sequential` | boolean | No | Sequential vs parallel execution |
| `maxErrors` | number | No | Max consecutive errors before stopping |
| `autoCommit` | boolean | No | Auto-commit successful operations |

## Module Types Reference

### Triggers
- `webhook:CustomWebhook`
- `http:Get`
- `gmail:WatchEmails`
- `scheduler:Trigger`

### Actions
- `http:ActionSendData` (HTTP request)
- `gmail:SendEmail`
- `slack:ActionPostMessage`
- `database:SelectRows`, `database:InsertRow`, `database:UpdateRows`
- `airtable:CreateRecord`, `airtable:UpdateRecord`

### Control Flow
- `router:Router`
- `iterator:Iterator`
- `aggregator:NumericAggregator`, `aggregator:ArrayAggregator`
- `util:Sleep`

### Data Transformation
- `json:ParseJSON`, `json:CreateJSON`
- `text-parser:MatchPattern`

### Error Handling
- `error-handler:Resume`
- `error-handler:Commit`
- `error-handler:Rollback`
- `error-handler:Ignore`
- `error-handler:Break`

## Mapping Syntax Reference

### Basic Field Reference
```json
"{{1.fieldName}}"
```

### Nested Fields
```json
"{{1.data.user.email}}"
```

### Array Access
```json
"{{1.items[0]}}"
```

### Array Iteration
```json
"{{1.items}}"  // Whole array
```

### String Concatenation
```json
"Hello {{1.firstName}} {{1.lastName}}"
```

### Functions
```json
"{{upper(1.name)}}"
"{{formatDate(now, 'YYYY-MM-DD')}}"
"{{toJSON(1)}}"
```

## Filter Condition Reference

### Structure
```json
{
  "name": "Filter Name",
  "conditions": [
    [
      {
        "a": "{{1.field}}",  // Left operand
        "o": "equal",        // Operator
        "b": "value"         // Right operand
      }
    ]
  ]
}
```

### Operators
- `equal`, `notEqual`
- `greater`, `less`, `greaterOrEqual`, `lessOrEqual`
- `contains`, `notContains`
- `startsWith`, `endsWith`
- `exists`, `notExists`
- `matches`, `notMatches` (regex)

### AND Logic (multiple conditions in same array)
```json
{
  "conditions": [
    [
      {"a": "{{1.status}}", "o": "equal", "b": "active"},
      {"a": "{{1.plan}}", "o": "equal", "b": "premium"}
    ]
  ]
}
```

### OR Logic (multiple arrays)
```json
{
  "conditions": [
    [{"a": "{{1.plan}}", "o": "equal", "b": "premium"}],
    [{"a": "{{1.plan}}", "o": "equal", "b": "enterprise"}]
  ]
}
```

## Router Structure

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
        {"id": 3, "module": "...", ...}
      ]
    },
    {
      "filter": {
        "name": "Route 2",
        "conditions": [[...]]
      },
      "flow": [
        {"id": 4, "module": "...", ...}
      ]
    }
  ]
}
```

## Common Patterns

### Pattern: Linear Flow (A → B → C)
```json
{
  "flow": [
    {"id": 1, "module": "webhook:CustomWebhook"},
    {"id": 2, "module": "http:Get"},
    {"id": 3, "module": "gmail:SendEmail"}
  ],
  "connections": [
    {"sourceModuleId": 1, "targetModuleId": 2},
    {"sourceModuleId": 2, "targetModuleId": 3}
  ]
}
```

### Pattern: Router (A → Router → [B | C])
```json
{
  "flow": [
    {"id": 1, "module": "webhook:CustomWebhook"},
    {
      "id": 2,
      "module": "router:Router",
      "routes": [
        {"filter": {...}, "flow": [{"id": 3, ...}]},
        {"filter": {...}, "flow": [{"id": 4, ...}]}
      ]
    }
  ],
  "connections": [
    {"sourceModuleId": 1, "targetModuleId": 2}
  ]
}
```

### Pattern: Iterator (A → Iterator → B → Aggregator → C)
```json
{
  "flow": [
    {"id": 1, "module": "http:Get"},
    {"id": 2, "module": "iterator:Iterator", "mapper": {"array": "{{1.items}}"}},
    {"id": 3, "module": "database:InsertRow"},
    {
      "id": 4,
      "module": "aggregator:NumericAggregator",
      "mapper": {
        "source": 2,
        "target": 3,
        "aggregateFunction": "count"
      }
    },
    {"id": 5, "module": "slack:SendMessage"}
  ],
  "connections": [
    {"sourceModuleId": 1, "targetModuleId": 2},
    {"sourceModuleId": 2, "targetModuleId": 3},
    {"sourceModuleId": 3, "targetModuleId": 4},
    {"sourceModuleId": 4, "targetModuleId": 5}
  ]
}
```
