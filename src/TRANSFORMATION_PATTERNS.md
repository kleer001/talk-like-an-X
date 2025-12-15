# Text Transformation Patterns Analysis

## Executive Summary

After analyzing `nyc.ts`, `klaus.ts`, and `newspeak.ts`, we identified **10 high-level transformation patterns** that these filters use to modify text. This document describes each pattern at a conceptual level.

---

## The 10 Core Patterns

### 1. Simple Word/Phrase Substitution

**What it does**: Direct 1-to-1 replacement of words or phrases with alternatives.

**Examples**:
- klaus: "the" → "ze", "Yes" → "Jawohl", "with" → "mitt"
- newspeak: "bad" → "ungood", "God" → "Big Brother"
- nyc: "you" → "yuh", "with" → "wit'"

**Use case**: The backbone of most filters. Vocabulary replacement.

**Implementation note**: Must handle word boundaries to avoid replacing "the" inside "theater".

---

### 2. Character/Letter Pair Replacement

**What it does**: Substitutes individual characters or character sequences.

**Examples**:
- klaus: "v" → "f", "w" → "v", "th" → "d", "sh" → "sch"
- nyc: "er" → "uh" (at word end), "ing" → "in'"

**Use case**: Creating phonetic accents, speech impediments, stylistic effects.

**Implementation note**: Order matters - match longer sequences before shorter ones.

---

### 3. Multi-Word Phrase Consolidation

**What it does**: Collapses multi-word phrases into single words or contractions.

**Examples**:
- nyc: "I'm going to" → "I'manna", "going to" → "gonna", "want to" → "wanna"
- nyc: "did you" → "d'ja", "how are you" → "howahrya"
- newspeak: "kind of" → "plus", "more than a little" → "plus"

**Use case**: Colloquial speech, casual language, dialect effects.

**Implementation note**: Must be applied BEFORE single-word substitution to prevent breaking up phrases.

---

### 4. Suffix/Prefix Morphology

**What it does**: Systematically transforms word endings or beginnings according to linguistic rules.

**Examples**:
- newspeak: "-less" → "un-ful" (harmless → unharmful)
- newspeak: "-ly" → "-wise" (quickly → quickwise)
- newspeak: "-ous" → "-ful" (dangerous → dangerful)
- newspeak: "not the X" → "the unX"
- newspeak: "anti-" → "un-"

**Use case**: Creating systematic grammatical transformations, constructed languages.

**Implementation note**: Powerful for creating consistent linguistic rules across all words.

---

### 5. Compound Word Creation

**What it does**: Merges words or concepts into compound forms.

**Examples**:
- newspeak: "person" → "party worker"
- newspeak: "family" → "family unit"
- newspeak: "research" → "crimethink"
- newspeak: "faith" → "bellyfeel"

**Use case**: Technical jargon, political doublespeak, specialized vocabularies.

**Implementation note**: Creates the effect of a specialized or restricted vocabulary.

---

### 6. Context-Aware Boundary Detection

**What it does**: Applies transformations only when specific conditions are met (word boundaries, position in word, surrounding context).

**Examples**:
- All filters: Only match "the" as a complete word, not in "theater"
- nyc: "ing" → "in'" only at word end, not in "finger" → "fin'ger"
- newspeak: Patterns only match with specific whitespace/punctuation around them

**Use case**: Preventing over-eager replacements, maintaining word integrity.

**Implementation note**: Essential for realistic transformations. Uses regex lookahead/lookbehind and word boundary markers.

---

### 7. Case Preservation

**What it does**: Maintains the original capitalization pattern when replacing text.

**Examples**:
- "Hello" → "Hey" (preserve initial cap)
- "HELLO" → "HEY" (preserve all caps)
- "hello" → "hey" (preserve lowercase)

**Use case**: Making transformations look natural in running text.

**Implementation note**: All three TypeScript filters use a `sameCap()` utility function for this.

---

### 8. Conditional/Pattern-Based Substitution

**What it does**: Chooses replacement based on the actual content matched, not just a fixed string.

**Examples**:
- nyc: "[ao]ther" checks the first letter:
  - "other" → "udder"
  - "aother" → "adder"
- klaus: Name substitutions based on pattern matching
  - "John" → "Johann"
  - "William" → "Wilhelm"

**Use case**: Context-dependent transformations where the replacement depends on what was matched.

**Implementation note**: Uses callback functions instead of simple string replacements.

---

### 9. Punctuation/Sentence Augmentation

**What it does**: Adds phrases or modifies text at sentence boundaries (punctuation marks).

**Examples**:
- nyc: "!" → "! Okay?"
- nyc: "?" → ", or what?"
- nyc: "." → periodically adds expletives ("Okay?", "Right?", "Ya' dig?")
- newspeak: End of quoted sentences get "Hail Big Brother!"

**Use case**: Adding verbal tics, emphasis, catchphrases, dialect markers.

**Implementation note**: Often uses counters to add phrases periodically rather than every time.

---

### 10. Character Translation Tables

**What it does**: One-to-one character mapping across the entire text.

**Examples**:
- lib.ts provides `tr()` function (like Perl's tr///)
- Could map "aeiou" → "43!0v" for leetspeak
- Could map accented characters to plain ASCII

**Use case**: Character set conversions, simple ciphers, accent mark handling.

**Implementation note**: Available but not heavily used in the analyzed filters. Useful for preprocessing.

---

## Pattern Application Order

For realistic results, patterns should generally be applied in this order:

1. **Multi-word phrases** (most specific)
2. **Conditional replacements** (context-dependent)
3. **Single word substitution** (main dictionary)
4. **Character substitution** (accents, phonetics)
5. **Suffix/prefix morphology** (systematic rules)
6. **Sentence augmentation** (punctuation effects, should be last)

**Why order matters**: If you replace "going" before consolidating "going to", you'll never match the phrase.

---

## Common Utilities

All three TypeScript filters share these utility patterns:

### sameCap(match, replacement)
Preserves the capitalization pattern of the original text.

### simuLex(text, rules)
Simulates a lexical scanner - tests rules in order, applies the longest match.

### Regex with word boundaries
Uses `{W}` (whitespace), `{EW}` (end-of-word) patterns extensively.

---

## Design Philosophy

The key insight from these filters:

> **Most text transformations are combinations of a small set of patterns.**

Rather than writing custom logic for each transformation, identify which pattern(s) apply and use the appropriate tools. This makes filters:

- **Easier to create** (mix and match patterns)
- **Easier to maintain** (patterns are reusable)
- **More consistent** (same pattern behaves the same way everywhere)
- **Data-driven** (transformations in JSON, not code)

---

## Real-World Pattern Usage

### NYC Filter (Brooklyn Accent)
- **Primary patterns**: Word substitution, character substitution, phrase consolidation
- **Key technique**: Conditional replacements for vowel sounds
- **Special feature**: Periodic sentence augmentation with expletives

### Klaus Filter (German Accent)
- **Primary patterns**: Character substitution, word substitution
- **Key technique**: Systematic consonant replacements (v→f, w→v, th→d)
- **Special feature**: Name substitutions with pattern matching

### Newspeak Filter (Orwellian Language)
- **Primary patterns**: Word substitution, compound creation, morphology
- **Key technique**: Systematic suffix transformations (-ly→-wise, -less→un-ful)
- **Special feature**: Complex negation handling ("not the X" → "the unX")

---

## Conclusion

These 10 patterns provide a complete toolkit for creating text transformation filters. By understanding and combining them appropriately, you can create convincing dialects, accents, slang filters, and constructed languages.

The Python library (`text_transformer.py`) implements all these patterns in a clean, reusable way following SOLID principles.
