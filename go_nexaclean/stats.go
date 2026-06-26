package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"time"
)

type Stats struct {
	FoldersDeleted   int    `json:"folders_deleted"`
	ShortcutsDeleted int    `json:"shortcuts_deleted"`
	TempFilesDeleted int    `json:"temp_files_deleted"`
	FilesOrganized   int    `json:"files_organized"`
	TotalCleanedSize int64  `json:"total_cleaned_size"`
	FirstUseDate     string `json:"first_use_date"`
	LastCleanupDate  string `json:"last_cleanup_date"`
	Theme            string `json:"theme"`
}

func NewStats() *Stats {
	return &Stats{
		FirstUseDate: time.Now().Format("2006-01-02 15:04:05"),
	}
}

func (s *Stats) GetStatsPath() string {
	exePath, err := os.Executable()
	if err != nil {
		return "nexaclean_stats.json"
	}
	return filepath.Join(filepath.Dir(exePath), "nexaclean_stats.json")
}

func (s *Stats) Load() {
	data, err := os.ReadFile(s.GetStatsPath())
	if err != nil {
		return
	}
	var saved Stats
	if err := json.Unmarshal(data, &saved); err != nil {
		return
	}
	s.FoldersDeleted = saved.FoldersDeleted
	s.ShortcutsDeleted = saved.ShortcutsDeleted
	s.TempFilesDeleted = saved.TempFilesDeleted
	s.FilesOrganized = saved.FilesOrganized
	s.TotalCleanedSize = saved.TotalCleanedSize
	s.FirstUseDate = saved.FirstUseDate
	s.LastCleanupDate = saved.LastCleanupDate
	s.Theme = saved.Theme
}

func (s *Stats) Save() {
	data, err := json.MarshalIndent(s, "", "  ")
	if err != nil {
		return
	}
	os.WriteFile(s.GetStatsPath(), data, 0644)
}

func (s *Stats) Reset() {
	now := time.Now().Format("2006-01-02 15:04:05")
	s.FoldersDeleted = 0
	s.ShortcutsDeleted = 0
	s.TempFilesDeleted = 0
	s.FilesOrganized = 0
	s.TotalCleanedSize = 0
	s.FirstUseDate = now
	s.LastCleanupDate = ""
	s.Save()
}

func FormatFileSize(sizeBytes int64) string {
	if sizeBytes == 0 {
		return "0 B"
	}
	units := []string{"B", "KB", "MB", "GB"}
	size := float64(sizeBytes)
	i := 0
	for size >= 1024 && i < len(units)-1 {
		size /= 1024
		i++
	}
	if i == 0 {
		return "0 B"
	}
	return formatFloat(size) + " " + units[i]
}

func formatFloat(f float64) string {
	intPart := int64(f)
	fracPart := f - float64(intPart)
	fracInt := int64(fracPart * 10)
	if fracInt < 0 {
		fracInt = -fracInt
	}
	return itoa(intPart) + "." + itoa(fracInt)
}

func itoa(n int64) string {
	if n == 0 {
		return "0"
	}
	result := ""
	neg := false
	if n < 0 {
		neg = true
		n = -n
	}
	for n > 0 {
		result = string(rune('0'+n%10)) + result
		n /= 10
	}
	if neg {
		result = "-" + result
	}
	return result
}
