# NexaClean Go Port - Development Notes

## Overview

Full rewrite of NexaClean from Python (tkinter) to Go (Fyne v2 GUI framework).

## Tech Stack

- **Language:** Go 1.26
- **GUI:** Fyne v2.4.4 (cross-platform UI toolkit)
- **Native Dialogs:** sqweek/dialog (Windows folder picker)
- **Build:** MinGW GCC via MSYS2 (required for CGO/OpenGL)

## File Structure

```
go_nexaclean/
├── main.go            # UI + application logic
├── themes.go          # 9 theme definitions (color palettes)
├── custom_theme.go    # Fyne Theme interface implementation
├── stats.go           # Statistics persistence (JSON)
├── go.mod / go.sum    # Go module dependencies
└── .gitignore         # Ignores exe and stats files
```

## Features

- 5 tabs: Folders, Organize, Shortcuts, Temp Files, Statistics
- 9 built-in themes with real-time switching
- Custom Fyne Theme engine (overrides all colors)
- Icons on every button (Fyne built-in icons)
- Accent bar on each tab header
- Native Windows folder picker dialog
- Export statistics to text file
- Single exe output (~34MB)

## Build

```bash
# Requires: Go 1.26+, MSYS2 with MinGW GCC
$env:Path = "C:\msys64\mingw64\bin;" + $env:Path
$env:CGO_ENABLED="1"
go build -ldflags "-H windowsgui" -o nexaclean.exe .
```

`-H windowsgui` hides the console window (GUI-only app).

## Known Limitations

- Fyne doesn't support gradient backgrounds or custom title bars
- Window size is fixed (not resizable) to match Python version
- Custom fonts not supported in Fyne (uses system fonts)
