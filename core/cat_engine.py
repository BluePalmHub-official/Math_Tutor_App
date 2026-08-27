# =============================================================================
# core/cat_engine.py
# Computerised Adaptive Test (CAT) engine.
#
# Drives two modes with the same adaptive algorithm:
#   - "pretest" : diagnostic assessment, no mastery required, lighter
#                 pass/fail thresholds. Covers ALL topics regardless of
#                 mastery status (student has not studied yet).
#   - "final"   : competency confirmation exam, only drawn from topics the
#                 student has already mastered, stricter thresholds.
#
# Adaptive rule: correct answers move difficulty up one level, wrong
# answers move it down one level (capped at easy/hard). The session ends
# early on a strong Hard-difficulty streak (pass) or a run of Easy-level
# failures (fail), or times out at total_questions and is graded on score.
#
# No GUI code here — pure logic only.
# =============================================================================

import random
import time
import logging
from datetime import datetime
from typing import Any, Optional

import config
from core.problem_engine import get_problem, is_topic_available
from utils.file_io import save_cat_result

logger = logging.getLogger(__name__)

FLOAT_TOLERANCE = 0.01

_ALL_SUBJECT_TOPICS = {
    config.SUBJECT_ALGEBRA:  config.ALGEBRA_TOPICS,
    config.SUBJECT_GEOMETRY: config.GEOMETRY_TOPICS,
    config.SUBJECT_ADVANCED: config.ADVANCED_TOPICS,
}


class CATEngine:
    """
    Drives one Computerised Adaptive Test session at a time.

    Usage:
        cat = CATEngine(tracker, mode=config.CAT_MODE_PRETEST)
        problem = cat.start()
        result  = cat.submit_answer("3")
        if result["is_complete"]:
            summary = cat.get_summary()
    """

    def __init__(self, tracker, mode: str = config.CAT_MODE_PRETEST):
        self.tracker = tracker
        self.mode    = mode
        self._apply_thresholds()

        # Session state — populated by start()
        self.question_number     = None
        self.current_difficulty  = None
        self.hard_streak         = None
        self.hard_streak_peak    = None
        self.easy_fail_streak    = None
        self.total_correct       = None
        self.total_answered      = None
        self.total_hard_answered = None
        self.answer_log          = None
        self.seen_questions      = None
        self.status              = None
        self.pass_fail           = None
        self.start_time          = None
        self.terminated_early    = None
        self.current_problem     = None

    # -----------------------------------------------------------------------
    # Mode / thresholds
    # -----------------------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        """Switch modes and re-apply the matching threshold constants."""
        self.mode = mode
        self._apply_thresholds()

    def _apply_thresholds(self) -> None:
        if self.mode == config.CAT_MODE_PRETEST:
            self.minimum_questions = config.PRETEST_MINIMUM_QUESTIONS
            self.total_questions   = config.PRETEST_TOTAL_QUESTIONS
            self.pass_hard_streak  = config.PRETEST_PASS_HARD_STREAK
            self.fail_easy_streak  = config.PRETEST_FAIL_EASY_STREAK
            self.pass_score        = config.PRETEST_PASS_SCORE_PERCENT
            self.fail_score        = config.PRETEST_FAIL_SCORE_PERCENT
            self.min_hard_for_pass = config.PRETEST_MIN_HARD_FOR_PASS
        else:
            self.minimum_questions = config.CAT_MINIMUM_QUESTIONS
            self.total_questions   = config.CAT_TOTAL_QUESTIONS
            self.pass_hard_streak  = config.CAT_PASS_HARD_STREAK
            self.fail_easy_streak  = config.CAT_FAIL_EASY_STREAK
            self.pass_score        = config.CAT_PASS_SCORE_PERCENT
            self.fail_score        = config.CAT_FAIL_SCORE_PERCENT
            self.min_hard_for_pass = config.CAT_MIN_HARD_FOR_PASS

    # -----------------------------------------------------------------------
    # Session lifecycle
    # -----------------------------------------------------------------------

    def start(self) -> dict:
        """Reset all session state and return the first problem."""
        self.question_number     = 0
        self.current_difficulty  = config.CAT_START_DIFFICULTY
        self.hard_streak         = 0
        self.hard_streak_peak    = 0
        self.easy_fail_streak    = 0
        self.total_correct       = 0
        self.total_answered      = 0
        self.total_hard_answered = 0
        self.answer_log          = []
        self.seen_questions      = set()
        self.status              = "in_progress"
        self.pass_fail           = None
        self.terminated_early    = False
        self.start_time          = time.time()

        logger.info("CAT session started | mode=%s", self.mode)
        return self._get_next_problem()

    def submit_answer(self, student_input: str) -> dict:
        """Evaluate one answer, update adaptive state, and check for completion."""
        problem = self.current_problem
        cleaned = student_input.strip()
        correct = self._evaluate_answer(
            cleaned, problem.get("answer"), problem.get("type", "numeric")
        )

        difficulty_played = self.current_difficulty
        if difficulty_played == config.DIFFICULTY_HARD:
            self.total_hard_answered += 1

        self.question_number += 1
        self.total_answered  += 1
        if correct:
            self.total_correct += 1

        self.answer_log.append({
            "q_number":        self.question_number,
            "subject":         problem.get("subject", ""),
            "topic":           problem.get("topic", ""),
            "question":        problem.get("question", ""),
            "student_input":   cleaned,
            "expected_answer": str(problem.get("answer")),
            "correct":         correct,
            "difficulty":      difficulty_played,
        })

        idx = config.DIFFICULTY_ORDER.index(self.current_difficulty)

        if correct:
            self.easy_fail_streak = 0
            if difficulty_played == config.DIFFICULTY_HARD:
                self.hard_streak      += 1
                self.hard_streak_peak  = max(self.hard_streak_peak, self.hard_streak)
            if idx < len(config.DIFFICULTY_ORDER) - 1:
                self.current_difficulty = config.DIFFICULTY_ORDER[idx + 1]
        else:
            self.hard_streak = 0
            if difficulty_played == config.DIFFICULTY_EASY:
                self.easy_fail_streak += 1
            if idx > 0:
                self.current_difficulty = config.DIFFICULTY_ORDER[idx - 1]

        is_complete = self._check_termination()

        result = {
            "correct":            correct,
            "student_input":      cleaned,
            "expected_answer":    problem.get("answer"),
            "explanation":        problem.get("explanation", ""),
            "question_number":    self.question_number,
            "difficulty_played":  difficulty_played,
            "next_difficulty":    self.current_difficulty,
            "hard_streak":        self.hard_streak,
            "hard_streak_peak":   self.hard_streak_peak,
            "easy_fail_streak":   self.easy_fail_streak,
            "total_correct":      self.total_correct,
            "total_answered":     self.total_answered,
            "score_percent":      self._score_percent(),
            "is_complete":        is_complete,
            "pass_fail":          self.pass_fail,
            "mode":               self.mode,
            "next_problem":       None if is_complete else self._get_next_problem(),
        }

        if is_complete:
            save_cat_result(self.get_summary())
            logger.info(
                "CAT session complete | mode=%s | pass_fail=%s | score=%d%%",
                self.mode, self.pass_fail, self._score_percent(),
            )

        return result

    def _check_termination(self) -> bool:
        """Update self.status / self.pass_fail and return True if the session is over."""
        if self.total_answered >= self.minimum_questions:
            if (self.hard_streak >= self.pass_hard_streak
                    and self.total_hard_answered >= self.min_hard_for_pass):
                self.status = "complete"
                self.pass_fail = "pass"
                self.terminated_early = True
                return True

            if self.easy_fail_streak >= self.fail_easy_streak:
                self.status = "complete"
                self.pass_fail = "fail"
                self.terminated_early = True
                return True

        if self.total_answered >= self.total_questions:
            score = self._score_percent()
            self.status = "complete"
            self.terminated_early = False
            if score >= self.pass_score:
                self.pass_fail = "pass"
            elif score <= self.fail_score:
                self.pass_fail = "fail"
            else:
                self.pass_fail = "borderline"
            return True

        return False

    # -----------------------------------------------------------------------
    # Problem selection
    # -----------------------------------------------------------------------

    def get_next_problem_pool(self) -> list:
        """
        Return the (subject, topic) pairs this mode is allowed to draw from.

        Pretest  — every implemented topic, regardless of mastery (the
                   student has not studied yet, so mastery is irrelevant).
        Final    — only topics the student has already mastered.
        """
        pool = []
        for subject, topics in _ALL_SUBJECT_TOPICS.items():
            for topic in topics:
                if not is_topic_available(subject, topic):
                    continue
                if self.mode == config.CAT_MODE_PRETEST:
                    pool.append((subject, topic))
                elif self.tracker.is_topic_mastered(subject, topic):
                    pool.append((subject, topic))
        return pool

    def _get_next_problem(self) -> dict:
        """Pick a weighted-random topic and return a fresh problem from it."""
        pool = self.get_next_problem_pool()
        if not pool:
            stub = {
                "question":    "No problems are available for this assessment yet.",
                "answer":      "0",
                "type":        "numeric",
                "explanation": "",
                "subject":     "",
                "topic":       "",
            }
            self.current_problem = stub
            return stub

        weights = [self._topic_weight(subject, topic) for subject, topic in pool]
        subject, topic = random.choices(pool, weights=weights, k=1)[0]

        candidate = None
        for _ in range(5):
            candidate = get_problem(subject, topic, self.current_difficulty)
            if candidate.get("question", "") not in self.seen_questions:
                break

        candidate["subject"] = subject
        candidate["topic"]   = topic
        self.seen_questions.add(candidate.get("question", ""))
        self.current_problem = candidate
        return candidate

    def _topic_weight(self, subject: str, topic: str) -> float:
        """Weight under-performing / unseen topics more heavily for selection."""
        seen = [
            r for r in self.answer_log
            if r["subject"] == subject and r["topic"] == topic
        ]
        if not seen:
            return 1.5
        pct_correct = sum(1 for r in seen if r["correct"]) / len(seen)
        if pct_correct < 0.5:
            return 2.0
        return 1.0

    # -----------------------------------------------------------------------
    # Answer evaluation  (mirrors core/evaluator.py's _is_correct logic)
    # -----------------------------------------------------------------------

    def _evaluate_answer(self, student_input: str, expected: Any, answer_type: str) -> bool:
        if not student_input:
            return False

        if answer_type == "numeric":
            return self._numeric_match(student_input, expected)

        if answer_type == "multiple_choice":
            return student_input.lower().strip() == str(expected).lower().strip()

        if answer_type in ("expression", "inequality"):
            return self._expression_match(student_input, expected)

        return student_input.lower() == str(expected).lower()

    def _numeric_match(self, student_input: str, expected: Any) -> bool:
        try:
            if "/" in student_input:
                parts = student_input.split("/")
                if len(parts) != 2:
                    return False
                student_val = float(parts[0]) / float(parts[1])
            else:
                student_val = float(student_input)
            expected_val = float(expected)
            return abs(student_val - expected_val) <= FLOAT_TOLERANCE
        except (ValueError, ZeroDivisionError):
            return False

    def _expression_match(self, student_input: str, expected: Any) -> bool:
        def normalise(s: str) -> str:
            return s.lower().replace(" ", "").replace("*", "")
        return normalise(student_input) == normalise(str(expected))

    # -----------------------------------------------------------------------
    # Scoring / summary
    # -----------------------------------------------------------------------

    def _score_percent(self) -> int:
        if self.total_answered == 0:
            return 0
        return int((self.total_correct / self.total_answered) * 100)

    def _result_message(self) -> str:
        if self.mode == config.CAT_MODE_PRETEST:
            if self.pass_fail == "pass":
                return config.PRETEST_RESULT_STRONG
            if self.pass_fail == "borderline":
                return config.PRETEST_RESULT_ADEQUATE
            return config.PRETEST_RESULT_WEAK

        if self.pass_fail == "pass":
            return config.CAT_RESULT_PASS_EARLY if self.terminated_early else config.CAT_RESULT_PASS_SCORE
        if self.pass_fail == "borderline":
            return config.CAT_RESULT_BORDERLINE
        return config.CAT_RESULT_FAIL_EARLY if self.terminated_early else config.CAT_RESULT_FAIL_SCORE

    def get_summary(self) -> dict:
        """Return the full end-of-session summary, ready for the result screen and history."""
        topic_breakdown: dict = {}
        for record in self.answer_log:
            key = f"{record['subject']}/{record['topic']}"
            entry = topic_breakdown.setdefault(key, {
                "subject":   record["subject"],
                "topic":     record["topic"],
                "label":     config.TOPIC_LABELS.get(record["topic"], record["topic"]),
                "attempted": 0,
                "correct":   0,
            })
            entry["attempted"] += 1
            if record["correct"]:
                entry["correct"] += 1

        strong_topics, adequate_topics, weak_topics = [], [], []
        weak_topic_pairs: list = []

        for entry in topic_breakdown.values():
            pct = (entry["correct"] / entry["attempted"] * 100) if entry["attempted"] else 0
            entry["percent"] = int(pct)
            if pct >= 80:
                entry["strength"] = "strong"
                strong_topics.append(entry["label"])
            elif pct >= 50:
                entry["strength"] = "adequate"
                adequate_topics.append(entry["label"])
            else:
                entry["strength"] = "weak"
                weak_topics.append(entry["label"])
                weak_topic_pairs.append((entry["subject"], entry["topic"]))

        if self.mode == config.CAT_MODE_PRETEST:
            if weak_topic_pairs:
                _, first_weak_topic = weak_topic_pairs[0]
                recommended_start = config.TOPIC_LABELS.get(first_weak_topic, first_weak_topic)
            else:
                recommended_start = "You are ready to begin!"
        else:
            recommended_start = ""

        elapsed = int(time.time() - self.start_time) if self.start_time else 0

        return {
            "mode":               self.mode,
            "total_answered":     self.total_answered,
            "total_correct":      self.total_correct,
            "score_percent":      self._score_percent(),
            "pass_fail":          self.pass_fail,
            "result_message":     self._result_message(),
            "hard_streak_peak":   self.hard_streak_peak,
            "difficulty_journey": [r["difficulty"] for r in self.answer_log],
            "topic_breakdown":    topic_breakdown,
            "strong_topics":      strong_topics,
            "adequate_topics":    adequate_topics,
            "weak_topics":        weak_topics,
            "weak_topic_pairs":   weak_topic_pairs,
            "answer_log":         self.answer_log,
            "elapsed_seconds":    elapsed,
            "date":               datetime.now().isoformat(timespec="seconds"),
            "recommended_start":  recommended_start,
        }
