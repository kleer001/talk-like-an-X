# TypeScript Filter Development Guide

This directory contains the original TypeScript implementation of text transformation filters, ported from the classic debian `filters` package.

---

## 📁 Directory Structure

```
src/
├── lib.ts              # Shared utilities (simuLex, sameCap, etc.)
├── nyc.ts              # Brooklyn/NYC accent
├── klaus.ts            # German accent
├── newspeak.ts         # Orwellian Newspeak
├── chef.ts             # Swedish Chef
├── fudd.ts             # Elmer Fudd
├── cockney.ts          # Cockney English
├── pirate.ts           # Pirate speak
├── scramble.ts         # Letter scrambling
├── studly.ts           # StUdLy CaPs
├── upsidedown.ts       # Upside-down text
├── censor.ts           # Profanity filter
├── jibberish.ts        # Random filter composition
└── ... (21 more filters)
```

---

## 🎯 Creating a New TypeScript Filter

### Option 1: Port to Python (Recommended)

For most filters, we recommend creating a **Python JSON filter** instead, which requires no coding:

1. Analyze the TypeScript filter to identify transformation patterns
2. Extract vocabulary into a JSON file
3. Use the Python `FilterFactory` to build the filter automatically

**Why?** 70% of filters are just vocabulary transformations that can be pure data.

See **[python/FILTER_ANALYSIS.md](../python/FILTER_ANALYSIS.md)** for pattern analysis.

### Option 2: TypeScript Filter (For Algorithmic Cases)

If your filter requires **algorithmic transformations** (scrambling, position-based alternation, complex logic), create a TypeScript filter:

#### 1. Create Your Filter File

```typescript
// src/my_filter.ts

/**
 * My custom filter
 *
 * @copyright (c) 2024 Your Name
 * @license GPL-2+
 */

export function myFilter(initialString: string): string {
  return initialString
    .replace(/pattern1/g, 'replacement1')
    .replace(/pattern2/g, 'replacement2');
}
```

#### 2. Use Shared Utilities

The `lib.ts` file provides helpful utilities:

```typescript
import { sameCap, sameCapReplacer, simuLex, tr } from './lib';

export function myFilter(input: string): string {
  // Preserve capitalization
  return input.replace(/hello/gi, (match) => sameCap(match, 'goodbye'));

  // Character translation (like Perl's tr///)
  return tr(input, 'aeiou', '43!0v');

  // Create a case-preserving replacer
  const replacer = sameCapReplacer('replacement');
  return input.replace(/pattern/gi, replacer);
}
```

#### 3. Use the simuLex Pattern (Advanced)

For complex filters with many rules, use the `simuLex` (simulated Lex scanner) pattern:

```typescript
import { simuLex, SimulexRawRule } from './lib';

const rawRules: SimulexRawRule[] = [
  ['[Tt]he', () => 'ze'],                    // Simple replacement
  ['ing\\b', () => "in'"],                   // Word ending
  ['\\b[Hh]ello', (match) => 'Hi'],          // With callback
];

const rules = simuLex.preprocessRules(rawRules);

export function myFilter(input: string): string {
  return simuLex(input, rules);
}
```

**How simuLex works**:
- Tests each rule in order
- Uses the longest matching rule
- Falls back to passing characters through unchanged
- Mimics the behavior of Lex parsers

#### 4. Export from index.ts

Add your filter to the main export:

```typescript
// index.ts
export { myFilter } from './src/my_filter';
```

#### 5. Add Tests

Create test snapshots:

```typescript
// tests/index.test.ts
import { myFilter } from '../src/my_filter';

describe('myFilter', () => {
  it('should transform text correctly', () => {
    expect(myFilter('Hello world!')).toMatchSnapshot();
  });
});
```

Run tests:
```bash
npm run test
```

---

## 🔍 Common Patterns

### Pattern 1: Simple String Replacement Chain

Most filters are just a chain of `.replace()` calls:

```typescript
export function simple(input: string): string {
  return input
    .replace(/foo/g, 'bar')
    .replace(/baz/g, 'qux');
}
```

**Python equivalent**: Pure JSON with `substitutions` field.

### Pattern 2: Character Substitution

```typescript
export function accent(input: string): string {
  return input
    .replace(/th/g, 'd')
    .replace(/w/g, 'v');
}
```

**Python equivalent**: JSON with `characters` field.

### Pattern 3: Word Boundary Aware

```typescript
export function wordAware(input: string): string {
  return input
    .replace(/\bthe\b/g, 'ze')         // Only complete word "the"
    .replace(/ing\b/g, "in'");         // Only at word end
}
```

**Python equivalent**: JSON with `word_boundary: true`.

### Pattern 4: Case Preservation

```typescript
import { sameCap } from './lib';

export function caseAware(input: string): string {
  return input.replace(/hello/gi, (match) => sameCap(match, 'goodbye'));
}
// "Hello" → "Goodbye", "HELLO" → "GOODBYE", "hello" → "goodbye"
```

**Python equivalent**: JSON with `preserve_case: true` (automatic).

### Pattern 5: Conditional Replacement

```typescript
export function conditional(input: string): string {
  return input.replace(/[ao]ther/g, (match) => {
    return match[0] === 'a' ? 'adder' : 'udder';
  });
}
```

**Python equivalent**: Requires custom Python transformer.

### Pattern 6: Random/Probabilistic

```typescript
import { getRandFn } from './lib';

export function random(input: string): string {
  const rand = getRandFn();

  return input.replace(/word/g, () => {
    if (rand() % 2 === 0) {
      return 'replacement1';
    } else {
      return 'replacement2';
    }
  });
}
```

**Python equivalent**: Requires custom Python transformer.

### Pattern 7: Algorithmic Transformation

```typescript
export function algorithmic(input: string): string {
  return input.split('')
    .map((char, i) => i % 2 === 0 ? char.toUpperCase() : char.toLowerCase())
    .join('');
}
```

**Python equivalent**: Requires custom Python transformer.

---

## 🛠️ Utilities in lib.ts

### `sameCap(original, replacement)`

Preserves the capitalization pattern:

```typescript
sameCap("Hello", "goodbye")  // "Goodbye"
sameCap("HELLO", "goodbye")  // "GOODBYE"
sameCap("hello", "goodbye")  // "goodbye"
```

### `sameCapReplacer(replacement)`

Creates a replacer function for use with `.replace()`:

```typescript
const replacer = sameCapReplacer("goodbye");
input.replace(/hello/gi, replacer);
```

### `simuLex(input, rules, extraUtils?)`

Simulates a Lex scanner:

```typescript
const rules = simuLex.preprocessRules([
  ['pattern1', () => 'replacement1'],
  ['pattern2', () => 'replacement2'],
]);

const output = simuLex(input, rules);
```

### `tr(input, from, to)`

Character-by-character translation (like Perl's `tr///`):

```typescript
tr("hello", "helo", "w3l0")  // "w3ll0"
```

### `getRandFn(seed?)`

Creates a seeded pseudo-random number generator:

```typescript
const rand = getRandFn();
const randomNumber = rand();  // Deterministic based on seed
```

---

## 📋 TypeScript vs Python Decision Matrix

| Filter Type | Use TypeScript If... | Use Python JSON If... |
|-------------|---------------------|----------------------|
| Simple vocabulary | ❌ No | ✅ Yes |
| Accent (character pairs) | ❌ No | ✅ Yes |
| Slang dictionary | ❌ No | ✅ Yes |
| Word boundary aware | ❌ No | ✅ Yes (automatic) |
| Case preservation | ❌ No | ✅ Yes (automatic) |
| Complex probability | ✅ Yes | ❌ No |
| Letter scrambling | ✅ Yes | ❌ No |
| Position-based | ✅ Yes | ❌ No |
| String reversal | ✅ Yes | ❌ No |
| Filter composition | ✅ Yes | ❌ No |

**Rule of Thumb**: If it's primarily vocabulary/patterns, use Python JSON. If it's algorithmic, use TypeScript (or custom Python).

---

## 🏗️ Build System

The TypeScript filters compile to JavaScript for npm distribution:

```bash
# Compile TypeScript
npm run build

# Run tests
npm run test

# Test against original C implementations
npm run test:original
```

**Note**: Most development now happens in Python. The TypeScript filters remain for:
- Legacy compatibility
- npm package distribution
- Algorithmic filters that need TypeScript/JavaScript

---

## 📚 Learning from Existing Filters

### Simple Filter Example: `fudd.ts`

```typescript
export function fudd(initialString: string): string {
  return initialString
    .replace(/[rl]/g, 'w')
    .replace(/qu/g, 'qw')
    .replace(/th\b/g, 'f')
    .replace(/th\B/g, 'd')
    // ... more replacements
}
```

**Lesson**: Simple character/word substitution → Perfect for Python JSON.

### Complex Filter Example: `scramble.ts`

```typescript
function scramble_string(toScramble: string, rand: () => number): string {
  // Fisher-Yates shuffle algorithm
  let scrambled;
  do {
    let tmpstr = toScramble.split('');
    scrambled = [];
    while (tmpstr.length) {
      let i = rand() % tmpstr.length;
      scrambled.push(tmpstr[i]);
      tmpstr.splice(i, 1);
    }
  } while (toScramble === scrambled.join(''));

  return scrambled.join('');
}

export function scramble(input: string): string {
  const rand = getRandFn();
  return input.replace(/[A-Za-z][A-Za-z]{2,}(?=[A-Za-z])/g,
    (match) => match[0] + scramble_string(match.slice(1), rand)
  );
}
```

**Lesson**: Algorithmic transformation → Must be TypeScript (or custom Python class).

---

## 🚀 Migration Path

If you're creating a new filter:

1. **Start with Python JSON** - Try to express it as pure data
2. **Review [python/FILTER_ANALYSIS.md](../python/FILTER_ANALYSIS.md)** - Check if patterns exist
3. **Only use TypeScript if**:
   - You need algorithmic transformations
   - You need complex stateful logic
   - You need JavaScript/npm distribution

**70% of filters** can be pure JSON → much easier to create and maintain!

---

## 🎓 Additional Resources

- **[python/README.md](../python/README.md)** - Python library documentation
- **[python/FILTER_SCHEMA.md](../python/FILTER_SCHEMA.md)** - JSON filter schema
- **[python/FILTER_ANALYSIS.md](../python/FILTER_ANALYSIS.md)** - Analysis of all 25 filters
- **[python/DEVELOPER_GUIDE.md](../python/DEVELOPER_GUIDE.md)** - Python filter development
- **[original/debian/copyright](../original/debian/copyright)** - License information

---

## 📜 License

All filters inherit licenses from the original authors. Most are GPL-2+ or GPL-3+. See individual file headers and `original/debian/copyright` for details.

When creating new filters, please:
- Add appropriate copyright header
- Specify license (GPL-2+ recommended for compatibility)
- Credit original inspiration if applicable

---

**Happy filtering!** 🎉

For most use cases, check out the **[Python JSON filters](../python/README.md)** first - they're much easier to create!
