# JavaScript Function Examples

Ready-to-use JavaScript function examples for Make.com scenarios.

## Data Validation

### Email Validator
```javascript
function main(input) {
  const { email } = input;
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const isValid = emailRegex.test(email);
  
  return {
    email: email,
    isValid: isValid,
    error: isValid ? null : 'Invalid email format'
  };
}
```

### Phone Number Formatter
```javascript
function main(input) {
  const { phone } = input;
  
  // Remove all non-digits
  const cleaned = phone.replace(/\D/g, '');
  
  // Format as (XXX) XXX-XXXX
  if (cleaned.length === 10) {
    const formatted = `(${cleaned.substring(0,3)}) ${cleaned.substring(3,6)}-${cleaned.substring(6)}`;
    return {
      original: phone,
      formatted: formatted,
      isValid: true
    };
  }
  
  return {
    original: phone,
    formatted: null,
    isValid: false,
    error: 'Phone number must be 10 digits'
  };
}
```

### Credit Card Validator
```javascript
function main(input) {
  const { cardNumber } = input;
  
  // Luhn algorithm
  const digits = cardNumber.replace(/\D/g, '');
  let sum = 0;
  let isEven = false;
  
  for (let i = digits.length - 1; i >= 0; i--) {
    let digit = parseInt(digits[i]);
    
    if (isEven) {
      digit *= 2;
      if (digit > 9) digit -= 9;
    }
    
    sum += digit;
    isEven = !isEven;
  }
  
  return {
    isValid: sum % 10 === 0,
    lastFourDigits: digits.slice(-4)
  };
}
```

## Data Transformation

### CSV to JSON
```javascript
function main(input) {
  const { csvData } = input;
  
  const lines = csvData.trim().split('\n');
  const headers = lines[0].split(',');
  
  const jsonData = lines.slice(1).map(line => {
    const values = line.split(',');
    const obj = {};
    
    headers.forEach((header, index) => {
      obj[header.trim()] = values[index]?.trim();
    });
    
    return obj;
  });
  
  return {
    count: jsonData.length,
    data: jsonData
  };
}
```

### Flatten Nested Object
```javascript
function main(input) {
  const { data } = input;
  
  function flatten(obj, prefix = '') {
    const flattened = {};
    
    for (const key in obj) {
      const newKey = prefix ? `${prefix}.${key}` : key;
      
      if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
        Object.assign(flattened, flatten(obj[key], newKey));
      } else {
        flattened[newKey] = obj[key];
      }
    }
    
    return flattened;
  }
  
  return {
    flattened: flatten(data)
  };
}
```

### Group By Property
```javascript
function main(input) {
  const { items, groupBy } = input;
  
  const grouped = items.reduce((acc, item) => {
    const key = item[groupBy];
    if (!acc[key]) {
      acc[key] = [];
    }
    acc[key].push(item);
    return acc;
  }, {});
  
  return {
    groups: Object.keys(grouped).length,
    data: grouped
  };
}
```

## Calculations

### Tax Calculator
```javascript
function main(input) {
  const { amount, taxRate, country } = input;
  
  const tax = amount * (taxRate / 100);
  const total = amount + tax;
  
  return {
    subtotal: amount.toFixed(2),
    tax: tax.toFixed(2),
    total: total.toFixed(2),
    taxRate: taxRate,
    country: country
  };
}
```

### Discount Calculator
```javascript
function main(input) {
  const { price, discountPercent, quantity } = input;
  
  const subtotal = price * quantity;
  const discountAmount = subtotal * (discountPercent / 100);
  const total = subtotal - discountAmount;
  
  return {
    originalPrice: price.toFixed(2),
    quantity: quantity,
    subtotal: subtotal.toFixed(2),
    discountPercent: discountPercent,
    discountAmount: discountAmount.toFixed(2),
    total: total.toFixed(2),
    savings: discountAmount.toFixed(2)
  };
}
```

### Compound Interest
```javascript
function main(input) {
  const { principal, rate, years, compound } = input;
  
  const n = compound || 12; // Monthly by default
  const amount = principal * Math.pow((1 + rate / 100 / n), n * years);
  const interest = amount - principal;
  
  return {
    principal: principal.toFixed(2),
    interest: interest.toFixed(2),
    total: amount.toFixed(2),
    years: years,
    annualRate: rate
  };
}
```

## String Manipulation

### Slug Generator
```javascript
function main(input) {
  const { title } = input;
  
  const slug = title
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, '-')
    .replace(/^-+|-+$/g, '');
  
  return {
    original: title,
    slug: slug
  };
}
```

### Extract URLs
```javascript
function main(input) {
  const { text } = input;
  
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  const urls = text.match(urlRegex) || [];
  
  return {
    urlCount: urls.length,
    urls: urls,
    uniqueUrls: [...new Set(urls)]
  };
}
```

### Word Counter
```javascript
function main(input) {
  const { text } = input;
  
  const words = text.trim().split(/\s+/);
  const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
  
  const wordFrequency = words.reduce((acc, word) => {
    const cleanWord = word.toLowerCase().replace(/[^\w]/g, '');
    acc[cleanWord] = (acc[cleanWord] || 0) + 1;
    return acc;
  }, {});
  
  return {
    wordCount: words.length,
    sentenceCount: sentences.length,
    charCount: text.length,
    avgWordLength: (text.replace(/\s/g, '').length / words.length).toFixed(2),
    topWords: Object.entries(wordFrequency)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([word, count]) => ({ word, count }))
  };
}
```

## Date & Time

### Business Days Calculator
```javascript
function main(input) {
  const { startDate, days } = input;
  
  const start = new Date(startDate);
  let count = 0;
  let current = new Date(start);
  
  while (count < days) {
    current.setDate(current.getDate() + 1);
    const dayOfWeek = current.getDay();
    
    // Skip weekends
    if (dayOfWeek !== 0 && dayOfWeek !== 6) {
      count++;
    }
  }
  
  return {
    startDate: start.toISOString().split('T')[0],
    endDate: current.toISOString().split('T')[0],
    businessDays: days
  };
}
```

### Age Calculator
```javascript
function main(input) {
  const { birthDate } = input;
  
  const birth = new Date(birthDate);
  const today = new Date();
  
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  
  const nextBirthday = new Date(today.getFullYear(), birth.getMonth(), birth.getDate());
  if (nextBirthday < today) {
    nextBirthday.setFullYear(today.getFullYear() + 1);
  }
  
  const daysUntil = Math.ceil((nextBirthday - today) / (1000 * 60 * 60 * 24));
  
  return {
    birthDate: birthDate,
    age: age,
    nextBirthday: nextBirthday.toISOString().split('T')[0],
    daysUntilBirthday: daysUntil
  };
}
```

### Time Zone Converter
```javascript
function main(input) {
  const { dateTime, fromZone, toZone } = input;
  
  const date = new Date(dateTime);
  
  const options = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: toZone,
    hour12: false
  };
  
  const converted = new Intl.DateTimeFormat('en-US', options).format(date);
  
  return {
    original: dateTime,
    fromZone: fromZone,
    toZone: toZone,
    converted: converted
  };
}
```

## Array Operations

### Remove Duplicates
```javascript
function main(input) {
  const { items } = input;
  
  const unique = [...new Set(items)];
  const duplicates = items.filter((item, index) => items.indexOf(item) !== index);
  
  return {
    original: items,
    unique: unique,
    duplicates: [...new Set(duplicates)],
    originalCount: items.length,
    uniqueCount: unique.length,
    duplicateCount: items.length - unique.length
  };
}
```

### Sort and Rank
```javascript
function main(input) {
  const { items, sortBy } = input;
  
  const sorted = [...items].sort((a, b) => {
    return b[sortBy] - a[sortBy];
  });
  
  const ranked = sorted.map((item, index) => ({
    ...item,
    rank: index + 1
  }));
  
  return {
    sortedBy: sortBy,
    count: ranked.length,
    data: ranked
  };
}
```

### Paginate Array
```javascript
function main(input) {
  const { items, page, pageSize } = input;
  
  const start = (page - 1) * pageSize;
  const end = start + pageSize;
  const pageItems = items.slice(start, end);
  
  const totalPages = Math.ceil(items.length / pageSize);
  
  return {
    page: page,
    pageSize: pageSize,
    totalItems: items.length,
    totalPages: totalPages,
    hasNext: page < totalPages,
    hasPrev: page > 1,
    data: pageItems
  };
}
```

## Advanced Patterns

### Fuzzy String Match
```javascript
function main(input) {
  const { str1, str2 } = input;
  
  function levenshtein(a, b) {
    const matrix = [];
    
    for (let i = 0; i <= b.length; i++) {
      matrix[i] = [i];
    }
    
    for (let j = 0; j <= a.length; j++) {
      matrix[0][j] = j;
    }
    
    for (let i = 1; i <= b.length; i++) {
      for (let j = 1; j <= a.length; j++) {
        if (b.charAt(i - 1) === a.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1];
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1,
            matrix[i][j - 1] + 1,
            matrix[i - 1][j] + 1
          );
        }
      }
    }
    
    return matrix[b.length][a.length];
  }
  
  const distance = levenshtein(str1.toLowerCase(), str2.toLowerCase());
  const maxLen = Math.max(str1.length, str2.length);
  const similarity = ((maxLen - distance) / maxLen * 100).toFixed(2);
  
  return {
    string1: str1,
    string2: str2,
    distance: distance,
    similarity: parseFloat(similarity),
    isMatch: similarity > 80
  };
}
```

### Generate Random String
```javascript
function main(input) {
  const { length, includeNumbers, includeSymbols } = input;
  
  let chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
  if (includeNumbers) chars += '0123456789';
  if (includeSymbols) chars += '!@#$%^&*()_+-=[]{}|;:,.<>?';
  
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  
  return {
    randomString: result,
    length: result.length,
    config: {
      numbers: includeNumbers,
      symbols: includeSymbols
    }
  };
}
```
