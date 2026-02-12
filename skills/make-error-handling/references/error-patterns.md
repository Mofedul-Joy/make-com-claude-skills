# Error Handler Patterns

Quick reference for Make.com error handling strategies

## Strategy Decision Matrix

| Scenario | Recommended Strategy | Why |
|----------|---------------------|-----|
| Optional API call | **Resume** | Provide fallback data and continue |
| Batch record creation | **Commit** | Save successful records before failure |
| Payment transaction | **Rollback** | All-or-nothing, maintain integrity |
| Non-critical notification | **Ignore** | Skip and continue with workflow |
| Critical data validation | **Break** | Stop immediately on invalid data |
| Transactional updates | **Rollback** | Undo all changes on any failure |
| Iterating through items | **Ignore** | Skip failed items, process rest |
| Primary/fallback APIs | **Resume** | Use fallback on primary failure |

## Resume Patterns

### Pattern: Fallback Data
```json
{
  "id": 5,
  "module": "error-handler:Resume",
  "mapper": {
    "defaultData": {
      "status": "unavailable",
      "data": null,
      "source": "fallback"
    }
  },
  "metadata": {
    "errorHandler": {
      "moduleId": 3,
      "strategy": "resume"
    }
  }
}
```

### Pattern: Retry with Resume
```json
{
  "id": 5,
  "module": "error-handler:Resume",
  "mapper": {
    "retry": true,
    "maxAttempts": 3,
    "delay": 5,
    "defaultData": {"failed": true}
  },
  "metadata": {
    "errorHandler": {
      "moduleId": 2,
      "strategy": "resume"
    }
  }
}
```

## Commit Patterns

### Pattern: Save Successful Batch Items
```json
{
  "flow": [
    {
      "id": 1,
      "module": "iterator:Iterator",
      "mapper": {"array": "{{trigger.items}}"}
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
      "module": "error-handler:Commit",
      "metadata": {
        "errorHandler": {
          "moduleId": 2,
          "strategy": "commit"
        }
      }
    }
  ]
}
```

### Pattern: Partial Success Logging
```json
{
  "id": 5,
  "module": "error-handler:Commit",
  "mapper": {
    "logSuccess": true,
    "successCount": "{{completed}}",
    "failureReason": "{{error.message}}"
  },
  "metadata": {
    "errorHandler": {
      "moduleId": 4,
      "strategy": "commit"
    }
  }
}
```

## Rollback Patterns

### Pattern: Database Transaction
```json
{
  "flow": [
    {
      "id": 1,
      "module": "database:InsertRow",
      "mapper": {
        "table": "orders",
        "values": "{{trigger}}"
      }
    },
    {
      "id": 2,
      "module": "database:UpdateRows",
      "mapper": {
        "table": "inventory",
        "condition": "product_id = {{trigger.productId}}",
        "values": {"stock": "stock - {{trigger.quantity}}"}
      }
    },
    {
      "id": 3,
      "module": "http:Post",
      "mapper": {
        "url": "https://payment.example.com/charge",
        "body": "{{toJSON(trigger)}}"
      }
    },
    {
      "id": 4,
      "module": "error-handler:Rollback",
      "metadata": {
        "errorHandler": {
          "moduleId": 3,
          "strategy": "rollback"
        }
      }
    }
  ]
}
```

### Pattern: Multi-Service Rollback
```json
{
  "flow": [
    {
      "id": 1,
      "module": "airtable:CreateRecord",
      "mapper": {"base": "base-id", "table": "Users"}
    },
    {
      "id": 2,
      "module": "slack:SendMessage",
      "mapper": {"channel": "new-users", "text": "Welcome!"}
    },
    {
      "id": 3,
      "module": "database:InsertRow",
      "mapper": {"table": "user_logs"}
    },
    {
      "id": 4,
      "module": "error-handler:Rollback",
      "metadata": {
        "errorHandler": {
          "moduleId": 3,
          "strategy": "rollback"
        }
      }
    }
  ]
}
```

## Ignore Patterns

### Pattern: Skip Failed Items in Iteration
```json
{
  "flow": [
    {
      "id": 1,
      "module": "iterator:Iterator",
      "mapper": {"array": "{{trigger.users}}"}
    },
    {
      "id": 2,
      "module": "gmail:SendEmail",
      "mapper": {
        "to": "{{1.email}}",
        "subject": "Newsletter"
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
    }
  ]
}
```

### Pattern: Optional Notification
```json
{
  "flow": [
    {
      "id": 1,
      "module": "database:InsertRow",
      "mapper": {"table": "orders"}
    },
    {
      "id": 2,
      "module": "slack:SendMessage",
      "mapper": {
        "channel": "orders",
        "text": "New order: {{1.id}}"
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
      "module": "http:Post",
      "mapper": {
        "url": "https://api.example.com/process",
        "body": "{{toJSON(1)}}"
      }
    }
  ]
}
```

## Break Patterns

### Pattern: Stop on Critical Failure
```json
{
  "flow": [
    {
      "id": 1,
      "module": "database:SelectRows",
      "mapper": {
        "table": "config",
        "condition": "key = 'api_key'"
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
        "text": "🚨 Critical config load failed!"
      }
    }
  ]
}
```

### Pattern: Data Validation
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
      "module": "router:Router",
      "routes": [
        {
          "filter": {
            "name": "Invalid Data",
            "conditions": [[{"a": "{{1.valid}}", "o": "equal", "b": "false"}]]
          },
          "flow": [
            {
              "id": 3,
              "module": "error-handler:Break",
              "metadata": {"errorHandler": {"moduleId": 1, "strategy": "break"}}
            }
          ]
        }
      ]
    }
  ]
}
```

## Combined Strategy Patterns

### Pattern: Primary/Fallback with Error Logging
```json
{
  "flow": [
    {
      "id": 1,
      "module": "http:Get",
      "mapper": {"url": "https://primary-api.com/data"}
    },
    {
      "id": 2,
      "module": "error-handler:Resume",
      "mapper": {
        "defaultData": {"useFallback": true}
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
      "module": "database:InsertRow",
      "mapper": {
        "table": "error_log",
        "values": {
          "error": "{{2.error}}",
          "timestamp": "{{now}}"
        }
      }
    },
    {
      "id": 4,
      "module": "router:Router",
      "routes": [
        {
          "filter": {
            "name": "Use Fallback",
            "conditions": [[{"a": "{{2.useFallback}}", "o": "equal", "b": "true"}]]
          },
          "flow": [
            {
              "id": 5,
              "module": "http:Get",
              "mapper": {"url": "https://fallback-api.com/data"}
            }
          ]
        }
      ]
    }
  ]
}
```

### Pattern: Retry with Exponential Backoff
```json
{
  "flow": [
    {
      "id": 1,
      "module": "http:Post",
      "parameters": {
        "maxRetries": 3,
        "retryStrategy": "exponential",
        "baseDelay": 5
      },
      "mapper": {
        "url": "https://api.example.com/endpoint"
      }
    },
    {
      "id": 2,
      "module": "error-handler:Resume",
      "mapper": {
        "defaultData": {
          "success": false,
          "retries_exhausted": true
        }
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

## Error Logging Pattern

Universal error logging module to attach to any error handler:

```json
{
  "flow": [
    {
      "id": 1,
      "module": "http:Get",
      "mapper": {"url": "{{apiUrl}}"}
    },
    {
      "id": 2,
      "module": "error-handler:Resume",
      "mapper": {"defaultData": null},
      "metadata": {
        "errorHandler": {
          "moduleId": 1,
          "strategy": "resume"
        }
      }
    },
    {
      "id": 3,
      "module": "database:InsertRow",
      "mapper": {
        "table": "error_log",
        "values": {
          "scenario_id": "{{scenario.id}}",
          "module_id": "{{2.moduleId}}",
          "error_message": "{{2.error.message}}",
          "error_code": "{{2.error.code}}",
          "timestamp": "{{now}}",
          "input_data": "{{toJSON(1)}}"
        }
      }
    }
  ]
}
```

## Monitoring & Alerts Pattern

Send Slack alert on critical errors:

```json
{
  "flow": [
    {
      "id": 1,
      "module": "database:UpdateRows",
      "mapper": {"table": "critical_data"}
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
        "channel": "critical-alerts",
        "text": "🚨 CRITICAL ERROR: {{2.error.message}}\nScenario: {{scenario.name}}\nModule: {{2.moduleId}}"
      }
    }
  ]
}
```
