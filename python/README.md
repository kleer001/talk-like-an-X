# Python Text Transformation Library

A Python port of the text transformation patterns used in the TypeScript filters (NYC, Klaus, Newspeak).

## 🎯 Key Innovation: Data-Driven Filters

**No Python coding required!** Define filters entirely in JSON files.

```bash
# Create a filter with just JSON - no Python class needed
python filter_factory.py disco.json "Hello friend!"
# Output: "Hey baby cat!"
```

## Quick Start

### Using Pre-Made Filters

```bash
# Disco slang (1970s)
./filter_factory.py disco "Hello, how are you today?"
# Output: "Hey baby, what's happenin' today?"

# Pirate speak
./filter_factory.py pirate "Hello my friend! Yes, I am happy."
# Output: "Ahoy me matey!, arr! Aye, I be stoked."

# German accent
./filter_factory.py german "The weather is very warm."
# Output: "Ze feader ist fery farm."

# Swedish Chef
./filter_factory.py chef "The weather is wonderful!"
# Output: "Zee veazeer is vonderful!
Bork Bork Bork!"

# Elmer Fudd
./filter_factory.py fudd "Be very quiet. I'm hunting rabbits."
# Output: "Be vewy quiet., uh-hah-hah-hah. I'm hunting wabbits."

# Note: .json extension is optional!
```

### Creating Your Own Filter

1. **Copy an example JSON file** (e.g., `disco.json`)
2. **Edit the vocabulary** - no coding needed!
3. **Test it**:
   ```bash
   python filter_factory.py my_filter.json "test text"
   ```

That's it! No Python class to write, no logic to duplicate.

## Architecture

### The Old Way (Duplicated Logic) ❌

```
disco_filter.py   ─┐
pirate_filter.py  ├─ All contain the same filter-building logic
valley_filter.py  ┘
```

### The New Way (DRY) ✅

```
filter_factory.py ──► Universal filter builder (write once)
        │
        ├─► disco.json    (just data)
        ├─► pirate.json   (just data)
        └─► valley.json   (just data)
```

### Why This Is Better

**DRY (Don't Repeat Yourself)**:
- Filter-building logic lives in ONE place (`filter_factory.py`)
- Each filter is just data (JSON)
- No duplicated Python code

**YAGNI (You Ain't Gonna Need It)**:
- No custom Python class for each filter
- No boilerplate code
- JSON is simpler to edit than Python

**Separation of Concerns**:
- Data (vocabulary) separated from logic (transformation)
- Non-programmers can create filters
- Easier to maintain and version control

## Files

### Core Library
- **text_transformer.py** - Transformation classes (the engine)
- **filter_factory.py** - Universal filter builder (reads JSON)

### Documentation
- **FILTER_SCHEMA.md** - Complete JSON schema reference
- **TRANSFORMATION_PATTERNS.md** - High-level pattern analysis
- **FILTER_ANALYSIS.md** - Analysis of all 25 TypeScript filters
- **DEVELOPER_GUIDE.md** - Advanced usage and custom transformers

### Example Filters (JSON Only!)
- **disco.json** - 1970s disco slang
- **pirate.json** - Pirate speak
- **german.json** - German accent
- **chef.json** - Swedish Chef (Bork Bork Bork!)
- **fudd.json** - Elmer Fudd

### Legacy (Deprecated)
- ~~disco_filter.py~~ (replaced by disco.json + filter_factory.py)
- ~~disco_slang.json~~ (merged into disco.json)

## JSON Filter Format

Minimal example:

```json
{
  "name": "My Filter",
  "substitutions": {
    "hello": "hey",
    "goodbye": "later"
  }
}
```

Full-featured example:

```json
{
  "name": "1970s Disco",
  "substitutions": {
    "hello": "hey baby",
    "how are you": "what's happening",
    "going to": "gonna"
  },
  "characters": {
    "th": "d"
  },
  "suffixes": {
    "ing": "in'"
  },
  "sentence_augmentation": [
    {
      "punctuation": ".",
      "additions": [" dig?", " right on!"],
      "frequency": 3
    }
  ]
}
```

See **FILTER_SCHEMA.md** for complete documentation.

## Available Transformation Types

| Type | What It Does | Example |
|------|--------------|---------|
| `substitutions` | Replace words/phrases | "hello" → "hey" |
| `characters` | Replace character pairs | "th" → "d" |
| `suffixes` | Transform word endings | "ing" → "in'" |
| `prefixes` | Transform word beginnings | "un" → "not" |
| `sentence_augmentation` | Add at punctuation | "." → ". Right?" |

## Usage from Python

```python
from filter_factory import FilterFactory

# Load any JSON filter
filter = FilterFactory.from_json('disco.json')

# Transform text
result = filter.transform("Hello friend, how are you?")
print(result)
# "Hey baby cat, what's happening?"
```

## Usage from Command Line

```bash
# Direct text
python filter_factory.py disco.json "Hello world"

# Pipe input
echo "Hello world" | python filter_factory.py disco.json

# File processing
python filter_factory.py disco.json < input.txt > output.txt
```

## Design Principles

### SOLID
- **Single Responsibility**: Each transformer class has one job
- **Open/Closed**: Extend via JSON, not code modification
- **Liskov Substitution**: All transformers implement same protocol
- **Interface Segregation**: Simple `transform()` interface
- **Dependency Inversion**: FilterFactory depends on abstractions

### DRY
- Filter-building logic written once in `FilterFactory`
- Shared `RegexTransformer` base class
- No duplicated pattern compilation code

### YAGNI
- No custom classes per filter
- No over-engineering
- Simple JSON schema without unnecessary complexity

## Pattern Analysis

Based on analyzing nyc.ts, klaus.ts, and newspeak.ts, we identified **10 core transformation patterns**:

1. Word/Phrase Substitution
2. Character Pair Replacement
3. Multi-Word Phrase Consolidation *(merged with #1)*
4. Suffix/Prefix Morphology
5. Compound Word Creation *(handled by substitutions)*
6. Context-Aware Boundary Detection
7. Case Preservation
8. Conditional Pattern Matching
9. Punctuation/Sentence Augmentation
10. Character Translation

The library implements all patterns while staying DRY and simple.

## Creating Your Own Filter - Step by Step

### 1. Start with a Template

Copy an existing JSON file:
```bash
cp disco.json my_filter.json
```

### 2. Edit the Metadata

```json
{
  "name": "My Awesome Filter",
  "description": "What it does",
  "author": "Your Name"
}
```

### 3. Add Your Vocabulary

```json
{
  "substitutions": {
    "hello": "greetings",
    "friend": "companion",
    "going to": "shall"
  }
}
```

### 4. Add Other Transformations (Optional)

```json
{
  "suffixes": {
    "ing": "eth"
  },
  "sentence_augmentation": [
    {
      "punctuation": ".",
      "additions": [" verily!", " forsooth!"],
      "frequency": 2
    }
  ]
}
```

### 5. Test It

```bash
python filter_factory.py my_filter.json "Hello friend, I am going to town."
```

### 6. Iterate and Refine

Add more words, adjust settings, test edge cases.

**No Python coding needed at any step!**

## Advanced: Custom Transformers in Python

If JSON isn't enough, you can still write custom Python transformers:

```python
from text_transformer import TextFilter, RegexTransformer

class MyCustomTransformer(RegexTransformer):
    def __init__(self):
        super().__init__()
        # Your custom logic here

filter = TextFilter()
filter.add(MyCustomTransformer())
```

See **DEVELOPER_GUIDE.md** for advanced usage.

## Testing

```bash
# Run all example filters
./filter_factory.py disco "Hello friend"
./filter_factory.py pirate "Hello friend"
./filter_factory.py german "Hello friend"
./filter_factory.py chef "Hello friend"
./filter_factory.py fudd "Hello friend"

# Test the library directly
python text_transformer.py
```

## Coverage

After analyzing all 25 TypeScript filters in `src/`, we found that **~70% can be fully implemented in JSON** with no custom Python code needed! See **FILTER_ANALYSIS.md** for details.

The remaining 30% require algorithmic transformations (like letter scrambling, position-based alternation, etc.) that are filter-specific and should be implemented as custom Python classes - which is exactly the right design!

## Requirements

- Python 3.7+ (uses `typing.Protocol`)
- No external dependencies

## License

GPL (matching the original TypeScript filters)

## Contributing

To add a new filter:

1. Create `your_filter.json` following the schema
2. Test it with `filter_factory.py`
3. Add example output to this README
4. Submit a pull request!

**That's it!** No Python code to review, just JSON data.

## Migration from Old System

If you have an old-style filter class:

**Before** (disco_filter.py - 80 lines):
```python
class DiscoFilter:
    def __init__(self):
        # Load JSON
        # Build filter
        # Configure transformers
        # ... lots of boilerplate
```

**After** (disco.json - just data):
```json
{
  "name": "1970s Disco",
  "substitutions": { ... }
}
```

**Usage**:
```bash
# Old way
python disco_filter.py "Hello"

# New way
python filter_factory.py disco.json "Hello"
```

Same result, way less code!

## Philosophy

> **Most text transformations are data, not logic.**

Instead of writing Python classes that do the same thing with different vocabularies, we separate:
- **Logic**: Universal transformation patterns (written once)
- **Data**: Vocabulary and settings (JSON files)

This makes filters:
- ✅ Easier to create (no coding)
- ✅ Easier to maintain (edit data, not code)
- ✅ Easier to share (JSON is universal)
- ✅ Easier to version control (clean diffs)

---

**Happy filtering!** 🎉
