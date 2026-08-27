# =============================================================================
# gui/screens/cat_screen.py
# Computerised Adaptive Test (CAT) session screen.
#
# Drives one CAT session (either mode) using the shared CATEngine:
#   - Renders one adaptive question at a time
#   - Shows live difficulty, streaks, score, and elapsed time
#   - Auto-advances 2s after each answer (no hints, no show solution)
#   - Navigates to cat_result_screen when the engine reports completion
# =============================================================================

import time
import tkinter as tk
from tkinter import ttk
import logging

import config
from gui.styles import COLOURS, FONTS, PAD, make_button

logger = logging.getLogger(__name__)

# Mode-specific accent colours (not part of the shared palette — CAT-only)
_MODE_ACCENT = {
    config.CAT_MODE_PRETEST: "#17A398",   # teal / cyan
    config.CAT_MODE_FINAL:   COLOURS["accent_purple"],
}
_MODE_LABEL = {
    config.CAT_MODE_PRETEST: "📋  Diagnostic Pre-Test",
    config.CAT_MODE_FINAL:   "🎓  Final Adaptive Exam",
}
_DIFFICULTY_PILL_COLOUR = {
    config.DIFFICULTY_EASY:   COLOURS["accent_blue"],
    config.DIFFICULTY_MEDIUM: COLOURS["accent_orange"],
    config.DIFFICULTY_HARD:   COLOURS["accent_red"],
}


class CATScreen(tk.Frame):

    def __init__(self, parent: tk.Widget, app, mode: str = "pretest", **kwargs):
        super().__init__(parent, bg=COLOURS["bg_main"])
        self.app        = app
        self.mode       = mode
        self.cat_engine = app.cat_engine
        self.cat_engine.set_mode(mode)
        self.accent     = _MODE_ACCENT.get(mode, COLOURS["accent_blue"])

        self._answered      = False
        self._paused        = False
        self._pause_started = 0.0
        self._pending_result = None
        self._timer_job    = None
        self._banner_job   = None
        self._advance_job  = None

        self.current_problem = self.cat_engine.start()
        self._start_time = time.time()

        self._build()
        self._render_problem()
        self._tick_timer()

    # -----------------------------------------------------------------------
    # Layout
    # -----------------------------------------------------------------------

    def _build(self) -> None:
        self._build_header()
        self._build_body()
        self._build_footer()

    def _build_header(self) -> None:
        header = tk.Frame(self, bg=COLOURS["bg_header"], height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=_MODE_LABEL.get(self.mode, "CAT"),
            font=FONTS["subheading"],
            fg=self.accent,
            bg=COLOURS["bg_header"],
        ).pack(side="left", padx=PAD["lg"])

        self._diff_pill = tk.Label(
            header,
            text="",
            font=FONTS["small_bold"],
            fg=COLOURS["text_white"],
            padx=PAD["md"], pady=4,
        )
        self._diff_pill.pack(side="left", padx=PAD["lg"])

        self._counter_label = tk.Label(
            header,
            text="",
            font=FONTS["small_bold"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_header"],
        )
        self._counter_label.pack(side="right", padx=PAD["lg"])

    def _build_body(self) -> None:
        body = tk.Frame(self, bg=COLOURS["bg_main"])
        body.pack(fill="both", expand=True, padx=PAD["xl"], pady=PAD["md"])

        # ── Progress bar + score ─────────────────────────────────────────────
        bar_row = tk.Frame(body, bg=COLOURS["bg_main"])
        bar_row.pack(fill="x", pady=(0, PAD["sm"]))

        self._progress_var = tk.DoubleVar(value=0)
        ttk.Progressbar(
            bar_row,
            variable=self._progress_var,
            maximum=self.cat_engine.total_questions,
            style="Green.Horizontal.TProgressbar",
        ).pack(side="left", fill="x", expand=True)

        self._score_label = tk.Label(
            bar_row,
            text="Score: 0/0 (0%)",
            font=FONTS["small_bold"],
            fg=COLOURS["accent_green"],
            bg=COLOURS["bg_main"],
        )
        self._score_label.pack(side="left", padx=(PAD["sm"], 0))

        # ── Streak row ───────────────────────────────────────────────────────
        streak_row = tk.Frame(body, bg=COLOURS["bg_main"])
        streak_row.pack(fill="x", pady=(0, PAD["sm"]))

        self._streak_dots_frame = tk.Frame(streak_row, bg=COLOURS["bg_main"])
        self._streak_dots_frame.pack(side="left")

        self._streak_text_label = tk.Label(
            streak_row,
            text="",
            font=FONTS["small"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_main"],
        )
        self._streak_text_label.pack(side="left", padx=(PAD["sm"], 0))

        # ── Difficulty shift banner (hidden until triggered) ───────────────
        self._banner_frame = tk.Frame(body, bg=COLOURS["bg_main"])
        self._banner_label = tk.Label(
            self._banner_frame,
            text="",
            font=FONTS["small_bold"],
            fg=COLOURS["text_dark"],
            pady=4,
        )
        self._banner_label.pack()

        # ── No-hints notice ──────────────────────────────────────────────────
        tk.Label(
            body,
            text="⚠️  Adaptive exam mode — no hints, no show solution.",
            font=FONTS["small"],
            fg=COLOURS["accent_orange"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["sm"]))

        # ── Question card ────────────────────────────────────────────────────
        self._q_card = tk.Frame(
            body, bg=COLOURS["bg_card"],
            highlightthickness=2,
            highlightbackground=self.accent,
        )
        self._q_card.pack(fill="x", pady=(0, PAD["md"]))

        q_hdr = tk.Frame(self._q_card, bg=self.accent)
        q_hdr.pack(fill="x")

        self._subj_topic_label = tk.Label(
            q_hdr,
            text="",
            font=FONTS["small_bold"],
            fg=COLOURS["text_white"],
            bg=self.accent,
            padx=PAD["md"], pady=4,
        )
        self._subj_topic_label.pack(side="left")

        self._diff_badge = tk.Label(
            q_hdr,
            text="",
            font=FONTS["tiny"],
            fg=COLOURS["text_white"],
            bg=self.accent,
            padx=PAD["md"],
        )
        self._diff_badge.pack(side="right")

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

        # ── Answer entry ─────────────────────────────────────────────────────
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
            highlightcolor=self.accent,
            highlightbackground=COLOURS["border"],
            width=16,
        )
        self._answer_entry.pack(side="left", ipady=8)
        self._answer_entry.bind("<Return>", lambda e: self._on_submit())

        self._submit_btn = make_button(
            answer_row, "Submit →", self._on_submit,
            variant="primary", pady=8, padx=16,
        )
        self._submit_btn.pack(side="left", padx=(PAD["sm"], 0))

        # ── Feedback panel ───────────────────────────────────────────────────
        self._feedback_frame = tk.Frame(
            body, bg=COLOURS["bg_main"],
            highlightthickness=1,
            highlightbackground=COLOURS["bg_main"],
        )
        self._feedback_label = tk.Label(
            self._feedback_frame,
            text="",
            font=FONTS["body_bold"],
            fg=COLOURS["text_primary"],
            bg=COLOURS["bg_main"],
            padx=PAD["md"], pady=PAD["sm"],
        )
        self._feedback_label.pack(anchor="w")

    def _build_footer(self) -> None:
        footer = tk.Frame(self, bg=COLOURS["bg_header"], height=48)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        self._timer_label = tk.Label(
            footer,
            text="0:00",
            font=FONTS["small_bold"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_header"],
        )
        self._timer_label.pack(side="left", padx=PAD["lg"])

        self._pause_btn = make_button(
            footer, "⏸ Pause", self._toggle_pause,
            variant="ghost", pady=4, padx=12, size="small_bold",
        )
        self._pause_btn.pack(side="right", padx=PAD["lg"])

    # -----------------------------------------------------------------------
    # Rendering
    # -----------------------------------------------------------------------

    def _render_problem(self) -> None:
        self._answered = False
        p = self.current_problem
        difficulty = self.cat_engine.current_difficulty

        q_num = self.cat_engine.question_number + 1
        total = self.cat_engine.total_questions
        self._counter_label.config(text=f"Q {q_num} of {total}")

        self._set_difficulty_pill(difficulty)
        self._diff_badge.config(text=difficulty.title())

        subject = p.get("subject", "")
        topic   = p.get("topic", "")
        topic_label = config.TOPIC_LABELS.get(topic, topic)
        self._subj_topic_label.config(
            text=f"{subject.title()} · {topic_label}" if subject else "Assessment"
        )

        self._q_label.config(text=p.get("question", ""))

        self._progress_var.set(self.cat_engine.total_answered)
        self._update_score_label()
        self._render_streak_dots()

        self._answer_var.set("")
        self._answer_entry.config(state="normal", highlightbackground=COLOURS["border"])
        self._answer_entry.focus_set()
        self._submit_btn.config(state="normal")

        self._feedback_frame.pack_forget()
        self._feedback_label.config(text="")

    def _set_difficulty_pill(self, difficulty: str) -> None:
        colour = _DIFFICULTY_PILL_COLOUR.get(difficulty, COLOURS["accent_blue"])
        self._diff_pill.config(text=f"● {difficulty.title()}", bg=colour)

    def _update_score_label(self) -> None:
        answered = self.cat_engine.total_answered
        correct  = self.cat_engine.total_correct
        pct = int((correct / answered) * 100) if answered else 0
        self._score_label.config(text=f"Score: {correct}/{answered} ({pct}%)")

    def _render_streak_dots(self) -> None:
        for child in self._streak_dots_frame.winfo_children():
            child.destroy()

        target  = self.cat_engine.pass_hard_streak
        current = self.cat_engine.hard_streak
        for i in range(target):
            filled = i < current
            tk.Label(
                self._streak_dots_frame,
                text="●" if filled else "○",
                font=FONTS["body_bold"],
                fg=COLOURS["accent_gold"] if filled else COLOURS["text_muted"],
                bg=COLOURS["bg_main"],
            ).pack(side="left")

        self._streak_text_label.config(
            text=f"Hard streak: {current} / {target} to pass"
        )

    # -----------------------------------------------------------------------
    # Answer submission
    # -----------------------------------------------------------------------

    def _on_submit(self) -> None:
        if self._answered or self._paused:
            return

        raw = self._answer_var.get().strip()
        if not raw:
            return

        self._answered = True
        old_difficulty = self.cat_engine.current_difficulty
        result = self.cat_engine.submit_answer(raw)
        self._pending_result = result

        self._progress_var.set(result["total_answered"])
        self._update_score_label()
        self._render_streak_dots()

        correct = result["correct"]
        bg  = COLOURS["bg_correct"]   if correct else COLOURS["bg_incorrect"]
        hlt = COLOURS["accent_green"] if correct else COLOURS["accent_red"]
        fg  = COLOURS["accent_green"] if correct else COLOURS["accent_red"]
        text = "✓ Correct!" if correct else f"✗ Incorrect — Answer: {result['expected_answer']}"

        self._feedback_frame.config(bg=bg, highlightbackground=hlt)
        self._feedback_label.config(text=text, fg=fg, bg=bg)
        self._feedback_frame.pack(fill="x", pady=(0, PAD["sm"]))

        self._answer_entry.config(state="disabled", highlightbackground=hlt)
        self._submit_btn.config(state="disabled")

        self._show_difficulty_banner(old_difficulty, result["next_difficulty"])

        self._advance_job = self.after(2000, self._advance_to_next)

    def _advance_to_next(self) -> None:
        try:
            result = self._pending_result
            if result is None:
                return

            if result.get("is_complete"):
                summary = self.cat_engine.get_summary()
                self._cleanup_jobs()
                self.app.go_cat_result(summary)
                return

            self.current_problem = result["next_problem"]
            self._render_problem()
        except tk.TclError:
            pass

    # -----------------------------------------------------------------------
    # Difficulty shift banner
    # -----------------------------------------------------------------------

    def _show_difficulty_banner(self, old_difficulty: str, new_difficulty: str) -> None:
        if old_difficulty == new_difficulty:
            self._banner_frame.pack_forget()
            return

        order = config.DIFFICULTY_ORDER
        moved_up = order.index(new_difficulty) > order.index(old_difficulty)

        if moved_up:
            colour = COLOURS["accent_green"] if new_difficulty == config.DIFFICULTY_HARD else COLOURS["accent_blue"]
            text = f"↑ Level Up — Moving to {new_difficulty.title()}"
        else:
            colour = COLOURS["accent_orange"]
            text = f"↓ Level Down — Moving to {new_difficulty.title()}"

        self._banner_label.config(text=text, bg=colour)
        self._banner_frame.config(bg=colour)
        self._banner_frame.pack(fill="x", before=self._q_card, pady=(0, PAD["sm"]))

        if self._banner_job is not None:
            try:
                self.after_cancel(self._banner_job)
            except tk.TclError:
                pass
        self._banner_job = self.after(1500, self._hide_banner)

    def _hide_banner(self) -> None:
        try:
            self._banner_frame.pack_forget()
        except tk.TclError:
            pass

    # -----------------------------------------------------------------------
    # Pause / resume
    # -----------------------------------------------------------------------

    def _toggle_pause(self) -> None:
        self._paused = not self._paused

        if self._paused:
            self._pause_started = time.time()
            self._pause_btn.config(text="▶ Click to Resume")
            self._q_label.config(text="🔒  Paused", fg=COLOURS["text_muted"])
            self._answer_entry.config(state="disabled")
            self._submit_btn.config(state="disabled")
        else:
            paused_duration = time.time() - self._pause_started
            self._start_time += paused_duration
            self._pause_btn.config(text="⏸ Pause")
            self._q_label.config(
                text=self.current_problem.get("question", ""),
                fg=COLOURS["text_primary"],
            )
            if not self._answered:
                self._answer_entry.config(state="normal")
                self._submit_btn.config(state="normal")
                self._answer_entry.focus_set()

    # -----------------------------------------------------------------------
    # Timer
    # -----------------------------------------------------------------------

    def _tick_timer(self) -> None:
        try:
            if not self._paused:
                elapsed = int(time.time() - self._start_time)
                mins, secs = divmod(elapsed, 60)
                self._timer_label.config(text=f"{mins}:{secs:02d}")
            self._timer_job = self.after(1000, self._tick_timer)
        except tk.TclError:
            pass

    # -----------------------------------------------------------------------
    # Cleanup
    # -----------------------------------------------------------------------

    def _cleanup_jobs(self) -> None:
        for job in (self._timer_job, self._banner_job, self._advance_job):
            if job is not None:
                try:
                    self.after_cancel(job)
                except tk.TclError:
                    pass
