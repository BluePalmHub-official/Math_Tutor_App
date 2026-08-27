#!/usr/bin/env python3
"""
dev_tools.py — development helpers for Math Foundation Builder.

Interactive usage:
    python3 dev_tools.py
        Shows a menu:
          1. Reset all progress
          2. Unlock algebra
          3. Unlock algebra + geometry
          4. Unlock everything
          5. Add fake CAT history
          6. Reset CAT history

CLI usage (unchanged, for scripting):
    python3 dev_tools.py unlock-algebra     Marks all algebra topics mastered
                                             (geometry/advanced stay locked).
    python3 dev_tools.py unlock-geometry    Marks all algebra topics as mastered
                                             and unlocks the geometry module.
    python3 dev_tools.py unlock-advanced    Marks all algebra + geometry topics
                                             as mastered and unlocks Advanced.
    python3 dev_tools.py fake-cat-history   Adds 3 fake pretest + 3 fake final
                                             CAT results for UI testing.
    python3 dev_tools.py reset-cat-history  Clears cat_history back to empty.
    python3 dev_tools.py reset              Wipes progress.json back to defaults
                                             for a clean start.
"""

import sys
import copy
from datetime import datetime, timedelta

import config
from utils.file_io import (
    get_progress_path,
    initialise_progress_if_missing,
    read_json,
    write_json,
    DEFAULT_PROGRESS,
)

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _load() -> dict:
    initialise_progress_if_missing()
    return read_json(get_progress_path())


def _save(data: dict) -> None:
    if not write_json(get_progress_path(), data):
        print("ERROR: could not write progress.json")
        sys.exit(1)


def _mastered_topic() -> dict:
    return {
        "learn": {
            "status": config.STATUS_COMPLETE,
        },
        "practice": {
            "status":      config.STATUS_COMPLETE,
            "best_streak": config.PRACTICE_PASS_STREAK,
            "attempts":    config.PRACTICE_PASS_STREAK,
        },
        "evaluate": {
            "status":     config.STATUS_MASTERED,
            "attempts":   1,
            "best_score": 100,
            "mastered":   True,
            "difficulty": config.DIFFICULTY_MEDIUM,
        },
    }


def _unlocked_geo_topic() -> dict:
    return {
        "learn": {
            "status": config.STATUS_NOT_STARTED,
        },
        "practice": {
            "status":      config.STATUS_NOT_STARTED,
            "best_streak": 0,
            "attempts":    0,
        },
        "evaluate": {
            "status":     config.STATUS_NOT_STARTED,
            "attempts":   0,
            "best_score": 0,
            "mastered":   False,
            "difficulty": config.DIFFICULTY_EASY,
        },
    }


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def unlock_algebra() -> None:
    """
    Mark every algebra topic as mastered. Geometry and Advanced stay locked.
    Student name is preserved.
    """
    data    = _load()
    student = data.get("student_name", "")
    changes = []

    for topic in config.ALGEBRA_TOPICS:
        label = config.TOPIC_LABELS.get(topic, topic)
        old = (data.get(config.SUBJECT_ALGEBRA, {}).get(topic, {})
               .get(config.PHASE_EVALUATE, {}).get("status", "unknown"))
        data.setdefault(config.SUBJECT_ALGEBRA, {})[topic] = _mastered_topic()
        if old != config.STATUS_MASTERED:
            changes.append(f"  algebra  /  {label}")

    _save(data)

    print("=" * 56)
    print("  dev_tools  —  unlock-algebra")
    print("=" * 56)
    print(f"  Student : {student or '(not set)'}")
    print(f"  File    : {get_progress_path()}")
    print()
    if changes:
        print("  Topics set to mastered:")
        for line in changes:
            print(f"    {line.strip()}")
    else:
        print("  No changes needed (algebra already mastered).")
    print()
    print("  Geometry and Advanced remain locked.")
    print("  Run  python3 main.py  to launch.")
    print("=" * 56)


def unlock_geometry() -> None:
    """
    Mark every algebra topic as mastered and unlock the geometry module.
    Student name is preserved.
    """
    data      = _load()
    student   = data.get("student_name", "")
    changes   = []

    # ── Algebra: mark all topics as mastered ────────────────────────────────
    for topic in config.ALGEBRA_TOPICS:
        label = config.TOPIC_LABELS.get(topic, topic)
        old_ev_status = (
            data
            .get(config.SUBJECT_ALGEBRA, {})
            .get(topic, {})
            .get(config.PHASE_EVALUATE, {})
            .get("status", "unknown")
        )
        data.setdefault(config.SUBJECT_ALGEBRA, {})[topic] = _mastered_topic()
        if old_ev_status != config.STATUS_MASTERED:
            changes.append(f"  algebra  /  {label}")

    # ── Geometry: unlock subject and reset all topics ────────────────────────
    geo_was_locked = (
        data.get(config.SUBJECT_GEOMETRY, {}).get("status") == config.STATUS_LOCKED
    )
    geo = data.setdefault(config.SUBJECT_GEOMETRY, {})
    geo["status"] = config.STATUS_NOT_STARTED

    for topic in config.GEOMETRY_TOPICS:
        geo[topic] = _unlocked_geo_topic()

    if geo_was_locked:
        changes.append(f"  geometry module  →  unlocked")

    _save(data)

    # ── Report ───────────────────────────────────────────────────────────────
    print("=" * 56)
    print("  dev_tools  —  unlock-geometry")
    print("=" * 56)
    print(f"  Student : {student or '(not set)'}")
    print(f"  File    : {get_progress_path()}")
    print()
    if changes:
        print("  Topics set to mastered / unlocked:")
        for line in changes:
            print(f"    {line.strip()}")
    else:
        print("  No changes needed (algebra already mastered).")
    print()
    print("  Geometry topics set to  not_started :")
    for topic in config.GEOMETRY_TOPICS:
        label = config.TOPIC_LABELS.get(topic, topic)
        print(f"    geometry  /  {label}")
    print()
    print("  Run  python3 main.py  to launch with geometry unlocked.")
    print("=" * 56)


def unlock_advanced() -> None:
    """
    Mark every algebra and geometry topic as mastered and unlock the Advanced module.
    Student name is preserved.
    """
    data    = _load()
    student = data.get("student_name", "")
    changes = []

    # ── Algebra ────────────────────────────────────────────────────────────────
    for topic in config.ALGEBRA_TOPICS:
        old = (data.get(config.SUBJECT_ALGEBRA, {}).get(topic, {})
               .get(config.PHASE_EVALUATE, {}).get("status", "unknown"))
        data.setdefault(config.SUBJECT_ALGEBRA, {})[topic] = _mastered_topic()
        if old != config.STATUS_MASTERED:
            changes.append(f"  algebra  /  {config.TOPIC_LABELS.get(topic, topic)}")

    # ── Geometry ───────────────────────────────────────────────────────────────
    geo = data.setdefault(config.SUBJECT_GEOMETRY, {})
    geo["status"] = config.STATUS_NOT_STARTED
    for topic in config.GEOMETRY_TOPICS:
        old = geo.get(topic, {}).get(config.PHASE_EVALUATE, {}).get("status", "unknown")
        geo[topic] = _mastered_topic()
        if old != config.STATUS_MASTERED:
            changes.append(f"  geometry / {config.TOPIC_LABELS.get(topic, topic)}")

    # ── Advanced: unlock subject and reset all topics ──────────────────────────
    adv_was_locked = (
        data.get(config.SUBJECT_ADVANCED, {}).get("status") == config.STATUS_LOCKED
    )
    adv = data.setdefault(config.SUBJECT_ADVANCED, {})
    adv["status"] = config.STATUS_NOT_STARTED
    for topic in config.ADVANCED_TOPICS:
        adv[topic] = _unlocked_geo_topic()
    if adv_was_locked:
        changes.append("  advanced module  →  unlocked")

    _save(data)

    print("=" * 56)
    print("  dev_tools  —  unlock-advanced")
    print("=" * 56)
    print(f"  Student : {student or '(not set)'}")
    print(f"  File    : {get_progress_path()}")
    print()
    if changes:
        print("  Topics set to mastered / unlocked:")
        for line in changes:
            print(f"    {line.strip()}")
    else:
        print("  No changes needed (already fully mastered).")
    print()
    print("  Advanced topics set to  not_started :")
    for topic in config.ADVANCED_TOPICS:
        print(f"    advanced  /  {config.TOPIC_LABELS.get(topic, topic)}")
    print()
    print("  Run  python3 main.py  to launch with Advanced unlocked.")
    print("=" * 56)


def unlock_everything() -> None:
    """
    Mark every topic in every subject (including Advanced) as mastered.
    Alias used by the interactive menu's "Unlock everything" option.
    """
    unlock_advanced()

    data = _load()
    changes = []
    for topic in config.ADVANCED_TOPICS:
        old = (data.get(config.SUBJECT_ADVANCED, {}).get(topic, {})
               .get(config.PHASE_EVALUATE, {}).get("status", "unknown"))
        data.setdefault(config.SUBJECT_ADVANCED, {})[topic] = _mastered_topic()
        if old != config.STATUS_MASTERED:
            changes.append(f"  advanced / {config.TOPIC_LABELS.get(topic, topic)}")
    _save(data)

    if changes:
        print()
        print("  Advanced topics also set to mastered:")
        for line in changes:
            print(f"    {line.strip()}")
        print("=" * 56)


def add_fake_cat_history() -> None:
    """
    Add 3 fake pretest + 3 fake final-exam results to progress.json so the
    history panels (home, progress, CAT result screens) have data to show.
    """
    data = _load()
    history = data.setdefault("cat_history", {"pretest": [], "final": []})
    now = datetime.now()

    def _breakdown(weak_topics, strong_topics):
        breakdown = {}
        for t in weak_topics:
            breakdown[f"algebra/{t}"] = {
                "subject": "algebra", "topic": t,
                "label": config.TOPIC_LABELS.get(t, t),
                "attempted": 4, "correct": 1, "percent": 25, "strength": "weak",
            }
        for t in strong_topics:
            breakdown[f"algebra/{t}"] = {
                "subject": "algebra", "topic": t,
                "label": config.TOPIC_LABELS.get(t, t),
                "attempted": 5, "correct": 4, "percent": 80, "strength": "strong",
            }
        return breakdown

    def _fake(mode, score, pass_fail, days_ago, weak, strong):
        total_answered = config.PRETEST_MINIMUM_QUESTIONS if mode == "pretest" else config.CAT_MINIMUM_QUESTIONS
        return {
            "date":             (now - timedelta(days=days_ago)).isoformat(timespec="seconds"),
            "mode":             mode,
            "score_percent":    score,
            "pass_fail":        pass_fail,
            "total_answered":   total_answered,
            "hard_streak_peak": 3 if mode == "pretest" else 5,
            "elapsed_seconds":  600 + days_ago * 5,
            "weak_topics":      [config.TOPIC_LABELS.get(t, t) for t in weak],
            "strong_topics":    [config.TOPIC_LABELS.get(t, t) for t in strong],
            "topic_breakdown":  _breakdown(weak, strong),
        }

    pretest_fakes = [
        _fake("pretest", 40, "fail",       10, ["quadratics", "word_problems"], ["linear_equations"]),
        _fake("pretest", 60, "borderline", 5,  ["quadratics"],                  ["linear_equations", "inequalities"]),
        _fake("pretest", 82, "pass",       1,  [],                              ["linear_equations", "inequalities", "quadratics"]),
    ]
    final_fakes = [
        _fake("final", 45, "fail",       8, ["exponents_radicals"], ["linear_equations"]),
        _fake("final", 65, "borderline", 4, ["exponents_radicals"], ["linear_equations", "quadratics"]),
        _fake("final", 85, "pass",       1, [],                     ["linear_equations", "quadratics", "exponents_radicals"]),
    ]

    history.setdefault("pretest", []).extend(pretest_fakes)
    history.setdefault("final", []).extend(final_fakes)
    history["pretest"] = history["pretest"][-10:]
    history["final"]   = history["final"][-10:]

    _save(data)

    print("=" * 56)
    print("  dev_tools  —  fake-cat-history")
    print("=" * 56)
    print(f"  File : {get_progress_path()}")
    print()
    print(f"  Added {len(pretest_fakes)} fake pre-test results.")
    print(f"  Added {len(final_fakes)} fake final-exam results.")
    print()
    print("  Run  python3 main.py  and check the Home / Progress screens.")
    print("=" * 56)


def reset_cat_history() -> None:
    """Clear cat_history back to empty lists. All other progress is untouched."""
    data = _load()
    data["cat_history"] = {"pretest": [], "final": []}
    _save(data)

    print("=" * 56)
    print("  dev_tools  —  reset-cat-history")
    print("=" * 56)
    print(f"  File : {get_progress_path()}")
    print()
    print("  cat_history cleared (pretest + final).")
    print("=" * 56)


def reset_progress() -> None:
    """
    Wipe progress.json back to factory defaults.
    All progress and the student name are cleared.
    """
    _save(copy.deepcopy(DEFAULT_PROGRESS))

    print("=" * 56)
    print("  dev_tools  —  reset")
    print("=" * 56)
    print(f"  File    : {get_progress_path()}")
    print()
    print("  progress.json wiped to factory defaults.")
    print("  All topics → not_started, geometry → locked.")
    print()
    print("  Run  python3 main.py  to start fresh.")
    print("=" * 56)


# ---------------------------------------------------------------------------
# CLI dispatch  (backward-compatible, non-interactive scripting)
# ---------------------------------------------------------------------------

_COMMANDS = {
    "unlock-algebra":    unlock_algebra,
    "unlock-geometry":   unlock_geometry,
    "unlock-advanced":   unlock_advanced,
    "fake-cat-history":  add_fake_cat_history,
    "reset-cat-history": reset_cat_history,
    "reset":             reset_progress,
}

_USAGE = """\
Math Foundation Builder — dev tools

Run with no arguments for the interactive menu, or use a direct command:

    python3 dev_tools.py unlock-algebra
    python3 dev_tools.py unlock-geometry
    python3 dev_tools.py unlock-advanced
    python3 dev_tools.py fake-cat-history
    python3 dev_tools.py reset-cat-history
    python3 dev_tools.py reset
"""

# ---------------------------------------------------------------------------
# Interactive menu
# ---------------------------------------------------------------------------

_MENU_ACTIONS = {
    "1": reset_progress,
    "2": unlock_algebra,
    "3": unlock_geometry,
    "4": unlock_everything,
    "5": add_fake_cat_history,
    "6": reset_cat_history,
}


def _run_interactive_menu() -> None:
    print("Dev Tools — Math Foundation Builder")
    print("1. Reset all progress")
    print("2. Unlock algebra")
    print("3. Unlock algebra + geometry")
    print("4. Unlock everything")
    print("5. Add fake CAT history")
    print("6. Reset CAT history")
    choice = input("Choose option: ").strip()

    action = _MENU_ACTIONS.get(choice)
    if action is None:
        print(f"Unknown option: {choice!r}")
        sys.exit(1)
    action()


def main() -> None:
    if len(sys.argv) == 2 and sys.argv[1] in _COMMANDS:
        _COMMANDS[sys.argv[1]]()
        return

    if len(sys.argv) > 1:
        print(_USAGE)
        sys.exit(1)

    _run_interactive_menu()


if __name__ == "__main__":
    main()
