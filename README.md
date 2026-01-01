# talk-like-an-X

**Text transformation filters for creating fun dialect and accent conversions**

Transform normal English text in various fun ways - from pirate speak to computer glitches, from 1950s greasers to 1970s punks. Available as both JavaScript and Python implementations. Create custom filters with just JSON, no coding required!

```bash
# Pirate speak
./src/python/filter_factory.py pirate "Hello friend, how are you?"
# "Ahoy matey, how be ye?"

# Computer glitch effect
./src/python/filter_factory.py glitch-50 "System malfunction!"
# "S◆s◓●m ▓◅lf◂n◓◀i◍n!"

# 1970s disco slang
./src/python/filter_factory.py disco "This party is great!"
# "This boogie is outta sight!"
```

---

## Features

**Data-Driven Architecture**
- Create filters entirely in JSON - no coding needed!
- Extensive slang dictionaries (100+ terms per filter)
- Smart word boundary detection and case preservation

**40+ Ready-to-Use Filters**
- **Accents**: Pirate, German, Swedish Chef, Elmer Fudd, Scottish, NYC
- **Subcultures**: 1920s Flappers, 1940s Zoot Suiters, 1950s Beatniks, 1950s Greasers, 1950s IBM Engineers, 1950s Teddy Boys, 1960s Hippies, 1960s Mid-Century Modern, 1960s Mods, 1960s Outlaw Bikers, 1960s Skinheads, 1960s Surfers, 1970s Disco, 1970s Metalheads, 1970s Punks, 1970s Rastafarians, 1980s Club Kids, 1980s Goths, 1980s Hip Hop Breakers, 1980s New Romantic Goths, 1980s Ravers, 1980s Yuppies, 1990s Grunge Musicians, 1990s Hackers, 1990s Riot Grrrl, 1990s Slackers
- **Effects**: Computer Glitches (10%, 25%, 50%, 100%), Duck, Studly Caps, LOLCAT

**Extensible Design**
- SOLID architecture with reusable transformers
- Custom algorithmic filters as modules
- Clean separation: JSON for data, code for algorithms
- Mix and match transformation patterns

---

## Quick Start

### Interactive Web Demo (Recommended)

**[→ Open the interactive demo](docs/index.html)** (or [try it online](https://kleer001.github.io/talk-like-an-X/))

The static web demo runs entirely in your browser:
- Try all 40+ filters instantly
- Transform text in real-time
- Compare input and output side-by-side
- No server, no installation, no command-line needed
- Works offline after first load
- Pure JavaScript implementation

### Command Line (Python)

```bash
cd src/python

# Pirate speak
./filter_factory.py pirate "Hello my friend! Yes, I am happy."
# Output: "Ahoy me matey!, arr! Aye, I be stoked."

# 1980s club kids
./filter_factory.py club_kids_1980s "This party is amazing!"
# Output: "This rave is phenomenal! No doubt!"

# Computer glitch (50% corruption)
./filter_factory.py glitch-50 "Error: System malfunction!"
# Output: "E▓◅or: S◆◓◀●▓ ▓◅l◂◂n◓◀i◍n!"
```

### Creating Your Own Filter

1. **Copy an example JSON file**:
   ```bash
   cp src/filters/disco.json src/filters/my_filter.json
   ```

2. **Edit the vocabulary** - no coding needed!

3. **Test it**:
   ```bash
   ./src/python/filter_factory.py my_filter "test text"
   ```

That's it! See [`src/README.md`](src/README.md) for complete documentation.

### Alternative: Flask Web App

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask web demo
python3 web/app.py

# Open http://localhost:5000 in your browser
```

---

## Documentation

- **[src/README.md](src/README.md)** - Complete library documentation
- **[src/FILTER_SCHEMA.md](src/FILTER_SCHEMA.md)** - JSON schema reference
- **[src/DEVELOPER_GUIDE.md](src/DEVELOPER_GUIDE.md)** - Advanced guide
- **[src/FILTER_ANALYSIS.md](src/FILTER_ANALYSIS.md)** - Pattern analysis
- **[docs/README.md](docs/README.md)** - JavaScript web demo documentation

---

## Architecture

This project separates **data** (vocabularies) from **logic** (transformation patterns):

```
Repository Structure:
├─ src/
│  ├─ filters/          ──► JSON filter definitions (shared data)
│  ├─ javascript/       ──► JavaScript implementation
│  └─ python/          ──► Python implementation
├─ docs/               ──► Static JavaScript web demo
└─ web/                ──► Flask Python web app

Filter Architecture:
src/filters/*.json ──► Universal filter data
        │
        ├─► disco.json          (pure data)
        ├─► pirate.json         (pure data)
        ├─► club_kids_1980s.json (pure data)
        │
        └─► For custom algorithms:
            ├─► duck.json ──► duck.js / duck.py
            ├─► studly.json ──► studly.js / studly.py
            └─► glitch.json ──► glitch.js / glitch.py
```

**Two approaches**:
- **~70% of filters**: Pure JSON (no coding!)
- **~30% of filters**: Custom modules for algorithms (clean separation)

See [src/FILTER_ANALYSIS.md](src/FILTER_ANALYSIS.md) for the complete analysis.

---

## Credits & Attribution

This library is a complete redesign implementing a data-driven architecture inspired by the classic text transformation filters.

### Lineage

This work builds upon a rich history of text transformation filters:

**Original Filters** (1980s-2000s): From the **[debian `filters` package](https://packages.debian.org/jessie/games/filters)** collected by **[Joey Hess](http://joeyh.name/code/filters/)**, with contributions from:
- Joey Hess (package maintainer and filter author)
- Daniel Klein (nyc, cockney filters, 1986)
- John Sparks (klaus filter, 1989)
- Jamie Zawinski (newspeak filter, 1991)
- Nick Phillips (studly filter)
- Andrew J. Buehler (scramble filter, 2009)
- And many others from the original Debian filters package

**JavaScript/TypeScript Port**: **[Aaron Wells](https://github.com/agwells/talk-like-a)** (2019) modernized these classic filters

**Python & JavaScript Implementations**: Claude (Anthropic), 2024
- Created data-driven architecture separating vocabularies from logic
- Analyzed transformation patterns and created reusable library
- Designed JSON schema for filter configuration
- Created subculture slang dictionaries (100+ terms each)
- Added glitch effect transformers
- JavaScript port with static web demo

**With Direction From**: kleer001 (repository owner)

---

## License

This project inherits the licenses from the original filters package. Each filter has its own license (GPL-2+, GPL-3+, MIT-like, or public domain).

**Library code** (in `/src`) is licensed under **GPL** to match the original filters.

---

## Contributing

Want to add a new filter?

1. **For JSON filters**: Create a `.json` file in `/src/filters/` following the schema in [FILTER_SCHEMA.md](src/FILTER_SCHEMA.md)
2. **For algorithmic filters**: Create a custom transformer - see [DEVELOPER_GUIDE.md](src/DEVELOPER_GUIDE.md)

Most filters can be created with just JSON - no coding required!

---

## Design Philosophy

> **Most text transformations are data, not logic.**

Instead of writing code for each filter, we separate:
- **Data** (vocabularies, slang) → JSON files
- **Logic** (transformation patterns) → Reusable library (JavaScript/Python)
- **Algorithms** (special cases) → Custom transformers when needed

This makes filters:
- Easy to create (no coding for most filters)
- Easy to maintain (edit data, not code)
- Easy to share (JSON is universal)
- Easy to version control (clean diffs)

---

## Statistics

- **40+** filters available (covering 20th-century subcultures and effects)
- **~70%** of text transformations can be pure JSON (no code needed)
- **10** transformation patterns identified and implemented
- **100+** slang terms per subculture filter
- **4** algorithmic module patterns (duck, studly, lolcat, glitch)

---

**Happy filtering!**

**Standing on the shoulders of giants:**
Joey Hess, Daniel Klein, Jamie Zawinski, Aaron Wells, and many others
