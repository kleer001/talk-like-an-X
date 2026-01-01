"""
Glitch Filter
=============

Corrupts text by replacing characters with Unicode blocks and shapes.

License: GPL
"""

import random


def transform(text: str, percentage: int = 100, seed: int = 42, **kwargs) -> str:
    """
    Apply glitch effect by replacing characters with Unicode blocks.

    Args:
        text: Input text to corrupt
        percentage: Percentage of characters to corrupt (0-100)
        seed: Random seed for reproducibility (default: 42)
        **kwargs: Additional parameters (ignored)

    Returns:
        Corrupted text with Unicode glitch characters
    """
    # Unicode blocks and shapes for glitch effect
    GLITCH_CHARS = [
        '█', '▓', '▒', '░', '▀', '▄', '▌', '▐', '■', '□',
        '▪', '▫', '▬', '▭', '▮', '▯', '▰', '▱', '▲', '△',
        '▴', '▵', '▶', '▷', '▸', '▹', '►', '▻', '▼', '▽',
        '▾', '▿', '◀', '◁', '◂', '◃', '◄', '◅', '◆', '◇',
        '◈', '◉', '◊', '○', '◌', '◍', '◎', '●', '◐', '◑',
        '◒', '◓', '◔', '◕', '◖', '◗', '◘', '◙', '◚', '◛',
        '◜', '◝', '◞', '◟', '◠', '◡', '◢', '◣', '◤', '◥',
        '◦', '◧', '◨', '◩', '◪', '◫', '◬', '◭', '◮', '◯',
    ]

    rng = random.Random(seed)
    result = []

    for char in text:
        # Only corrupt alphanumeric characters
        if char.isalnum():
            # Determine if this character should be corrupted
            if rng.randint(1, 100) <= percentage:
                result.append(rng.choice(GLITCH_CHARS))
            else:
                result.append(char)
        else:
            # Preserve punctuation and whitespace
            result.append(char)

    return ''.join(result)
