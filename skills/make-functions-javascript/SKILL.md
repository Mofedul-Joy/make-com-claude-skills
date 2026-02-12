---
name: make-functions-javascript
description: Custom JavaScript function development for Make.com scenarios including mapping functions, data transformations, and advanced logic
---

# Make.com JavaScript Functions

## Overview

Make.com allows custom JavaScript functions within scenarios for advanced data manipulation, complex logic, and transformations not possible with built-in functions. This skill teaches how to write, test, and use JavaScript functions in Make.com.

## When to Use This Skill

Use this skill when:
- Writing custom functions for data transformation
- Implementing complex mapping logic
- Processing data with JavaScript in modules
- Creating reusable custom functions
- Handling advanced JSON manipulation
- Performing calculations or validations

## JavaScript in Make.com

### Inline JavaScript in Mappers

You can use JavaScript expressions directly in mapper fields:

```json
{
  "mapper": {
    "fullName": "{{1.firstName}} {{1.lastName}}",
    "email": "{{lower(1.email)}}",
    "calculation": "{{1.price * 1.1}}"
  }
}
```

### Built-in Functions

Make.com provides built-in functions:

#### String Functions
- `upper()` - Convert to uppercase
- `lower()` - Convert to lowercase
- `trim()` - Remove whitespace
- `replace(string, find, replace)` - Replace text
- `substring(string, start, length)` - Extract substring
- `length()` - Get string length

#### Date Functions
- `now` - Current timestamp
- `formatDate(date, format)` - Format date
- `addDays(date, days)` - Add days to date
- `parseDate(string, format)` - Parse date string

#### JSON Functions
- `toJSON(object)` - Convert to JSON string
- `parseJSON(string)` - Parse JSON string

#### Math Functions
- `round(number, decimals)` - Round number
- `ceil(number)` - Round up
- `floor(number)` - Round down
- `abs(number)` - Absolute value

#### Utility Functions
- `if(condition, trueValue, falseValue)` - Conditional
- `ifempty(value, default)` - Default if empty
- `concat(...values)` - Concatenate values

### Custom Function Module

For complex logic, use the Custom Function module:

```json
{
  "id": 5,
  "module": "custom-function:Run",
  "parameters": {
    "functionId": "function-id-here"
  },
  "mapper": {
    "input": "{{1.data}}"
  }
}
```

## Creating Custom Functions

### Function Structure

```javascript
/**
 * Function: processUserData
 * Input: { firstName, lastName, email, age }
 * Output: { fullName, formattedEmail, isAdult }
 */
function main(input) {
  const { firstName, lastName, email, age } = input;
  
  return {
    fullName: `${firstName} ${lastName}`,
    formattedEmail: email.toLowerCase().trim(),
    isAdult: age >= 18
  };
}
```

### Input/Output Format

Functions must:
1. Accept a single `input` parameter (object)
2. Return an object
3. Be synchronous (no async/await in most contexts)

### Using MCP Tools

Create custom functions via MCP:

```typescript
{
  "tool": "functions_create",
  "parameters": {
    "name": "Process User Data",
    "code": "function main(input) { ... }"
  }
}
```

## Common Function Patterns

### Pattern 1: Data Validation

```javascript
function main(input) {
  const { email, phone, age } = input;
  
  const errors = [];
  
  // Validate email
  if (!email || !email.includes('@')) {
    errors.push('Invalid email');
  }
  
  // Validate phone
  if (!phone || phone.length < 10) {
    errors.push('Invalid phone');
  }
  
  // Validate age
  if (age < 18) {
    errors.push('Must be 18 or older');
  }
  
  return {
    isValid: errors.length === 0,
    errors: errors
  };
}
```

### Pattern 2: Data Transformation

```javascript
function main(input) {
  const { items } = input;
  
  // Transform array of items
  const transformed = items.map(item => ({
    id: item.productId,
    name: item.productName.toUpperCase(),
    price: parseFloat(item.price).toFixed(2),
    discountPrice: (parseFloat(item.price) * 0.9).toFixed(2)
  }));
  
  return {
    items: transformed,
    totalItems: transformed.length
  };
}
```

### Pattern 3: Aggregation

```javascript
function main(input) {
  const { orders } = input;
  
  const total = orders.reduce((sum, order) => {
    return sum + parseFloat(order.amount);
  }, 0);
  
  const avgOrderValue = total / orders.length;
  
  return {
    totalRevenue: total.toFixed(2),
    averageOrderValue: avgOrderValue.toFixed(2),
    orderCount: orders.length
  };
}
```

### Pattern 4: Conditional Logic

```javascript
function main(input) {
  const { userType, purchaseAmount } = input;
  
  let discount = 0;
  let tier = 'standard';
  
  if (userType === 'premium') {
    if (purchaseAmount >= 1000) {
      discount = 0.20;
      tier = 'platinum';
    } else if (purchaseAmount >= 500) {
      discount = 0.15;
      tier = 'gold';
    } else {
      discount = 0.10;
      tier = 'silver';
    }
  } else if (userType === 'standard') {
    if (purchaseAmount >= 500) {
      discount = 0.05;
    }
  }
  
  const finalAmount = purchaseAmount * (1 - discount);
  
  return {
    originalAmount: purchaseAmount,
    discountPercent: discount * 100,
    discountAmount: (purchaseAmount * discount).toFixed(2),
    finalAmount: finalAmount.toFixed(2),
    tier: tier
  };
}
```

### Pattern 5: String Manipulation

```javascript
function main(input) {
  const { text } = input;
  
  const words = text.split(' ');
  const wordCount = words.length;
  const charCount = text.length;
  
  // Capitalize first letter of each word
  const titleCase = words.map(word => {
    return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
  }).join(' ');
  
  // Extract hashtags
  const hashtags = text.match(/#\w+/g) || [];
  
  return {
    originalText: text,
    titleCase: titleCase,
    wordCount: wordCount,
    charCount: charCount,
    hashtags: hashtags
  };
}
```

### Pattern 6: Date Manipulation

```javascript
function main(input) {
  const { dateString } = input;
  
  const date = new Date(dateString);
  
  // Add 30 days
  const futureDate = new Date(date);
  futureDate.setDate(date.getDate() + 30);
  
  // Format dates
  const formatDate = (d) => {
    return d.toISOString().split('T')[0];
  };
  
  return {
    originalDate: formatDate(date),
    futureDate: formatDate(futureDate),
    dayOfWeek: date.toLocaleDateString('en-US', { weekday: 'long' }),
    isWeekend: date.getDay() === 0 || date.getDay() === 6
  };
}
```

### Pattern 7: JSON Processing

```javascript
function main(input) {
  const { jsonString } = input;
  
  try {
    const parsed = JSON.parse(jsonString);
    
    // Extract specific fields
    const extracted = {
      userId: parsed.user?.id,
      userName: parsed.user?.name,
      orderId: parsed.order?.id,
      orderTotal: parsed.order?.total
    };
    
    return {
      success: true,
      data: extracted
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}
```

### Pattern 8: Array Filtering

```javascript
function main(input) {
  const { users, minAge, status } = input;
  
  // Filter users
  const filtered = users.filter(user => {
    return user.age >= minAge && user.status === status;
  });
  
  // Sort by age
  const sorted = filtered.sort((a, b) => b.age - a.age);
  
  return {
    filteredUsers: sorted,
    count: sorted.length,
    averageAge: sorted.reduce((sum, u) => sum + u.age, 0) / sorted.length
  };
}
```

## Advanced Patterns

### Error Handling

```javascript
function main(input) {
  try {
    const { num1, num2, operation } = input;
    
    let result;
    
    switch(operation) {
      case 'add':
        result = num1 + num2;
        break;
      case 'subtract':
        result = num1 - num2;
        break;
      case 'multiply':
        result = num1 * num2;
        break;
      case 'divide':
        if (num2 === 0) {
          throw new Error('Division by zero');
        }
        result = num1 / num2;
        break;
      default:
        throw new Error('Invalid operation');
    }
    
    return {
      success: true,
      result: result
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}
```

### Nested Data Processing

```javascript
function main(input) {
  const { order } = input;
  
  // Calculate totals from nested line items
  const lineItems = order.items.map(item => {
    const subtotal = item.quantity * item.price;
    const tax = subtotal * 0.1;
    const total = subtotal + tax;
    
    return {
      ...item,
      subtotal: subtotal.toFixed(2),
      tax: tax.toFixed(2),
      total: total.toFixed(2)
    };
  });
  
  const orderTotal = lineItems.reduce((sum, item) => {
    return sum + parseFloat(item.total);
  }, 0);
  
  return {
    orderId: order.id,
    lineItems: lineItems,
    orderTotal: orderTotal.toFixed(2),
    itemCount: lineItems.length
  };
}
```

## Best Practices

### 1. **Keep Functions Pure**
Avoid side effects, return consistent results for same input

### 2. **Handle Errors Gracefully**
Use try/catch and return error information

### 3. **Validate Input**
Check for required fields and correct types

### 4. **Return Consistent Structure**
Always return an object with predictable fields

### 5. **Use Descriptive Names**
Name functions and variables clearly

### 6. **Comment Complex Logic**
Add comments for non-obvious code

### 7. **Test with Sample Data**
Test functions with known inputs before deployment

### 8. **Avoid External Dependencies**
Can't use npm packages in custom functions

### 9. **Keep Functions Small**
Break complex logic into multiple functions

### 10. **Document Input/Output**
Comment expected input structure and output format

## Limitations

- **No async/await**: Functions must be synchronous
- **No external libraries**: Can't import npm packages
- **Execution timeout**: Functions have time limits
- **No global state**: Each execution is isolated

## Testing Custom Functions

### Use functions_test MCP Tool

```typescript
{
  "tool": "functions_test",
  "parameters": {
    "functionId": "function-id",
    "input": {
      "firstName": "John",
      "lastName": "Doe",
      "email": "JOHN@EXAMPLE.COM",
      "age": 25
    }
  }
}
```

### Expected Output

```json
{
  "success": true,
  "output": {
    "fullName": "John Doe",
    "formattedEmail": "john@example.com",
    "isAdult": true
  }
}
```

## Related Skills

- **make-scenario-builder**: Using functions in scenarios
- **make-module-configuration**: Configuring function modules
- **make-validation-expert**: Debugging function errors

## References

- [JavaScript Function Examples](references/function-examples.md)
