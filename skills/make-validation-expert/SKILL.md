---
name: make-validation-expert
description: Debugging, troubleshooting, and scenario validation techniques for identifying and fixing Make.com scenario issues
---

# Make.com Validation Expert

## Overview

This skill provides expert guidance on debugging Make.com scenarios, identifying common errors, interpreting execution logs, and systematically troubleshooting issues. Use this skill to diagnose problems and validate scenario correctness before production.

## When to Use This Skill

Use this skill when:
- Debugging failed scenario executions
- Validating scenario structure before deployment
- Interpreting error messages and execution logs
- Identifying module configuration issues
- Troubleshooting connection problems
- Analyzing dead letter queue items

## Validation Checklist

Before deploying a scenario, verify:

### 1. **Scenario Structure**
- [ ] All modules have sequential IDs (1, 2, 3...)
- [ ] No missing module IDs in the sequence
- [ ] Every module (except first) has an incoming connection
- [ ] Router modules have `routes` defined
- [ ] No circular connections

### 2. **Module Configuration**
- [ ] All required fields are populated
- [ ] Module references `{{N.field}}` only reference earlier modules
- [ ] Connection IDs are valid
- [ ] Data types match field expectations
- [ ] No syntax errors in expressions

### 3. **Connections**
- [ ] `sourceModuleId` and `targetModuleId` exist
- [ ] Filter conditions use valid operators
- [ ] No orphaned modules (unreachable modules)

### 4. **Scheduling**
- [ ] Scheduling type is valid (`interval`, `cron`, or `instant`)
- [ ] Interval values are: 1, 5, 15, 30, or 60
- [ ] Cron expressions are valid
- [ ] Trigger modules match scheduling type

### 5. **Error Handling**
- [ ] Error handlers reference valid module IDs
- [ ] Error strategies are appropriate for use case
- [ ] Critical operations have error handlers

## Common Errors and Solutions

### Error: "Module not found"

**Cause**: Module ID referenced in mapper doesn't exist

```json
{
  "id": 2,
  "mapper": {
    "field": "{{5.value}}"  // Module 5 doesn't exist
  }
}
```

**Solution**: Ensure referenced module exists and has a lower ID

```json
{
  "id": 2,
  "mapper": {
    "field": "{{1.value}}"  // Valid reference
  }
}
```

### Error: "Invalid connection"

**Cause**: Connection ID is wrong or expired

**Solution**: 
1. Use `connections_list` to get valid connection IDs
2. Test connection with `connections_test`
3. Re-authorize if OAuth token expired

```typescript
// Test connection
{
  "tool": "connections_test",
  "parameters": {
    "connectionId": "connection-id-here"
  }
}
```

### Error: "Required field missing"

**Cause**: Module mapper is missing a required field

**Solution**: Check app documentation and add required fields

```json
// Before (missing "to" field)
{
  "module": "gmail:SendEmail",
  "mapper": {
    "subject": "Hello"
  }
}

// After (fixed)
{
  "module": "gmail:SendEmail",
  "mapper": {
    "to": "user@example.com",
    "subject": "Hello"
  }
}
```

### Error: "Invalid scheduling configuration"

**Cause**: Scheduling object is malformed

```json
// Wrong
{
  "scheduling": {
    "interval": 15  // Missing "type"
  }
}

// Correct
{
  "scheduling": {
    "type": "interval",
    "interval": 15
  }
}
```

### Error: "Circular dependency detected"

**Cause**: Module references itself or creates a loop

**Solution**: Restructure connections to eliminate loops

### Error: "Invalid JSON in mapper"

**Cause**: JSON syntax error in field mapping

```json
// Wrong
{
  "mapper": {
    "data": "{{1.items}"  // Missing closing }}
  }
}

// Correct
{
  "mapper": {
    "data": "{{1.items}}"
  }
}
```

### Error: "Webhook not found"

**Cause**: Invalid webhook ID in CustomWebhook module

**Solution**: Create webhook first with `webhooks_create` MCP tool

```typescript
{
  "tool": "webhooks_create",
  "parameters": {
    "name": "My Webhook"
  }
}
// Use returned webhook ID in module
```

### Error: "Rate limit exceeded"

**Cause**: Too many API requests in short time

**Solution**: 
- Increase scheduling interval
- Add sleep modules between API calls
- Use exponential backoff in retries

### Error: "Timeout"

**Cause**: Module took too long to execute

**Solution**: Increase timeout in HTTP module parameters

```json
{
  "parameters": {
    "timeout": 300  // seconds
  }
}
```

## Execution Log Analysis

### Successful Execution
```json
{
  "executionId": "exec-123",
  "status": "success",
  "modules": [
    {
      "moduleId": 1,
      "status": "success",
      "output": {...}
    },
    {
      "moduleId": 2,
      "status": "success",
      "output": {...}
    }
  ]
}
```

### Failed Execution
```json
{
  "executionId": "exec-456",
  "status": "error",
  "modules": [
    {
      "moduleId": 1,
      "status": "success",
      "output": {...}
    },
    {
      "moduleId": 2,
      "status": "error",
      "error": {
        "message": "Connection refused",
        "code": "ECONNREFUSED"
      }
    }
  ]
}
```

**Analysis Steps:**
1. Identify failed module ID
2. Check error message and code
3. Review module configuration
4. Verify inputs from previous modules
5. Test with manual execution

## Debugging Workflow

### Step 1: Reproduce the Error
1. Use `scenarios_run` to trigger manual execution
2. Monitor execution with `executions_get`
3. Note exact error message and failed module

### Step 2: Inspect Module Configuration
1. Use `scenarios_get` to retrieve scenario JSON
2. Locate failed module by ID
3. Check mapper, parameters, and connections

### Step 3: Verify Inputs
1. Check output from previous modules
2. Ensure required fields exist
3. Validate data types

### Step 4: Test Connections
1. Use `connections_test` on module's connection
2. Re-authorize if needed
3. Verify API credentials

### Step 5: Simplify and Test
1. Remove complex logic temporarily
2. Test with hardcoded values
3. Gradually add back complexity

### Step 6: Check DLQ
1. Use `dlq_list` to see failed executions
2. Review failure patterns
3. Fix underlying issues

## Testing Strategies

### 1. **Manual Test Execution**
Always test before activating:

```typescript
{
  "tool": "scenarios_run",
  "parameters": {
    "scenarioId": "123456"
  }
}
```

### 2. **Test with Sample Data**
Create test webhook payloads with known data

### 3. **Validate Each Module**
Test modules individually before connecting them

### 4. **Check Filter Conditions**
Ensure filters don't accidentally block all data

```json
// Bad: Will never match
{
  "filter": {
    "conditions": [
      [
        {"a": "{{1.status}}", "o": "equal", "b": "active"},
        {"a": "{{1.status}}", "o": "equal", "b": "inactive"}
      ]
    ]
  }
}

// Good: OR logic
{
  "filter": {
    "conditions": [
      [{"a": "{{1.status}}", "o": "equal", "b": "active"}],
      [{"a": "{{1.status}}", "o": "equal", "b": "inactive"}]
    ]
  }
}
```

### 5. **Monitor Execution Frequency**
Check that scheduling doesn't overwhelm APIs

## MCP Tools for Debugging

### Get Scenario Details
```typescript
{
  "tool": "scenarios_get",
  "parameters": {
    "scenarioId": "123456"
  }
}
```

### List Recent Executions
```typescript
{
  "tool": "executions_list",
  "parameters": {
    "scenarioId": "123456",
    "limit": 10
  }
}
```

### Get Execution Details
```typescript
{
  "tool": "executions_get",
  "parameters": {
    "executionId": "exec-id"
  }
}
```

### Check Dead Letter Queue
```typescript
{
  "tool": "dlq_list",
  "parameters": {
    "scenarioId": "123456"
  }
}
```

### Test Connection
```typescript
{
  "tool": "connections_test",
  "parameters": {
    "connectionId": "conn-id"
  }
}
```

## Performance Optimization

### 1. **Minimize HTTP Requests**
Batch operations where possible

### 2. **Use Filters Early**
Filter data before expensive operations

### 3. **Avoid Nested Iterations**
Use aggregators efficiently

### 4. **Set Appropriate Timeouts**
Don't wait too long for unresponsive APIs

### 5. **Monitor Execution Time**
Track slow modules and optimize

## Best Practices

### 1. **Test Before Deploying**
Always run manual tests before activating scheduling

### 2. **Use Descriptive Module Names**
Name modules clearly in `metadata.designer.name`

### 3. **Add Error Handlers**
Every critical module should have an error handler

### 4. **Log Errors**
Send errors to database or monitoring service

### 5. **Monitor DLQ Daily**
Check dead letter queue for recurring issues

### 6. **Version Control Scenarios**
Clone scenarios before major changes

### 7. **Document Complex Logic**
Add comments in module names explaining purpose

### 8. **Set Up Alerts**
Get notified on critical failures via Slack/email

### 9. **Review Execution Logs Weekly**
Look for patterns in failures

### 10. **Keep Scenarios Simple**
Break complex workflows into multiple scenarios

## Troubleshooting Checklist

When a scenario fails:

- [ ] Check execution log for error message
- [ ] Identify failed module ID
- [ ] Review module configuration (mapper, parameters)
- [ ] Verify connection is valid and authorized
- [ ] Test connection with `connections_test`
- [ ] Check that referenced modules exist
- [ ] Validate data types match expectations
- [ ] Look for syntax errors in expressions
- [ ] Review filter conditions for logic errors
- [ ] Check API rate limits
- [ ] Verify webhook URL is correct (if webhook trigger)
- [ ] Test with manual execution
- [ ] Check DLQ for similar failures
- [ ] Review Make.com status page for service issues

## Related Skills

- **make-scenario-builder**: Building correct scenario structure
- **make-mcp-tools-expert**: Using MCP tools for debugging
- **make-error-handling**: Implementing error handlers
- **make-module-configuration**: Configuring modules correctly
