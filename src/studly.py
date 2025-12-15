"""
Studly Caps Filter
==================

Randomly capitalizes letters to create "StUdLy CaPs" effect.

Author: Nick Phillips (original)
License: GPL-2+
"""

import random


def transform(text: str, seed: int = 42, **kwargs) -> str:
    """
    Transform text with random capitalization (studly caps).

    Args:
        text: Input text to transform
        seed: Random seed for reproducibility (default: 42)
        **kwargs: Additional parameters (ignored)

    Returns:
        Text with StUdLy CaPiTaLiZaTiOn
    """
    rng = random.Random(seed)
    result = []

    for char in text:
        if char.isalpha():
            # Randomly capitalize or lowercase
            if rng.random() < 0.5:
                result.append(char.upper())
            else:
                result.append(char.lower())
        else:
            result.append(char)

    return ''.join(result)
