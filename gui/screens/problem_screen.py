# =============================================================================
# gui/screens/problem_screen.py
# Phase 3 — EVALUATE screen.
#
# Formal scored assessment:
#   - 10 randomised problems
#   - NO hints, NO show solution
#   - Score tracked per answer
#   - Progress bar counts down questions
#   - Transitions to result_screen on completion
# =============================================================================

import tkinter as tk
from tkinter import ttk
import logging

import config
from core.session_manager import SessionManager
from gui.styles import COLOURS, FONTS, PAD, make_button

logger = logging.getLogger(__name__)


class ProblemScreen(tk.Frame):

    def __init__(self, parent: tk.Widget, app,
                 subject: str = "algebra",
                 topic: str = "linear_equations",
                 **kwargs):
        super().__init__(parent, bg=COLOURS["bg_main"])
        self.app     = app
        self.tracker = app.tracker
        self.subject = subject
        self.topic   = topic
        self.sm: SessionManager = app.session_manager

        self._answered = False

        # Start evaluate session
        self.sm.start_session(subject, topic, config.PHASE_EVALUATE)

        self._build()
        self._render_problem()

    # -----------------------------------------------------------------------
    # Layout
    # -----------------------------------------------------------------------

    def _build(self) -> None:
        self._build_header()
        self._build_body()
        self._build_footer()

    # -----------------------------------------------------------------------
    # Header
    # -----------------------------------------------------------------------

    def _build_header(self) -> None:
        header = tk.Frame(self, bg=COLOURS["bg_header"], height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        topic_label = config.TOPIC_LABELS.get(self.topic, self.topic)
        tk.Label(
            header,
            text=f"🎯  Evaluate — {topic_label}",
            font=FONTS["subheading"],
            fg=COLOURS["accent_purple"],
            bg=COLOURS["bg_header"],
        ).pack(side="left", padx=PAD["lg"])

        # Question counter
        self._counter_label = tk.Label(
            header,
            text=f"Question  1  of  {config.PROBLEMS_PER_ROUND}",
            font=FONTS["small_bold"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_header"],
        )
        self._counter_label.pack(side="right", padx=PAD["lg"])

        tk.Label(
            header,
            text="PHASE 3 OF 3",
            font=FONTS["tiny"],
            fg=COLOURS["accent_purple"],
            bg=COLOURS["bg_header"],
        ).pack(side="right", padx=(0, PAD["sm"]))

    # -----------------------------------------------------------------------
    # Body
    # -----------------------------------------------------------------------

    def _build_body(self) -> None:
        body = tk.Frame(self, bg=COLOURS["bg_main"])
        body.pack(fill="both", expand=True, padx=PAD["xl"], pady=PAD["lg"])

        # ── Progress bar ────────────────────────────────────────────────────
        bar_row = tk.Frame(body, bg=COLOURS["bg_main"])
        bar_row.pack(fill="x", pady=(0, PAD["lg"]))

        self._progress_var = tk.DoubleVar(value=0)
        ttk.Progressbar(
            bar_row,
            variable=self._progress_var,
            maximum=config.PROBLEMS_PER_ROUND,
            style="Green.Horizontal.TProgressbar",
        ).pack(side="left", fill="x", expand=True)

        self._score_label = tk.Label(
            bar_row,
            text="Score: 0 / 0",
            font=FONTS["small_bold"],
            fg=COLOURS["accent_green"],
            bg=COLOURS["bg_main"],
        )
        self._score_label.pack(side="left", padx=(PAD["sm"], 0))

        # ── No hints notice ─────────────────────────────────────────────────
        tk.Label(
            body,
            text="⚠️  Evaluation mode — no hints available. Do your best!",
            font=FONTS["small"],
            fg=COLOURS["accent_orange"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["md"]))

        # ── Question card ───────────────────────────────────────────────────
        self._q_card = tk.Frame(
            body, bg=COLOURS["bg_card"],
            highlightthickness=2,
            highlightbackground=COLOURS["accent_purple"],
        )
        self._q_card.pack(fill="x", pady=(0, PAD["lg"]))

        # Card header bar
        q_hdr = tk.Frame(self._q_card, bg=COLOURS["accent_purple"])
        q_hdr.pack(fill="x")
        self._q_num_label = tk.Label(
            q_hdr,
            text="Question 1",
            font=FONTS["small_bold"],
            fg=COLOURS["text_white"],
            bg=COLOURS["accent_purple"],
            padx=PAD["md"], pady=4,
        )
        self._q_num_label.pack(side="left")

        self._diff_label = tk.Label(
            q_hdr,
            text="",
            font=FONTS["tiny"],
            fg=COLOURS["text_white"],
            bg=COLOURS["accent_purple"],
            padx=PAD["md"],
        )
        self._diff_label.pack(side="right")

        # Question text
        self._q_label = tk.Label(
            self._q_card,
            text="",
            font=FONTS["mono_large"],
            fg=COLOURS["text_primary"],
            bg=COLOURS["bg_card"],
            wraplength=580,
            justify="left",
            padx=PAD["lg"], pady=PAD["lg"],
        )
        self._q_label.pack(anchor="w")

        # ── Answer entry ────────────────────────────────────────────────────
        answer_row = tk.Frame(body, bg=COLOURS["bg_main"])
        answer_row.pack(fill="x", pady=(0, PAD["sm"]))

        tk.Label(
            answer_row,
            text="Your answer:",
            font=FONTS["body_bold"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_main"],
        ).pack(side="left", padx=(0, PAD["sm"]))

        self._answer_var = tk.StringVar()
        self._answer_entry = tk.Entry(
            answer_row,
            textvariable=self._answer_var,
            font=FONTS["mono_large"],
            bg=COLOURS["bg_input"],
            fg=COLOURS["text_primary"],
            insertbackground=COLOURS["text_primary"],
            relief="flat", bd=0,
            highlightthickness=2,
            highlightcolor=COLOURS["accent_purple"],
            highlightbackground=COLOURS["border"],
            width=16,
        )
        self._answer_entry.pack(side="left", ipady=8)
        self._answer_entry.bind("<Return>", lambda e: self._on_submit())
        self._answer_entry.focus_set()

        self._submit_btn = make_button(
            answer_row, "Submit Answer →", self._on_submit,
            variant="primary", pady=8, padx=16,
        )
        self._submit_btn.pack(side="left", padx=(PAD["sm"], 0))

        # ── Feedback (correct / incorrect indicator only — no explanation) ──
        self._feedback_frame = tk.Frame(
            body, bg=COLOURS["bg_main"],
            highlightthickness=1,
            highlightbackground=COLOURS["bg_main"],
        )
        self._feedback_frame.pack(fill="x", pady=(0, PAD["sm"]))

        self._feedback_label = tk.Label(
            self._feedback_frame,
            text="",
            font=FONTS["body_bold"],
            fg=COLOURS["text_primary"],
            bg=COLOURS["bg_main"],
            padx=PAD["md"], pady=PAD["sm"],
        )
        self._feedback_label.pack(anchor="w")

    # -----------------------------------------------------------------------
    # Footer
    # -----------------------------------------------------------------------

    def _build_footer(self) -> None:
        footer = tk.Frame(self, bg=COLOURS["bg_header"], height=48)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        self._next_btn = make_button(
            footer, "Next Question →", self._on_next,
            variant="primary", pady=6, padx=16,
        )
        self._next_btn.pack(side="right", padx=PAD["lg"], pady=PAD["sm"])
        self._next_btn.config(state="disabled")

        self._footer_status = tk.Label(
            footer,
            text="",
            font=FONTS["small"],
            fg=COLOURS["text_muted"],
            bg=COLOURS["bg_header"],
        )
        self._footer_status.pack(side="left", padx=PAD["lg"])

    # -----------------------------------------------------------------------
    # Render problem
    # -----------------------------------------------------------------------

    def _render_problem(self) -> None:
        p = self.sm.current_problem()
        if not p:
            self._finish()
            return

        self._answered = False
        q_num  = self.sm.current_question_number()
        total  = self.sm.total_questions()
        diff   = self.sm.difficulty.title()

        self._q_label.config(text=p.get("question", ""))
        self._q_num_label.config(text=f"Question {q_num}")
        self._diff_label.config(text=diff)
        self._counter_label.config(
            text=f"Question  {q_num}  of  {total}"
        )
        self._progress_var.set(q_num - 1)

        self._answer_var.set("")
        self._answer_entry.config(
            state="normal",
            highlightbackground=COLOURS["border"],
        )
        self._answer_entry.focus_set()
        self._submit_btn.config(state="normal")
        self._next_btn.config(state="disabled",
                              text="Next Question →",
                              command=self._on_next)
        self._feedback_label.config(text="", bg=COLOURS["bg_main"])
        self._feedback_frame.config(
            bg=COLOURS["bg_main"],
            highlightbackground=COLOURS["bg_main"],
        )
        self._footer_status.config(text="")

    # -----------------------------------------------------------------------
    # Answer submission
    # -----------------------------------------------------------------------

    def _on_submit(self) -> None:
        if self._answered:
            return

        raw = self._answer_var.get().strip()
        if not raw:
            self._feedback_label.config(
                text="Please enter an answer.",
                fg=COLOURS["accent_orange"],
                bg=COLOURS["bg_main"],
            )
            return

        result = self.sm.submit_answer(raw)
        self._answered = True

        correct = result["correct"]
        q_num   = result["question_number"]
        total   = self.sm.total_questions()
        correct_count = self.sm.current_score_percent * total // 100

        # Update score display
        self._score_label.config(
            text=f"Score: {self.sm._evaluator.total_correct} / {q_num}"
        )
        self._progress_var.set(q_num)

        # Feedback — simple correct / incorrect, no full explanation
        bg  = COLOURS["bg_correct"]   if correct else COLOURS["bg_incorrect"]
        hlt = COLOURS["accent_green"] if correct else COLOURS["accent_red"]
        fg  = COLOURS["accent_green"] if correct else COLOURS["accent_red"]
        icon = "✓  Correct!" if correct else "✗  Incorrect"

        self._feedback_frame.config(bg=bg, highlightbackground=hlt)
        self._feedback_label.config(text=icon, fg=fg, bg=bg)

        self._answer_entry.config(
            state="disabled",
            highlightbackground=hlt,
        )
        self._submit_btn.config(state="disabled")

        # Update footer status
        remaining = total - q_num
        if remaining > 0:
            self._footer_status.config(
                text=f"{remaining} question{'s' if remaining != 1 else ''} remaining"
            )
        else:
            self._footer_status.config(text="Last question answered!")

        # Is this the final question?
        if result.get("is_last") or self.sm.is_session_complete():
            self._next_btn.config(
                text="See Results →",
                command=self._finish,
                state="normal",
                bg=COLOURS["accent_gold"],
                fg=COLOURS["text_dark"],
            )
        else:
            self._next_btn.config(state="normal")

    # -----------------------------------------------------------------------
    # Next question / finish
    # -----------------------------------------------------------------------

    def _on_next(self) -> None:
        self._render_problem()

    def _finish(self) -> None:
        """End the session and navigate to the result screen."""
        result_data = self.sm.finish_session()
        self.app.go_result(result_data)