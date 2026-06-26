package main

import "image/color"

type Theme struct {
	Name       string
	BgDark     color.NRGBA
	BgCard     color.NRGBA
	BgInput    color.NRGBA
	Accent     color.NRGBA
	AccentGreen color.NRGBA
	AccentBlue  color.NRGBA
	AccentOrange color.NRGBA
	TextPrimary  color.NRGBA
	TextSecondary color.NRGBA
	Success    color.NRGBA
	Danger     color.NRGBA
	Warning    color.NRGBA
}

var themes = map[string]Theme{
	"Macrium Dark": {
		Name:        "Macrium Dark",
		BgDark:      color.NRGBA{R: 28, G: 28, B: 28, A: 255},
		BgCard:      color.NRGBA{R: 45, G: 45, B: 45, A: 255},
		BgInput:     color.NRGBA{R: 58, G: 58, B: 58, A: 255},
		Accent:      color.NRGBA{R: 232, G: 133, B: 12, A: 255},
		AccentGreen: color.NRGBA{R: 92, G: 184, B: 92, A: 255},
		AccentBlue:  color.NRGBA{R: 91, G: 192, B: 222, A: 255},
		AccentOrange: color.NRGBA{R: 232, G: 133, B: 12, A: 255},
		TextPrimary:  color.NRGBA{R: 224, G: 224, B: 224, A: 255},
		TextSecondary: color.NRGBA{R: 153, G: 153, B: 153, A: 255},
		Success: color.NRGBA{R: 92, G: 184, B: 92, A: 255},
		Danger:  color.NRGBA{R: 217, G: 83, B: 79, A: 255},
		Warning: color.NRGBA{R: 232, G: 133, B: 12, A: 255},
	},
	"Dark Neon": {
		Name:        "Dark Neon",
		BgDark:      color.NRGBA{R: 26, G: 26, B: 46, A: 255},
		BgCard:      color.NRGBA{R: 22, G: 33, B: 62, A: 255},
		BgInput:     color.NRGBA{R: 15, G: 52, B: 96, A: 255},
		Accent:      color.NRGBA{R: 233, G: 69, B: 96, A: 255},
		AccentGreen: color.NRGBA{R: 0, G: 212, B: 170, A: 255},
		AccentBlue:  color.NRGBA{R: 67, G: 97, B: 238, A: 255},
		AccentOrange: color.NRGBA{R: 255, G: 107, B: 53, A: 255},
		TextPrimary:  color.NRGBA{R: 255, G: 255, B: 255, A: 255},
		TextSecondary: color.NRGBA{R: 160, G: 160, B: 176, A: 255},
		Success: color.NRGBA{R: 0, G: 212, B: 170, A: 255},
		Danger:  color.NRGBA{R: 233, G: 69, B: 96, A: 255},
		Warning: color.NRGBA{R: 255, G: 107, B: 53, A: 255},
	},
	"Light Clean": {
		Name:        "Light Clean",
		BgDark:      color.NRGBA{R: 245, G: 245, B: 245, A: 255},
		BgCard:      color.NRGBA{R: 255, G: 255, B: 255, A: 255},
		BgInput:     color.NRGBA{R: 232, G: 232, B: 232, A: 255},
		Accent:      color.NRGBA{R: 59, G: 130, B: 246, A: 255},
		AccentGreen: color.NRGBA{R: 34, G: 197, B: 94, A: 255},
		AccentBlue:  color.NRGBA{R: 59, G: 130, B: 246, A: 255},
		AccentOrange: color.NRGBA{R: 249, G: 115, B: 22, A: 255},
		TextPrimary:  color.NRGBA{R: 31, G: 41, B: 55, A: 255},
		TextSecondary: color.NRGBA{R: 107, G: 114, B: 128, A: 255},
		Success: color.NRGBA{R: 34, G: 197, B: 94, A: 255},
		Danger:  color.NRGBA{R: 239, G: 68, B: 68, A: 255},
		Warning: color.NRGBA{R: 249, G: 115, B: 22, A: 255},
	},
	"Ocean Blue": {
		Name:        "Ocean Blue",
		BgDark:      color.NRGBA{R: 10, G: 25, B: 41, A: 255},
		BgCard:      color.NRGBA{R: 19, G: 47, B: 76, A: 255},
		BgInput:     color.NRGBA{R: 26, G: 58, B: 92, A: 255},
		Accent:      color.NRGBA{R: 0, G: 119, B: 182, A: 255},
		AccentGreen: color.NRGBA{R: 6, G: 214, B: 160, A: 255},
		AccentBlue:  color.NRGBA{R: 0, G: 150, B: 199, A: 255},
		AccentOrange: color.NRGBA{R: 252, G: 163, B: 17, A: 255},
		TextPrimary:  color.NRGBA{R: 255, G: 255, B: 255, A: 255},
		TextSecondary: color.NRGBA{R: 148, G: 163, B: 184, A: 255},
		Success: color.NRGBA{R: 6, G: 214, B: 160, A: 255},
		Danger:  color.NRGBA{R: 230, G: 57, B: 70, A: 255},
		Warning: color.NRGBA{R: 252, G: 163, B: 17, A: 255},
	},
	"Forest Green": {
		Name:        "Forest Green",
		BgDark:      color.NRGBA{R: 26, G: 47, B: 26, A: 255},
		BgCard:      color.NRGBA{R: 45, G: 74, B: 45, A: 255},
		BgInput:     color.NRGBA{R: 61, G: 92, B: 61, A: 255},
		Accent:      color.NRGBA{R: 74, G: 222, B: 128, A: 255},
		AccentGreen: color.NRGBA{R: 34, G: 197, B: 94, A: 255},
		AccentBlue:  color.NRGBA{R: 96, G: 165, B: 250, A: 255},
		AccentOrange: color.NRGBA{R: 251, G: 191, B: 36, A: 255},
		TextPrimary:  color.NRGBA{R: 255, G: 255, B: 255, A: 255},
		TextSecondary: color.NRGBA{R: 163, G: 190, B: 140, A: 255},
		Success: color.NRGBA{R: 34, G: 197, B: 94, A: 255},
		Danger:  color.NRGBA{R: 248, G: 113, B: 113, A: 255},
		Warning: color.NRGBA{R: 251, G: 191, B: 36, A: 255},
	},
	"Sunset Orange": {
		Name:        "Sunset Orange",
		BgDark:      color.NRGBA{R: 45, G: 27, B: 27, A: 255},
		BgCard:      color.NRGBA{R: 61, G: 37, B: 37, A: 255},
		BgInput:     color.NRGBA{R: 77, G: 48, B: 48, A: 255},
		Accent:      color.NRGBA{R: 251, G: 146, B: 60, A: 255},
		AccentGreen: color.NRGBA{R: 74, G: 222, B: 128, A: 255},
		AccentBlue:  color.NRGBA{R: 96, G: 165, B: 250, A: 255},
		AccentOrange: color.NRGBA{R: 249, G: 115, B: 22, A: 255},
		TextPrimary:  color.NRGBA{R: 255, G: 255, B: 255, A: 255},
		TextSecondary: color.NRGBA{R: 212, G: 165, B: 116, A: 255},
		Success: color.NRGBA{R: 74, G: 222, B: 128, A: 255},
		Danger:  color.NRGBA{R: 248, G: 113, B: 113, A: 255},
		Warning: color.NRGBA{R: 251, G: 191, B: 36, A: 255},
	},
	"Purple Haze": {
		Name:        "Purple Haze",
		BgDark:      color.NRGBA{R: 30, G: 16, B: 51, A: 255},
		BgCard:      color.NRGBA{R: 42, G: 24, B: 69, A: 255},
		BgInput:     color.NRGBA{R: 58, G: 37, B: 85, A: 255},
		Accent:      color.NRGBA{R: 168, G: 85, B: 247, A: 255},
		AccentGreen: color.NRGBA{R: 74, G: 222, B: 128, A: 255},
		AccentBlue:  color.NRGBA{R: 129, G: 140, B: 248, A: 255},
		AccentOrange: color.NRGBA{R: 251, G: 146, B: 60, A: 255},
		TextPrimary:  color.NRGBA{R: 255, G: 255, B: 255, A: 255},
		TextSecondary: color.NRGBA{R: 196, G: 181, B: 253, A: 255},
		Success: color.NRGBA{R: 74, G: 222, B: 128, A: 255},
		Danger:  color.NRGBA{R: 248, G: 113, B: 113, A: 255},
		Warning: color.NRGBA{R: 251, G: 146, B: 60, A: 255},
	},
	"Glitch Purple": {
		Name:        "Glitch Purple",
		BgDark:      color.NRGBA{R: 240, G: 232, B: 255, A: 255},
		BgCard:      color.NRGBA{R: 255, G: 255, B: 255, A: 255},
		BgInput:     color.NRGBA{R: 232, G: 223, B: 245, A: 255},
		Accent:      color.NRGBA{R: 139, G: 92, B: 246, A: 255},
		AccentGreen: color.NRGBA{R: 34, G: 197, B: 94, A: 255},
		AccentBlue:  color.NRGBA{R: 99, G: 102, B: 241, A: 255},
		AccentOrange: color.NRGBA{R: 249, G: 115, B: 22, A: 255},
		TextPrimary:  color.NRGBA{R: 30, G: 27, B: 75, A: 255},
		TextSecondary: color.NRGBA{R: 107, G: 114, B: 128, A: 255},
		Success: color.NRGBA{R: 34, G: 197, B: 94, A: 255},
		Danger:  color.NRGBA{R: 239, G: 68, B: 68, A: 255},
		Warning: color.NRGBA{R: 249, G: 115, B: 22, A: 255},
	},
	"Retro Purple": {
		Name:        "Retro Purple",
		BgDark:      color.NRGBA{R: 26, G: 16, B: 37, A: 255},
		BgCard:      color.NRGBA{R: 42, G: 29, B: 61, A: 255},
		BgInput:     color.NRGBA{R: 58, G: 45, B: 82, A: 255},
		Accent:      color.NRGBA{R: 179, G: 136, B: 255, A: 255},
		AccentGreen: color.NRGBA{R: 165, G: 214, B: 167, A: 255},
		AccentBlue:  color.NRGBA{R: 144, G: 202, B: 249, A: 255},
		AccentOrange: color.NRGBA{R: 255, G: 204, B: 128, A: 255},
		TextPrimary:  color.NRGBA{R: 232, G: 213, B: 245, A: 255},
		TextSecondary: color.NRGBA{R: 149, G: 117, B: 205, A: 255},
		Success: color.NRGBA{R: 165, G: 214, B: 167, A: 255},
		Danger:  color.NRGBA{R: 239, G: 154, B: 154, A: 255},
		Warning: color.NRGBA{R: 255, G: 204, B: 128, A: 255},
	},
}

func getThemeNames() []string {
	names := make([]string, 0, len(themes))
	for name := range themes {
		names = append(names, name)
	}
	return names
}

func hexToNRGBA(hex string) color.NRGBA {
	r, g, b := 0, 0, 0
	if len(hex) == 7 {
		vals := []int{}
		for i := 1; i < 7; i += 2 {
			v := 0
			for _, c := range hex[i : i+2] {
				v *= 16
				if c >= '0' && c <= '9' {
					v += int(c - '0')
				} else if c >= 'a' && c <= 'f' {
					v += int(c-'a') + 10
				} else if c >= 'A' && c <= 'F' {
					v += int(c-'A') + 10
				}
			}
			vals = append(vals, v)
		}
		r, g, b = vals[0], vals[1], vals[2]
	}
	return color.NRGBA{R: uint8(r), G: uint8(g), B: uint8(b), A: 255}
}
