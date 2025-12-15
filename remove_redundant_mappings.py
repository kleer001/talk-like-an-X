#!/usr/bin/env python3
import json
from pathlib import Path

src_dir = Path("/home/user/talk-like-an-X/src")

# Get all JSON files
json_files = sorted(src_dir.glob("*.json"))

total_removed = 0

for json_file in json_files:
    with open(json_file, 'r') as f:
        data = json.load(f)

    if 'substitutions' not in data:
        continue

    original_count = len(data['substitutions'])

    # Remove self-mappings
    data['substitutions'] = {
        key: value
        for key, value in data['substitutions'].items()
        if key != value
    }

    new_count = len(data['substitutions'])
    removed = original_count - new_count

    if removed > 0:
        print(f"{json_file.name}: removed {removed} self-mappings")
        total_removed += removed

        # Write back with nice formatting
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')

print(f"\nTotal self-mappings removed: {total_removed}")
