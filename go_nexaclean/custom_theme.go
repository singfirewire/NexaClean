package main

import (
	"image/color"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/theme"
)

type NexaCleanTheme struct {
	colors *Theme
}

var _ fyne.Theme = (*NexaCleanTheme)(nil)

func (t *NexaCleanTheme) Color(name fyne.ThemeColorName, variant fyne.ThemeVariant) color.Color {
	switch name {
	case theme.ColorNameBackground:
		return t.colors.BgDark
	case theme.ColorNameButton:
		return t.colors.AccentBlue
	case theme.ColorNameDisabledButton:
		return t.colors.BgInput
	case theme.ColorNameForeground:
		return t.colors.TextPrimary
	case theme.ColorNamePlaceHolder:
		return t.colors.TextSecondary
	case theme.ColorNameHover:
		return lightenNRGBA(t.colors.AccentBlue, 1.2)
	case theme.ColorNamePressed:
		return darkenNRGBA(t.colors.AccentBlue, 0.8)
	case theme.ColorNamePrimary:
		return t.colors.Accent
	case theme.ColorNameHeaderBackground:
		return t.colors.BgCard
	case theme.ColorNameSeparator:
		return t.colors.BgInput
	case theme.ColorNameOverlayBackground:
		return t.colors.BgCard
	case theme.ColorNameInputBackground:
		return t.colors.BgInput
	case theme.ColorNameScrollBar:
		return t.colors.BgInput
	case theme.ColorNameShadow:
		return color.NRGBA{R: 0, G: 0, B: 0, A: 80}
	case theme.ColorNameSuccess:
		return t.colors.Success
	case theme.ColorNameWarning:
		return t.colors.Warning
	case theme.ColorNameError:
		return t.colors.Danger
	}

	if variant == theme.VariantDark {
		return color.NRGBA{R: 30, G: 30, B: 30, A: 255}
	}
	return color.NRGBA{R: 245, G: 245, B: 245, A: 255}
}

func (t *NexaCleanTheme) Font(style fyne.TextStyle) fyne.Resource {
	return theme.DefaultTheme().Font(style)
}

func (t *NexaCleanTheme) Icon(name fyne.ThemeIconName) fyne.Resource {
	return theme.DefaultTheme().Icon(name)
}

func (t *NexaCleanTheme) Size(name fyne.ThemeSizeName) float32 {
	switch name {
	case theme.SizeNameText:
		return 14
	case theme.SizeNameSubHeadingText:
		return 16
	case theme.SizeNameHeadingText:
		return 20
	case theme.SizeNameCaptionText:
		return 11
	case theme.SizeNameInputBorder:
		return 2
	}
	return theme.DefaultTheme().Size(name)
}

func lightenNRGBA(c color.NRGBA, factor float64) color.NRGBA {
	r := float64(c.R) * factor
	g := float64(c.G) * factor
	b := float64(c.B) * factor
	if r > 255 {
		r = 255
	}
	if g > 255 {
		g = 255
	}
	if b > 255 {
		b = 255
	}
	return color.NRGBA{R: uint8(r), G: uint8(g), B: uint8(b), A: c.A}
}

func darkenNRGBA(c color.NRGBA, factor float64) color.NRGBA {
	r := float64(c.R) * factor
	g := float64(c.G) * factor
	b := float64(c.B) * factor
	return color.NRGBA{R: uint8(r), G: uint8(g), B: uint8(b), A: c.A}
}
