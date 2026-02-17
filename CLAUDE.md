# a-box-of-mac-and-cheese — Claude Code Rules

> Per-project rules for Claude Code. The root `.claude/CLAUDE.md` rules also apply.

## Project Context

- **Type**: Submodule (added 2026-02-16) — Web app for book cover generation
- **Purpose**: Generates "A (Blank) of (Blank) and (Blank)" book covers
- **Remote**: https://github.com/aaronjones003/a-box-of-mac-and-cheese
- **Tech Stack**: HTML5, Bootstrap, Vanilla JavaScript, Canvas API

## Project-Specific Rules

- This is a static web application with no build process
- Main entry point: `index.html`
- Uses Bootstrap 5.3.3 for styling (via CDN)
- JavaScript logic is in `scripts.js`
- Uses Canvas API for generating book cover images
- Word lists are stored in the `functions/` directory
- When making changes, test by opening `index.html` in a browser
- The app generates random book titles and creates visual covers

## File Organization

- `index.html` — Main HTML file with Bootstrap setup
- `scripts.js` — JavaScript logic for title generation and image creation
- `functions/` — Directory containing word lists and generation functions
- No build process required — direct browser execution
