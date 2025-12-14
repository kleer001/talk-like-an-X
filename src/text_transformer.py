"""
Text Transformation Library
===========================

A generalized library for creating fun language-mangling text filters.
Based on analysis of nyc.ts, klaus.ts, and newspeak.ts filters.

Author: Generated from TypeScript filter analysis
License: GPL (matching original filters)
"""

import re
from typing import Callable, List, Tuple, Dict, Protocol


# ============================================================================
# SOLID: Define transformer protocol (Interface Segregation)
# ============================================================================

class Transformer(Protocol):
    """Protocol that all transformers must implement."""
    def transform(self, text: str) -> str:
        """Transform input text and return modified text."""
        ...


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def same_cap(original: str, replacement: str) -> str:
    """
    Preserve the capitalization pattern of the original text.

    Examples:
        same_cap("Hello", "goodbye") -> "Goodbye"
        same_cap("HELLO", "goodbye") -> "GOODBYE"
        same_cap("hello", "goodbye") -> "goodbye"
    """
    if not original or not replacement:
        return replacement

    if original.isupper():
        return replacement.upper()
    elif original[0].isupper():
        return replacement[0].upper() + replacement[1:]
    else:
        return replacement[0].lower() + replacement[1:]


def same_cap_replacer(replacement: str) -> Callable[[re.Match], str]:
    """Create a replacer function that preserves capitalization."""
    def replacer(match: re.Match) -> str:
        return same_cap(match.group(0), replacement)
    return replacer


# ============================================================================
# BASE TRANSFORMER (DRY: Common pattern compilation logic)
# ============================================================================

class RegexTransformer:
    """
    Base class for regex-based transformers.
    DRY: Consolidates common regex compilation and application logic.
    """

    def __init__(self):
        self.rules: List[Tuple[re.Pattern, Callable[[re.Match], str]]] = []

    def _add_rule(self, pattern: str, replacer: Callable[[re.Match], str],
                  flags: int = 0):
        """Add a compiled regex rule."""
        self.rules.append((re.compile(pattern, flags), replacer))

    def transform(self, text: str) -> str:
        """Apply all rules in sequence."""
        for pattern, replacer in self.rules:
            text = pattern.sub(replacer, text)
        return text


# ============================================================================
# PATTERN 1 & 3: WORD AND PHRASE SUBSTITUTION
# Single class handles both - YAGNI (don't need separate classes)
# ============================================================================

class Substitution(RegexTransformer):
    """
    Replace words and phrases with alternatives.
    Handles both single words and multi-word phrases.
    Preserves capitalization by default.
    """

    def __init__(self, mappings: Dict[str, str],
                 word_boundary: bool = True,
                 preserve_case: bool = True):
        """
        Args:
            mappings: {original: replacement} dictionary
            word_boundary: Match complete words only
            preserve_case: Maintain original capitalization
        """
        super().__init__()
        self._compile_mappings(mappings, word_boundary, preserve_case)

    def _compile_mappings(self, mappings: Dict[str, str],
                         word_boundary: bool, preserve_case: bool):
        """Compile all mappings into regex rules (DRY)."""
        # Sort by length (longest first) to match phrases before words
        sorted_items = sorted(mappings.items(), key=lambda x: len(x[0]), reverse=True)

        for original, replacement in sorted_items:
            # Build pattern with flexible whitespace for phrases
            if ' ' in original:
                # Multi-word phrase: "going to" -> "going\s+to"
                pattern = r'\s+'.join(re.escape(word) for word in original.split())
            else:
                # Single word
                pattern = re.escape(original)

            # Add word boundaries if requested
            if word_boundary:
                pattern = r'\b' + pattern + r'\b'

            # Create replacer function
            flags = re.IGNORECASE if preserve_case else 0
            if preserve_case:
                replacer = same_cap_replacer(replacement)
            else:
                replacer = lambda m, r=replacement: r

            self._add_rule(pattern, replacer, flags)


# ============================================================================
# PATTERN 2: CHARACTER SUBSTITUTION
# ============================================================================

class CharacterSubstitution(RegexTransformer):
    """
    Replace character pairs and single characters.
    Useful for creating accents (v->f, th->d, etc.)
    """

    def __init__(self, mappings: Dict[str, str],
                 preserve_case: bool = True):
        """
        Args:
            mappings: {original: replacement} character/pair mappings
            preserve_case: Maintain original capitalization
        """
        super().__init__()
        # Sort by length (longest first) to match pairs before singles
        sorted_items = sorted(mappings.items(), key=lambda x: len(x[0]), reverse=True)

        for original, replacement in sorted_items:
            pattern = re.escape(original)
            flags = re.IGNORECASE if preserve_case else 0

            if preserve_case:
                replacer = same_cap_replacer(replacement)
            else:
                replacer = lambda m, r=replacement: r

            self._add_rule(pattern, replacer, flags)


# ============================================================================
# PATTERN 4: SUFFIX/PREFIX TRANSFORMATIONS
# ============================================================================

class SuffixReplacer(RegexTransformer):
    """Replace word suffixes (e.g., -ing -> -in', -ly -> -wise)."""

    def add_rule(self, suffix: str, replacement: str, min_stem: int = 2):
        """
        Add a suffix replacement rule.

        Args:
            suffix: The suffix pattern to match (e.g., 'ing')
            replacement: What to replace it with (e.g., "in'")
            min_stem: Minimum stem length before suffix
        """
        pattern = rf'([a-zA-Z]{{{min_stem},}})' + re.escape(suffix) + r'\b'
        replacer = lambda m, r=replacement: m.group(1) + r
        self._add_rule(pattern, replacer, re.IGNORECASE)


class PrefixReplacer(RegexTransformer):
    """Replace word prefixes (e.g., un- -> not-)."""

    def add_rule(self, prefix: str, replacement: str):
        """
        Add a prefix replacement rule.

        Args:
            prefix: The prefix to match (e.g., 'un')
            replacement: What to replace it with
        """
        pattern = r'\b' + re.escape(prefix) + r'([a-zA-Z]+)'
        replacer = lambda m, r=replacement: r + m.group(1)
        self._add_rule(pattern, replacer, re.IGNORECASE)


# ============================================================================
# PATTERN 9: SENTENCE AUGMENTATION
# ============================================================================

class SentenceAugmenter:
    """
    Add phrases at sentence boundaries (punctuation).
    Example: "." -> ". Right on!" every N sentences.
    """

    def __init__(self):
        self.rules: List[Tuple[str, List[str], int]] = []
        self._counters: Dict[str, int] = {}

    def add_rule(self, punctuation: str, additions: List[str], frequency: int = 1):
        """
        Add punctuation augmentation rule.

        Args:
            punctuation: Punctuation mark to augment
            additions: List of phrases to add (cycles through them)
            frequency: 1=always, 2=every other, 3=every third, etc.
        """
        self.rules.append((punctuation, additions, frequency))
        if frequency > 1:
            self._counters[punctuation] = 0

    def transform(self, text: str) -> str:
        """Apply all augmentation rules."""
        for punct, additions, freq in self.rules:
            if freq == 1:
                # Always add (cycle through additions)
                parts = text.split(punct)
                result = []
                for i, part in enumerate(parts[:-1]):
                    result.append(part + punct + additions[i % len(additions)])
                result.append(parts[-1])
                text = ''.join(result)
            else:
                # Add every Nth occurrence
                parts = text.split(punct)
                result = []
                counter = self._counters.get(punct, 0)

                for i, part in enumerate(parts[:-1]):
                    result.append(part + punct)
                    if counter % freq == 0:
                        result.append(additions[counter % len(additions)])
                    counter += 1

                result.append(parts[-1])
                text = ''.join(result)
                self._counters[punct] = counter

        return text


# ============================================================================
# PATTERN 10: CHARACTER TRANSLATION
# ============================================================================

def character_translation(text: str, from_chars: str, to_chars: str) -> str:
    """
    Character-by-character translation (like Perl's tr///).

    Example:
        character_translation("hello", "helo", "w3l0") -> "w3ll0"
    """
    return text.translate(str.maketrans(from_chars, to_chars))


# ============================================================================
# PATTERN 11: GLITCH TRANSFORMER (ALGORITHMIC)
# ============================================================================

class GlitchTransformer:
    """
    Replace characters with Unicode blocks/shapes based on probability.
    Simulates computer glitch/corruption effects.

    Example:
        glitch = GlitchTransformer(percentage=50)
        glitch.transform("Hello")  # "H▓l█o" or similar
    """

    # Unicode block/shape characters for glitch effect
    GLITCH_CHARS = [
        '█', '▓', '▒', '░', '▀', '▄', '▌', '▐', '■', '□',
        '▪', '▫', '▬', '▭', '▮', '▯', '▰', '▱', '▲', '△',
        '▴', '▵', '▶', '▷', '▸', '▹', '►', '▻', '▼', '▽',
        '▾', '▿', '◀', '◁', '◂', '◃', '◄', '◅', '◆', '◇',
        '◈', '◉', '◊', '○', '◌', '◍', '◎', '●', '◐', '◑',
        '◒', '◓', '◔', '◕', '◖', '◗', '◘', '◙', '◚', '◛',
    ]

    def __init__(self, percentage: int = 100, seed: int = 42):
        """
        Args:
            percentage: Percentage of letters to glitch (0-100)
            seed: Random seed for reproducible results
        """
        self.percentage = percentage
        import random
        self.random = random.Random(seed)

    def transform(self, text: str) -> str:
        """Apply glitch effect to text."""
        result = []
        for char in text:
            # Only glitch letters and numbers
            if char.isalnum() and self.random.randint(1, 100) <= self.percentage:
                result.append(self.random.choice(self.GLITCH_CHARS))
            else:
                result.append(char)
        return ''.join(result)


# ============================================================================
# MAIN FILTER ENGINE
# ============================================================================

class TextFilter:
    """
    Main transformation engine that applies multiple transformers in sequence.

    Example:
        filter = TextFilter()
        filter.add(Substitution({"hello": "hey"}))
        filter.add(CharacterSubstitution({"th": "d"}))
        result = filter.transform("Hello the theater")
    """

    def __init__(self):
        self.transformers: List[Transformer] = []
        self.prefix: str = ""
        self.suffix: str = ""

    def add(self, transformer: Transformer):
        """Add a transformer to the pipeline."""
        self.transformers.append(transformer)

    def set_prefix(self, prefix: str):
        """Add text before the output."""
        self.prefix = prefix

    def set_suffix(self, suffix: str):
        """Add text after the output."""
        self.suffix = suffix

    def transform(self, text: str) -> str:
        """Apply all transformers in sequence."""
        result = text
        for transformer in self.transformers:
            result = transformer.transform(result)
        return self.prefix + result + self.suffix


# ============================================================================
# CONVENIENCE: All-in-one simple filter
# ============================================================================

def simple_filter(word_map: Dict[str, str]) -> TextFilter:
    """
    Quick helper to create a basic word-substitution filter.

    Example:
        filter = simple_filter({"hello": "hey", "bye": "later"})
        filter.transform("Hello and bye")  # "Hey and later"
    """
    f = TextFilter()
    f.add(Substitution(word_map))
    return f


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Quick demo
    filter = TextFilter()

    # Add word/phrase substitutions
    filter.add(Substitution({
        "going to": "gonna",    # Phrase
        "hello": "yo",          # Word
        "the": "da"             # Word
    }))

    # Add character substitutions
    chars = CharacterSubstitution({"th": "d"})
    filter.add(chars)

    # Add suffix changes
    suffix = SuffixReplacer()
    suffix.add_rule("ing", "in'")
    filter.add(suffix)

    # Test
    text = "Hello! I am going to the theater and singing"
    result = filter.transform(text)
    print(f"Original: {text}")
    print(f"Result:   {result}")
    # "Yo! I am gonna da deater and singin'"
