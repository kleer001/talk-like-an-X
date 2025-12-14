# talk-like-an-X

**A Python library for creating fun text transformation filters**

Transform normal English text in various fun ways - from pirate speak to computer glitches, from 1950s greasers to 1970s punks. Create custom filters with just JSON, no coding required!

```bash
# Pirate speak
./python/filter_factory.py pirate "Hello friend, how are you?"
# "Ahoy matey, how be ye?"

# Computer glitch effect
./python/filter_factory.py glitch-50 "System malfunction!"
# "S◆s◓●m ▓◅lf◂n◓◀i◍n!"

# 1970s disco slang
./python/filter_factory.py disco "This party is great!"
# "This boogie is outta sight!"
```

---

## ✨ Features

**🎯 Data-Driven Architecture**
- Create filters entirely in JSON - no Python coding needed!
- Extensive slang dictionaries (100+ terms per filter)
- Smart word boundary detection and case preservation

**🎨 15 Ready-to-Use Filters**
- **Accents**: Pirate, German, Swedish Chef, Elmer Fudd
- **Subcultures**: 1970s Disco, 1980s Club Kids, 1950s Greasers, 1970s Punks
- **Effects**: Computer Glitches (10%, 25%, 50%, 100% corruption)

**🔧 Extensible Design**
- SOLID architecture with reusable transformers
- Custom algorithmic filters in Python
- Mix and match transformation patterns

---

## 🚀 Quick Start

### Using Pre-Made Filters

```bash
cd python

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
   cp python/disco.json python/my_filter.json
   ```

2. **Edit the vocabulary** - no coding needed!

3. **Test it**:
   ```bash
   ./python/filter_factory.py my_filter "test text"
   ```

That's it! See [`python/README.md`](python/README.md) for complete documentation.

---

## 📚 Documentation

- **[python/README.md](python/README.md)** - Complete library documentation
- **[python/FILTER_SCHEMA.md](python/FILTER_SCHEMA.md)** - JSON schema reference
- **[python/DEVELOPER_GUIDE.md](python/DEVELOPER_GUIDE.md)** - Advanced guide
- **[python/FILTER_ANALYSIS.md](python/FILTER_ANALYSIS.md)** - Pattern analysis

---

## 🏗️ Architecture

This project separates **data** (vocabularies) from **logic** (transformation patterns):

```
python/filter_factory.py ──► Universal filter builder (logic)
        │
        ├─► disco.json          (data)
        ├─► pirate.json         (data)
        ├─► club_kids_1980s.json (data)
        └─► ... (add your own!)
```

**Result**: ~70% of text filters can be created with **just JSON**, no code!

See [python/FILTER_ANALYSIS.md](python/FILTER_ANALYSIS.md) for the complete analysis.

---

## 🎓 Credits & Attribution

This Python library is a complete redesign implementing a data-driven architecture inspired by the classic text transformation filters.

### Lineage

This work builds upon a rich history of text transformation filters:

**Original Filters** (1980s-2000s): From the **[debian `filters` package](https://packages.debian.org/jessie/games/filters)** collected by **[Joey Hess](http://joeyh.name/code/filters/)**, with contributions from:
- Joey Hess (package maintainer and filter author)
- Daniel Klein (nyc, cockney filters, 1986)
- John Sparks (klaus filter, 1989)
- Jamie Zawinski (newspeak filter, 1991)
- Nick Phillips (studly filter)
- Andrew J. Buehler (scramble filter, 2009)
- And many others (see `/original/debian/copyright` for full credits)

**JavaScript/TypeScript Port**: **[Aaron Wells](https://github.com/agwells/talk-like-a)** (2019) modernized these classic filters

**Python Implementation**: Claude (Anthropic), 2024
- Created data-driven architecture separating vocabularies from logic
- Analyzed transformation patterns and created reusable library
- Designed JSON schema for filter configuration
- Created subculture slang dictionaries (100+ terms each)
- Added glitch effect transformers

**With Direction From**: kleer001 (repository owner)

---

## 📜 License

This project inherits the licenses from the original filters package. Each filter has its own license (GPL-2+, GPL-3+, MIT-like, or public domain). See **[original/debian/copyright](original/debian/copyright)** for complete license information.

**Python library code** (in `/python`) is licensed under **GPL** to match the original filters.

---

## 🤝 Contributing

Want to add a new filter?

1. **For JSON filters**: Create a `.json` file in `/python` following the schema in [FILTER_SCHEMA.md](python/FILTER_SCHEMA.md)
2. **For algorithmic filters**: Create a custom transformer in Python - see [DEVELOPER_GUIDE.md](python/DEVELOPER_GUIDE.md)

Most filters can be created with just JSON - no coding required!

---

## 🎯 Design Philosophy

> **Most text transformations are data, not logic.**

Instead of writing code for each filter, we separate:
- **Data** (vocabularies, slang) → JSON files
- **Logic** (transformation patterns) → Reusable Python library
- **Algorithms** (special cases) → Custom transformers when needed

This makes filters:
- ✅ Easy to create (no coding for most filters)
- ✅ Easy to maintain (edit data, not code)
- ✅ Easy to share (JSON is universal)
- ✅ Easy to version control (clean diffs)

---

## 📊 Statistics

- **15** Python filters available (11 JSON-based, 4 algorithmic)
- **~70%** of text transformations can be pure JSON (no code needed)
- **10** transformation patterns identified and implemented
- **100+** slang terms per subculture filter

---

**Happy filtering!** 🎉

**Standing on the shoulders of giants:**
Joey Hess, Daniel Klein, Jamie Zawinski, Aaron Wells, and many others
