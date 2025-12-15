#!/usr/bin/env python3
import json
import glob
from pathlib import Path

culture_filters = [
    "beatnik_1950s",
    "club_kids_1980s",
    "disco",
    "flappers_1920s",
    "goths_1980s",
    "greasers_1950s",
    "grunge_musicians_1990s",
    "hackers_1990s",
    "hip_hop_breakers_1980s",
    "hippies_1960s",
    "ibm_engineers_1950s",
    "metalheads_1970s",
    "mid_century_modern_1960s",
    "mods_1960s",
    "new_romantic_goth_1980s",
    "outlaw_bikers_1960s",
    "punk_rockers_1970s",
    "rastafarians_1970s",
    "ravers_1980s",
    "riot_grrrl_1990s",
    "skinheads_1960s",
    "slackers_1990s",
    "surfers_1960s",
    "teddy_boys_1950s",
    "yuppies_1980s",
    "zoot_suiters_1940s"
]

all_words = set()

src_dir = Path("/home/user/talk-like-an-X/src")

for filter_name in culture_filters:
    filter_path = src_dir / f"{filter_name}.json"
    if filter_path.exists():
        with open(filter_path, 'r') as f:
            data = json.load(f)
            if 'substitutions' in data:
                all_words.update(data['substitutions'].keys())

unique_sorted = sorted(all_words, key=str.lower)

output_path = Path("/home/user/talk-like-an-X/20th_century_culture_master_wordlist.txt")
with open(output_path, 'w') as f:
    for word in unique_sorted:
        f.write(f"{word}\n")

print(f"Compiled {len(unique_sorted)} unique words and phrases")
print(f"Output written to: {output_path}")
