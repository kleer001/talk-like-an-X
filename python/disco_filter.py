#!/usr/bin/env python3
"""
1970s Disco Enthusiast Filter
==============================

Transforms ordinary English into the far-out language of a 1970s disco enthusiast.

Usage:
    python disco_filter.py "Hello friend, how are you doing today?"

Author: Demo implementation
License: GPL
"""

import json
import sys
import os
from text_transformer import TextFilter, Substitution, SuffixReplacer, SentenceAugmenter


class DiscoFilter:
    """
    Transforms text into 1970s disco slang.

    This demonstrates the recommended pattern:
    1. Load slang dictionary from JSON
    2. Configure transformers with the library
    3. Apply in correct order (phrases -> words -> characters -> suffixes -> augmentation)
    """

    def __init__(self, slang_dict_path: str = None):
        """Initialize with path to slang dictionary JSON file."""
        if slang_dict_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            slang_dict_path = os.path.join(script_dir, 'disco_slang.json')

        with open(slang_dict_path, 'r') as f:
            self.slang = json.load(f)

        self.filter = self._build_filter()

    def _build_filter(self) -> TextFilter:
        """
        Build transformation pipeline.
        Order: phrases -> exclamations -> words -> suffixes -> augmentation
        """
        filter = TextFilter()

        # 1. Phrases (most specific - must come first)
        all_mappings = {}
        if 'phrases' in self.slang:
            all_mappings.update(self.slang['phrases'])

        # 2. Exclamations (before general words)
        if 'exclamations' in self.slang:
            all_mappings.update(self.slang['exclamations'])

        # 3. Words (main dictionary)
        if 'words' in self.slang:
            all_mappings.update(self.slang['words'])

        # Add all substitutions at once (library handles sorting by length)
        filter.add(Substitution(all_mappings))

        # 4. Suffixes
        if 'affixes' in self.slang and 'suffixes' in self.slang['affixes']:
            suffix = SuffixReplacer()
            for suffix_pattern, replacement in self.slang['affixes']['suffixes'].items():
                suffix.add_rule(suffix_pattern, replacement)
            filter.add(suffix)

        # 5. Sentence augmentation (last)
        if 'sentence_fillers' in self.slang:
            augmenter = SentenceAugmenter()
            augmenter.add_rule('.', self.slang['sentence_fillers'], frequency=3)
            filter.add(augmenter)

        return filter

    def transform(self, text: str) -> str:
        """Transform text into disco speak."""
        return self.filter.transform(text)


def main():
    """Command-line interface."""
    if len(sys.argv) > 1:
        input_text = ' '.join(sys.argv[1:])
    else:
        if not sys.stdin.isatty():
            input_text = sys.stdin.read()
        else:
            # Demo text
            input_text = """
Hello friend! How are you doing today? I hope you're having a great time.
This party is really amazing. The music is very good and everyone is dancing.
I think we should leave soon and go get some food. Do you understand what I'm saying?
That would be excellent! Let's go right now.
"""

    disco = DiscoFilter()
    print(disco.transform(input_text))


if __name__ == "__main__":
    main()
