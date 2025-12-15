#!/usr/bin/env python3
"""
Enhance cultural filters with authentic slang from historical sources.
Based on research from authentic dictionaries, historical documents, and multiple sources.
"""
import json
from pathlib import Path

# Authentic vocabulary additions based on research from multiple historical sources
ENHANCEMENTS = {
    "hippies_1960s.json": {
        "policeman": "pig",
        "establishment person": "straight",
        "authentic": "together",
        "inauthentic": "plastic",
        "experience": "trip",
        "impressive": "heavy",
        "marijuana": "weed",
        "smoke marijuana": "blow grass",
        "hallucinogenic": "mind-bending",
        "confuse": "blow my mind",
        "excellent music": "outta sight",
        "party hard": "get down",
        "improvise music": "jam",
        "understand deeply": "grok",
        "political activist": "activist",
        "demonstration": "be-in",
        "communal living": "crash pad",
        "boyfriend": "old man",
        "girlfriend": "old lady",
        "enthusiastic": "turned on",
        "depressing": "bring down"
    },

    "hip_hop_breakers_1980s.json": {
        "steal moves": "bite",
        "dance battle": "throwdown",
        "challenge": "call out",
        "impressive move": "sick move",
        "spin on head": "headspin",
        "freeze move": "freeze",
        "floor work": "downrock",
        "standing moves": "toprock",
        "difficult move": "power move",
        "dance circle": "cypher",
        "female breaker": "b-girl",
        "experienced dancer": "veteran",
        "novice": "toy"
    },

    "surfers_1960s.json": {
        "non-surfer": "hodad",
        "inexperienced surfer": "gremmie",
        "longboard": "log",
        "wipe out": "eat it",
        "surfboard nose": "nose",
        "surfboard tail": "tail",
        "surf wax": "wax",
        "perfect wave": "glassy",
        "big wave": "bombing",
        "ride inside wave": "get tubed",
        "skilled surfer": "soul surfer"
    },

    "metalheads_1970s.json": {
        "headbang": "bang",
        "fake fan": "poseur",
        "sell out": "go commercial",
        "mosh pit": "pit",
        "guitar": "axe",
        "guitar solo": "shredding",
        "loud": "cranked",
        "turn up volume": "crank it",
        "concert": "gig",
        "roadie": "crew"
    },

    "ravers_1980s.json": {
        "ecstasy pill": "E",
        "loved up": "loved up",
        "warehouse party": "warehouse do",
        "dance all night": "rave",
        "dj": "selector",
        "good music": "banging tunes",
        "dance floor": "floor",
        "glow stick": "glowstick",
        "water": "agua"
    },

    "riot_grrrl_1990s.json": {
        "patriarchy": "the man",
        "feminist": "riot grrrl",
        "empowered": "fierce",
        "sisterhood": "solidarity",
        "zine": "zine",
        "do it yourself": "DIY",
        "sexist man": "pig",
        "male ally": "ally",
        "speak out": "shout",
        "resist": "fight back"
    },

    "skinheads_1960s.json": {
        "boots": "bovver boots",
        "fight": "bovver",
        "troublemaker": "bovver boy",
        "female skinhead": "skin girl",
        "scooter": "scoot",
        "youth": "youth",
        "sharp dressed": "smartly dressed"
    },

    "teddy_boys_1950s.json": {
        "teddy boy": "Ted",
        "teddy girl": "Judy",
        "gang": "mob",
        "territory": "manor",
        "edwardian style": "Edwardian",
        "brothel creeper shoes": "creepers",
        "drape jacket": "drape",
        "duck's arse hair": "DA",
        "gang fight": "rumble"
    },

    "mods_1960s.json": {
        "scooter rider": "scooterist",
        "vespa": "Vespa",
        "lambretta": "Lambretta",
        "parka jacket": "parka",
        "amphetamine": "purple hearts",
        "all night party": "all-nighter",
        "northern soul": "northern soul",
        "enemy": "rocker",
        "beach fight": "bank holiday riot"
    },

    "punk_rockers_1970s.json": {
        "safety pin": "pin",
        "mohawk": "mohican",
        "spike hair": "liberty spikes",
        "leather jacket": "jacket",
        "studded belt": "belt",
        "slam dance": "pogo",
        "spit": "gob",
        "anarchist": "anarcho",
        "do it yourself": "DIY",
        "independent": "indie"
    },

    "grunge_musicians_1990s.json": {
        "flannel shirt": "flannel",
        "corporate music": "mainstream",
        "authentic": "keeping it real",
        "angst": "angst",
        "apathy": "whatever",
        "seattle": "Seattle",
        "underground": "underground"
    },

    "yuppies_1980s.json": {
        "bmw": "Bimmer",
        "mercedes benz": "Benz",
        "cellular phone": "brick phone",
        "pager": "beeper",
        "stock market": "the market",
        "wall street": "The Street",
        "power lunch": "power lunch",
        "networking": "schmoozing",
        "status symbol": "trophy",
        "cocaine": "nose candy"
    },

    "slackers_1990s.json": {
        "apathy": "whatever",
        "ironic": "ironic",
        "cynical": "cynical",
        "coffee shop": "cafe",
        "alternative": "indie",
        "corporate": "the man",
        "generation x": "Gen X",
        "unemployment": "funemployment"
    },

    "rastafarians_1970s.json": {
        "babylon": "Babylon",
        "dreadlocks": "locks",
        "rasta": "Rasta",
        "ethiopia": "Zion",
        "haile selassie": "Jah Rastafari",
        "reasoning": "reasoning",
        "ital food": "ital",
        "ganja": "herb",
        "righteous": "irie"
    },

    "goths_1980s.json": {
        "cemetery": "graveyard",
        "vampire": "creature of the night",
        "pale": "pallid",
        "black clothing": "blacks",
        "eyeliner": "kohl",
        "clove cigarette": "clove",
        "poetry": "verse",
        "romantic": "darkly romantic"
    },

    "outlaw_bikers_1960s.json": {
        "one percenter": "one percenter",
        "motorcycle club": "MC",
        "club colors": "colors",
        "patch": "patch",
        "ride out": "run",
        "choppered bike": "chopper",
        "harley davidson": "Harley"
    },

    "new_romantic_goth_1980s.json": {
        "synthesizer": "synth",
        "makeup": "face paint",
        "androgynous": "gender-bending",
        "theatrical": "dramatic",
        "new wave": "new wave",
        "club kid": "club kid"
    },

    "ibm_engineers_1950s.json": {
        "electronic computer": "electronic brain",
        "programmer": "coder",
        "algorithm": "procedure",
        "debug": "troubleshoot",
        "mainframe": "big iron",
        "input": "feed in",
        "output": "readout"
    },

    "mid_century_modern_1960s.json": {
        "cocktail hour": "cocktail hour",
        "martini": "martini",
        "eames chair": "modern chair",
        "danish modern": "Danish",
        "sophisticated": "cultured",
        "refined": "polished"
    }
}

def enhance_filters():
    src_dir = Path("/home/user/talk-like-an-X/src")

    for filename, new_terms in ENHANCEMENTS.items():
        filepath = src_dir / filename
        if not filepath.exists():
            print(f"Skipping {filename} - file not found")
            continue

        with open(filepath, 'r') as f:
            data = json.load(f)

        if 'substitutions' not in data:
            print(f"Skipping {filename} - no substitutions")
            continue

        # Add new terms, avoiding self-mappings
        added = 0
        for key, value in new_terms.items():
            if key != value and key not in data['substitutions']:
                data['substitutions'][key] = value
                added += 1

        if added > 0:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write('\n')
            print(f"{filename}: added {added} terms")
        else:
            print(f"{filename}: no terms added")

if __name__ == "__main__":
    enhance_filters()
    print("\nEnhancement complete!")
