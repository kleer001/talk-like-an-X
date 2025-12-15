# Developer Guide: Creating Custom Language Filters

## Table of Contents
1. [Introduction](#introduction)
2. [Core Transformation Patterns](#core-transformation-patterns)
3. [Quick Start Guide](#quick-start-guide)
4. [Best Practices](#best-practices)
5. [Pattern Reference](#pattern-reference)
6. [Real-World Examples](#real-world-examples)
7. [Performance Tips](#performance-tips)

---

## Introduction

This guide shows you how to create your own fun language-mangling filters using the `text_transformer` library. The library is based on analysis of successful TypeScript filters (NYC, Klaus, Newspeak) and provides 10 core transformation patterns that can be mixed and matched.

### Philosophy

The key insight is that **most text transformations can be decomposed into a small set of patterns**:

- Word substitution
- Character/letter replacement
- Phrase consolidation
- Morphological transformations (prefixes/suffixes)
- Compound word creation
- Context-aware replacements
- Case preservation
- Sentence augmentation

By combining these patterns in the right order, you can create convincing dialects, accents, and language styles.

---

## Core Transformation Patterns

### 1. Word Substitution
Replace complete words with alternatives.

```python
from text_transformer import WordSubstitution

# Simple word replacements
pirate = WordSubstitution({
    "hello": "ahoy",
    "yes": "aye",
    "my": "me",
    "friend": "matey",
    "the": "th'"
})

text = pirate.transform("Hello my friend!")
# Output: "Ahoy me matey!"
```

**When to use**: The backbone of most filters. Start here.

**Pro tip**: Use `word_boundary=True` (default) to avoid replacing parts of words.

---

### 2. Character/Letter Substitution
Replace individual characters or character pairs.

```python
from text_transformer import CharacterSubstitution

# German accent
german = CharacterSubstitution({
    "w": "v",
    "v": "f",
    "th": "d"
}, word_position='end')

text = german.transform("with that")
# Output: "vit dat"
```

**When to use**: Creating accents, phonetic transformations.

**Pro tip**: Use `word_position` to target specific locations.

---

### 3. Phrase Consolidation
Collapse multi-word phrases into contractions.

```python
from text_transformer import PhraseConsolidation

# Casual speech
casual = PhraseConsolidation({
    "going to": "gonna",
    "want to": "wanna",
    "got to": "gotta",
    "out of": "outta"
})

text = casual.transform("I am going to go out of here")
# Output: "I am gonna go outta here"
```

**When to use**: Colloquial speech, slang, contractions.

**Pro tip**: Apply BEFORE word substitution to prevent breaking up phrases.

---

### 4. Morphology Transformer
Systematically modify prefixes and suffixes.

```python
from text_transformer import MorphologyTransformer

# Newspeak-style
morph = MorphologyTransformer()

# "-ly" becomes "-wise"
morph.add_suffix_rule(r'ly\b', 'wise')

# "not the X" becomes "the unX"
morph.add_negation_rule("not the", prefix="un", insert_after="the ")

text = morph.transform("quickly and not the happiest")
# Output: "quickwise and the unhappiest"
```

**When to use**: Systematic grammatical transformations, invented languages.

**Pro tip**: Great for creating consistent linguistic rules.

---

### 5. Compound Creator
Merge words into compounds.

```python
from text_transformer import CompoundCreator

# Orwellian compounds
compounds = CompoundCreator({
    "person": ("party", "worker"),
    "family": ("family", "unit")
}, separator=" ")

text = compounds.transform("Every person and family")
# Output: "Every party worker and family unit"
```

**When to use**: Creating specialized vocabularies, technical jargon.

---

### 6. Sentence Augmenter
Add phrases at punctuation boundaries.

```python
from text_transformer import SentenceAugmenter

# Valley girl
valley = SentenceAugmenter()
valley.add_punctuation_replacement(
    punctuation=".",
    replacement=[", like, totally!", ", you know?", ", whatever!"],
    frequency=2  # Every other sentence
)

text = valley.transform("I went to the store. It was fun.")
# Output: "I went to the store, like, totally! It was fun."
```

**When to use**: Adding verbal tics, catchphrases, emphasis.

**Pro tip**: Apply LAST in your transformation pipeline.

---

### 7. Conditional Replacer
Context-aware transformations based on what was matched.

```python
from text_transformer import ConditionalReplacer

# Context-dependent replacements
conditional = ConditionalReplacer()

def replace_other(match):
    # "other" -> "udder", "aother" -> "adder"
    text = match.group(0)
    if text[0] == 'a':
        return 'adder'
    else:
        return 'udder'

conditional.add_rule(r'[ao]ther', replace_other)
```

**When to use**: When replacement depends on matched content or context.

---

## Quick Start Guide

### Step 1: Create Your Slang Dictionary

Create a JSON file with your vocabulary:

```json
{
  "words": {
    "hello": "sup",
    "friend": "homie",
    "cool": "rad"
  },
  "phrases": {
    "how are you": "what's good",
    "going to": "gonna"
  },
  "affixes": {
    "suffixes": {
      "ing": "in'"
    }
  },
  "sentence_fillers": [
    " bro!",
    " dude!",
    " man!"
  ]
}
```

### Step 2: Create Your Filter Class

```python
from text_transformer import TextFilter, WordSubstitution, PhraseConsolidation
import json

class MyCustomFilter:
    def __init__(self, dict_path):
        with open(dict_path) as f:
            self.slang = json.load(f)
        self.filter = self._build_filter()

    def _build_filter(self):
        filter = TextFilter("My Custom Filter")

        # Apply transformations in order:
        # 1. Phrases (most specific)
        phrases = PhraseConsolidation(self.slang['phrases'])
        filter.add_transformer(phrases)

        # 2. Words (main dictionary)
        words = WordSubstitution(self.slang['words'])
        filter.add_transformer(words)

        # 3. More patterns as needed...

        return filter

    def transform(self, text):
        return self.filter.transform(text)
```

### Step 3: Use Your Filter

```python
# In your script
filter = MyCustomFilter('my_slang.json')
output = filter.transform("Hello friend, how are you today?")
print(output)
```

---

## Best Practices

### 1. **Order Matters!**

Apply transformations from **largest to smallest** units:

```python
# ✅ CORRECT ORDER
filter.add_transformer(phrases)        # Multi-word first
filter.add_transformer(words)          # Then single words
filter.add_transformer(characters)     # Then characters
filter.add_transformer(morphology)     # Then suffixes
filter.add_transformer(augmenter)      # Sentence stuff last
```

**Why?** If you replace "going" before consolidating "going to", you'll never match the phrase.

### 2. **Use Specificity**

More specific transformations should come before general ones:

```python
# ✅ CORRECT: Exclamations before general words
filter.add_transformer(exclamations)   # "Wow!" -> "Far out!"
filter.add_transformer(general_words)  # "wow" -> "amazing"
```

### 3. **Test Edge Cases**

Watch out for:
- Capitalization ("The" vs "the")
- Punctuation boundaries
- Words within words ("the" in "theater")
- Multi-word phrases breaking

### 4. **Keep Dictionaries Maintainable**

Use JSON for easy editing:

```json
{
  "comment": "Group related terms together",
  "greetings": {
    "hello": "hey",
    "hi": "yo"
  },
  "farewells": {
    "goodbye": "peace",
    "bye": "later"
  }
}
```

Then merge them in code:

```python
all_words = {**slang['greetings'], **slang['farewells']}
```

### 5. **DRY Principle**

Let the dictionary do the work, not the code:

```python
# ❌ BAD: Hard-coding every transformation
def transform(text):
    text = text.replace("hello", "hey")
    text = text.replace("Hello", "Hey")
    text = text.replace("HELLO", "HEY")
    # ... 100 more lines

# ✅ GOOD: Data-driven with case preservation
words = WordSubstitution({"hello": "hey"})
```

### 6. **SOLID Principles**

Each transformer has a **single responsibility**:

```python
# ✅ GOOD: Separate transformers
words = WordSubstitution(word_dict)
chars = CharacterSubstitution(char_dict)
phrases = PhraseConsolidation(phrase_dict)

# ❌ BAD: One giant transformer doing everything
```

---

## Pattern Reference

### When to Use Each Pattern

| Pattern | Use Case | Example |
|---------|----------|---------|
| **WordSubstitution** | Direct vocabulary changes | "hello" → "ahoy" |
| **CharacterSubstitution** | Accents, phonetics | "th" → "d" |
| **PhraseConsolidation** | Contractions, idioms | "going to" → "gonna" |
| **MorphologyTransformer** | Systematic grammar rules | "-ly" → "-wise" |
| **CompoundCreator** | Technical vocabulary | "person" → "party worker" |
| **SentenceAugmenter** | Verbal tics, emphasis | "." → ". Right on!" |
| **ConditionalReplacer** | Context-dependent logic | "[ao]ther" → varies |
| **character_translation** | 1-to-1 char mapping | "aeiou" → "43!0v" |

---

## Real-World Examples

### Example 1: Pirate Speak

```python
class PirateFilter:
    def __init__(self):
        self.filter = TextFilter("Pirate")

        # Words
        words = WordSubstitution({
            "hello": "ahoy",
            "hi": "ahoy",
            "friend": "matey",
            "friends": "crew",
            "yes": "aye",
            "no": "nay",
            "my": "me",
            "is": "be",
            "are": "be",
            "the": "th'",
            "you": "ye",
            "your": "yer"
        })
        self.filter.add_transformer(words)

        # Phrases
        phrases = PhraseConsolidation({
            "I am": "I be",
            "you are": "ye be"
        })
        self.filter.add_transformer(phrases)

        # Sentence endings
        augmenter = SentenceAugmenter()
        augmenter.add_punctuation_replacement(
            "!",
            [", arr!", ", me hearty!", ", ye scallywag!"],
            frequency=2
        )
        self.filter.add_transformer(augmenter)

    def transform(self, text):
        return self.filter.transform(text)
```

### Example 2: Corporate Jargon

```python
# corporate_jargon.json
{
  "words": {
    "problem": "challenge",
    "fired": "transitioned",
    "layoffs": "rightsizing",
    "idea": "thought leadership",
    "meeting": "sync",
    "talk": "touch base",
    "later": "going forward"
  },
  "phrases": {
    "talk about": "circle back on",
    "think about": "take offline",
    "I think": "in my humble opinion",
    "in the future": "going forward"
  }
}
```

### Example 3: Elizabethan English

```python
class ElizabethanFilter:
    def __init__(self):
        self.filter = TextFilter("Elizabethan")

        # Pronouns
        pronouns = WordSubstitution({
            "you": "thou",
            "your": "thy",
            "yours": "thine"
        })
        self.filter.add_transformer(pronouns)

        # Verb endings
        morph = MorphologyTransformer()
        # thou goest, thou makest
        morph.add_suffix_rule(r'(?<=thou\s\w{2,})s\b', 'est')
        self.filter.add_transformer(morph)
```

---

## Performance Tips

### 1. **Compile Once, Use Many Times**

```python
# ✅ GOOD: Reuse the same filter
filter = MyFilter()
for line in big_file:
    print(filter.transform(line))

# ❌ BAD: Creating new filter each time
for line in big_file:
    filter = MyFilter()  # Slow!
    print(filter.transform(line))
```

### 2. **Order Rules by Frequency**

Put the most common replacements first:

```python
words = WordSubstitution({
    "the": "da",      # Very common - check first
    "zephyr": "wind"  # Rare - check last
})
```

The library automatically sorts by length, but manual ordering can help within same-length groups.

### 3. **Avoid Overlapping Rules**

```python
# ❌ BAD: These overlap and cause double-replacement
{"going": "goin'", "going to": "gonna"}

# ✅ GOOD: Handle in correct order
phrases = PhraseConsolidation({"going to": "gonna"})
words = WordSubstitution({"going": "goin'"})
filter.add_transformer(phrases)  # First
filter.add_transformer(words)     # Second
```

---

## Testing Your Filter

### Basic Test Template

```python
def test_my_filter():
    filter = MyFilter()

    # Test case preservation
    assert filter.transform("Hello") == "Hey"
    assert filter.transform("HELLO") == "HEY"

    # Test word boundaries
    assert filter.transform("the theater") == "da theater"
    # Should NOT change "the" inside "theater"

    # Test phrases
    assert filter.transform("going to") == "gonna"

    # Test punctuation
    assert "!" in filter.transform("Great!")

    print("All tests passed!")

test_my_filter()
```

---

## Advanced Topics

### Custom Transformers

You can create your own transformer by implementing a `transform()` method:

```python
class CustomTransformer:
    def transform(self, text):
        # Your custom logic here
        return text.upper()

filter = TextFilter()
filter.add_transformer(CustomTransformer())
```

### Combining Filters

Chain multiple filters for complex effects:

```python
pirate = PirateFilter()
yelling = YellingFilter()

text = pirate.transform("Hello friend")
text = yelling.transform(text)  # AHOY MATEY!
```

### Stateful Transformations

Some filters need to track state (like counters):

```python
class StatefulFilter:
    def __init__(self):
        self.counter = 0

    def transform(self, text):
        self.counter += 1
        return f"[{self.counter}] {text}"
```

---

## Troubleshooting

### "My phrases aren't being matched!"

**Solution**: Make sure phrase consolidation comes BEFORE word substitution.

### "Capitalization is wrong"

**Solution**: Use `case_sensitive=False` in WordSubstitution and let it handle caps automatically.

### "Words are being replaced inside other words"

**Solution**: Use `word_boundary=True` (default) in WordSubstitution.

### "Some rules aren't applying"

**Solution**: Check the order! Later transformers might undo earlier ones.

---

## Contributing Your Filter

Want to share your filter?

1. Create a directory: `filters/my_filter/`
2. Include:
   - `my_filter.py` - The filter class
   - `slang_dict.json` - Your dictionary
   - `README.md` - Description and examples
   - `test_my_filter.py` - Basic tests
3. Submit a pull request!

---

## Resources

- **text_transformer.py** - Full API reference
- **disco_filter.py** - Complete working example
- **disco_slang.json** - Example dictionary structure
- Original TypeScript filters:
  - `src/nyc.ts` - Brooklyn accent
  - `src/klaus.ts` - German accent
  - `src/newspeak.ts` - Orwellian newspeak

---

## Quick Recipe: Creating a New Filter in 5 Minutes

1. **Copy the template**:
```bash
cp disco_filter.py my_filter.py
cp disco_slang.json my_slang.json
```

2. **Edit `my_slang.json`** with your vocabulary

3. **Update `my_filter.py`**:
   - Change class name
   - Update JSON path
   - Adjust transformation order if needed

4. **Test it**:
```bash
python my_filter.py "Test sentence here"
```

5. **Done!**

---

## Final Tips

1. **Start simple** - Begin with just word substitution, add complexity as needed
2. **Listen to real speech** - Authentic filters come from real observation
3. **Iterate** - Test with real text and refine
4. **Have fun!** - These filters are meant to be entertaining

Happy filtering! 🎉
