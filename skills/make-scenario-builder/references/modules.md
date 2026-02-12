# Common Make.com Modules

This reference provides examples of frequently used Make.com modules.

## Webhook Modules

### Custom Webhook (Trigger)
```json
{
  "id": 1,
  "module": "webhook:CustomWebhook",
  "version": 1,
  "parameters": {
    "hook": "webhook-id-here",
    "dataStructure": null
  }
}
```

### Webhook Response
```json
{
  "id": 5,
  "module": "webhook:WebhookResponse",
  "mapper": {
    "status": "200",
    "body": "{{json(2)}}",
    "headers": []
  }
}
```

## HTTP Modules

### HTTP GET Request
```json
{
  "id": 2,
  "module": "http:ActionSendData",
  "parameters": {
    "handleErrors": false
  },
  "mapper": {
    "url": "https://api.example.com/users",
    "method": "GET",
    "headers": [
      {
        "name": "Authorization",
        "value": "Bearer {{token}}"
      }
    ]
  }
}
```

### HTTP POST Request
```json
{
  "id": 3,
  "module": "http:ActionSendData",
  "mapper": {
    "url": "https://api.example.com/create",
    "method": "POST",
    "headers": [
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ],
    "body": "{{toJSON(1)}}",
    "parseResponse": true
  }
}
```

## Database Modules (Generic SQL)

### Select Rows
```json
{
  "id": 4,
  "module": "postgresql:SelectRows",
  "parameters": {
    "connection": "connection-id"
  },
  "mapper": {
    "table": "users",
    "fields": ["id", "email", "name"],
    "condition": "email = {{1.email}}"
  }
}
```

### Insert Row
```json
{
  "id": 5,
  "module": "postgresql:InsertRow",
  "mapper": {
    "table": "orders",
    "values": {
      "user_id": "{{1.userId}}",
      "total": "{{1.amount}}",
      "status": "pending"
    }
  }
}
```

### Update Rows
```json
{
  "id": 6,
  "module": "postgresql:UpdateRows",
  "mapper": {
    "table": "users",
    "values": {
      "last_login": "{{now}}"
    },
    "condition": "id = {{1.userId}}"
  }
}
```

## Email Modules

### Gmail: Send Email
```json
{
  "id": 7,
  "module": "gmail:ActionSendEmail",
  "mapper": {
    "to": "{{1.email}}",
    "subject": "Your Order Confirmation",
    "html": "<h1>Thanks for your order!</h1><p>Order ID: {{1.orderId}}</p>",
    "attachments": []
  }
}
```

### Mailgun: Send Email
```json
{
  "id": 8,
  "module": "mailgun:SendEmail",
  "mapper": {
    "to": "{{1.email}}",
    "from": "noreply@example.com",
    "subject": "Welcome!",
    "text": "Hello {{1.name}}",
    "html": "<h1>Welcome {{1.name}}!</h1>"
  }
}
```

## Data Transformation Modules

### JSON: Parse
```json
{
  "id": 9,
  "module": "json:ParseJSON",
  "mapper": {
    "json": "{{1.body}}"
  }
}
```

### JSON: Create
```json
{
  "id": 10,
  "module": "json:CreateJSON",
  "mapper": {
    "object": {
      "name": "{{1.name}}",
      "email": "{{1.email}}",
      "timestamp": "{{now}}"
    }
  }
}
```

### Text Parser: Match Pattern
```json
{
  "id": 11,
  "module": "text-parser:MatchPattern",
  "mapper": {
    "pattern": "Order #(\\d+)",
    "text": "{{1.body}}",
    "global": false
  }
}
```

## CRM Modules

### Airtable: Create Record
```json
{
  "id": 12,
  "module": "airtable:CreateRecord",
  "parameters": {
    "connection": "airtable-connection-id"
  },
  "mapper": {
    "base": "base-id",
    "table": "Contacts",
    "fields": {
      "Name": "{{1.name}}",
      "Email": "{{1.email}}",
      "Status": "Active"
    }
  }
}
```

### HubSpot: Create Contact
```json
{
  "id": 13,
  "module": "hubspot:CreateContact",
  "mapper": {
    "properties": {
      "email": "{{1.email}}",
      "firstname": "{{1.firstName}}",
      "lastname": "{{1.lastName}}"
    }
  }
}
```

## Communication Modules

### Slack: Send Message
```json
{
  "id": 14,
  "module": "slack:ActionPostMessage",
  "parameters": {
    "connection": "slack-connection-id"
  },
  "mapper": {
    "channel": "C123456789",
    "text": "New order received: {{1.orderId}}",
    "attachments": [],
    "blocks": []
  }
}
```

### Discord: Send Message
```json
{
  "id": 15,
  "module": "discord:SendMessage",
  "mapper": {
    "webhookUrl": "{{webhookUrl}}",
    "content": "Alert: {{1.message}}",
    "username": "Bot",
    "embeds": []
  }
}
```

## File Storage Modules

### Google Drive: Upload File
```json
{
  "id": 16,
  "module": "google-drive:UploadFile",
  "mapper": {
    "folderId": "folder-id-here",
    "fileName": "report-{{formatDate(now, 'YYYY-MM-DD')}}.pdf",
    "data": "{{1.file}}"
  }
}
```

### Dropbox: Create File
```json
{
  "id": 17,
  "module": "dropbox:CreateFile",
  "mapper": {
    "path": "/reports/{{1.filename}}",
    "data": "{{1.fileContent}}",
    "mode": "add"
  }
}
```

## Scheduling Modules

### Sleep (Delay)
```json
{
  "id": 18,
  "module": "util:Sleep",
  "mapper": {
    "delay": 5
  }
}
```

## Control Flow Modules

### Iterator
```json
{
  "id": 19,
  "module": "iterator:Iterator",
  "mapper": {
    "array": "{{1.data.items}}"
  }
}
```

### Aggregator
```json
{
  "id": 20,
  "module": "aggregator:NumericAggregator",
  "mapper": {
    "source": 19,
    "target": 21,
    "aggregateFunction": "sum",
    "value": "{{21.amount}}"
  }
}
```

## Error Handling Modules

### Error Handler: Resume
```json
{
  "id": 21,
  "module": "error-handler:Resume",
  "mapper": {}
}
```

### Error Handler: Commit
```json
{
  "id": 22,
  "module": "error-handler:Commit",
  "mapper": {}
}
```

## Custom Functions

### Run Custom Function
```json
{
  "id": 23,
  "module": "custom-function:Run",
  "parameters": {
    "functionId": "function-id-here"
  },
  "mapper": {
    "input": "{{1.data}}"
  }
}
```
