# =============================================================================
# gui/styles.py
# Centralised style definitions for the entire app.
#
# ALL colours, fonts, padding, and widget configurations live here.
# No screen or widget file hardcodes colours or fonts directly —
# they import from this module so the entire look can be changed in one place.
#
# Usage:
#   from gui.styles import COLOURS, FONTS, apply_button_style
# =============================================================================

import tkinter as tk
from tkinter import ttk

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------

COLOURS = {
    # Backgrounds
    "bg_main":        "#1E2A38",   # deep navy — main window background
    "bg_card":        "#243447",   # slightly lighter navy — content cards
    "bg_sidebar":     "#16202C",   # darkest navy — sidebar panels
    "bg_header":      "#16202C",   # header bar
    "bg_input":       "#2C3E50",   # input fields
    "bg_correct":     "#1A3A2A",   # green tint — correct answer feedback
    "bg_incorrect":   "#3A1A1A",   # red tint — incorrect answer feedback
    "bg_highlight":   "#2C3E50",   # formula / code highlight boxes

    # Accent colours
    "accent_blue":    "#3498DB",   # primary action — buttons, links
    "accent_green":   "#2ECC71",   # success, correct, mastered
    "accent_orange":  "#E67E22",   # in-progress, practice phase
    "accent_red":     "#E74C3C",   # error, incorrect, warning
    "accent_gold":    "#F1C40F",   # badges, highlights, streaks
    "accent_purple":  "#9B59B6",   # evaluate phase accent

    # Text
    "text_primary":   "#ECF0F1",   # main text — near white
    "text_secondary": "#95A5A6",   # labels, subtitles — grey
    "text_muted":     "#566573",   # disabled, placeholder
    "text_dark":      "#1E2A38",   # text on light backgrounds
    "text_white":     "#FFFFFF",   # pure white for high contrast

    # Phase indicator colours
    "phase_locked":   "#566573",
    "phase_learn":    "#3498DB",
    "phase_practice": "#E67E22",
    "phase_evaluate": "#9B59B6",
    "phase_mastered": "#F1C40F",

    # Progress bar
    "bar_bg":         "#2C3E50",
    "bar_fill":       "#2ECC71",

    # Borders / dividers
    "border":         "#2C3E50",
    "divider":        "#243447",
}

# ---------------------------------------------------------------------------
# Fonts
# Tuples of (family, size, weight) — passed directly to Tkinter font= params
# ---------------------------------------------------------------------------

FONTS = {
    "title":        ("Helvetica", 24, "bold"),
    "heading":      ("Helvetica", 18, "bold"),
    "subheading":   ("Helvetica", 14, "bold"),
    "body":         ("Helvetica", 12, "normal"),
    "body_bold":    ("Helvetica", 12, "bold"),
    "small":        ("Helvetica", 10, "normal"),
    "small_bold":   ("Helvetica", 10, "bold"),
    "tiny":         ("Helvetica", 9,  "normal"),
    "mono":         ("Courier",   13, "normal"),   # math expressions
    "mono_large":   ("Courier",   16, "bold"),     # worked example steps
    "mono_small":   ("Courier",   11, "normal"),   # inline formulas
    "button":       ("Helvetica", 12, "bold"),
    "button_small": ("Helvetica", 10, "bold"),
}

# ---------------------------------------------------------------------------
# Padding / spacing constants
# ---------------------------------------------------------------------------

PAD = {
    "xs":   4,
    "sm":   8,
    "md":   16,
    "lg":   24,
    "xl":   40,
    "xxl":  60,
}

# ---------------------------------------------------------------------------
# Widget style helpers
# These functions return a dict of kwargs you spread into widget constructors
# ---------------------------------------------------------------------------

def card_style() -> dict:
    """Style for a content card Frame."""
    return {
        "bg":           COLOURS["bg_card"],
        "relief":       "flat",
        "bd":           0,
        "highlightthickness": 1,
        "highlightbackground": COLOURS["border"],
    }


def header_style() -> dict:
    """Style for the top header bar Frame."""
    return {
        "bg":    COLOURS["bg_header"],
        "relief": "flat",
        "bd":    0,
    }


def label_style(size: str = "body", colour: str = "text_primary") -> dict:
    """Style for a standard Label."""
    return {
        "bg":   COLOURS["bg_main"],
        "fg":   COLOURS[colour],
        "font": FONTS[size],
    }


def card_label_style(size: str = "body", colour: str = "text_primary") -> dict:
    """Style for a Label sitting on a card background."""
    return {
        "bg":   COLOURS["bg_card"],
        "fg":   COLOURS[colour],
        "font": FONTS[size],
    }


def mono_label_style(size: str = "mono") -> dict:
    """Style for a monospace math expression Label."""
    return {
        "bg":   COLOURS["bg_highlight"],
        "fg":   COLOURS["accent_gold"],
        "font": FONTS[size],
    }


def input_style() -> dict:
    """Style for answer Entry widgets."""
    return {
        "bg":                  COLOURS["bg_input"],
        "fg":                  COLOURS["text_primary"],
        "insertbackground":    COLOURS["text_primary"],   # cursor colour
        "font":                FONTS["mono_large"],
        "relief":              "flat",
        "bd":                  0,
        "highlightthickness":  2,
        "highlightcolor":      COLOURS["accent_blue"],
        "highlightbackground": COLOURS["border"],
    }


# ---------------------------------------------------------------------------
# Button factory
# Returns a tk.Button with consistent styling.
# Call with the parent widget and a variant name.
# ---------------------------------------------------------------------------

BUTTON_VARIANTS = {
    "primary": {
        "bg":              COLOURS["accent_blue"],
        "fg":              COLOURS["text_white"],
        "activebackground":"#2980B9",
        "activeforeground":COLOURS["text_white"],
    },
    "success": {
        "bg":              COLOURS["accent_green"],
        "fg":              COLOURS["text_dark"],
        "activebackground":"#27AE60",
        "activeforeground":COLOURS["text_dark"],
    },
    "warning": {
        "bg":              COLOURS["accent_orange"],
        "fg":              COLOURS["text_white"],
        "activebackground":"#D35400",
        "activeforeground":COLOURS["text_white"],
    },
    "danger": {
        "bg":              COLOURS["accent_red"],
        "fg":              COLOURS["text_white"],
        "activebackground":"#C0392B",
        "activeforeground":COLOURS["text_white"],
    },
    "gold": {
        "bg":              COLOURS["accent_gold"],
        "fg":              COLOURS["text_dark"],
        "activebackground":"#D4AC0D",
        "activeforeground":COLOURS["text_dark"],
    },
    "ghost": {
        "bg":              COLOURS["bg_card"],
        "fg":              COLOURS["text_secondary"],
        "activebackground":COLOURS["bg_highlight"],
        "activeforeground":COLOURS["text_primary"],
    },
    "sidebar": {
        "bg":              COLOURS["bg_sidebar"],
        "fg":              COLOURS["text_primary"],
        "activebackground":COLOURS["bg_card"],
        "activeforeground":COLOURS["text_white"],
    },
}


def make_button(
    parent,
    text: str,
    command,
    variant: str = "primary",
    size: str = "button",
    width: int = None,
    pady: int = 10,
    padx: int = 20,
) -> tk.Button:
    """
    Create and return a styled tk.Button.

    Parameters:
        parent   : parent widget
        text     : button label
        command  : callback function
        variant  : one of BUTTON_VARIANTS keys
        size     : font size key from FONTS
        width    : optional fixed character width
        pady     : internal vertical padding
        padx     : internal horizontal padding
    """
    styles  = BUTTON_VARIANTS.get(variant, BUTTON_VARIANTS["primary"])
    kwargs  = {
        "text":              text,
        "command":           command,
        "font":              FONTS[size],
        "relief":            "flat",
        "cursor":            "hand2",
        "bd":                0,
        "padx":              padx,
        "pady":              pady,
        **styles,
    }
    if width is not None:
        kwargs["width"] = width

    btn = tk.Button(parent, **kwargs)

    # Subtle hover effect
    original_bg     = styles["bg"]
    active_bg       = styles["activebackground"]

    def on_enter(e):
        btn.config(bg=active_bg)

    def on_leave(e):
        btn.config(bg=original_bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    return btn


# ---------------------------------------------------------------------------
# Phase badge colours (used in topic cards)
# ---------------------------------------------------------------------------

def phase_colour(status: str) -> str:
    """Return the accent colour for a given phase status string."""
    mapping = {
        "not_started":  COLOURS["text_muted"],
        "in_progress":  COLOURS["accent_orange"],
        "complete":     COLOURS["accent_green"],
        "locked":       COLOURS["phase_locked"],
        "mastered":     COLOURS["accent_gold"],
    }
    return mapping.get(status, COLOURS["text_muted"])


def phase_dot(status: str) -> str:
    """Return a Unicode dot character styled for a phase status."""
    if status in ("complete", "mastered"):
        return "●"
    if status == "in_progress":
        return "◑"
    if status == "locked":
        return "○"
    return "○"   # not_started


# ---------------------------------------------------------------------------
# ttk style configuration (for Scrollbar and Progressbar widgets)
# Call configure_ttk_styles(root) once from app_root.py after root is created
# ---------------------------------------------------------------------------

def configure_ttk_styles(root: tk.Tk) -> None:
    """
    Apply dark-theme styles to ttk widgets.
    Must be called after the Tk root window is created.
    """
    style = ttk.Style(root)
    style.theme_use("default")

    # Scrollbar
    style.configure(
        "Dark.Vertical.TScrollbar",
        background=COLOURS["bg_card"],
        troughcolor=COLOURS["bg_sidebar"],
        arrowcolor=COLOURS["text_secondary"],
        bordercolor=COLOURS["bg_sidebar"],
        lightcolor=COLOURS["bg_card"],
        darkcolor=COLOURS["bg_sidebar"],
    )

    # Progress bar
    style.configure(
        "Green.Horizontal.TProgressbar",
        troughcolor=COLOURS["bar_bg"],
        background=COLOURS["bar_fill"],
        thickness=12,
    )

    style.configure(
        "Gold.Horizontal.TProgressbar",
        troughcolor=COLOURS["bar_bg"],
        background=COLOURS["accent_gold"],
        thickness=12,
    )