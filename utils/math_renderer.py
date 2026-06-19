# =============================================================================
# utils/math_renderer.py
# Utilities for formatting and cleaning math text for Tkinter display.
#
# Tkinter cannot render LaTeX or MathML — everything is plain text.
# These helpers make math expressions readable using Unicode characters
# and consistent spacing conventions.
#
# Used by: learn_screen.py, practice_screen.py, problem_screen.py
# =============================================================================

# ---------------------------------------------------------------------------
# Unicode math symbols available in most system fonts
# ---------------------------------------------------------------------------

SYMBOLS = {
    # Arithmetic
    "times":        "×",
    "divide":       "÷",
    "plus_minus":   "±",
    "not_equal":    "≠",

    # Comparison
    "leq":          "≤",    # less than or equal
    "geq":          "≥",    # greater than or equal
    "approx":       "≈",

    # Algebra
    "squared":      "²",
    "cubed":        "³",
    "sqrt":         "√",
    "infinity":     "∞",

    # Greek
    "pi":           "π",
    "theta":        "θ",
    "alpha":        "α",

    # Misc
    "degree":       "°",
    "bullet":       "•",
    "arrow_right":  "→",
    "checkmark":    "✓",
    "cross":        "✗",
}


# ---------------------------------------------------------------------------
# Text substitution helpers
# ---------------------------------------------------------------------------

def apply_symbols(text: str) -> str:
    """
    Replace ASCII math shorthand with Unicode symbols for cleaner display.

    Conversions applied:
        **2   →  ²
        **3   →  ³
        >=    →  ≥
        <=    →  ≤
        !=    →  ≠
        ~=    →  ≈
        sqrt  →  √
        pi    →  π
        deg   →  °
    """
    replacements = [
        ("**2",  "²"),
        ("**3",  "³"),
        (">=",   "≥"),
        ("<=",   "≤"),
        ("!=",   "≠"),
        ("~=",   "≈"),
        ("sqrt", "√"),
        (" pi ", " π "),
        ("deg",  "°"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def format_question(text: str) -> str:
    """
    Prepare a problem question string for display in the problem screen.
    - Applies Unicode symbol substitution
    - Normalises whitespace around operators
    - Strips leading/trailing whitespace
    """
    text = apply_symbols(text)
    text = text.strip()
    return text


def format_step(description: str, working: str) -> tuple[str, str]:
    """
    Format one step of a worked example.
    Returns (formatted_description, formatted_working).
    """
    return description.strip(), apply_symbols(working.strip())


def format_explanation(text: str) -> str:
    """
    Format a multi-line explanation string for display.
    Applies symbol substitution and normalises line endings.
    """
    text = apply_symbols(text)
    # Normalise Windows line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.strip()


def format_formula(text: str) -> str:
    """
    Format a formula string for display in a highlighted formula box.
    Centred, with symbol substitution applied.
    """
    if not text:
        return ""
    return apply_symbols(text.strip())


# ---------------------------------------------------------------------------
# Answer formatting
# ---------------------------------------------------------------------------

def format_answer_for_display(answer) -> str:
    """
    Convert any answer value to a clean display string.

    Examples:
        3       →  "3"
        3.0     →  "3"
        3.5     →  "3.5"
        0.3333  →  "0.3333"
    """
    if isinstance(answer, float):
        # Show as integer if it's a whole number
        if answer == int(answer):
            return str(int(answer))
        return str(answer)
    return str(answer)


def clean_student_input(text: str) -> str:
    """
    Clean and normalise student input before passing to the evaluator.
    - Strips whitespace
    - Replaces common alternatives: 'x' as multiply, etc.
    - Does NOT attempt to evaluate — just normalises
    """
    text = text.strip()
    # Allow students to type "3.0" or "3" — evaluator handles both
    return text


# ---------------------------------------------------------------------------
# Progress / score display helpers
# ---------------------------------------------------------------------------

def format_score(correct: int, total: int) -> str:
    """Return a formatted score string: '7 / 10  (70%)'"""
    pct = int((correct / total) * 100) if total > 0 else 0
    return f"{correct} / {total}  ({pct}%)"


def format_streak(streak: int) -> str:
    """Return a streak display string with fire emoji for milestones."""
    if streak == 0:
        return ""
    if streak >= 5:
        return f"🔥 {streak} in a row!"
    if streak >= 3:
        return f"✓ {streak} in a row"
    return f"✓ {streak}"


def format_elapsed_time(seconds: int) -> str:
    """Convert seconds to mm:ss display string."""
    minutes = seconds // 60
    secs    = seconds % 60
    return f"{minutes}:{secs:02d}"


def phase_label(phase: str) -> str:
    """Return a human-readable phase label."""
    labels = {
        "learn":    "Learn",
        "practice": "Practice",
        "evaluate": "Evaluate",
    }
    return labels.get(phase, phase.title())


def difficulty_label(difficulty: str) -> str:
    """Return a display label for a difficulty level."""
    labels = {
        "easy":   "Beginner",
        "medium": "Intermediate",
        "hard":   "Advanced",
    }
    return labels.get(difficulty, difficulty.title())