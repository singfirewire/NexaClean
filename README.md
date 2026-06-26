# NexaClean

Desktop cleanup and organization tool for Windows with modern dark UI.

## Features

- **New Folder Cleanup** - Find and delete unnecessary "New folder" directories
- **File Organization** - Sort files by extension into subfolders
- **Shortcut Management** - Move shortcuts to a dedicated folder
- **Temp File Cleanup** - Remove temporary and junk files (.tmp, .temp, .log, .cache)
- **Statistics** - Track your cleanup progress
- **9 Themes** - Dark Neon, Light Clean, Ocean Blue, Forest Green, Sunset Orange, Purple Haze, Glitch Purple, Retro Purple

## Screenshots

Dark Neon theme with modern UI design.

## Requirements

- Windows OS
- Python 3.x (for Python version)
- Go 1.26+ + MSYS2/MinGW (for Go version)

## Quick Start

Download `NexaClean.exe` from the [Releases](https://github.com/singfirewire/NexaClean/releases) page and run it directly.

## Run from Source (Python)

```bash
python nexaclean.py
```

## Run from Source (Go)

```bash
cd go_nexaclean
go build -ldflags "-H windowsgui" -o nexaclean.exe .
./nexaclean.exe
```

## Build Executable (Python)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=favicon-FOLDER.ico nexaclean.py
```

## Build Executable (Go)

```bash
cd go_nexaclean
go build -ldflags "-H windowsgui" -o nexaclean.exe .
```

## License

MIT
