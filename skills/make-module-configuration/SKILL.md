---
name: make-module-configuration
description: App-specific module setup and parameter configuration patterns for popular Make.com integrations
---

# Make.com Module Configuration

## Overview

This skill provides detailed guidance on configuring specific app modules in Make.com scenarios. Different apps have unique parameter requirements, authentication methods, and data structures. This skill helps ensure modules are configured correctly for reliable execution.

## When to Use This Skill

Use this skill when:
- Configuring a new module for a specific app (Gmail, Slack, HTTP, etc.)
- Understanding app-specific parameter requirements
- Setting up connections and authentication
- Mapping data fields correctly for an app
- Troubleshooting module configuration errors

## Module Configuration Components

Every Make.com module has three key configuration areas:

### 1. **Parameters** (Static Configuration)
Fixed settings that don't change between executions:
- Connection ID
- App-specific settings
- Error handling preferences

### 2. **Mapper** (Dynamic Configuration)
Field mappings that can reference previous modules:
- Email addresses, URLs, message content
- Data from previous modules (`{{1.field}}`)
- Computed values and functions

### 3. **Metadata** (Visual & Organizational)
Designer positioning and module naming:
- X/Y coordinates for visual layout
- Custom module name for clarity

## Connection Setup

Most app modules require a connection to authenticate with external services.

### Creating Connections

```json
{
  "parameters": {
    "connection": "connection-id-here"
  }
}
```

Use the `connections_create` MCP tool to create connections:

```typescript
{
  "app": "gmail",
  "accountName": "My Gmail Account",
  "credentials": {
    // Gmail OAuth credentials
  }
}
```

### Common Connection Patterns

#### OAuth-Based Apps (Gmail, Google Drive, Slack)
```json
{
  "parameters": {
    "connection": "oauth-connection-id"
  }
}
```

#### API Key Apps (HTTP, Custom APIs)
```json
{
  "parameters": {
    "connection": "api-key-connection-id"
  },
  "mapper": {
    "headers": [
      {
        "name": "Authorization",
        "value": "Bearer {{connection.apiKey}}"
      }
    ]
  }
}
```

#### Database Connections
```json
{
  "parameters": {
    "connection": "database-connection-id",
    "database": "production_db"
  }
}
```

## App-Specific Configuration

### HTTP Module

```json
{
  "id": 1,
  "module": "http:ActionSendData",
  "parameters": {
    "handleErrors": false
  },
  "mapper": {
    "url": "https://api.example.com/endpoint",
    "method": "POST",
    "headers": [
      {
        "name": "Content-Type",
        "value": "application/json"
      },
      {
        "name": "Authorization",
        "value": "Bearer {{apiToken}}"
      }
    ],
    "body": "{{toJSON(1.data)}}",
    "parseResponse": true,
    "timeout": 300
  }
}
```

**Key Fields:**
- `url`: Endpoint URL (can include query params)
- `method`: GET, POST, PUT, DELETE, PATCH
- `headers`: Array of {name, value} objects
- `body`: Request body (use `toJSON()` for objects)
- `parseResponse`: Auto-parse JSON responses
- `timeout`: Seconds to wait for response

### Gmail Module

#### Send Email
```json
{
  "id": 2,
  "module": "gmail:ActionSendEmail",
  "parameters": {
    "connection": "gmail-connection-id"
  },
  "mapper": {
    "to": "{{1.email}}",
    "cc": "",
    "bcc": "",
    "subject": "Order Confirmation #{{1.orderId}}",
    "html": "<h1>Thanks for your order!</h1><p>{{1.message}}</p>",
    "text": "Thanks for your order! {{1.message}}",
    "attachments": []
  }
}
```

**Key Fields:**
- `to`: Recipient email (required)
- `subject`: Email subject
- `html`: HTML email body
- `text`: Plain text alternative
- `attachments`: Array of file objects

#### Watch Emails (Trigger)
```json
{
  "id": 1,
  "module": "gmail:WatchEmails",
  "parameters": {
    "connection": "gmail-connection-id",
    "criteria": "is:unread"
  }
}
```

### Slack Module

#### Send Message
```json
{
  "id": 3,
  "module": "slack:ActionPostMessage",
  "parameters": {
    "connection": "slack-connection-id"
  },
  "mapper": {
    "channel": "C123456789",  // Channel ID
    "text": "New order: {{1.orderId}}",
    "username": "Order Bot",
    "iconEmoji": ":package:",
    "attachments": [],
    "blocks": []
  }
}
```

**Key Fields:**
- `channel`: Channel ID (not name)
- `text`: Message text (supports Slack markdown)
- `username`: Override bot username
- `iconEmoji`: Bot icon emoji
- `blocks`: Slack Block Kit for rich formatting

### Database Modules (PostgreSQL, MySQL)

#### Select Rows
```json
{
  "id": 4,
  "module": "postgresql:SelectRows",
  "parameters": {
    "connection": "db-connection-id"
  },
  "mapper": {
    "table": "users",
    "fields": ["id", "email", "name", "created_at"],
    "condition": "email = '{{1.email}}'",
    "orderBy": "created_at DESC",
    "limit": 10
  }
}
```

**Key Fields:**
- `table`: Table name
- `fields`: Array of column names
- `condition`: WHERE clause (use single quotes for strings)
- `orderBy`: Sorting
- `limit`: Max rows to return

#### Insert Row
```json
{
  "id": 5,
  "module": "postgresql:InsertRow",
  "parameters": {
    "connection": "db-connection-id"
  },
  "mapper": {
    "table": "orders",
    "values": {
      "user_id": "{{1.userId}}",
      "total": "{{1.amount}}",
      "status": "pending",
      "created_at": "{{now}}"
    }
  }
}
```

### Airtable Module

#### Create Record
```json
{
  "id": 6,
  "module": "airtable:CreateRecord",
  "parameters": {
    "connection": "airtable-connection-id"
  },
  "mapper": {
    "base": "app1234567890",
    "table": "Contacts",
    "fields": {
      "Name": "{{1.name}}",
      "Email": "{{1.email}}",
      "Status": "Active",
      "Tags": ["customer", "new"]
    }
  }
}
```

**Key Fields:**
- `base`: Base ID (starts with "app")
- `table`: Table name
- `fields`: Object with Airtable field names as keys

### Webhook Module

#### Custom Webhook (Trigger)
```json
{
  "id": 1,
  "module": "webhook:CustomWebhook",
  "parameters": {
    "hook": "webhook-id-generated-by-make",
    "dataStructure": null
  }
}
```

**Key Fields:**
- `hook`: Webhook ID (create via `webhooks_create` MCP tool)
- `dataStructure`: Optional schema definition

#### Webhook Response
```json
{
  "id": 7,
  "module": "webhook:WebhookResponse",
  "mapper": {
    "status": "200",
    "body": "{{toJSON(2)}}",
    "headers": [
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ]
  }
}
```

### JSON Module

#### Parse JSON
```json
{
  "id": 8,
  "module": "json:ParseJSON",
  "mapper": {
    "json": "{{1.body}}"
  }
}
```

#### Create JSON
```json
{
  "id": 9,
  "module": "json:CreateJSON",
  "mapper": {
    "object": {
      "orderId": "{{1.orderId}}",
      "customer": {
        "name": "{{1.name}}",
        "email": "{{1.email}}"
      },
      "timestamp": "{{now}}"
    }
  }
}
```

### Iterator & Aggregator

#### Iterator
```json
{
  "id": 10,
  "module": "iterator:Iterator",
  "mapper": {
    "array": "{{1.items}}"
  }
}
```

#### Numeric Aggregator
```json
{
  "id": 12,
  "module": "aggregator:NumericAggregator",
  "mapper": {
    "source": 10,  // Iterator module ID
    "target": 11,  // Last module in iteration
    "aggregateFunction": "sum",  // sum, avg, count, min, max
    "value": "{{11.amount}}"
  }
}
```

## Common Configuration Patterns

### Pattern 1: API Request with Auth
```json
{
  "module": "http:ActionSendData",
  "mapper": {
    "url": "https://api.example.com/users",
    "method": "GET",
    "headers": [
      {
        "name": "Authorization",
        "value": "Bearer {{env.API_KEY}}"
      },
      {
        "name": "Accept",
        "value": "application/json"
      }
    ]
  }
}
```

### Pattern 2: Conditional Email Sending
```json
{
  "module": "gmail:ActionSendEmail",
  "mapper": {
    "to": "{{1.email}}",
    "subject": "{{if(1.status = 'premium', 'Premium Welcome', 'Standard Welcome')}}",
    "html": "<h1>Welcome {{1.name}}!</h1>"
  }
}
```

### Pattern 3: Database with Dynamic Condition
```json
{
  "module": "postgresql:SelectRows",
  "mapper": {
    "table": "orders",
    "fields": ["*"],
    "condition": "user_id = {{1.userId}} AND status = '{{1.statusFilter}}'"
  }
}
```

## Best Practices

### 1. **Always Test Connections**
Use `connections_test` MCP tool before using in scenarios.

### 2. **Validate Required Fields**
Check app documentation for required vs optional fields.

### 3. **Use Proper Data Types**
- Strings: Wrap in quotes or use `{{toString(value)}}`
- Numbers: No quotes, or use `{{toNumber(value)}}`
- Booleans: `true` or `false` (no quotes)
- Arrays: Ensure field expects array format
- Objects: Use `{{toJSON(object)}}` when needed

### 4. **Handle Empty Values**
Use `{{ifempty(1.field, 'default')}}` to provide fallbacks.

### 5. **Format Dates Consistently**
```json
{
  "mapper": {
    "date": "{{formatDate(1.timestamp, 'YYYY-MM-DD HH:mm:ss')}}"
  }
}
```

### 6. **Escape Special Characters**
In SQL conditions, escape single quotes: `O''Reilly`

### 7. **Use Connection Variables**
Reference connection-stored values: `{{connection.apiKey}}`

### 8. **Set Timeouts Appropriately**
For slow APIs, increase timeout in HTTP modules.

## Troubleshooting Configuration

### Error: "Required field missing"
- Check app's required fields
- Ensure mapper includes all required fields
- Verify data types match expectations

### Error: "Invalid connection"
- Test connection with `connections_test`
- Re-authorize OAuth connections if expired
- Verify connection ID is correct

### Error: "Invalid JSON"
- Validate JSON with `{{toJSON()}}` function
- Check for proper escaping of quotes

### Error: "Field not found"
- Verify previous module outputs the field
- Check for typos in field names
- Use `{{1}}` to see all available fields

## Related Skills

- **make-scenario-builder**: Building complete scenarios
- **make-mcp-tools-expert**: Managing connections via MCP
- **make-validation-expert**: Debugging configuration issues
