# =============================================================================
# utils/file_io.py
# Cross-platform file I/O helpers.
#
# Responsibilities:
#   - Determine the correct writable save-data directory per OS
#     (macOS: ~/Library/Application Support/MathLearningApp/)
#     (Windows: C:\Users\name\AppData\Roaming\MathLearningApp\)
#   - Resolve resource paths for bundled assets so PyInstaller .app works
#   - Safe JSON read / write with error handling
#   - Initialise default data files on first run
# =============================================================================

import os
import sys
import json
import logging

from config import APP_NAME

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Directory resolution
# ---------------------------------------------------------------------------

def get_data_dir() -> str:
    """
    Return the writable directory where save data lives.

    Development  : <project_root>/data/
    macOS .app   : ~/Library/Application Support/MathLearningApp/
    Windows .exe : C:\\Users\\<name>\\AppData\\Roaming\\MathLearningApp\\

    The directory is created if it does not exist.
    """
    if getattr(sys, "frozen", False):
        # Running inside a PyInstaller bundle
        if sys.platform == "darwin":
            base = os.path.expanduser("~/Library/Application Support")
        elif sys.platform == "win32":
            base = os.environ.get("APPDATA", os.path.expanduser("~"))
        else:
            base = os.path.expanduser("~/.local/share")
        data_dir = os.path.join(base, APP_NAME)
    else:
        # Development: use the data/ folder at the project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_root, "data")

    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def resource_path(relative_path: str) -> str:
    """
    Resolve the absolute path to a bundled resource (image, font, etc.).

    In development  : resolves relative to the project root.
    In PyInstaller  : resolves relative to sys._MEIPASS (temp extraction dir).

    Usage:
        icon = tk.PhotoImage(file=resource_path("assets/badge_gold.png"))
    """
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)


# ---------------------------------------------------------------------------
# Path helpers for specific files
# ---------------------------------------------------------------------------

def get_progress_path() -> str:
    """Absolute path to progress.json in the writable data directory."""
    return os.path.join(get_data_dir(), "progress.json")


def get_session_log_path() -> str:
    """Absolute path to session_log.json in the writable data directory."""
    return os.path.join(get_data_dir(), "session_log.json")


def get_log_path() -> str:
    """Absolute path to app.log in the writable data directory."""
    return os.path.join(get_data_dir(), "app.log")


# ---------------------------------------------------------------------------
# JSON I/O
# ---------------------------------------------------------------------------

def read_json(filepath: str):
    """
    Read and return the contents of a JSON file.

    Returns an empty dict {} if the file does not exist or cannot be parsed.
    Never raises — errors are logged and a safe default is returned.
    """
    if not os.path.exists(filepath):
        logger.debug("read_json: file not found, returning {}: %s", filepath)
        return {}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error("read_json: JSON parse error in %s: %s", filepath, e)
        return {}
    except OSError as e:
        logger.error("read_json: OS error reading %s: %s", filepath, e)
        return {}


def write_json(filepath: str, data) -> bool:
    """
    Write data to a JSON file (pretty-printed, UTF-8).

    Returns True on success, False on failure.
    Uses atomic write (temp file + rename) to prevent corrupt saves.
    Never raises — errors are logged.
    """
    try:
        tmp_path = filepath + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, filepath)   # atomic on POSIX and Windows
        logger.debug("write_json: saved %s", filepath)
        return True
    except OSError as e:
        logger.error("write_json: OS error writing %s: %s", filepath, e)
        return False


# ---------------------------------------------------------------------------
# Default topic record  (helper used by DEFAULT_PROGRESS below)
# ---------------------------------------------------------------------------

def _make_topic_default(locked: bool = False) -> dict:
    """Return the default per-topic progress record."""
    status = "locked" if locked else "not_started"
    return {
        "learn": {
            "status": status,
        },
        "practice": {
            "status":      status,
            "best_streak": 0,
            "attempts":    0,
        },
        "evaluate": {
            "status":     status,
            "attempts":   0,
            "best_score": 0,
            "mastered":   False,
            "difficulty": "easy",
        },
    }


# ---------------------------------------------------------------------------
# Default progress structure  (written to progress.json on first launch)
# ---------------------------------------------------------------------------

DEFAULT_PROGRESS = {
    "student_name": "",
    "algebra": {
        "linear_equations":   _make_topic_default(),
        "inequalities":       _make_topic_default(),
        "quadratics":         _make_topic_default(),
        "exponents_radicals": _make_topic_default(),
        "word_problems":      _make_topic_default(),
    },
    "geometry": {
        "status":              "locked",
        "angles_lines":        _make_topic_default(locked=True),
        "triangles":           _make_topic_default(locked=True),
        "polygons":            _make_topic_default(locked=True),
        "circles":             _make_topic_default(locked=True),
        "coordinate_geometry": _make_topic_default(locked=True),
    },
    "advanced": {
        "status":              "locked",
        "linear_functions":    _make_topic_default(locked=True),
        "systems_of_equations":_make_topic_default(locked=True),
        "similar_triangles":   _make_topic_default(locked=True),
        "trigonometry":        _make_topic_default(locked=True),
        "parabolas_graphs":    _make_topic_default(locked=True),
        "circle_equations":    _make_topic_default(locked=True),
        "solid_geometry":      _make_topic_default(locked=True),
    },
    "cat_history": {
        "pretest": [],
        "final":   [],
    },
}

# Maximum number of CAT results kept per mode — oldest are dropped first.
_CAT_HISTORY_LIMIT = 10


# ---------------------------------------------------------------------------
# First-run initialisation  (called once from main.py at startup)
# ---------------------------------------------------------------------------

def initialise_progress_if_missing() -> None:
    """
    Write DEFAULT_PROGRESS to progress.json only if the file does not
    already exist or is empty. Safe to call on every launch.
    """
    path = get_progress_path()
    existing = read_json(path)
    if not existing:
        logger.info("First launch — creating default progress.json")
        write_json(path, DEFAULT_PROGRESS)


def initialise_session_log_if_missing() -> None:
    """
    Write an empty list [] to session_log.json only if the file is missing.
    """
    path = get_session_log_path()
    if not os.path.exists(path):
        write_json(path, [])


def save_cat_result(result: dict) -> None:
    """
    Append one completed CAT session result to progress.json's cat_history,
    keyed by mode ("pretest" or "final"). Keeps only the most recent
    _CAT_HISTORY_LIMIT results per mode — oldest are dropped first.
    """
    path = get_progress_path()
    data = read_json(path)

    history = data.setdefault("cat_history", {"pretest": [], "final": []})
    mode = result.get("mode", "pretest")
    bucket = history.setdefault(mode, [])

    bucket.append(result)
    if len(bucket) > _CAT_HISTORY_LIMIT:
        del bucket[:len(bucket) - _CAT_HISTORY_LIMIT]

    write_json(path, data)
    logger.debug("save_cat_result: saved %s result, mode=%s", path, mode)