package main

import (
	"fmt"
	"image/color"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"time"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
	nativedialog "github.com/sqweek/dialog"
)

type NexaClean struct {
	app        fyne.App
	mainWindow fyne.Window
	themeName  string
	stats      *Stats

	desktopPath string
	appDir      string

	folderPath    string
	duplicateMode string
	newFolders    []string
	tempFiles     []TempFile
	shortcuts     []string
	extensions    map[string]int

	statusLabel *widget.Label
	progressBar *widget.ProgressBar

	folderList     *widget.List
	tempList       *widget.List
	shortcutList   *widget.List
	extensionTable *widget.Table

	folderSelected   map[int]bool
	tempSelected     map[int]bool
	shortcutSelected map[int]bool

	statsLabels map[string]*widget.Label
}

type TempFile struct {
	Path string
	Size int64
	Name string
}

func NewNexaClean() *NexaClean {
	homeDir, _ := os.UserHomeDir()
	nc := &NexaClean{
		desktopPath:      filepath.Join(homeDir, "Desktop"),
		appDir:           getExecDir(),
		folderPath:       filepath.Join(homeDir, "Desktop"),
		duplicateMode:    "skip",
		themeName:        "Retro Purple",
		extensions:       make(map[string]int),
		folderSelected:   make(map[int]bool),
		tempSelected:     make(map[int]bool),
		shortcutSelected: make(map[int]bool),
		statsLabels:      make(map[string]*widget.Label),
	}
	nc.stats = NewStats()
	nc.stats.Load()
	if nc.stats.Theme != "" {
		nc.themeName = nc.stats.Theme
	}
	return nc
}

func getExecDir() string {
	exe, err := os.Executable()
	if err != nil {
		return "."
	}
	return filepath.Dir(exe)
}

func (nc *NexaClean) Run() {
	nc.app = app.New()
	nc.mainWindow = nc.app.NewWindow("NexaClean - Desktop Cleanup")

	t := themes[nc.themeName]
	nc.app.Settings().SetTheme(&NexaCleanTheme{colors: &t})

	nc.mainWindow.Resize(fyne.NewSize(720, 680))
	nc.mainWindow.SetContent(nc.buildUI())
	nc.mainWindow.ShowAndRun()
}

func (nc *NexaClean) buildUI() fyne.CanvasObject {
	nc.statusLabel = widget.NewLabel("  Ready")
	nc.progressBar = widget.NewProgressBar()

	themeNames := []string{
		"Retro Purple", "Dark Neon", "Macrium Dark",
		"Light Clean", "Ocean Blue", "Forest Green",
		"Sunset Orange", "Purple Haze", "Glitch Purple",
	}
	themeSelect := widget.NewSelect(themeNames, func(name string) {
		nc.themeName = name
		t := themes[name]
		nc.app.Settings().SetTheme(&NexaCleanTheme{colors: &t})
		nc.stats.Theme = name
		nc.stats.Save()
	})
	themeSelect.SetSelected(nc.themeName)

	topBar := container.NewHBox(
		widget.NewLabel("  Theme:"),
		themeSelect,
		layout.NewSpacer(),
		widget.NewLabelWithStyle("NexaClean v1.0", fyne.TextAlignTrailing, fyne.TextStyle{Italic: true}),
	)

	tabs := container.NewAppTabs(
		nc.buildTab1(),
		nc.buildTab2(),
		nc.buildTab3(),
		nc.buildTab4(),
		nc.buildTab5(),
	)
	tabs.SetTabLocation(container.TabLocationTop)

	statusBar := container.NewBorder(nil, nil, nc.statusLabel, nc.progressBar)

	return container.NewBorder(topBar, statusBar, nil, nil, tabs)
}

func makeHeaderCard(title, subtitle string, accent color.Color) *fyne.Container {
	titleLbl := widget.NewLabel(title)
	titleLbl.TextStyle = fyne.TextStyle{Bold: true}
	titleLbl.Importance = widget.HighImportance

	subLbl := widget.NewLabel(subtitle)
	subLbl.Importance = widget.LowImportance

	accentBar := canvas.NewRectangle(accent)
	accentBar.SetMinSize(fyne.NewSize(4, 50))

	return container.NewBorder(nil, nil, accentBar, nil,
		container.NewVBox(
			layout.NewSpacer(),
			titleLbl,
			subLbl,
			layout.NewSpacer(),
		),
	)
}

func makeIconButton(label string, icon fyne.Resource, importance widget.Importance, fn func()) *widget.Button {
	btn := widget.NewButtonWithIcon(label, icon, fn)
	btn.Importance = importance
	return btn
}

func (nc *NexaClean) buildTab1() *container.TabItem {
	t := themes[nc.themeName]

	searchBtn := makeIconButton("Search Folders", theme.SearchIcon(), widget.HighImportance, nc.searchFolders)
	deleteBtn := makeIconButton("Delete Selected", theme.DeleteIcon(), widget.WarningImportance, nc.deleteSelectedFolders)

	buttonBar := container.NewHBox(searchBtn, deleteBtn)

	nc.folderList = widget.NewList(
		func() int { return len(nc.newFolders) },
		func() fyne.CanvasObject {
			cb := widget.NewCheck("", nil)
			icon := widget.NewIcon(theme.FolderIcon())
			name := widget.NewLabel("name")
			name.Wrapping = fyne.TextTruncate
			pathLbl := widget.NewLabel("path")
			pathLbl.Importance = widget.LowImportance
			return container.NewHBox(cb, icon, name, pathLbl)
		},
		func(id widget.ListItemID, obj fyne.CanvasObject) {
			if id < len(nc.newFolders) {
				c := obj.(*fyne.Container)
				cb := c.Objects[0].(*widget.Check)
				name := c.Objects[2].(*widget.Label)
				pathLbl := c.Objects[3].(*widget.Label)
				cb.SetChecked(nc.folderSelected[id])
				cb.OnChanged = func(checked bool) { nc.folderSelected[id] = checked }
				name.SetText(filepath.Base(nc.newFolders[id]))
				p := nc.newFolders[id]
				if len(p) > 50 {
					p = p[:47] + "..."
				}
				pathLbl.SetText(p)
			}
		},
	)
	nc.folderList.OnSelected = func(id widget.ListItemID) { nc.folderList.UnselectAll() }

	header := makeHeaderCard("New Folder Cleanup", "Find and delete unnecessary 'New folder' directories on Desktop", t.AccentGreen)

	content := container.NewBorder(
		container.NewVBox(header, buttonBar, widget.NewSeparator()),
		nil, nil, nil,
		nc.folderList,
	)
	return container.NewTabItemWithIcon(" Folders ", theme.FolderIcon(), content)
}

func (nc *NexaClean) buildTab2() *container.TabItem {
	t := themes[nc.themeName]

	folderEntry := widget.NewEntry()
	folderEntry.SetText(nc.folderPath)
	folderEntry.OnChanged = func(s string) { nc.folderPath = s }

	browseBtn := makeIconButton("Browse", theme.FolderOpenIcon(), widget.MediumImportance, func() {
		dir, err := nativedialog.Directory().Title("Select Folder").Browse()
		if err == nil && dir != "" {
			nc.folderPath = dir
			folderEntry.SetText(nc.folderPath)
		}
	})

	folderRow := container.NewBorder(nil, nil, widget.NewIcon(theme.FolderIcon()), browseBtn, folderEntry)

	radioGroup := widget.NewRadioGroup([]string{"Skip", "Overwrite", "Keep Newest"}, func(s string) {
		nc.duplicateMode = strings.ToLower(s)
	})
	radioGroup.SetSelected("Skip")
	dupRow := container.NewHBox(widget.NewLabel("Duplicates:"), radioGroup)

	scanBtn := makeIconButton("Scan Extensions", theme.SearchIcon(), widget.MediumImportance, nc.scanExtensions)
	moveBtn := makeIconButton("Move by Extension", theme.MoveUpIcon(), widget.HighImportance, nc.organizeFiles)
	clearBtn := makeIconButton("Clear", theme.DeleteIcon(), widget.LowImportance, func() {
		nc.folderPath = filepath.Join(nc.desktopPath)
		nc.extensions = make(map[string]int)
		nc.extensionTable.Refresh()
	})

	buttonBar := container.NewHBox(scanBtn, moveBtn, layout.NewSpacer(), clearBtn)

	nc.extensionTable = widget.NewTable(
		func() (int, int) { return len(nc.extensions) + 1, 3 },
		func() fyne.CanvasObject {
			return widget.NewLabel("cell")
		},
		func(id widget.TableCellID, obj fyne.CanvasObject) {
			lbl := obj.(*widget.Label)
			lbl.TextStyle = fyne.TextStyle{}
			if id.Row == 0 {
				switch id.Col {
				case 0:
					lbl.SetText("  Extension")
					lbl.TextStyle = fyne.TextStyle{Bold: true}
				case 1:
					lbl.SetText("  Count")
					lbl.TextStyle = fyne.TextStyle{Bold: true}
				case 2:
					lbl.SetText("  Folder Exists")
					lbl.TextStyle = fyne.TextStyle{Bold: true}
				}
			} else {
				exts := sortedExts(nc.extensions)
				if id.Row-1 < len(exts) {
					ext := exts[id.Row-1]
					switch id.Col {
					case 0:
						lbl.SetText("  " + ext)
					case 1:
						lbl.SetText(fmt.Sprintf("  %d", nc.extensions[ext]))
					case 2:
						folderName := strings.ToUpper(strings.TrimPrefix(ext, "."))
						target := filepath.Join(nc.folderPath, folderName)
						if _, err := os.Stat(target); err == nil {
							lbl.SetText("  Yes")
						} else {
							lbl.SetText("  No")
						}
					}
				}
			}
		},
	)
	nc.extensionTable.SetColumnWidth(0, 250)
	nc.extensionTable.SetColumnWidth(1, 150)
	nc.extensionTable.SetColumnWidth(2, 150)

	header := makeHeaderCard("File Organization", "Scan and organize files by extension into folders", t.AccentBlue)

	content := container.NewBorder(
		container.NewVBox(header, folderRow, dupRow, buttonBar, widget.NewSeparator()),
		nil, nil, nil,
		nc.extensionTable,
	)
	return container.NewTabItemWithIcon(" Organize ", theme.FolderIcon(), content)
}

func (nc *NexaClean) buildTab3() *container.TabItem {
	t := themes[nc.themeName]

	searchBtn := makeIconButton("Search Shortcuts", theme.SearchIcon(), widget.MediumImportance, nc.searchShortcuts)
	moveBtn := makeIconButton("Move Selected", theme.MoveUpIcon(), widget.HighImportance, nc.moveSelectedShortcuts)
	moveAllBtn := makeIconButton("Move All", theme.MailForwardIcon(), widget.MediumImportance, nc.moveAllShortcuts)

	buttonBar := container.NewHBox(searchBtn, moveBtn, moveAllBtn)

	nc.shortcutList = widget.NewList(
		func() int { return len(nc.shortcuts) },
		func() fyne.CanvasObject {
			cb := widget.NewCheck("", nil)
			icon := widget.NewIcon(theme.ComputerIcon())
			name := widget.NewLabel("shortcut name")
			return container.NewHBox(cb, icon, name)
		},
		func(id widget.ListItemID, obj fyne.CanvasObject) {
			if id < len(nc.shortcuts) {
				c := obj.(*fyne.Container)
				cb := c.Objects[0].(*widget.Check)
				name := c.Objects[2].(*widget.Label)
				cb.SetChecked(nc.shortcutSelected[id])
				cb.OnChanged = func(checked bool) { nc.shortcutSelected[id] = checked }
				name.SetText(filepath.Base(nc.shortcuts[id]))
			}
		},
	)

	header := makeHeaderCard("Shortcut Management", "Move .lnk shortcuts to a dedicated SHORTCUT folder", t.AccentOrange)

	content := container.NewBorder(
		container.NewVBox(header, buttonBar, widget.NewSeparator()),
		nil, nil, nil,
		nc.shortcutList,
	)
	return container.NewTabItemWithIcon(" Shortcuts ", theme.ComputerIcon(), content)
}

func (nc *NexaClean) buildTab4() *container.TabItem {
	t := themes[nc.themeName]

	searchBtn := makeIconButton("Search Temp Files", theme.SearchIcon(), widget.MediumImportance, nc.searchTempFiles)
	deleteBtn := makeIconButton("Delete Selected", theme.DeleteIcon(), widget.WarningImportance, nc.deleteSelectedTempFiles)
	deleteAllBtn := makeIconButton("Delete All Temp", theme.ErrorIcon(), widget.WarningImportance, nc.deleteAllTempFiles)

	buttonBar := container.NewHBox(searchBtn, deleteBtn, deleteAllBtn)

	nc.tempList = widget.NewList(
		func() int { return len(nc.tempFiles) },
		func() fyne.CanvasObject {
			cb := widget.NewCheck("", nil)
			icon := widget.NewIcon(theme.FileIcon())
			name := widget.NewLabel("file name")
			sizeLbl := widget.NewLabel("0 KB")
			sizeLbl.Importance = widget.LowImportance
			return container.NewHBox(cb, icon, name, sizeLbl)
		},
		func(id widget.ListItemID, obj fyne.CanvasObject) {
			if id < len(nc.tempFiles) {
				c := obj.(*fyne.Container)
				cb := c.Objects[0].(*widget.Check)
				name := c.Objects[2].(*widget.Label)
				sizeLbl := c.Objects[3].(*widget.Label)
				cb.SetChecked(nc.tempSelected[id])
				cb.OnChanged = func(checked bool) { nc.tempSelected[id] = checked }
				name.SetText(nc.tempFiles[id].Name)
				sizeLbl.SetText(FormatFileSize(nc.tempFiles[id].Size))
			}
		},
	)

	header := makeHeaderCard("Temp File Cleanup", "Remove temporary and junk files (.tmp, .temp, .log, .cache)", t.Danger)

	content := container.NewBorder(
		container.NewVBox(header, buttonBar, widget.NewSeparator()),
		nil, nil, nil,
		nc.tempList,
	)
	return container.NewTabItemWithIcon(" Temp Files ", theme.DeleteIcon(), content)
}

func (nc *NexaClean) buildTab5() *container.TabItem {
	t := themes[nc.themeName]

	header := makeHeaderCard("Statistics & Reports", "Track cleanup progress and export reports", t.Accent)

	statsData := []struct {
		Label string
		Key   string
	}{
		{"Folders deleted:", "folders_deleted"},
		{"Shortcuts managed:", "shortcuts_deleted"},
		{"Temp files deleted:", "temp_files_deleted"},
		{"Files organized:", "files_organized"},
		{"Space recovered:", "total_cleaned_size"},
		{"First use:", "first_use_date"},
		{"Last cleanup:", "last_cleanup_date"},
	}

	statsGrid := container.NewVBox()
	for _, sd := range statsData {
		val := nc.getStatValue(sd.Key)
		valLabel := widget.NewLabel(val)
		valLabel.TextStyle = fyne.TextStyle{Bold: true}
		valLabel.Importance = widget.HighImportance
		nc.statsLabels[sd.Key] = valLabel
		row := container.NewHBox(
			widget.NewLabel(sd.Label),
			valLabel,
		)
		statsGrid.Add(row)
	}

	refreshBtn := makeIconButton("Refresh Stats", theme.ViewRefreshIcon(), widget.HighImportance, nc.refreshStatsDisplay)
	resetBtn := makeIconButton("Reset Stats", theme.DeleteIcon(), widget.WarningImportance, nc.resetStats)
	exportBtn := makeIconButton("Export Report", theme.DocumentSaveIcon(), widget.MediumImportance, nc.exportReport)

	buttonBar := container.NewHBox(refreshBtn, resetBtn, exportBtn)

	summaryHeader := widget.NewLabel("  Cleanup Summary")
	summaryHeader.TextStyle = fyne.TextStyle{Bold: true}
	summaryText := widget.NewLabel(nc.generateSummary())
	content := container.NewBorder(
		container.NewVBox(header, statsGrid, buttonBar, widget.NewSeparator(), summaryHeader),
		nil, nil, nil,
		summaryText,
	)
	return container.NewTabItemWithIcon(" Stats ", theme.InfoIcon(), content)
}

func (nc *NexaClean) updateStatus(msg string) {
	nc.statusLabel.SetText("  " + msg)
}

func (nc *NexaClean) searchFolders() {
	nc.updateStatus("Searching for folders...")
	nc.newFolders = nil
	nc.folderSelected = make(map[int]bool)

	entries, err := os.ReadDir(nc.desktopPath)
	if err != nil {
		dialog.ShowError(err, nc.mainWindow)
		return
	}

	for _, entry := range entries {
		if entry.IsDir() && strings.HasPrefix(entry.Name(), "New folder") {
			nc.newFolders = append(nc.newFolders, filepath.Join(nc.desktopPath, entry.Name()))
			nc.folderSelected[len(nc.newFolders)-1] = true
		}
	}

	nc.folderList.Refresh()
	nc.updateStatus(fmt.Sprintf("Found: %d folders", len(nc.newFolders)))
}

func (nc *NexaClean) deleteSelectedFolders() {
	var selected []string
	for i, ok := range nc.folderSelected {
		if ok && i < len(nc.newFolders) {
			selected = append(selected, nc.newFolders[i])
		}
	}
	if len(selected) == 0 {
		dialog.ShowInformation("Info", "No folders selected", nc.mainWindow)
		return
	}

	dialog.ShowConfirm("Confirm Delete",
		fmt.Sprintf("Delete %d folders?", len(selected)),
		func(ok bool) {
			if !ok {
				return
			}
			nc.updateStatus("Deleting folders...")
			for _, p := range selected {
				os.RemoveAll(p)
			}
			nc.stats.FoldersDeleted += len(selected)
			nc.stats.LastCleanupDate = time.Now().Format("2006-01-02 15:04:05")
			nc.stats.Save()
			nc.searchFolders()
			nc.refreshStatsDisplay()
			nc.updateStatus("Ready")
		}, nc.mainWindow,
	)
}

func (nc *NexaClean) searchShortcuts() {
	nc.updateStatus("Searching for shortcuts...")
	nc.shortcuts = nil
	nc.shortcutSelected = make(map[int]bool)

	entries, err := os.ReadDir(nc.desktopPath)
	if err != nil {
		dialog.ShowError(err, nc.mainWindow)
		return
	}
	for _, entry := range entries {
		if !entry.IsDir() && strings.ToLower(filepath.Ext(entry.Name())) == ".lnk" {
			nc.shortcuts = append(nc.shortcuts, filepath.Join(nc.desktopPath, entry.Name()))
			nc.shortcutSelected[len(nc.shortcuts)-1] = true
		}
	}
	nc.shortcutList.Refresh()
	nc.updateStatus(fmt.Sprintf("Found: %d shortcuts", len(nc.shortcuts)))
}

func (nc *NexaClean) moveSelectedShortcuts() {
	var selected []string
	for i, ok := range nc.shortcutSelected {
		if ok && i < len(nc.shortcuts) {
			selected = append(selected, nc.shortcuts[i])
		}
	}
	if len(selected) == 0 {
		dialog.ShowInformation("Info", "No shortcuts selected", nc.mainWindow)
		return
	}
	nc.moveShortcuts(selected)
}

func (nc *NexaClean) moveAllShortcuts() {
	if len(nc.shortcuts) == 0 {
		dialog.ShowInformation("Info", "No shortcuts found", nc.mainWindow)
		return
	}
	nc.moveShortcuts(nc.shortcuts)
}

func (nc *NexaClean) moveShortcuts(paths []string) {
	dialog.ShowConfirm("Confirm Move",
		fmt.Sprintf("Move %d shortcuts to SHORTCUT folder?", len(paths)),
		func(ok bool) {
			if !ok {
				return
			}
			shortcutFolder := filepath.Join(nc.desktopPath, "SHORTCUT")
			os.MkdirAll(shortcutFolder, 0755)
			nc.updateStatus("Moving shortcuts...")
			moved := 0
			for _, p := range paths {
				filename := filepath.Base(p)
				target := filepath.Join(shortcutFolder, filename)
				if _, err := os.Stat(target); err == nil {
					name := strings.TrimSuffix(filename, filepath.Ext(filename))
					ext := filepath.Ext(filename)
					counter := 1
					for {
						target = filepath.Join(shortcutFolder, fmt.Sprintf("%s_%d%s", name, counter, ext))
						if _, err := os.Stat(target); err != nil {
							break
						}
						counter++
					}
				}
				if err := os.Rename(p, target); err == nil {
					moved++
				}
			}
			nc.stats.ShortcutsDeleted += moved
			nc.stats.LastCleanupDate = time.Now().Format("2006-01-02 15:04:05")
			nc.stats.Save()
			nc.searchShortcuts()
			nc.refreshStatsDisplay()
			nc.updateStatus("Ready")
		}, nc.mainWindow,
	)
}

func (nc *NexaClean) searchTempFiles() {
	nc.updateStatus("Searching for temp files...")
	nc.tempFiles = nil
	nc.tempSelected = make(map[int]bool)

	tempExts := map[string]bool{
		".tmp": true, ".temp": true, ".log": true, ".cache": true,
		".dmp": true, ".crash": true, ".chk": true, ".gid": true,
		".old": true, ".bak": true, "~": true,
	}

	entries, err := os.ReadDir(nc.desktopPath)
	if err != nil {
		dialog.ShowError(err, nc.mainWindow)
		return
	}

	for _, entry := range entries {
		if !entry.IsDir() {
			name := entry.Name()
			ext := strings.ToLower(filepath.Ext(name))
			isTemp := tempExts[ext] || strings.HasPrefix(name, "~") ||
				strings.Contains(strings.ToLower(name), "temp") ||
				strings.Contains(strings.ToLower(name), "cache")
			if isTemp {
				info, _ := entry.Info()
				size := int64(0)
				if info != nil {
					size = info.Size()
				}
				nc.tempFiles = append(nc.tempFiles, TempFile{
					Path: filepath.Join(nc.desktopPath, name),
					Size: size,
					Name: name,
				})
				nc.tempSelected[len(nc.tempFiles)-1] = true
			}
		}
	}

	nc.tempList.Refresh()
	var totalSize int64
	for _, f := range nc.tempFiles {
		totalSize += f.Size
	}
	nc.updateStatus(fmt.Sprintf("Found: %d temp files (%s)", len(nc.tempFiles), FormatFileSize(totalSize)))
}

func (nc *NexaClean) deleteSelectedTempFiles() {
	var selected []TempFile
	for i, ok := range nc.tempSelected {
		if ok && i < len(nc.tempFiles) {
			selected = append(selected, nc.tempFiles[i])
		}
	}
	if len(selected) == 0 {
		dialog.ShowInformation("Info", "No temp files selected", nc.mainWindow)
		return
	}
	var totalSize int64
	for _, f := range selected {
		totalSize += f.Size
	}
	dialog.ShowConfirm("Confirm Delete",
		fmt.Sprintf("Delete %d files (%s)?", len(selected), FormatFileSize(totalSize)),
		func(ok bool) {
			if !ok {
				return
			}
			nc.updateStatus("Deleting temp files...")
			deleted := 0
			var deletedSize int64
			for _, f := range selected {
				if err := os.Remove(f.Path); err == nil {
					deleted++
					deletedSize += f.Size
				}
			}
			nc.stats.TempFilesDeleted += deleted
			nc.stats.TotalCleanedSize += deletedSize
			nc.stats.LastCleanupDate = time.Now().Format("2006-01-02 15:04:05")
			nc.stats.Save()
			nc.searchTempFiles()
			nc.refreshStatsDisplay()
			nc.updateStatus("Ready")
		}, nc.mainWindow,
	)
}

func (nc *NexaClean) deleteAllTempFiles() {
	if len(nc.tempFiles) == 0 {
		dialog.ShowInformation("Info", "No temp files found", nc.mainWindow)
		return
	}
	var totalSize int64
	for _, f := range nc.tempFiles {
		totalSize += f.Size
	}
	dialog.ShowConfirm("Confirm Delete",
		fmt.Sprintf("Delete all %d temp files?\nWarning: This cannot be undone!", len(nc.tempFiles)),
		func(ok bool) {
			if !ok {
				return
			}
			nc.updateStatus("Deleting all temp files...")
			deleted := 0
			var deletedSize int64
			for _, f := range nc.tempFiles {
				if err := os.Remove(f.Path); err == nil {
					deleted++
					deletedSize += f.Size
				}
			}
			nc.stats.TempFilesDeleted += deleted
			nc.stats.TotalCleanedSize += deletedSize
			nc.stats.LastCleanupDate = time.Now().Format("2006-01-02 15:04:05")
			nc.stats.Save()
			nc.searchTempFiles()
			nc.refreshStatsDisplay()
			nc.updateStatus("Ready")
		}, nc.mainWindow,
	)
}

func (nc *NexaClean) scanExtensions() {
	if nc.folderPath == "" {
		dialog.ShowInformation("Warning", "Please select a folder first", nc.mainWindow)
		return
	}
	if _, err := os.Stat(nc.folderPath); os.IsNotExist(err) {
		dialog.ShowError(err, nc.mainWindow)
		return
	}

	nc.updateStatus("Scanning extensions...")
	nc.extensions = make(map[string]int)

	entries, err := os.ReadDir(nc.folderPath)
	if err != nil {
		dialog.ShowError(err, nc.mainWindow)
		return
	}
	for _, entry := range entries {
		if !entry.IsDir() {
			ext := strings.ToLower(filepath.Ext(entry.Name()))
			if ext != "" {
				nc.extensions[ext]++
			}
		}
	}
	nc.extensionTable.Refresh()
	nc.updateStatus("Ready")
}

func (nc *NexaClean) organizeFiles() {
	if len(nc.extensions) == 0 {
		dialog.ShowInformation("Warning", "Please scan extensions first", nc.mainWindow)
		return
	}

	dialog.ShowConfirm("Confirm Operation", "Move all files to folders by extension?",
		func(ok bool) {
			if !ok {
				return
			}
			nc.updateStatus("Organizing files...")
			moved := 0
			for ext := range nc.extensions {
				folderName := strings.ToUpper(strings.TrimPrefix(ext, "."))
				targetFolder := filepath.Join(nc.folderPath, folderName)
				os.MkdirAll(targetFolder, 0755)
				entries, _ := os.ReadDir(nc.folderPath)
				for _, entry := range entries {
					if !entry.IsDir() && strings.ToLower(filepath.Ext(entry.Name())) == ext {
						src := filepath.Join(nc.folderPath, entry.Name())
						dst := filepath.Join(targetFolder, entry.Name())
						if _, err := os.Stat(dst); os.IsNotExist(err) {
							if err := os.Rename(src, dst); err == nil {
								moved++
							}
						} else if nc.duplicateMode == "overwrite" {
							os.Remove(dst)
							if err := os.Rename(src, dst); err == nil {
								moved++
							}
						}
					}
				}
			}
			nc.stats.FilesOrganized += moved
			nc.stats.LastCleanupDate = time.Now().Format("2006-01-02 15:04:05")
			nc.stats.Save()
			nc.scanExtensions()
			nc.refreshStatsDisplay()
			nc.updateStatus("Ready")
		}, nc.mainWindow,
	)
}

func (nc *NexaClean) refreshStatsDisplay() {
	data := map[string]string{
		"folders_deleted":    fmt.Sprintf("%d items", nc.stats.FoldersDeleted),
		"shortcuts_deleted":  fmt.Sprintf("%d items", nc.stats.ShortcutsDeleted),
		"temp_files_deleted": fmt.Sprintf("%d items", nc.stats.TempFilesDeleted),
		"files_organized":    fmt.Sprintf("%d items", nc.stats.FilesOrganized),
		"total_cleaned_size": FormatFileSize(nc.stats.TotalCleanedSize),
		"first_use_date":     nc.stats.FirstUseDate,
		"last_cleanup_date":  nc.stats.LastCleanupDate,
	}
	if nc.stats.LastCleanupDate == "" {
		data["last_cleanup_date"] = "Never"
	}
	for key, val := range data {
		if lbl, ok := nc.statsLabels[key]; ok {
			lbl.SetText(val)
		}
	}
}

func (nc *NexaClean) resetStats() {
	dialog.ShowConfirm("Confirm Reset", "Reset all statistics to defaults?",
		func(ok bool) {
			if !ok {
				return
			}
			nc.stats.Reset()
			nc.refreshStatsDisplay()
			dialog.ShowInformation("Success", "Statistics reset successfully", nc.mainWindow)
		}, nc.mainWindow,
	)
}

func (nc *NexaClean) exportReport() {
	content := "==================================================\n"
	content += "          NexaClean Report\n"
	content += "==================================================\n\n"
	content += fmt.Sprintf("Report generated: %s\n", time.Now().Format("2006-01-02 15:04:05"))
	content += fmt.Sprintf("First use: %s\n", nc.stats.FirstUseDate)
	content += fmt.Sprintf("Last cleanup: %s\n\n", nc.getStatValue("last_cleanup_date"))
	content += "Cleanup Statistics:\n"
	content += "------------------------------\n"
	content += fmt.Sprintf("Folders deleted: %d items\n", nc.stats.FoldersDeleted)
	content += fmt.Sprintf("Shortcuts managed: %d items\n", nc.stats.ShortcutsDeleted)
	content += fmt.Sprintf("Temp files deleted: %d items\n", nc.stats.TempFilesDeleted)
	content += fmt.Sprintf("Files organized: %d items\n", nc.stats.FilesOrganized)
	content += fmt.Sprintf("Space recovered: %s\n\n", FormatFileSize(nc.stats.TotalCleanedSize))
	content += nc.generateSummary()

	dialog.ShowFileSave(func(writer fyne.URIWriteCloser, err error) {
		if err != nil || writer == nil {
			return
		}
		defer writer.Close()
		writer.Write([]byte(content))
		dialog.ShowInformation("Success", "Report exported", nc.mainWindow)
	}, nc.mainWindow)
}

func (nc *NexaClean) getStatValue(key string) string {
	switch key {
	case "folders_deleted":
		return fmt.Sprintf("%d items", nc.stats.FoldersDeleted)
	case "shortcuts_deleted":
		return fmt.Sprintf("%d items", nc.stats.ShortcutsDeleted)
	case "temp_files_deleted":
		return fmt.Sprintf("%d items", nc.stats.TempFilesDeleted)
	case "files_organized":
		return fmt.Sprintf("%d items", nc.stats.FilesOrganized)
	case "total_cleaned_size":
		return FormatFileSize(nc.stats.TotalCleanedSize)
	case "first_use_date":
		return nc.stats.FirstUseDate
	case "last_cleanup_date":
		if nc.stats.LastCleanupDate == "" {
			return "Never"
		}
		return nc.stats.LastCleanupDate
	}
	return ""
}

func (nc *NexaClean) generateSummary() string {
	totalItems := nc.stats.FoldersDeleted + nc.stats.ShortcutsDeleted + nc.stats.TempFilesDeleted
	s := fmt.Sprintf("Overall Cleanup Summary\n\n")
	s += fmt.Sprintf("- Total items removed: %d\n", totalItems)
	s += fmt.Sprintf("- Space recovered: %s\n", FormatFileSize(nc.stats.TotalCleanedSize))
	s += fmt.Sprintf("- Files organized: %d\n\n", nc.stats.FilesOrganized)
	if totalItems == 0 {
		s += "Tip: Start cleaning using the tabs above"
	} else if totalItems < 10 {
		s += "Good job! Your Desktop is fairly clean"
	} else if totalItems < 50 {
		s += "Excellent! You've cleaned up a lot"
	} else {
		s += "Outstanding! You're a Desktop management pro"
	}
	s += fmt.Sprintf("\n\nLast updated: %s", time.Now().Format("2006-01-02 15:04"))
	return s
}

func sortedExts(m map[string]int) []string {
	keys := make([]string, 0, len(m))
	for k := range m {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	return keys
}

func main() {
	nc := NewNexaClean()
	nc.Run()
}
