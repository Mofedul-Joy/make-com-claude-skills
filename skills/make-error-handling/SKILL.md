---
name: make-error-handling
description: Error handler patterns (Resume, Commit, Rollback, Ignore, Break) and retry strategies for robust Make.com scenarios
---

# Make.com Error Handling

## Overview

Error handling in Make.com ensures scenarios handle failures gracefully. This skill covers error handler strategies (Resume, Commit, Rollback, Ignore, Break), retry logic, dead letter queue management, and building fault-tolerant workflows.

## When to Use This Skill

Use this skill when:
- Adding error handlers to scenarios
- Implementing retry logic for failed operations
- Managing dead letter queue (DLQ) items
- Building fault-tolerant workflows
- Troubleshooting scenario execution failures

## Error Handler Types

Make.com provides five error handler strategies:

### 1. **Resume** - Continue with default data
Allows the scenario to continue execution with fallback data when a module fails.

```json
{
  "id": 5,
  "module": "error-handler:Resume",
  "mapper": {
    "defaultData": {
      "status": "error",
      "message": "Operation failed, using default"
    }
  },
  "metadata": {
    "errorHandler": {
      "moduleId": 3,  // Module this handles errors for
      "strategy": "resume"
    }
  }
}
```

**Use Cases:**
- Provide default values when API calls fail
- Continue processing even if one operation fails
- Log errors but don't stop the workflow

### 2. **Commit** - Save progress and stop
Saves all completed operations and stops the scenario.

```json
{
  "id": 6,
  "module": "error-handler:Commit",
  "mapper": {},
  "metadata": {
    "errorHandler": {
      "moduleId": 4,
      "strategy": "commit"
    }
  }
}
```

**Use Cases:**
- Partially complete batch operations
- Save successful records before failure
- Prevent rollback of already completed work

### 3. **Rollback** - Undo all changes
Reverts all changes made during this scenario execution.

```json
{
  "id": 7,
  "module": "error-handler:Rollback",
  "mapper": {},
  "metadata": {
    "errorHandler": {
      "moduleId": 2,
      "strategy": "rollback"
    }
  }
}
```

**Use Cases:**
- Database transactions that must be atomic
- All-or-nothing operations
- Maintaining data integrity

### 4. **Ignore** - Skip and continue
Ignores the error and continues with the next iteration or module.

```json
{
  "id": 8,
  "module": "error-handler:Ignore",
  "mapper": {},
  "metadata": {
    "errorHandler": {
      "moduleId": 3,
      "strategy": "ignore"
    }
  }
}
```

**Use Cases:**
- Non-critical operations
- Optional processing steps
- Skip failed items in iteration

### 5. **Break** - Stop immediately
Stops scenario execution immediately without rolling back.

```json
{
  "id": 9,
  "module": "error-handler:Break",
  "mapper": {},
  "metadata": {
    "errorHandler": {
      "moduleId": 5,
      "strategy": "break"
    }
  }
}
```

**Use Cases:**
- Critical failures that require immediate attention
- Stop on invalid data
- Prevent cascading errors

## Error Handler Placement

Error handlers are attached to specific modules:

```json
{
  "flow": [
    {
      "id": 1,
      "module": "http:Get",
      "mapper": {"url": "https://api.example.com/data"}
    },
    {
      "id": 2,
      "module": "database:InsertRow",
      "mapper": {"table": "orders", "values": "{{1}}"}
    },
    {
      "id": 3,
      "module": "error-handler:Resume",
      "mapper": {
        "defaultData": {"status": "failed"}
      },
      "metadata": {
        "errorHandler": {
          "moduleId": 2,  // Handles errors from module 2
          "strategy": "resume"
        }
      }
    }
  ]
}
```

## Retry Logic

### Automatic Retries
Configure module-level retries:

```json
{
  "id": 2,
  "module": "http:ActionSendData",
  "parameters": {
    "maxRetries": 3,
    "retryDelay": 5  // seconds
  },
  "mapper": {
    "url": "https://api.example.com/endpoint"
  }
}
```

### Manual Retry with Error Handler
```json
{
  "flow": [
    {
      "id": 1,
      "module": "http:Post",
      "mapper": {"url": "{{apiUrl}}"}
    },
    {
      "id": 2,
      "module": "error-handler:Resume",
      "mapper": {
        "retry": true,
        "maxAttempts": 3,
        "delay": 10
      },
      "metadata": {
        "errorHandler": {
          "moduleId": 1,
          "strategy": "resume"
        }
      }
    }
  ]
}
```

### Exponential Backoff
Increase delay between retries:

```json
{
  "parameters": {
    "retryStrategy": "exponential",
    "baseDelay": 5,
    "maxRetries": 4
  }
}
```

Delays: 5s, 10s, 20s, 40s

## Common Error Handling Patterns

### Pattern 1: API Call with Fallback
```json
{
  "flow": [
    {
      "id": 1,
      "module": "http:Get",
      "mapper": {
        "url": "https://primary-api.com/data"
      }
    },
    {
      "id": 2,
      "module": "error-handler:Resume",
      "mapper": {
        "defaultData": {
          "source": "fallback",
          "data": []
        }
      },
      "metadata": {
        "errorHandler": {
          "moduleId": 1,
          "strategy": "resume"
        }
      }
    },
    {
      "id": 3,
      "module": "router:Router",
      "routes": [
        {
          "filter": {
            "name": "Fallback Route",
            "conditions": [[{"a": "{{2.source}}", "o": "equal", "b": "fallback"}]]
          },
          "flow": [
            {
              "id": 4,
              "module": "http:Get",
              "mapper": {
                "url": "https://backup-api.com/data"
              }
            }
          ]
        }
      ]
    }
  ]
}
```

### Pattern 2: Batch Processing with Error Logging
```json
{
  "flow": [
    {
      "id": 1,
      "module": "iterator:Iterator",
      "mapper": {"array": "{{1.items}}"}
    },
    {
      "id": 2,
      "module": "database:InsertRow",
      "mapper": {
        "table": "records",
        "values": "{{1}}"
      }
    },
    {
      "id": 3,
      "module": "error-handler:Ignore",
      "metadata": {
        "errorHandler": {
          "moduleId": 2,
          "strategy": "ignore"
        }
      }
    },
    {
      "id": 4,
      "module": "database:InsertRow",
      "mapper": {
        "table": "error_log",
        "values": {
          "item": "{{1}}",
          "error": "{{3.error}}",
          "timestamp": "{{now}}"
        }
      }
    }
  ]
}
```

### Pattern 3: Transaction with Rollback
```json
{
  "flow": [
    {
      "id": 1,
      "module": "database:InsertRow",
      "mapper": {
        "table": "orders",
        "values": "{{1}}"
      }
    },
    {
      "id": 2,
      "module": "database:UpdateRows",
      "mapper": {
        "table": "inventory",
        "condition": "product_id = {{1.product_id}}",
        "values": {"stock": "stock - {{1.quantity}}"}
      }
    },
    {
      "id": 3,
      "module": "http:Post",
      "mapper": {
        "url": "https://payment-gateway.com/charge",
        "body": "{{toJSON(1)}}"
      }
    },
    {
      "id": 4,
      "module": "error-handler:Rollback",
      "metadata": {
        "errorHandler": {
          "moduleId": 3,  // If payment fails, rollback all
          "strategy": "rollback"
        }
      }
    }
  ]
}
```

### Pattern 4: Critical Alert on Error
```json
{
  "flow": [
    {
      "id": 1,
      "module": "database:SelectRows",
      "mapper": {
        "table": "critical_data"
      }
    },
    {
      "id": 2,
      "module": "error-handler:Break",
      "metadata": {
        "errorHandler": {
          "moduleId": 1,
          "strategy": "break"
        }
      }
    },
    {
      "id": 3,
      "module": "slack:SendMessage",
      "mapper": {
        "channel": "alerts",
        "text": "🚨 Critical database query failed: {{2.error}}"
      }
    }
  ]
}
```

## Dead Letter Queue (DLQ) Management

Failed scenario executions go to the DLQ for manual review.

### Listing DLQ Items
Use `dlq_list` MCP tool:

```typescript
{
  "tool": "dlq_list",
  "parameters": {
    "scenarioId": "123456",
    "limit": 50
  }
}
```

### Getting DLQ Item Details
Use `dlq_get`:

```typescript
{
  "tool": "dlq_get",
  "parameters": {
    "dlqId": "dlq-item-id"
  }
}
```

### Retrying Failed Executions
Use `dlq_requeue`:

```typescript
{
  "tool": "dlq_requeue",
  "parameters": {
    "dlqId": "dlq-item-id"
  }
}
```

## Execution Monitoring

### Listing Executions
```typescript
{
  "tool": "executions_list",
  "parameters": {
    "scenarioId": "123456",
    "status": "error",
    "limit": 20
  }
}
```

### Getting Execution Details
```typescript
{
  "tool": "executions_get",
  "parameters": {
    "executionId": "execution-id"
  }
}
```

## Best Practices

### 1. **Use Resume for Optional Operations**
If an operation failing shouldn't stop the workflow, use Resume.

### 2. **Use Commit for Batch Processing**
When processing batches, commit successful work before failure.

### 3. **Use Rollback for Transactions**
For atomic operations (all-or-nothing), use Rollback.

### 4. **Use Ignore for Non-Critical Steps**
Skip errors in optional/low-priority operations.

### 5. **Use Break for Critical Failures**
Stop immediately when data integrity is at risk.

### 6. **Log All Errors**
Always log errors to a database or monitoring service:

```json
{
  "module": "database:InsertRow",
  "mapper": {
    "table": "error_log",
    "values": {
      "error": "{{errorHandler.message}}",
      "module": "{{errorHandler.moduleId}}",
      "timestamp": "{{now}}"
    }
  }
}
```

### 7. **Set Appropriate Retry Limits**
Don't retry forever. Use 3-5 retries max.

### 8. **Monitor DLQ Regularly**
Check dead letter queue daily and fix recurring issues.

### 9. **Use Exponential Backoff**
For rate-limited APIs, use exponential backoff.

### 10. **Test Error Scenarios**
Intentionally trigger errors to test handler behavior.

## Related Skills

- **make-scenario-builder**: Building complete scenarios
- **make-validation-expert**: Debugging execution failures
- **make-mcp-tools-expert**: Managing DLQ via MCP tools

## References

- [Error Handler Patterns](references/error-patterns.md)
