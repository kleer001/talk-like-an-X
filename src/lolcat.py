"""
LOLCAT Filter
=============

Converts text to LOLCAT speak with random capitalization and common substitutions.

License: GPL-2+
"""

import random
import re


def transform(text: str, seed: int = 42, **kwargs) -> str:
    """
    Transform text into LOLCAT speak.

    Combines vocabulary substitutions with random capitalization.

    Args:
        text: Input text to transform
        seed: Random seed for reproducibility (default: 42)
        **kwargs: Additional parameters (ignored)

    Returns:
        Text in LOLCAT style
    """
    rng = random.Random(seed)

    # Common LOLCAT substitutions
    substitutions = {
        'you': 'u',
        'your': 'ur',
        "you're": 'ur',
        'ok': 'k',
        'okay': 'k',
        'the': 'teh',
        'more': 'moar',
        'my': 'mah',
        'are': 'r',
        'what': 'wut',
        'cute': 'kyoot',
        'please': 'plz',
        'thanks': 'thx',
        'because': 'cuz',
        'love': 'luv',
        'oh': 'o',
        'to': '2',
        'too': '2',
        'for': '4',
    }

    # Apply substitutions (case-insensitive)
    result = text
    for old, new in substitutions.items():
        # Word boundary replacement
        pattern = re.compile(r'\b' + re.escape(old) + r'\b', re.IGNORECASE)
        result = pattern.sub(new, result)

    # Random capitalization on letters
    chars = []
    for char in result:
        if char.isalpha():
            if rng.random() < 0.3:  # 30% chance to uppercase
                chars.append(char.upper())
            else:
                chars.append(char.lower())
        else:
            chars.append(char)

    return ''.join(chars)
