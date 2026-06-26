# NexaClean - Development Notes

## Status: In Progress

## What's Done

### Themes (9 themes total)
- Dark Neon
- Light Clean
- Ocean Blue
- Forest Green
- Sunset Orange
- Purple Haze
- **Glitch Purple** - Light lavender theme
- **Retro Purple** - Dark purple with retro CRT style (default theme)

### Retro Purple Features
- Font: Consolas (monospace)
- Border: groove/ridge style (3px)
- Custom title bar (no Windows border)
- Buttons: raised style
- Default theme on startup

### Custom Title Bar (Retro Purple only)
- Minimize button (orange)
- Close button (red)
- Draggable title bar
- Auto borderless when Retro Purple selected

## Next Steps: Port to Rust

### Why Rust?
- Current .exe: ~10 MB (Python + PyInstaller)
- Rust .exe target: ~1-2 MB
- Better performance

### Plan
1. [ ] Create new Rust project with Cargo
2. [ ] Add `egui` and `eframe` for GUI
3. [ ] Port theme system (color definitions)
4. [ ] Port tab structure (New Folder, Move to Folder, etc.)
5. [ ] Port file operations (shutil equivalent)
6. [ ] Add file dialog support
7. [ ] Build and test

### Tech Stack (Rust)
- **egui** - Immediate mode GUI
- **eframe** - Native window wrapper
- **rfd** - File dialogs
- **std::fs** - File operations

## Notes
- Rust is installed: `rustc 1.96.0`
- Rust not tied to any company (Mozilla/Foundation, open source)
