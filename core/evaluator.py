# =============================================================================
# core/evaluator.py
# Answer evaluation, scoring, streak tracking, and session logging.
#
# Responsibilities:
#   - Check student answers against expected answers (numeric + expression types)
#   - Handle float tolerance so 3.0 and 3 both pass
#   - Calculate running score during an evaluate session
#   - Track consecutive-correct streaks for practice
#   - Select encouragement messages based on outcome
#   - Append every answer attempt to session_log.json
#
# No GUI code here — pure logic only.
# =============================================================================

import random
import logging
from datetime import datetime
from typing import Any

import config
from utils.file_io import read_json, write_json, get_session_log_path

logger = logging.getLogger(__name__)

# Tolerance for floating-point answer comparisons (e.g. 3.333 ≈ 3.33)
FLOAT_TOLERANCE = 0.01


class Evaluator:
    """
    Evaluates one answer at a time and maintains running session stats.

    One Evaluator instance lives for the duration of a single phase session
    (either a Practice session or an Evaluate round).  SessionManager holds
    the instance and resets it between sessions.

    Usage:
        ev = Evaluator(session_id="abc123", subject="algebra",
                       topic="linear_equations", phase="evaluate")
        result = ev.check("3", expected_answer=3, problem=problem_dict)
        print(result["correct"], result["feedback"])
    """

    def __init__(self, session_id: str, subject: str, topic: str, phase: str):
        self.session_id = session_id
        self.subject    = subject
        self.topic      = topic
        self.phase      = phase

        # Running totals for this session
        self.total_attempts  = 0
        self.total_correct   = 0
        self.current_streak  = 0   # consecutive correct answers
        self.best_streak     = 0

        # Per-question record for result_screen review
        self.answer_log: list[dict] = []

    # -----------------------------------------------------------------------
    # Core answer checking
    # -----------------------------------------------------------------------

    def check(
        self,
        student_input: str,
        expected_answer: Any,
        problem: dict,
        used_hint: bool = False,
        used_show_solution: bool = False,
    ) -> dict:
        """
        Evaluate one answer attempt.

        Parameters:
            student_input       : raw string typed by the student
            expected_answer     : correct answer from the problem generator
            problem             : full problem dict (for logging + feedback)
            used_hint           : True if student opened a hint this attempt
            used_show_solution  : True if student clicked Show Solution

        Returns a dict:
        {
          "correct":            bool,
          "student_input":      str,   cleaned input
          "expected_answer":    any,
          "feedback":           str,   message shown to student
          "explanation":        str,   full worked explanation from problem
          "streak":             int,   current consecutive-correct streak
          "score_percent":      int,   running score % for this session
          "used_hint":          bool,
          "used_show_solution": bool,
        }
        """
        cleaned = student_input.strip()
        correct = self._is_correct(cleaned, expected_answer, problem.get("type", "numeric"))

        self.total_attempts += 1

        if correct and not used_show_solution:
            self.total_correct  += 1
            self.current_streak += 1
            self.best_streak     = max(self.best_streak, self.current_streak)
        else:
            self.current_streak = 0

        score_percent = self._score_percent()
        feedback      = self._pick_feedback(correct, used_show_solution)

        record = {
            "q_number":           self.total_attempts,
            "question":           problem.get("question", ""),
            "student_input":      cleaned,
            "expected_answer":    str(expected_answer),
            "correct":            correct,
            "used_hint":          used_hint,
            "used_show_solution": used_show_solution,
            "feedback":           feedback,
        }
        self.answer_log.append(record)
        self._append_to_session_log(record)

        logger.debug(
            "Attempt %d | correct=%s | streak=%d | score=%d%%",
            self.total_attempts, correct, self.current_streak, score_percent,
        )

        return {
            "correct":            correct,
            "student_input":      cleaned,
            "expected_answer":    expected_answer,
            "feedback":           feedback,
            "explanation":        problem.get("explanation", ""),
            "hint":               problem.get("hint", ""),
            "streak":             self.current_streak,
            "score_percent":      score_percent,
            "used_hint":          used_hint,
            "used_show_solution": used_show_solution,
        }

    # -----------------------------------------------------------------------
    # Answer comparison
    # -----------------------------------------------------------------------

    def _is_correct(self, student_input: str, expected: Any, answer_type: str) -> bool:
        """
        Compare student_input to expected answer.

        Supported answer_type values (set by problem generators):
            "numeric"          — integer or float comparison with tolerance
            "multiple_choice"  — case-insensitive letter match  (a/b/c/d)
            "expression"       — simplified string match (spaces stripped)
            "inequality"       — e.g. "x > 3"  (normalised string match)
        """
        if not student_input:
            return False

        if answer_type == "numeric":
            return self._numeric_match(student_input, expected)

        if answer_type == "multiple_choice":
            return student_input.lower().strip() == str(expected).lower().strip()

        if answer_type in ("expression", "inequality"):
            return self._expression_match(student_input, expected)

        # Fallback — plain string comparison
        return student_input.lower() == str(expected).lower()

    def _numeric_match(self, student_input: str, expected: Any) -> bool:
        """Parse student input as a number and compare with tolerance."""
        # Accept common fraction inputs like "1/3"
        try:
            if "/" in student_input:
                parts = student_input.split("/")
                if len(parts) == 2:
                    student_val = float(parts[0]) / float(parts[1])
                else:
                    return False
            else:
                student_val = float(student_input)

            expected_val = float(expected)
            return abs(student_val - expected_val) <= FLOAT_TOLERANCE

        except (ValueError, ZeroDivisionError):
            return False

    def _expression_match(self, student_input: str, expected: Any) -> bool:
        """
        Normalise both strings (lowercase, strip spaces) and compare.
        Handles simple cases like  "x=3"  vs  "x = 3".
        """
        def normalise(s: str) -> str:
            return s.lower().replace(" ", "").replace("*", "")

        return normalise(student_input) == normalise(str(expected))

    # -----------------------------------------------------------------------
    # Scoring
    # -----------------------------------------------------------------------

    def _score_percent(self) -> int:
        """Running score as integer percentage (0–100)."""
        if self.total_attempts == 0:
            return 0
        return int((self.total_correct / self.total_attempts) * 100)

    def final_score_percent(self) -> int:
        """
        Final score for an Evaluate round — based on PROBLEMS_PER_ROUND,
        not just the attempts so far.
        """
        return int((self.total_correct / config.PROBLEMS_PER_ROUND) * 100)

    def get_summary(self) -> dict:
        """
        Return end-of-session summary dict used by result_screen.py.

        {
          "total_attempts":  int,
          "total_correct":   int,
          "score_percent":   int,   final %  (out of PROBLEMS_PER_ROUND)
          "best_streak":     int,
          "answer_log":      list,  per-question records
          "passed":          bool,  True if score >= MASTERY_SCORE_PERCENT
        }
        """
        score = self.final_score_percent()
        return {
            "total_attempts": self.total_attempts,
            "total_correct":  self.total_correct,
            "score_percent":  score,
            "best_streak":    self.best_streak,
            "answer_log":     self.answer_log,
            "passed":         score >= config.MASTERY_SCORE_PERCENT,
        }

    # -----------------------------------------------------------------------
    # Feedback messages
    # -----------------------------------------------------------------------

    def _pick_feedback(self, correct: bool, used_show_solution: bool) -> str:
        """Select an appropriate encouragement / feedback message."""
        if used_show_solution:
            return "Solution shown — review the steps and try the next one."

        if correct:
            # Streak milestone messages
            if self.current_streak in (3, 5, 7, 10):
                template = random.choice(config.ENCOURAGEMENT_STREAK)
                return template.format(n=self.current_streak)
            return random.choice(config.ENCOURAGEMENT_CORRECT)

        return random.choice(config.ENCOURAGEMENT_INCORRECT)

    # -----------------------------------------------------------------------
    # Session logging
    # -----------------------------------------------------------------------

    def _append_to_session_log(self, record: dict) -> None:
        """
        Append one answer record to session_log.json.
        Adds metadata (session_id, subject, topic, phase, timestamp).
        """
        entry = {
            "session_id": self.session_id,
            "subject":    self.subject,
            "topic":      self.topic,
            "phase":      self.phase,
            "timestamp":  datetime.now().isoformat(timespec="seconds"),
            **record,
        }

        try:
            log_path = get_session_log_path()
            existing = read_json(log_path)
            if not isinstance(existing, list):
                existing = []
            existing.append(entry)
            write_json(log_path, existing)
        except Exception as e:
            # Logging failure must never crash the app
            logger.error("Failed to write session log entry: %s", e)