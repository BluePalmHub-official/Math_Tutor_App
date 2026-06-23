# =============================================================================
# core/problem_engine.py
# Central dispatcher — given a subject, topic, and difficulty, returns
# a fully formed problem dict ready for the GUI to display.
#
# IMPORTANT — PyInstaller safety:
#   All imports are EXPLICIT and STATIC.  No importlib, no __import__(),
#   no string-based dynamic loading.  PyInstaller's static analyser must
#   be able to see every module at build time or it won't bundle them.
#
# Problem dict contract (every generator must return this shape):
# {
#   "question":    str,   the problem text shown to the student
#   "answer":      any,   the correct answer (numeric, str, etc.)
#   "hint":        str,   level-1 nudge (shown in practice mode)
#   "hint2":       str,   level-2 partial solution
#   "hint3":       str,   level-3 full method walkthrough
#   "explanation": str,   full worked solution shown after answering
#   "type":        str,   "numeric" | "multiple_choice" | "expression" | "inequality"
# }
# =============================================================================

import logging
import random
from typing import Optional

import config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Placeholder generator
# Used for topics whose full generator module has not been written yet.
# Returns a clearly labelled stub problem so the app never crashes.
# Replace by importing the real module as each is completed.
# ---------------------------------------------------------------------------

def _stub_generator(topic: str, difficulty: str) -> dict:
    """Temporary placeholder until a real generator is implemented."""
    return {
        "question":    f"[{topic} — {difficulty}] Problem generator coming soon.",
        "answer":      "0",
        "hint":        "This topic is not yet implemented.",
        "hint2":       "This topic is not yet implemented.",
        "hint3":       "This topic is not yet implemented.",
        "explanation": "The generator for this topic has not been written yet.",
        "type":        "numeric",
    }


# ---------------------------------------------------------------------------
# Explicit static imports — add each real module here as it is written.
# The comment markers make it easy to find which ones still need building.
# ---------------------------------------------------------------------------

# --- Algebra ---
# TODO: replace each stub call with the real module once written
try:
    from problems.algebra import linear_equations as _alg_linear
except ImportError:
    _alg_linear = None                          # not written yet

try:
    from problems.algebra import inequalities as _alg_inequalities
except ImportError:
    _alg_inequalities = None

try:
    from problems.algebra import quadratics as _alg_quadratics
except ImportError:
    _alg_quadratics = None

try:
    from problems.algebra import exponents_radicals as _alg_exp_rad
except ImportError:
    _alg_exp_rad = None

try:
    from problems.algebra import word_problems as _alg_word
except ImportError:
    _alg_word = None

# --- Geometry ---
try:
    from problems.geometry import angles_lines as _geo_angles
except ImportError:
    _geo_angles = None

try:
    from problems.geometry import triangles as _geo_triangles
except ImportError:
    _geo_triangles = None

try:
    from problems.geometry import polygons as _geo_polygons
except ImportError:
    _geo_polygons = None

try:
    from problems.geometry import circles as _geo_circles
except ImportError:
    _geo_circles = None

try:
    from problems.geometry import coordinate_geometry as _geo_coord
except ImportError:
    _geo_coord = None

# --- Advanced ---
try:
    from problems.advanced import linear_functions as _adv_linear
except ImportError:
    _adv_linear = None

try:
    from problems.advanced import systems_of_equations as _adv_systems
except ImportError:
    _adv_systems = None

try:
    from problems.advanced import similar_triangles as _adv_similar
except ImportError:
    _adv_similar = None

try:
    from problems.advanced import trigonometry as _adv_trig
except ImportError:
    _adv_trig = None

try:
    from problems.advanced import parabolas_graphs as _adv_parabolas
except ImportError:
    _adv_parabolas = None

try:
    from problems.advanced import circle_equations as _adv_circles
except ImportError:
    _adv_circles = None

try:
    from problems.advanced import solid_geometry as _adv_solid
except ImportError:
    _adv_solid = None


# ---------------------------------------------------------------------------
# Registry — maps (subject, topic) → imported module (or None for stubs)
# ---------------------------------------------------------------------------

_REGISTRY: dict[str, dict[str, object]] = {
    config.SUBJECT_ALGEBRA: {
        "linear_equations":   _alg_linear,
        "inequalities":       _alg_inequalities,
        "quadratics":         _alg_quadratics,
        "exponents_radicals": _alg_exp_rad,
        "word_problems":      _alg_word,
    },
    config.SUBJECT_GEOMETRY: {
        "angles_lines":        _geo_angles,
        "triangles":           _geo_triangles,
        "polygons":            _geo_polygons,
        "circles":             _geo_circles,
        "coordinate_geometry": _geo_coord,
    },
    config.SUBJECT_ADVANCED: {
        "linear_functions":    _adv_linear,
        "systems_of_equations":_adv_systems,
        "similar_triangles":   _adv_similar,
        "trigonometry":        _adv_trig,
        "parabolas_graphs":    _adv_parabolas,
        "circle_equations":    _adv_circles,
        "solid_geometry":      _adv_solid,
    },
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_problem(subject: str, topic: str, difficulty: str = config.DIFFICULTY_EASY) -> dict:
    """
    Return one randomised problem for the given subject / topic / difficulty.

    Each call produces a different problem (different numbers, same concept)
    because generators use random internally.

    Parameters:
        subject    : "algebra" or "geometry"
        topic      : e.g. "linear_equations"
        difficulty : "easy" | "medium" | "hard"

    Returns:
        A problem dict matching the contract at the top of this file.
    """
    module = _REGISTRY.get(subject, {}).get(topic)

    if module is None:
        logger.warning(
            "get_problem: no generator for %s/%s — returning stub", subject, topic
        )
        return _stub_generator(topic, difficulty)

    if not hasattr(module, "generate"):
        logger.error(
            "get_problem: module %s/%s has no generate() function", subject, topic
        )
        return _stub_generator(topic, difficulty)

    try:
        problem = module.generate(difficulty=difficulty)
        _validate_problem(problem, subject, topic)
        return problem
    except Exception as e:
        logger.error(
            "get_problem: generator %s/%s raised %s — returning stub", subject, topic, e
        )
        return _stub_generator(topic, difficulty)


def get_problem_set(
    subject: str,
    topic: str,
    difficulty: str = config.DIFFICULTY_EASY,
    count: int = config.PROBLEMS_PER_ROUND,
) -> list[dict]:
    """
    Return a list of `count` unique-ish problems for one evaluate session.

    Uniqueness is best-effort — generators randomise numbers so collisions
    are rare, but not impossible on very easy difficulty with few variables.

    Parameters:
        subject    : "algebra" or "geometry"
        topic      : topic key string
        difficulty : difficulty level
        count      : number of problems (default = PROBLEMS_PER_ROUND = 10)

    Returns:
        List of problem dicts.
    """
    problems = []
    seen_questions: set[str] = set()
    max_attempts = count * 4    # try up to 4x to avoid duplicates

    attempts = 0
    while len(problems) < count and attempts < max_attempts:
        p = get_problem(subject, topic, difficulty)
        attempts += 1
        q = p.get("question", "")
        if q not in seen_questions:
            problems.append(p)
            seen_questions.add(q)

    # If we couldn't get enough unique problems, pad with repeats
    while len(problems) < count:
        problems.append(get_problem(subject, topic, difficulty))

    random.shuffle(problems)    # extra shuffle for variety
    logger.debug(
        "get_problem_set: %d problems for %s/%s [%s]", count, subject, topic, difficulty
    )
    return problems


def is_topic_available(subject: str, topic: str) -> bool:
    """
    Return True if a real generator exists for this topic.
    Used by the UI to show a 'coming soon' badge on unimplemented topics.
    """
    module = _REGISTRY.get(subject, {}).get(topic)
    return module is not None and hasattr(module, "generate")


def get_available_topics(subject: str) -> list[str]:
    """Return list of topic keys that have real generators implemented."""
    return [t for t in _REGISTRY.get(subject, {}) if is_topic_available(subject, t)]


# ---------------------------------------------------------------------------
# Internal validation
# ---------------------------------------------------------------------------

_REQUIRED_KEYS = {"question", "answer", "hint", "explanation", "type"}

def _validate_problem(problem: dict, subject: str, topic: str) -> None:
    """
    Log a warning if a generator returns a problem missing required keys.
    Does not raise — missing keys get safe defaults applied.
    """
    missing = _REQUIRED_KEYS - set(problem.keys())
    if missing:
        logger.warning(
            "_validate_problem: %s/%s problem missing keys: %s", subject, topic, missing
        )
    # Apply safe defaults for missing keys so the GUI never KeyErrors
    problem.setdefault("hint",        "Think carefully about the steps.")
    problem.setdefault("hint2",       "Try breaking the problem into smaller parts.")
    problem.setdefault("hint3",       "Review the worked example in the Learn section.")
    problem.setdefault("explanation", "No explanation provided.")
    problem.setdefault("type",        "numeric")