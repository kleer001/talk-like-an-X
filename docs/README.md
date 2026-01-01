# Talk Like An X - Static Web Demo

This directory contains a pure JavaScript implementation of the Talk Like An X filters.

## How It Works

All transformation logic runs entirely in your browser:

- **No server required** - All code runs client-side
- **No build step** - Pure JavaScript, no transpilation
- **Offline capable** - Works after first load
- **GitHub Pages ready** - Served directly from the repository

## Architecture

- `index.html` - Main demo page
- `js/text-transformer.js` - Core transformation library (ported from Python)
- `js/special-filters.js` - Duck, Glitch, Studly, LOLCAT filters (ported from Python)
- `js/filter-factory.js` - JSON filter loader
- `js/app.js` - UI application logic
- `css/style.css` - Responsive styling

## Filter Data

Filter JSON files are loaded from `../src/*.json` via fetch API. This means:

- No duplication - Uses the same JSON files as the Python library
- Easy maintenance - Add new filter = just add new JSON file
- Automatic discovery - All filters in `src/` are available

## Testing Locally

```bash
# From repository root
python3 -m http.server 8000

# Open http://localhost:8000/docs/
```

## Credits

JavaScript port maintains feature parity with the Python implementation while adding:
- Seeded random number generator for reproducible results
- Direct JSON loading via fetch API
- Zero-dependency browser-native implementation
