# NexaClean

Desktop cleanup and organization tool for Windows.

## Features

- **New Folder Cleanup** - Find and delete unnecessary "New folder" directories
- **File Organization** - Sort files by extension into subfolders
- **Shortcut Management** - Move shortcuts to a dedicated folder
- **Temp File Cleanup** - Remove temporary and junk files
- **Statistics** - Track your cleanup progress

## Requirements

- Python 3.x
- tkinter (included with Python)
- Windows OS

## Usage

```bash
python nexaclean.py
```

## Build Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=favicon.ico nexaclean.py
```

## License

MIT
