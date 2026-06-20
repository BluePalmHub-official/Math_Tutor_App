# =============================================================================
# core/session_manager.py
# Manages the live state of one active learning session.
#
# A "session" is one run through a phase for a topic — e.g. the student
# opens the Practice phase for Linear Equations and answers problems until
# they finish or close the screen.
#
# Responsibilities:
#   - Hold all live state: subject, topic, phase, current question index,
#     problem set, timer, score
#   - Coordinate between ProgressTracker and Evaluator
#   - Provide clean start/advance/finish methods the GUI screens call
#   - Generate a unique session ID for logging
#
# The GUI never touches ProgressTracker or Evaluator directly —
# it goes through SessionManager only.
# =============================================================================

import uuid
import time
import logging
from typing import Optional

import config
from core.progress_tracker import ProgressTracker
from core.evaluator import Evaluator
from core.problem_engine import get_problem, get_problem_set

logger = logging.getLogger(__name__)


class SessionManager:
    """
    Single instance shared across the entire app lifetime.
    The GUI root (app_root.py) creates one instance and passes it to screens.

    Typical usage flow (Evaluate phase):
        sm.start_session("algebra", "linear_equations", "evaluate")
        problem = sm.current_problem()
        result  = sm.submit_answer("3")
        if sm.is_session_complete():
            summary = sm.finish_session()
    """

    def __init__(self, tracker: ProgressTracker):
        self.tracker = tracker

        # --- Active session state (reset on each start_session call) ---
        self._session_id:     str          = ""
        self._subject:        str          = ""
        self._topic:          str          = ""
        self._phase:          str          = ""
        self._difficulty:     str          = config.DIFFICULTY_EASY
        self._problems:       list[dict]   = []
        self._current_index:  int          = 0
        self._evaluator:      Optional[Evaluator] = None

        # Practice-mode specific
        self._used_hint:           bool = False
        self._used_show_solution:  bool = False

        # Timer support
        self._session_start_time:  float = 0.0

        logger.info("SessionManager initialised")

    # -----------------------------------------------------------------------
    # Session lifecycle
    # -----------------------------------------------------------------------

    def start_session(self, subject: str, topic: str, phase: str) -> None:
        """
        Begin a new session for the given subject / topic / phase.

        Generates the problem set, resets all counters, and creates a
        fresh Evaluator.  Call this every time the student enters a
        Practice or Evaluate screen.

        Parameters:
            subject : "algebra" or "geometry"
            topic   : e.g. "linear_equations"
            phase   : "practice" or "evaluate"
        """
        self._session_id    = str(uuid.uuid4())[:8]   # short ID for logs
        self._subject       = subject
        self._topic         = topic
        self._phase         = phase
        self._current_index = 0
        self._used_hint           = False
        self._used_show_solution  = False
        self._session_start_time  = time.time()

        # Difficulty comes from saved progress
        self._difficulty = self.tracker.get_current_difficulty(subject, topic)

        # Build the problem set
        if phase == config.PHASE_EVALUATE:
            self._problems = get_problem_set(
                subject, topic, self._difficulty, count=config.PROBLEMS_PER_ROUND
            )
        else:
            # Practice: generate a rolling set; we'll fetch fresh ones as needed
            self._problems = get_problem_set(
                subject, topic, self._difficulty,
                count=config.PRACTICE_WINDOW_SIZE * 2   # buffer
            )

        self._evaluator = Evaluator(
            session_id=self._session_id,
            subject=subject,
            topic=topic,
            phase=phase,
        )

        logger.info(
            "Session started | id=%s | %s/%s | phase=%s | difficulty=%s | %d problems",
            self._session_id, subject, topic, phase,
            self._difficulty, len(self._problems),
        )

    # -----------------------------------------------------------------------
    # Problem navigation
    # -----------------------------------------------------------------------

    def current_problem(self) -> Optional[dict]:
        """
        Return the current problem dict, or None if the session is complete.
        """
        if self._current_index < len(self._problems):
            return self._problems[self._current_index]
        return None

    def current_question_number(self) -> int:
        """1-based question number for display ("Question 3 of 10")."""
        return self._current_index + 1

    def total_questions(self) -> int:
        """Total number of problems in this session."""
        if self._phase == config.PHASE_EVALUATE:
            return config.PROBLEMS_PER_ROUND
        return len(self._problems)

    def is_session_complete(self) -> bool:
        """
        True when the student has answered all questions in an Evaluate round,
        or met the Practice pass condition.
        """
        if self._phase == config.PHASE_EVALUATE:
            return self._current_index >= config.PROBLEMS_PER_ROUND

        # Practice: complete when pass streak is met
        if self._evaluator:
            return self._evaluator.current_streak >= config.PRACTICE_PASS_STREAK
        return False

    def is_practice_passed(self) -> bool:
        """True if the practice streak threshold has been reached."""
        if self._evaluator:
            return self._evaluator.current_streak >= config.PRACTICE_PASS_STREAK
        return False

    # -----------------------------------------------------------------------
    # Answering
    # -----------------------------------------------------------------------

    def submit_answer(self, student_input: str) -> dict:
        """
        Submit the student's answer for the current problem.

        Calls Evaluator.check(), advances the question index, and — if in
        practice mode — updates ProgressTracker with the streak result.

        Returns the full result dict from Evaluator.check() plus:
            "question_number": int   (1-based)
            "is_last":         bool  True if this was the final question
            "practice_passed": bool  True if practice unlock condition just met
        """
        if not self._evaluator:
            raise RuntimeError("submit_answer called before start_session")

        problem = self.current_problem()
        if problem is None:
            raise RuntimeError("submit_answer called but no current problem")

        result = self._evaluator.check(
            student_input=student_input,
            expected_answer=problem["answer"],
            problem=problem,
            used_hint=self._used_hint,
            used_show_solution=self._used_show_solution,
        )

        # Advance to next question
        self._current_index += 1

        # Reset per-question flags
        self._used_hint          = False
        self._used_show_solution = False

        # Practice mode — sync streak with ProgressTracker
        practice_passed = False
        if self._phase == config.PHASE_PRACTICE:
            pt_result = self.tracker.update_practice(
                subject=self._subject,
                topic=self._topic,
                correct=result["correct"],
                used_show_solution=result["used_show_solution"],
            )
            practice_passed = pt_result.get("unlocked", False)

        is_last = self.is_session_complete()

        result["question_number"] = self._current_index   # now 1-based (after advance)
        result["is_last"]         = is_last
        result["practice_passed"] = practice_passed

        logger.debug(
            "Answer submitted | q=%d | correct=%s | streak=%d",
            result["question_number"], result["correct"], result["streak"],
        )

        return result

    # -----------------------------------------------------------------------
    # Hint / Show Solution flags  (set by GUI before submit_answer)
    # -----------------------------------------------------------------------

    def mark_hint_used(self) -> None:
        """Call when the student opens a hint panel."""
        self._used_hint = True

    def mark_show_solution_used(self) -> None:
        """Call when the student clicks Show Solution."""
        self._used_show_solution = True

    # -----------------------------------------------------------------------
    # Finishing a session
    # -----------------------------------------------------------------------

    def finish_session(self) -> dict:
        """
        Finalise the session and persist results.

        For Evaluate phase: records score in ProgressTracker and returns
        the full summary dict for result_screen.py to display.

        For Practice phase: the tracker is already updated per-answer via
        update_practice(), so this just returns the summary.

        Returns:
        {
          "summary":           dict,   from Evaluator.get_summary()
          "tracker_result":    dict,   from ProgressTracker (evaluate only)
          "elapsed_seconds":   int,    total session duration
          "subject":           str,
          "topic":             str,
          "phase":             str,
          "topic_label":       str,
        }
        """
        if not self._evaluator:
            raise RuntimeError("finish_session called before start_session")

        summary  = self._evaluator.get_summary()
        elapsed  = int(time.time() - self._session_start_time)
        tracker_result = {}

        if self._phase == config.PHASE_EVALUATE:
            tracker_result = self.tracker.record_evaluate_result(
                subject=self._subject,
                topic=self._topic,
                score_percent=summary["score_percent"],
            )

        logger.info(
            "Session finished | id=%s | %s/%s | score=%d%% | elapsed=%ds",
            self._session_id, self._subject, self._topic,
            summary["score_percent"], elapsed,
        )

        return {
            "summary":         summary,
            "tracker_result":  tracker_result,
            "elapsed_seconds": elapsed,
            "subject":         self._subject,
            "topic":           self._topic,
            "phase":           self._phase,
            "topic_label":     config.TOPIC_LABELS.get(self._topic, self._topic),
        }

    # -----------------------------------------------------------------------
    # Read-only state accessors  (used by GUI screens for display)
    # -----------------------------------------------------------------------

    @property
    def subject(self) -> str:
        return self._subject

    @property
    def topic(self) -> str:
        return self._topic

    @property
    def phase(self) -> str:
        return self._phase

    @property
    def difficulty(self) -> str:
        return self._difficulty

    @property
    def current_score_percent(self) -> int:
        """Live running score % during a session."""
        if self._evaluator:
            return self._evaluator._score_percent()
        return 0

    @property
    def current_streak(self) -> int:
        if self._evaluator:
            return self._evaluator.current_streak
        return 0

    def elapsed_seconds(self) -> int:
        return int(time.time() - self._session_start_time)

    def get_answer_log(self) -> list[dict]:
        """Return the per-question answer log for the current session."""
        if self._evaluator:
            return self._evaluator.answer_log
        return []