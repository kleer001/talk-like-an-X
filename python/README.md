# Python Text Transformation Library

A Python port of the text transformation patterns used in the TypeScript filters (NYC, Klaus, Newspeak).

## Overview

This library provides a clean, modular approach to creating text transformation filters following **SOLID**, **DRY**, and **YAGNI** principles.

### Key Features

- **10 Core Transformation Patterns** extracted from real filters
- **Protocol-based architecture** (SOLID)
- **Shared base classes** to eliminate duplication (DRY)
- **Simple API** without over-engineering (YAGNI)
- **Case preservation** built-in
- **Word boundary detection** automatic
- **Extensible** through the Transformer protocol

## Quick Start

### Basic Example

```python
from text_transformer import TextFilter, Substitution

# Create a filter
filter = TextFilter()

# Add transformations
filter.add(Substitution({
    "hello": "hey",
    "going to": "gonna",  # Handles phrases too!
    "the": "da"
}))

# Use it
result = filter.transform("Hello! I'm going to the store.")
# Output: "Hey! I'm gonna da store."
```

### Using the Disco Filter

```bash
# Run the example
python disco_filter.py "Hello friend, how are you doing?"
# Output: "Hey baby cat, what's happening, baby!"

# Or pipe text
echo "This party is great!" | python disco_filter.py
```

## Files

- **text_transformer.py** - Main library with all transformation classes
- **disco_filter.py** - Complete working example (1970s disco slang)
- **disco_slang.json** - Example slang dictionary
- **DEVELOPER_GUIDE.md** - Comprehensive guide for creating custom filters

## Architecture

### SOLID Principles Applied

1. **Single Responsibility**: Each transformer handles one type of transformation
2. **Open/Closed**: Extend via new Transformer implementations without modifying core
3. **Liskov Substitution**: All transformers implement the Transformer protocol
4. **Interface Segregation**: Simple `transform(text) -> text` protocol
5. **Dependency Inversion**: TextFilter depends on Transformer protocol, not concrete classes

### DRY Principle

All regex-based transformers share a common `RegexTransformer` base class that handles:
- Pattern compilation
- Rule storage
- Transformation application

### YAGNI Principle

- Merged WordSubstitution and PhraseConsolidation (same pattern, different scale)
- Removed unused features (random number generation, complex conditional logic)
- Kept API minimal but sufficient

## Available Transformers

| Class | Purpose | Example |
|-------|---------|---------|
| `Substitution` | Replace words/phrases | "hello" → "hey" |
| `CharacterSubstitution` | Replace characters | "th" → "d" |
| `SuffixReplacer` | Change suffixes | "-ing" → "-in'" |
| `PrefixReplacer` | Change prefixes | "un-" → "not-" |
| `SentenceAugmenter` | Add at punctuation | "." → ". Right on!" |
| `character_translation` | 1-to-1 char mapping | "a" → "@" |

## Creating Your Own Filter

See **DEVELOPER_GUIDE.md** for detailed instructions.

Quick recipe:

1. Create a JSON dictionary with your slang
2. Build a filter class that loads the dictionary
3. Add transformers in the right order:
   - Phrases first (most specific)
   - Words next
   - Characters
   - Suffixes
   - Sentence augmentation last

## Pattern Analysis Summary

Based on analyzing nyc.ts, klaus.ts, and newspeak.ts, we identified these transformation patterns:

1. **Word Substitution** - Direct vocabulary changes
2. **Character Substitution** - Accent/phonetic effects
3. **Phrase Consolidation** - Multi-word contractions
4. **Suffix/Prefix Morphology** - Systematic grammar rules
5. **Compound Creation** - Merge words into compounds
6. **Boundary Detection** - Context-aware matching
7. **Case Preservation** - Maintain capitalization
8. **Conditional Patterns** - Match-dependent replacement
9. **Sentence Augmentation** - Punctuation modifications
10. **Character Translation** - Character-by-character mapping

## Testing

```bash
# Run the built-in demo
python text_transformer.py

# Test the disco filter
python disco_filter.py
```

## Requirements

- Python 3.7+ (uses typing.Protocol)
- No external dependencies

## License

GPL (matching the original TypeScript filters)

## Contributing

To add your own filter to this collection:

1. Create `your_filter.py` based on `disco_filter.py`
2. Create `your_slang.json` with your vocabulary
3. Add tests and documentation
4. Submit a pull request!
