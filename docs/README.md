# Talk Like An X - Web Demo

This directory contains the browser-based demo interface for Talk Like An X.

## How It Works

All transformation logic runs entirely in your browser:

- **No server required** - All code runs client-side
- **No build step** - Pure JavaScript
- **Offline capable** - Works after first load
- **GitHub Pages ready** - Served directly from this directory

## Architecture

- `index.html` - Main demo page
- `js/app.js` - UI application logic
- `css/style.css` - Responsive styling

Core JavaScript libraries are loaded from `../src/javascript/`:
- `text-transformer.js` - Core transformation engine
- `special-filters.js` - Duck, Glitch, Studly, LOLCAT filters
- `filter-factory.js` - JSON filter loader

Filter data loaded from `../src/filters/*.json`

## Testing Locally

```bash
# From repository root
python3 -m http.server 8000

# Open http://localhost:8000/docs/
```
