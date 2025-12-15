#!/usr/bin/env python3
"""
Fix duplicate keys in JSON files by removing earlier occurrences.
Python's json.load() keeps the last occurrence, so we'll do the same.
"""
import json
from pathlib import Path

src_dir = Path("/home/user/talk-like-an-X/src")
json_files = sorted(src_dir.glob("*_19*.json")) + sorted(src_dir.glob("*_20*.json"))

for json_file in json_files:
    # Load the JSON (this will keep only the last occurrence of duplicate keys)
    with open(json_file, 'r') as f:
        data = json.load(f)

    if 'substitutions' not in data:
        continue

    # Count original entries by parsing the raw file
    with open(json_file, 'r') as f:
        content = f.read()

    original_count = content.count('":')
    final_count = len(data.get('substitutions', {}))

    if original_count != final_count:
        duplicates_removed = original_count - final_count
        print(f"{json_file.name}: removed {duplicates_removed} duplicate key(s)")

        # Write back the cleaned version
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')

print("\nDuplicate cleanup complete!")
