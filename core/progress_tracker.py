# =============================================================================
# core/progress_tracker.py
# All student progress read/write logic.
#
# This is the single source of truth for:
#   - What phase a student is on for each topic
#   - Whether a phase is complete / locked / mastered
#   - Unlocking the next phase or the geometry module
#   - Persisting all changes to progress.json via file_io
#
# No GUI code here — pure logic only.
# =============================================================================

import logging
from typing import Optional

import config
from utils.file_io import (
    read_json,
    write_json,
    get_progress_path,
    initialise_progress_if_missing,
)

logger = logging.getLogger(__name__)


class ProgressTracker:
    """
    Manages all reading and writing of student progress.

    Usage (from anywhere in the app):
        tracker = ProgressTracker()
        tracker.load()
        tracker.complete_learn("algebra", "linear_equations")
        tracker.save()
    """

    def __init__(self):
        self._data: dict = {}   # the full contents of progress.json in memory

    # -----------------------------------------------------------------------
    # Load / Save
    # -----------------------------------------------------------------------

    def load(self) -> None:
        """
        Load progress.json into memory.
        Creates the file with defaults if it does not exist.
        """
        initialise_progress_if_missing()
        self._data = read_json(get_progress_path())
        logger.info("Progress loaded for student: '%s'", self._data.get("student_name", ""))

    def save(self) -> bool:
        """Persist the in-memory progress data to progress.json."""
        success = write_json(get_progress_path(), self._data)
        if success:
            logger.debug("Progress saved.")
        else:
            logger.error("Progress FAILED to save.")
        return success

    # -----------------------------------------------------------------------
    # Student name
    # -----------------------------------------------------------------------

    def get_student_name(self) -> str:
        return self._data.get("student_name", "")

    def set_student_name(self, name: str) -> None:
        self._data["student_name"] = name.strip()
        self.save()

    # -----------------------------------------------------------------------
    # Low-level topic data accessors
    # -----------------------------------------------------------------------

    def _topic_data(self, subject: str, topic: str) -> dict:
        """Return the full progress dict for a given subject + topic."""
        return self._data.get(subject, {}).get(topic, {})

    def _phase_data(self, subject: str, topic: str, phase: str) -> dict:
        """Return the progress dict for a specific phase of a topic."""
        return self._topic_data(subject, topic).get(phase, {})

    def _set_phase_field(
        self, subject: str, topic: str, phase: str, field: str, value
    ) -> None:
        """Write a single field inside a phase record and save."""
        self._data[subject][topic][phase][field] = value
        self.save()

    # -----------------------------------------------------------------------
    # Phase status queries
    # -----------------------------------------------------------------------

    def get_phase_status(self, subject: str, topic: str, phase: str) -> str:
        """
        Return the status string for a phase.
        One of: not_started, in_progress, complete, locked, mastered.
        """
        return self._phase_data(subject, topic, phase).get(
            "status", config.STATUS_LOCKED
        )

    def is_phase_complete(self, subject: str, topic: str, phase: str) -> bool:
        status = self.get_phase_status(subject, topic, phase)
        return status in (config.STATUS_COMPLETE, config.STATUS_MASTERED)

    def is_topic_mastered(self, subject: str, topic: str) -> bool:
        """True only when the evaluate phase is marked mastered."""
        return self._phase_data(subject, topic, config.PHASE_EVALUATE).get(
            "mastered", False
        )

    def is_subject_locked(self, subject: str) -> bool:
        """True if the entire subject (e.g. geometry) is still locked."""
        return self._data.get(subject, {}).get("status") == config.STATUS_LOCKED

    def is_geometry_unlocked(self) -> bool:
        return not self.is_subject_locked(config.SUBJECT_GEOMETRY)

    # -----------------------------------------------------------------------
    # Phase completion — called by each screen when the student finishes
    # -----------------------------------------------------------------------

    def complete_learn(self, subject: str, topic: str) -> None:
        """
        Mark the Learn phase complete and unlock Practice.
        Called by learn_screen.py when all cards and examples are viewed.
        """
        self._data[subject][topic][config.PHASE_LEARN]["status"] = config.STATUS_COMPLETE
        # Unlock practice if it was locked
        if self._phase_data(subject, topic, config.PHASE_PRACTICE).get("status") \
                == config.STATUS_LOCKED:
            self._data[subject][topic][config.PHASE_PRACTICE]["status"] = \
                config.STATUS_NOT_STARTED
        self.save()
        logger.info("Learn complete: %s / %s", subject, topic)

    def update_practice(
        self, subject: str, topic: str, correct: bool, used_show_solution: bool
    ) -> dict:
        """
        Record one practice attempt and check whether the student has
        met the Practice → Evaluate unlock condition.

        Returns a dict:
            {
              "streak":   int,   current consecutive-correct streak
              "unlocked": bool,  True if Evaluate was just unlocked
            }
        """
        p = self._data[subject][topic][config.PHASE_PRACTICE]
        p["status"] = config.STATUS_IN_PROGRESS
        p["attempts"] = p.get("attempts", 0) + 1

        if correct and not used_show_solution:
            streak = p.get("best_streak", 0) + 1
        else:
            streak = 0                      # reset streak on wrong or show-solution

        p["best_streak"] = streak
        unlocked = False

        if streak >= config.PRACTICE_PASS_STREAK:
            p["status"] = config.STATUS_COMPLETE
            # Unlock evaluate phase
            eval_data = self._data[subject][topic][config.PHASE_EVALUATE]
            if eval_data.get("status") == config.STATUS_LOCKED:
                eval_data["status"] = config.STATUS_NOT_STARTED
                unlocked = True
                logger.info("Evaluate unlocked: %s / %s", subject, topic)

        self.save()
        return {"streak": streak, "unlocked": unlocked}

    def record_evaluate_result(
        self, subject: str, topic: str, score_percent: int
    ) -> dict:
        """
        Record one evaluation attempt with its score.
        Grants mastery if score meets the threshold.
        Advances difficulty if mastered at current level.

        Returns a dict:
            {
              "mastered":          bool,
              "best_score":        int,
              "difficulty":        str,
              "geometry_unlocked": bool,
            }
        """
        ev = self._data[subject][topic][config.PHASE_EVALUATE]
        ev["status"]   = config.STATUS_IN_PROGRESS
        ev["attempts"] = ev.get("attempts", 0) + 1

        if score_percent > ev.get("best_score", 0):
            ev["best_score"] = score_percent

        mastered = score_percent >= config.MASTERY_SCORE_PERCENT
        if mastered:
            ev["mastered"] = True
            ev["status"]   = config.STATUS_MASTERED
            # Advance difficulty for replay interest
            current_diff = ev.get("difficulty", config.DIFFICULTY_EASY)
            idx = config.DIFFICULTY_ORDER.index(current_diff)
            if idx < len(config.DIFFICULTY_ORDER) - 1:
                ev["difficulty"] = config.DIFFICULTY_ORDER[idx + 1]
            logger.info(
                "Topic mastered: %s / %s  score=%d%%", subject, topic, score_percent
            )

        self.save()

        geometry_unlocked = False
        if mastered and subject == config.SUBJECT_ALGEBRA:
            geometry_unlocked = self._check_unlock_geometry()

        return {
            "mastered":          mastered,
            "best_score":        ev["best_score"],
            "difficulty":        ev.get("difficulty", config.DIFFICULTY_EASY),
            "geometry_unlocked": geometry_unlocked,
        }

    # -----------------------------------------------------------------------
    # Geometry unlock
    # -----------------------------------------------------------------------

    def _check_unlock_geometry(self) -> bool:
        """
        Unlock geometry if every algebra topic is mastered.
        Returns True if geometry was just unlocked (was previously locked).
        """
        if not config.GEOMETRY_REQUIRES_ALGEBRA_MASTERY:
            return False

        if self.is_geometry_unlocked():
            return False    # already unlocked

        all_algebra_mastered = all(
            self.is_topic_mastered(config.SUBJECT_ALGEBRA, t)
            for t in config.ALGEBRA_TOPICS
        )

        if all_algebra_mastered:
            # Unlock the geometry subject and all its topics
            self._data[config.SUBJECT_GEOMETRY]["status"] = config.STATUS_NOT_STARTED
            for topic in config.GEOMETRY_TOPICS:
                for phase in config.PHASES_IN_ORDER:
                    self._data[config.SUBJECT_GEOMETRY][topic][phase]["status"] = \
                        config.STATUS_NOT_STARTED
            self.save()
            logger.info("🔓 Geometry module unlocked!")
            return True

        return False

    # -----------------------------------------------------------------------
    # Summary helpers  (used by home_screen and progress_screen)
    # -----------------------------------------------------------------------

    def get_topic_summary(self, subject: str, topic: str) -> dict:
        """
        Return a concise summary dict for a topic, used to render topic cards.

        {
          "label":       str,   human-readable topic name
          "learn":       str,   phase status
          "practice":   str,
          "evaluate":   str,
          "mastered":   bool,
          "best_score": int,
          "difficulty": str,
          "locked":     bool,   True if the subject itself is locked
        }
        """
        ev = self._phase_data(subject, topic, config.PHASE_EVALUATE)
        return {
            "label":      config.TOPIC_LABELS.get(topic, topic),
            "learn":      self.get_phase_status(subject, topic, config.PHASE_LEARN),
            "practice":   self.get_phase_status(subject, topic, config.PHASE_PRACTICE),
            "evaluate":   self.get_phase_status(subject, topic, config.PHASE_EVALUATE),
            "mastered":   ev.get("mastered", False),
            "best_score": ev.get("best_score", 0),
            "difficulty": ev.get("difficulty", config.DIFFICULTY_EASY),
            "locked":     self.is_subject_locked(subject),
        }

    def get_overall_progress(self) -> dict:
        """
        Return counts for the progress dashboard screen.

        {
          "algebra_mastered":  int,   topics mastered out of 5
          "algebra_total":     int,
          "geometry_mastered": int,
          "geometry_total":    int,
          "geometry_locked":   bool,
          "percent_overall":   int,   0-100
        }
        """
        alg_mastered = sum(
            1 for t in config.ALGEBRA_TOPICS
            if self.is_topic_mastered(config.SUBJECT_ALGEBRA, t)
        )
        geo_mastered = sum(
            1 for t in config.GEOMETRY_TOPICS
            if self.is_topic_mastered(config.SUBJECT_GEOMETRY, t)
        )
        total = len(config.ALGEBRA_TOPICS) + len(config.GEOMETRY_TOPICS)
        overall_mastered = alg_mastered + geo_mastered
        percent = int((overall_mastered / total) * 100) if total else 0

        return {
            "algebra_mastered":  alg_mastered,
            "algebra_total":     len(config.ALGEBRA_TOPICS),
            "geometry_mastered": geo_mastered,
            "geometry_total":    len(config.GEOMETRY_TOPICS),
            "geometry_locked":   self.is_subject_locked(config.SUBJECT_GEOMETRY),
            "percent_overall":   percent,
        }

    def get_current_difficulty(self, subject: str, topic: str) -> str:
        """Return the current difficulty level for a topic's evaluate phase."""
        return self._phase_data(subject, topic, config.PHASE_EVALUATE).get(
            "difficulty", config.DIFFICULTY_EASY
        )