# Filter JSON Schema Documentation

## Overview

Filters are defined entirely in JSON files - no Python code needed! The `FilterFactory` reads these JSON files and automatically builds the appropriate text transformation pipeline.

## Basic Structure

```json
{
  "name": "My Filter Name",
  "description": "What this filter does",
  "author": "Your name (optional)",

  "substitutions": { /* word/phrase replacements */ },
  "characters": { /* character replacements */ },
  "suffixes": { /* suffix transformations */ },
  "prefixes": { /* prefix transformations */ },
  "sentence_augmentation": [ /* punctuation effects */ ],

  "preserve_case": true,
  "word_boundary": true,
  "prefix_text": "",
  "suffix_text": ""
}
```

## Field Reference

### Metadata (Optional)

#### `name` (string)
The display name of your filter.

```json
"name": "1970s Disco Enthusiast"
```

#### `description` (string)
Brief description of what the filter does.

```json
"description": "Transforms text into far-out 1970s disco slang"
```

#### `author` (string)
Who created this filter.

```json
"author": "Your Name"
```

---

### Transformations

#### `substitutions` (object)

**Purpose**: Replace words and multi-word phrases with alternatives.

**Type**: Dictionary mapping original text to replacement text.

**Features**:
- Automatically handles both single words and multi-word phrases
- Preserves capitalization by default
- Respects word boundaries
- Longer matches take priority (phrases matched before words)

**Examples**:

```json
"substitutions": {
  "hello": "hey",
  "goodbye": "later",
  "how are you": "what's up",
  "going to": "gonna"
}
```

**Input**: "Hello friend, how are you? I'm going to the store."
**Output**: "Hey friend, what's up? I'm gonna the store."

**Case preservation**:
```json
"substitutions": {
  "hello": "hey"
}
```
- "hello" → "hey"
- "Hello" → "Hey"
- "HELLO" → "HEY"

---

#### `characters` (object)

**Purpose**: Replace individual characters or character sequences.

**Type**: Dictionary mapping character patterns to replacements.

**Use cases**: Accents, phonetic effects, stylistic changes.

**Examples**:

```json
"characters": {
  "th": "d",
  "w": "v",
  "v": "f"
}
```

**Input**: "The weather is very warm."
**Output**: "De veader is fery varm."

**Note**: Longer patterns are matched first, so "th" will be checked before "t" or "h".

---

#### `suffixes` (object)

**Purpose**: Transform word endings systematically.

**Type**: Dictionary mapping suffix patterns to replacements.

**Simple format**:
```json
"suffixes": {
  "ing": "in'",
  "ly": "wise"
}
```

**Advanced format** (with minimum stem length):
```json
"suffixes": {
  "ing": {
    "replacement": "in'",
    "min_stem": 3
  }
}
```

**Input**: "I am walking quickly."
**Output**: "I am walkin' quickwise."

**Note**: Only matches complete word endings, not mid-word patterns.

---

#### `prefixes` (object)

**Purpose**: Transform word beginnings.

**Type**: Dictionary mapping prefix patterns to replacements.

**Examples**:

```json
"prefixes": {
  "un": "not",
  "re": "again"
}
```

**Input**: "This is unhappy and replay."
**Output**: "This is nothappy and againplay."

---

#### `sentence_augmentation` (array)

**Purpose**: Add phrases at punctuation boundaries or modify punctuation.

**Type**: Array of augmentation rule objects.

**Rule format**:
```json
{
  "punctuation": ".",
  "additions": ["right on!", "dig it!", "far out!"],
  "frequency": 3
}
```

**Fields**:
- `punctuation` (string): Which punctuation mark to augment
- `additions` (array): List of phrases to add (cycles through them)
- `frequency` (integer): How often to add
  - `1` = every occurrence
  - `2` = every other occurrence
  - `3` = every third occurrence, etc.

**Examples**:

```json
"sentence_augmentation": [
  {
    "punctuation": "!",
    "additions": [", arr!", ", matey!"],
    "frequency": 1
  },
  {
    "punctuation": ".",
    "additions": [" Right?", " You dig?"],
    "frequency": 2
  }
]
```

**Input**: "Hello! Great! How are you."
**Output**: "Hello, arr! Great, matey! How are you Right?"

---

### Global Settings

#### `preserve_case` (boolean, default: true)

Whether to maintain the original capitalization pattern when replacing text.

```json
"preserve_case": true
```

- `true`: "Hello" → "Hey", "HELLO" → "HEY"
- `false`: "Hello" → "hey", "HELLO" → "hey"

---

#### `word_boundary` (boolean, default: true)

Whether to only match complete words (not substrings within words).

```json
"word_boundary": true
```

- `true`: "the" matches "the" but not the "the" in "theater"
- `false`: "the" matches both, resulting in "theater" → "deater"

**Recommendation**: Keep this `true` unless you specifically want substring replacement.

---

#### `prefix_text` (string, default: "")

Text to add before the transformed output.

```json
"prefix_text": "BEGIN: "
```

**Input**: "Hello world"
**Output**: "BEGIN: Hello vorld" (assuming other transformations)

---

#### `suffix_text` (string, default: "")

Text to add after the transformed output.

```json
"suffix_text": "\nHail Big Brother!\n"
```

**Input**: "Hello world"
**Output**: "Hello vorld\nHail Big Brother!\n"

---

## Complete Examples

### Minimal Filter

```json
{
  "name": "Simple Test",
  "substitutions": {
    "hello": "hi",
    "goodbye": "bye"
  }
}
```

### Full-Featured Filter

```json
{
  "name": "Valley Girl",
  "description": "Like, totally transforms your text",
  "author": "Demo",

  "substitutions": {
    "very": "so",
    "really": "totally",
    "yes": "yeah",
    "no": "as if",
    "i think": "i'm like"
  },

  "suffixes": {
    "ing": "in'"
  },

  "sentence_augmentation": [
    {
      "punctuation": ".",
      "additions": [", like, totally!", ", you know?", ", whatever!"],
      "frequency": 2
    },
    {
      "punctuation": "!",
      "additions": [", oh my god!", ", no way!"],
      "frequency": 1
    }
  ],

  "preserve_case": true,
  "word_boundary": true
}
```

---

## Transformation Order

Transformations are applied in this order:

1. **Substitutions** (phrases and words together)
2. **Characters** (accent effects)
3. **Suffixes** (word endings)
4. **Prefixes** (word beginnings)
5. **Sentence augmentation** (punctuation effects)

This order ensures:
- Phrases are matched before individual words
- Word-level transformations happen before character-level
- Punctuation effects are added last

You don't need to worry about this - the `FilterFactory` handles it automatically!

---

## Usage

### From Python

```python
from filter_factory import FilterFactory

# Load your filter
filter = FilterFactory.from_json('my_filter.json')

# Use it
result = filter.transform("Hello world!")
print(result)
```

### From Command Line

```bash
# Direct text
python filter_factory.py my_filter.json "Hello world"

# Pipe
echo "Hello world" | python filter_factory.py my_filter.json

# File redirect
python filter_factory.py my_filter.json < input.txt > output.txt
```

---

## Creating Your Own Filter

1. **Copy an example** (e.g., `disco.json` or `pirate.json`)
2. **Edit the JSON** with your vocabulary
3. **Test it**:
   ```bash
   python filter_factory.py your_filter.json "test sentence"
   ```
4. **Iterate** - add more words, adjust settings, refine

No Python coding required!

---

## Tips & Best Practices

### 1. Use Multi-Word Phrases

Instead of:
```json
"how": "wot",
"are": "r",
"you": "u"
```

Do this:
```json
"how are you": "wazzup"
```

This gives better, more natural results.

### 2. Order Your Substitutions Logically

Group related terms together for easy maintenance:

```json
"substitutions": {
  "__comment_greetings": "===== Greetings =====",
  "hello": "hey",
  "hi": "sup",

  "__comment_farewells": "===== Farewells =====",
  "goodbye": "later",
  "bye": "peace"
}
```

(Keys starting with `_` are ignored by the system)

### 3. Test Edge Cases

Test with:
- Different capitalizations
- Words at start/end of sentences
- Plurals and verb forms
- Words appearing in compounds

### 4. Start Small, Build Up

Begin with 10-20 core words, test thoroughly, then expand.

### 5. Listen to Real Speech

The best filters come from observing actual dialects, accents, or speech patterns.

---

## Troubleshooting

### "My phrase isn't being matched"

Make sure there are no typos and the phrase appears exactly as written (the filter handles capitalization automatically).

### "Words are being replaced inside other words"

Set `"word_boundary": true` in your JSON.

### "Capitalization is wrong"

Set `"preserve_case": true` in your JSON.

### "My longer phrase is being broken up"

This shouldn't happen - substitutions automatically sort by length. If it does, check for overlapping rules.

---

## JSON Schema Validation

Your JSON should validate against this structure:

```json
{
  "name": "string (optional)",
  "description": "string (optional)",
  "author": "string (optional)",
  "substitutions": {
    "string": "string"
  },
  "characters": {
    "string": "string"
  },
  "suffixes": {
    "string": "string or object"
  },
  "prefixes": {
    "string": "string"
  },
  "sentence_augmentation": [
    {
      "punctuation": "string",
      "additions": ["string"],
      "frequency": "integer"
    }
  ],
  "preserve_case": "boolean",
  "word_boundary": "boolean",
  "prefix_text": "string",
  "suffix_text": "string"
}
```

All fields are optional except at least one transformation type.
