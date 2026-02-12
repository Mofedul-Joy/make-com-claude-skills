---
name: make-mcp-tools-expert
description: Expert guidance on selecting the right Make.com MCP server tools and formatting parameters correctly for API operations
---

# Make.com MCP Tools Expert

## Overview

This skill provides expert guidance on using the Make.com MCP server tools effectively. The Make.com MCP server (@makehq/mcp-server) provides 130+ API operations for managing scenarios, connections, webhooks, data stores, templates, custom functions, teams, and more.

## When to Use This Skill

Use this skill when:
- Selecting the appropriate MCP tool for a Make.com operation
- Formatting tool parameters correctly
- Troubleshooting MCP tool errors
- Understanding API operation responses
- Working with scenarios, connections, webhooks, or other Make.com resources

## MCP Server Tools Overview

### Scenario Operations
- `scenarios_list` - List all scenarios
- `scenarios_get` - Get scenario by ID
- `scenarios_create` - Create new scenario
- `scenarios_update` - Update existing scenario
- `scenarios_delete` - Delete scenario
- `scenarios_clone` - Duplicate scenario
- `scenarios_run` - Trigger immediate execution
- `scenarios_activate` - Enable scenario
- `scenarios_deactivate` - Disable scenario

### Connection Operations
- `connections_list` - List all connections
- `connections_get` - Get connection details
- `connections_create` - Create new connection
- `connections_update` - Update connection
- `connections_delete` - Delete connection
- `connections_test` - Test connection validity

### Webhook Operations
- `webhooks_list` - List all webhooks
- `webhooks_get` - Get webhook details
- `webhooks_create` - Create webhook
- `webhooks_delete` - Delete webhook
- `webhooks_test` - Test webhook

### Data Store Operations
- `datastores_list` - List data stores
- `datastores_get` - Get data store
- `datastores_create` - Create data store
- `datastores_update` - Update data store
- `datastores_delete` - Delete data store
- `datastores_data_get` - Get data from store
- `datastores_data_add` - Add data to store
- `datastores_data_update` - Update data in store
- `datastores_data_delete` - Delete data from store

### Template Operations
- `templates_list` - List public templates
- `templates_get` - Get template details
- `templates_create_from_scenario` - Create template from scenario

### Custom Function Operations
- `functions_list` - List custom functions
- `functions_get` - Get function details
- `functions_create` - Create custom function
- `functions_update` - Update function
- `functions_delete` - Delete function
- `functions_test` - Test function execution

### Team & Organization Operations
- `teams_list` - List teams
- `teams_get` - Get team details
- `organizations_get` - Get organization info
- `users_list` - List users

### Execution & DLQ Operations
- `executions_list` - List scenario executions
- `executions_get` - Get execution details
- `dlq_list` - List dead letter queue items
- `dlq_get` - Get DLQ item
- `dlq_requeue` - Retry failed execution

## Common Tool Usage Patterns

### Pattern 1: Creating a Scenario

```typescript
// Use scenarios_create tool
{
  "name": "New Automation",
  "scheduling": {
    "type": "interval",
    "interval": 15
  },
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

### Pattern 2: Updating a Scenario

```typescript
// Use scenarios_update tool
{
  "scenarioId": "123456",
  "name": "Updated Automation",
  "flow": [...],  // Complete updated flow
  "connections": [...]
}
```

### Pattern 3: Listing Scenarios with Filters

```typescript
// Use scenarios_list tool
{
  "filter": {
    "active": true,
    "folderId": "folder-id"
  },
  "limit": 50
}
```

### Pattern 4: Running a Scenario

```typescript
// Use scenarios_run tool
{
  "scenarioId": "123456"
}
```

### Pattern 5: Creating a Connection

```typescript
// Use connections_create tool
{
  "app": "gmail",
  "accountName": "My Gmail",
  "credentials": {
    // App-specific credentials
  }
}
```

### Pattern 6: Managing Webhooks

```typescript
// Use webhooks_create tool
{
  "name": "Payment Webhook",
  "webhookUrl": "https://hook.make.com/...",
  "method": "POST"
}
```

## Parameter Formatting Best Practices

### 1. **Always Provide Required Fields**
Check the tool's expected parameters and ensure all required fields are present.

### 2. **Use Correct Data Types**
- IDs: String (e.g., `"123456"`)
- Booleans: `true` or `false`
- Numbers: No quotes (e.g., `15`)
- Objects: Properly nested JSON

### 3. **Scenario IDs**
Scenario IDs are typically numeric strings:
```typescript
{
  "scenarioId": "123456"  // Correct
  // NOT: scenarioId: 123456 (number)
}
```

### 4. **Complete vs Partial Updates**
- `scenarios_create`: Requires complete scenario structure
- `scenarios_update`: Also requires complete structure (not partial)
- Always include `flow` and `connections` when updating

### 5. **Scheduling Format**
Scheduling must match the exact format:
```typescript
{
  "scheduling": {
    "type": "interval",  // or "cron" or "instant"
    "interval": 15       // only for type: "interval"
    // or "cron": "0 9 * * *" for type: "cron"
  }
}
```

### 6. **Empty Arrays vs Null**
- Use empty arrays for no connections: `"connections": []`
- Use empty arrays for no routes: `"routes": []`
- Don't use `null` for array fields

## Error Handling

### Common Errors and Solutions

#### Error: "Scenario not found"
```typescript
// Problem: Invalid scenario ID
{ "scenarioId": "999999" }

// Solution: Verify scenario ID exists
// Use scenarios_list to get valid IDs
```

#### Error: "Invalid scheduling configuration"
```typescript
// Problem: Wrong scheduling format
{
  "scheduling": {
    "interval": 15  // Missing "type"
  }
}

// Solution: Include type field
{
  "scheduling": {
    "type": "interval",
    "interval": 15
  }
}
```

#### Error: "Invalid module reference"
```typescript
// Problem: Module references non-existent module
{
  "id": 2,
  "mapper": {
    "field": "{{3.value}}"  // Module 3 doesn't exist
  }
}

// Solution: Ensure referenced modules exist and have lower IDs
```

#### Error: "Connection not authorized"
```typescript
// Problem: Connection credentials expired or invalid

// Solution: Use connections_test to verify
// Re-authorize connection if needed
// Use connections_update to refresh credentials
```

## Response Handling

### Successful Response
```json
{
  "success": true,
  "data": {
    "scenarioId": "123456",
    "name": "My Scenario",
    ...
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "message": "Scenario not found",
    "code": "NOT_FOUND"
  }
}
```

### Pagination
Many list operations support pagination:
```typescript
{
  "limit": 50,  // Items per page
  "offset": 0   // Starting position
}
```

## Tool Selection Guide

| Goal | Recommended Tool | Notes |
|------|------------------|-------|
| Create new scenario | `scenarios_create` | Requires complete structure |
| Update scenario | `scenarios_update` | Pass complete updated structure |
| Enable scenario | `scenarios_activate` | Only needs scenario ID |
| Disable scenario | `scenarios_deactivate` | Only needs scenario ID |
| Run scenario now | `scenarios_run` | Triggers immediate execution |
| List all scenarios | `scenarios_list` | Supports filtering |
| Get scenario details | `scenarios_get` | Returns full scenario JSON |
| Delete scenario | `scenarios_delete` | Permanent deletion |
| Duplicate scenario | `scenarios_clone` | Creates copy with new ID |
| Create connection | `connections_create` | Requires app-specific credentials |
| List connections | `connections_list` | Shows all available connections |
| Create webhook | `webhooks_create` | Returns webhook URL |
| Test execution | `scenarios_run` | Use for validation |
| View execution logs | `executions_list` | Filter by scenario ID |
| Check failed runs | `dlq_list` | Shows dead letter queue |

## Best Practices

### 1. **Test Before Production**
Always test scenarios with `scenarios_run` before activating scheduling.

### 2. **Use Descriptive Names**
Name scenarios, connections, and webhooks clearly for easy identification.

### 3. **Validate Responses**
Check the `success` field before processing response data.

### 4. **Handle Pagination**
For large datasets, implement proper pagination with `limit` and `offset`.

### 5. **Monitor Executions**
Regularly check `executions_list` and `dlq_list` for errors.

### 6. **Version Control Scenarios**
Before major updates, use `scenarios_clone` to create a backup.

### 7. **Clean Up Unused Resources**
Delete unused scenarios, connections, and webhooks to keep environment clean.

## Environment Variables

The MCP server requires these environment variables:

- `MAKE_API_KEY` (required): Your Make.com API key
- `MAKE_ZONE` (optional): Region (us1, us2, eu1, eu2, etc.)
- `MAKE_TEAM_ID` (optional): Team ID for organization features

## Related Skills

- **make-scenario-builder**: Building scenario structure and modules
- **make-blueprint-syntax**: Understanding Blueprint JSON format
- **make-validation-expert**: Troubleshooting and debugging
- **make-module-configuration**: App-specific module setup
