# NexaClean

Desktop cleanup and organization tool for Windows with modern dark UI.

## Features

- **New Folder Cleanup** - Find and delete unnecessary "New folder" directories
- **File Organization** - Sort files by extension into subfolders
- **Shortcut Management** - Move shortcuts to a dedicated folder
- **Temp File Cleanup** - Remove temporary and junk files (.tmp, .temp, .log, .cache)
- **Statistics** - Track your cleanup progress
- **6 Themes** - Dark Neon, Light Clean, Ocean Blue, Forest Green, Sunset Orange, Purple Haze

## Screenshots

Dark Neon theme with modern UI design.

## Requirements

- Windows OS
- Python 3.x (for running from source)

## Quick Start

Download `NexaClean.exe` from the [Releases](https://github.com/singfirewire/NexaClean/releases) page and run it directly.

## Run from Source

```bash
python nexaclean.py
```

## Build Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=favicon-FOLDER.ico nexaclean.py
```

## License

MIT
