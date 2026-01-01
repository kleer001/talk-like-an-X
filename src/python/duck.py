"""
Duck Filter
===========

Replaces all words with variations of "quack" based on word length.

Author: Aaron Wells (2023)
License: Public domain
"""


def transform(text: str, **kwargs) -> str:
    """
    Transform text into duck speech.

    Short words (≤3 chars) become "qua"
    Medium words (4-9 chars) become "quack"
    Long words (≥10 chars) become "quackquack"

    Args:
        text: Input text to transform
        **kwargs: Unused, for compatibility

    Returns:
        Duck-ified text with preserved capitalization
    """
    import re

    def same_cap(original: str, replacement: str) -> str:
        """Preserve capitalization pattern from original."""
        if not original:
            return replacement

        if original.isupper():
            return replacement.upper()
        elif original[0].isupper():
            return replacement.capitalize()
        else:
            return replacement.lower()

    def duck_word(match):
        word = match.group(0)
        length = len(word)

        if length <= 3:
            duck = 'qua'
        elif length >= 10:
            duck = 'quackquack'
        else:
            duck = 'quack'

        return same_cap(word, duck)

    return re.sub(r'[a-zA-Z]+', duck_word, text)
