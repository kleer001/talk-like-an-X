#!/usr/bin/env python3
"""
Check for redundancies and issues in cultural filter JSON files.
"""
import json
from pathlib import Path
from collections import Counter

src_dir = Path("/home/user/talk-like-an-X/src")
json_files = sorted(src_dir.glob("*_19*.json")) + sorted(src_dir.glob("*_20*.json"))

total_self_mappings = 0
total_duplicates = 0

for json_file in json_files:
    with open(json_file, 'r') as f:
        data = json.load(f)

    if 'substitutions' not in data:
        continue

    subs = data['substitutions']

    # Check for self-mappings
    self_mappings = [k for k, v in subs.items() if k == v]
    if self_mappings:
        print(f"\n{json_file.name}:")
        print(f"  Self-mappings found: {len(self_mappings)}")
        for sm in self_mappings[:5]:  # Show first 5
            print(f"    - '{sm}': '{subs[sm]}'")
        if len(self_mappings) > 5:
            print(f"    ... and {len(self_mappings) - 5} more")
        total_self_mappings += len(self_mappings)

    # Check for duplicate keys (shouldn't happen but worth checking)
    with open(json_file, 'r') as f:
        content = f.read()
        # Count occurrences of each key pattern
        for key in subs.keys():
            count = content.count(f'"{key}":')
            if count > 1:
                print(f"\n{json_file.name}:")
                print(f"  Duplicate key found: '{key}' appears {count} times")
                total_duplicates += 1

print(f"\n{'='*60}")
print(f"Total self-mappings found: {total_self_mappings}")
print(f"Total duplicate keys found: {total_duplicates}")

if total_self_mappings == 0 and total_duplicates == 0:
    print("✓ All filters are clean - no redundancies found!")
