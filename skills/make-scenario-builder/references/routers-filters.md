# Routers and Filters in Make.com

This reference explains router and filter patterns for conditional logic in Make.com scenarios.

## Router Basics

A **router** splits a single data flow into multiple parallel routes. Each route can have its own filter conditions.

### Basic Router Structure
```json
{
  "id": 2,
  "module": "router:Router",
  "metadata": {
    "designer": {
      "x": 300,
      "y": 0
    }
  },
  "routes": [
    {
      "filter": {
        "name": "Route 1",
        "conditions": [[...]]
      },
      "flow": [...]
    },
    {
      "filter": {
        "name": "Route 2",
        "conditions": [[...]]
      },
      "flow": [...]
    }
  ]
}
```

## Filter Operators

### Comparison Operators
- `equal` - Exactly equal
- `notEqual` - Not equal
- `greater` - Greater than
- `less` - Less than
- `greaterOrEqual` - Greater than or equal
- `lessOrEqual` - Less than or equal

### String Operators
- `contains` - Contains substring
- `notContains` - Does not contain substring
- `startsWith` - Starts with
- `endsWith` - Ends with

### Existence Operators
- `exists` - Field exists and is not empty
- `notExists` - Field does not exist or is empty

### Pattern Operators
- `matches` - Matches regex pattern
- `notMatches` - Does not match regex pattern

## Filter Condition Structure

### Single Condition
```json
{
  "name": "Active Users",
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
```

### AND Conditions (Multiple conditions in one array)
```json
{
  "name": "Premium Active Users",
  "conditions": [
    [
      {
        "a": "{{1.status}}",
        "o": "equal",
        "b": "active"
      },
      {
        "a": "{{1.plan}}",
        "o": "equal",
        "b": "premium"
      }
    ]
  ]
}
```

### OR Conditions (Multiple arrays)
```json
{
  "name": "Premium or Enterprise",
  "conditions": [
    [
      {
        "a": "{{1.plan}}",
        "o": "equal",
        "b": "premium"
      }
    ],
    [
      {
        "a": "{{1.plan}}",
        "o": "equal",
        "b": "enterprise"
      }
    ]
  ]
}
```

### Complex Logic (AND + OR)
```json
{
  "name": "High Value Customers",
  "conditions": [
    [
      {
        "a": "{{1.plan}}",
        "o": "equal",
        "b": "premium"
      },
      {
        "a": "{{1.revenue}}",
        "o": "greater",
        "b": "1000"
      }
    ],
    [
      {
        "a": "{{1.plan}}",
        "o": "equal",
        "b": "enterprise"
      }
    ]
  ]
}
```

## Common Router Patterns

### Pattern 1: User Type Routing
```json
{
  "id": 2,
  "module": "router:Router",
  "routes": [
    {
      "filter": {
        "name": "Free Users",
        "conditions": [
          [{"a": "{{1.plan}}", "o": "equal", "b": "free"}]
        ]
      },
      "flow": [
        {
          "id": 3,
          "module": "gmail:SendEmail",
          "mapper": {
            "to": "{{1.email}}",
            "subject": "Upgrade to Premium",
            "body": "..."
          }
        }
      ]
    },
    {
      "filter": {
        "name": "Premium/Enterprise",
        "conditions": [
          [{"a": "{{1.plan}}", "o": "equal", "b": "premium"}],
          [{"a": "{{1.plan}}", "o": "equal", "b": "enterprise"}]
        ]
      },
      "flow": [
        {
          "id": 4,
          "module": "slack:SendMessage",
          "mapper": {
            "channel": "premium-support",
            "text": "New premium user: {{1.email}}"
          }
        }
      ]
    }
  ]
}
```

### Pattern 2: Error vs Success Routing
```json
{
  "id": 2,
  "module": "router:Router",
  "routes": [
    {
      "filter": {
        "name": "Success",
        "conditions": [
          [{"a": "{{1.status}}", "o": "equal", "b": "success"}]
        ]
      },
      "flow": [
        {
          "id": 3,
          "module": "database:InsertRow",
          "mapper": {
            "table": "successful_orders",
            "values": "{{1}}"
          }
        }
      ]
    },
    {
      "filter": {
        "name": "Error",
        "conditions": [
          [{"a": "{{1.status}}", "o": "equal", "b": "error"}]
        ]
      },
      "flow": [
        {
          "id": 4,
          "module": "slack:SendMessage",
          "mapper": {
            "channel": "alerts",
            "text": "⚠️ Order failed: {{1.orderId}}"
          }
        }
      ]
    }
  ]
}
```

### Pattern 3: Amount-Based Routing
```json
{
  "id": 2,
  "module": "router:Router",
  "routes": [
    {
      "filter": {
        "name": "High Value (>$1000)",
        "conditions": [
          [{"a": "{{1.amount}}", "o": "greater", "b": "1000"}]
        ]
      },
      "flow": [
        {
          "id": 3,
          "module": "hubspot:CreateDeal",
          "mapper": {
            "amount": "{{1.amount}}",
            "dealstage": "high-priority"
          }
        }
      ]
    },
    {
      "filter": {
        "name": "Medium Value ($100-$1000)",
        "conditions": [
          [
            {"a": "{{1.amount}}", "o": "greaterOrEqual", "b": "100"},
            {"a": "{{1.amount}}", "o": "lessOrEqual", "b": "1000"}
          ]
        ]
      },
      "flow": [
        {
          "id": 4,
          "module": "airtable:CreateRecord",
          "mapper": {
            "base": "leads",
            "table": "Medium Value"
          }
        }
      ]
    },
    {
      "filter": {
        "name": "Low Value (<$100)",
        "conditions": [
          [{"a": "{{1.amount}}", "o": "less", "b": "100"}]
        ]
      },
      "flow": [
        {
          "id": 5,
          "module": "util:SetVariable",
          "mapper": {
            "name": "leadQuality",
            "value": "low"
          }
        }
      ]
    }
  ]
}
```

### Pattern 4: Fallback/Default Route
```json
{
  "id": 2,
  "module": "router:Router",
  "routes": [
    {
      "filter": {
        "name": "Email Exists",
        "conditions": [
          [{"a": "{{1.email}}", "o": "exists"}]
        ]
      },
      "flow": [
        {
          "id": 3,
          "module": "gmail:SendEmail"
        }
      ]
    },
    {
      "filter": {
        "name": "No Email - Use SMS",
        "conditions": [
          [
            {"a": "{{1.email}}", "o": "notExists"},
            {"a": "{{1.phone}}", "o": "exists"}
          ]
        ]
      },
      "flow": [
        {
          "id": 4,
          "module": "twilio:SendSMS"
        }
      ]
    },
    {
      "filter": {
        "name": "No Contact Info - Log",
        "conditions": [
          [
            {"a": "{{1.email}}", "o": "notExists"},
            {"a": "{{1.phone}}", "o": "notExists"}
          ]
        ]
      },
      "flow": [
        {
          "id": 5,
          "module": "database:InsertRow",
          "mapper": {
            "table": "missing_contacts"
          }
        }
      ]
    }
  ]
}
```

## Stand-Alone Filters (Between Modules)

Filters can also be placed between modules without a router:

```json
{
  "sourceModuleId": 1,
  "targetModuleId": 2,
  "filter": {
    "name": "Only Active",
    "conditions": [
      [
        {"a": "{{1.status}}", "o": "equal", "b": "active"}
      ]
    ]
  }
}
```

This prevents module 2 from running unless the filter condition is met.

## Best Practices

### 1. **Name Your Routes Clearly**
Use descriptive filter names to clarify what each route handles.

### 2. **Cover All Cases**
Ensure your router routes cover all possible data states. Add a fallback/default route if needed.

### 3. **Use Existence Checks**
Always check if a field exists before comparing its value:

```json
[
  {"a": "{{1.email}}", "o": "exists"},
  {"a": "{{1.email}}", "o": "contains", "b": "@"}
]
```

### 4. **Avoid Overlapping Conditions**
Make route conditions mutually exclusive to prevent unexpected behavior.

### 5. **Test Edge Cases**
Test with empty values, null values, and unexpected data types.

## Reference Syntax

- `{{1.field}}` - Reference field from module 1
- `{{2.nested.field}}` - Reference nested field
- `{{1.array[0]}}` - Reference array element
- String values in conditions should be quoted: `"active"`
- Numeric values should not be quoted: `1000`
