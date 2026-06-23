#!/usr/bin/env python3
"""
dev_tools.py — development helpers for Math Foundation Builder.

Commands:
    python3 dev_tools.py unlock-geometry   Marks all algebra topics as mastered
                                           and unlocks the geometry module.
    python3 dev_tools.py unlock-advanced   Marks all algebra + geometry topics
                                           as mastered and unlocks Advanced.
    python3 dev_tools.py reset             Wipes progress.json back to defaults
                                           for a clean start.
"""

import sys
import copy

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
# CLI dispatch
# ---------------------------------------------------------------------------

_COMMANDS = {
    "unlock-geometry": unlock_geometry,
    "unlock-advanced": unlock_advanced,
    "reset":           reset_progress,
}

_USAGE = """\
Math Foundation Builder — dev tools

Usage:
    python3 dev_tools.py unlock-geometry
        Marks all algebra topics as mastered and unlocks the
        geometry module. Student name is preserved.

    python3 dev_tools.py unlock-advanced
        Marks all algebra and geometry topics as mastered and
        unlocks the Advanced module. Student name is preserved.

    python3 dev_tools.py reset
        Wipes progress.json back to factory defaults
        (all topics not_started, geometry + advanced locked).
"""


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in _COMMANDS:
        print(_USAGE)
        sys.exit(0 if len(sys.argv) == 1 else 1)
    _COMMANDS[sys.argv[1]]()


if __name__ == "__main__":
    main()
