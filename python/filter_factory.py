#!/usr/bin/env python3
"""
Universal Filter Factory
========================

Builds text transformation filters directly from JSON configuration files.
No need to write custom Python classes - just define your slang dictionary!

Usage:
    filter = FilterFactory.from_json('my_filter.json')
    result = filter.transform("Hello world")

Or from command line:
    ./filter_factory.py disco "Hello world"
    ./filter_factory.py disco.json "Hello world"  # .json is optional

Author: Universal filter builder
License: GPL
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List
from text_transformer import (
    TextFilter,
    Substitution,
    CharacterSubstitution,
    SuffixReplacer,
    PrefixReplacer,
    SentenceAugmenter,
    GlitchTransformer
)


class FilterFactory:
    """
    Builds TextFilter instances from JSON configuration.

    The JSON file defines all transformations - no Python code needed!
    """

    @staticmethod
    def from_json(json_path: str) -> TextFilter:
        """
        Load a filter from a JSON configuration file.

        Args:
            json_path: Path to JSON filter definition

        Returns:
            Configured TextFilter ready to use
        """
        with open(json_path, 'r') as f:
            config = json.load(f)

        return FilterFactory.from_dict(config)

    @staticmethod
    def from_dict(config: Dict[str, Any]) -> TextFilter:
        """
        Build a filter from a configuration dictionary.

        Supported keys:
            - name: Filter name (optional)
            - substitutions: Dict of word/phrase replacements
            - characters: Dict of character replacements
            - suffixes: Dict of suffix replacements
            - prefixes: Dict of prefix replacements
            - sentence_augmentation: List of punctuation augmentation rules
            - glitch: Int (percentage) or dict with 'percentage' and 'seed'
            - prefix_text: Text to add before output
            - suffix_text: Text to add after output
        """
        filter = TextFilter()

        # 1. Substitutions (words and phrases)
        # This is typically the main vocabulary
        if 'substitutions' in config:
            filter.add(Substitution(
                config['substitutions'],
                word_boundary=config.get('word_boundary', True),
                preserve_case=config.get('preserve_case', True)
            ))

        # 2. Character substitutions (for accents)
        if 'characters' in config:
            filter.add(CharacterSubstitution(
                config['characters'],
                preserve_case=config.get('preserve_case', True)
            ))

        # 3. Suffix replacements
        if 'suffixes' in config:
            suffix_replacer = SuffixReplacer()
            for suffix, replacement in config['suffixes'].items():
                # Support both simple dict and detailed config
                if isinstance(replacement, dict):
                    suffix_replacer.add_rule(
                        suffix,
                        replacement['replacement'],
                        min_stem=replacement.get('min_stem', 2)
                    )
                else:
                    suffix_replacer.add_rule(suffix, replacement)
            filter.add(suffix_replacer)

        # 4. Prefix replacements
        if 'prefixes' in config:
            prefix_replacer = PrefixReplacer()
            for prefix, replacement in config['prefixes'].items():
                prefix_replacer.add_rule(prefix, replacement)
            filter.add(prefix_replacer)

        # 5. Sentence augmentation (punctuation effects)
        if 'sentence_augmentation' in config:
            augmenter = SentenceAugmenter()
            for rule in config['sentence_augmentation']:
                augmenter.add_rule(
                    punctuation=rule['punctuation'],
                    additions=rule['additions'],
                    frequency=rule.get('frequency', 1)
                )
            filter.add(augmenter)

        # 6. Glitch effect (applied last to corrupt final output)
        if 'glitch' in config:
            glitch_config = config['glitch']
            if isinstance(glitch_config, dict):
                percentage = glitch_config.get('percentage', 100)
                seed = glitch_config.get('seed', 42)
            else:
                # If glitch is just a number, treat it as percentage
                percentage = int(glitch_config)
                seed = 42
            filter.add(GlitchTransformer(percentage=percentage, seed=seed))

        # 7. Prefix/suffix text
        if 'prefix_text' in config:
            filter.set_prefix(config['prefix_text'])
        if 'suffix_text' in config:
            filter.set_suffix(config['suffix_text'])

        return filter


def find_filter_file(filter_name: str) -> Path:
    """
    Find a filter JSON file by name.

    Searches in:
    1. Current directory
    2. Same directory as this script
    3. Accepts name with or without .json extension

    Args:
        filter_name: Filter name (e.g., 'disco' or 'disco.json')

    Returns:
        Path to the filter file

    Raises:
        FileNotFoundError: If filter file cannot be found
    """
    # Add .json extension if not present
    if not filter_name.endswith('.json'):
        filter_name = filter_name + '.json'

    # Search locations
    search_paths = [
        Path.cwd() / filter_name,                    # Current directory
        Path(__file__).parent / filter_name,         # Script directory
    ]

    for path in search_paths:
        if path.exists():
            return path

    # Not found - provide helpful error
    raise FileNotFoundError(
        f"Filter '{filter_name}' not found. Searched:\n" +
        "\n".join(f"  - {p}" for p in search_paths)
    )


def main():
    """Command-line interface for using any JSON filter."""
    if len(sys.argv) < 2:
        print("Usage: ./filter_factory.py FILTER [TEXT]")
        print("\nExamples:")
        print("  ./filter_factory.py disco 'Hello friend'")
        print("  ./filter_factory.py pirate 'Hello friend'")
        print("  echo 'Hello world' | ./filter_factory.py disco")
        print("  ./filter_factory.py disco < input.txt")
        print("\nNote: .json extension is optional")
        sys.exit(1)

    filter_name = sys.argv[1]

    # Find and load the filter
    try:
        json_file = find_filter_file(filter_name)
        filter = FilterFactory.from_json(str(json_file))
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filter_name}': {e}")
        sys.exit(1)

    # Get input text
    if len(sys.argv) > 2:
        # From command line arguments
        input_text = ' '.join(sys.argv[2:])
    elif not sys.stdin.isatty():
        # From stdin (pipe or redirect)
        input_text = sys.stdin.read()
    else:
        # Interactive mode
        print("Enter text to transform (Ctrl+D when done):")
        input_text = sys.stdin.read()

    # Transform and output
    output = filter.transform(input_text)
    print(output)


if __name__ == "__main__":
    main()
