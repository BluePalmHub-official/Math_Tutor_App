# =============================================================================
# gui/screens/practice_screen.py
# Phase 2 — PRACTICE screen.
#
# Low-stakes repetition with full scaffolding:
#   - Hints available (3 levels: nudge → partial → full method)
#   - Show Solution button available (resets streak)
#   - Immediate feedback after every answer
#   - Streak tracker — need PRACTICE_PASS_STREAK correct in a row
#   - No score pressure — unlimited attempts
#
# Transitions to: problem_screen (when streak threshold met)
# =============================================================================

import tkinter as tk
import logging

import config
from core.session_manager import SessionManager
from gui.styles import COLOURS, FONTS, PAD, make_button

logger = logging.getLogger(__name__)


class PracticeScreen(tk.Frame):

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

        # Per-question state
        self._answered          = False
        self._used_hint         = False
        self._used_show_sol     = False
        self._hint_level        = 0       # 0 = none shown, 1/2/3 = hint level
        self._current_problem   = None

        # Start session
        self.sm.start_session(subject, topic, config.PHASE_PRACTICE)
        self._current_problem = self.sm.current_problem()

        self._build()

    # -----------------------------------------------------------------------
    # Layout
    # -----------------------------------------------------------------------

    def _build(self) -> None:
        self._build_header()
        self._build_body()
        self._build_footer()
        self._render_problem()

    # -----------------------------------------------------------------------
    # Header
    # -----------------------------------------------------------------------

    def _build_header(self) -> None:
        header = tk.Frame(self, bg=COLOURS["bg_header"], height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        make_button(
            header, "← Topics",
            lambda: self.app.go_topic(self.subject),
            variant="ghost", pady=4, padx=12, size="small_bold",
        ).pack(side="left", padx=PAD["md"])

        topic_label = config.TOPIC_LABELS.get(self.topic, self.topic)
        tk.Label(
            header,
            text=f"✏️  Practice — {topic_label}",
            font=FONTS["subheading"],
            fg=COLOURS["accent_orange"],
            bg=COLOURS["bg_header"],
        ).pack(side="left", padx=PAD["sm"])

        tk.Label(
            header,
            text="PHASE 2 OF 3",
            font=FONTS["tiny"],
            fg=COLOURS["accent_orange"],
            bg=COLOURS["bg_header"],
        ).pack(side="right", padx=PAD["lg"])

    # -----------------------------------------------------------------------
    # Body
    # -----------------------------------------------------------------------

    def _build_body(self) -> None:
        body = tk.Frame(self, bg=COLOURS["bg_main"])
        body.pack(fill="both", expand=True, padx=PAD["xl"], pady=PAD["lg"])

        # ── Streak bar ──────────────────────────────────────────────────────
        streak_row = tk.Frame(body, bg=COLOURS["bg_main"])
        streak_row.pack(fill="x", pady=(0, PAD["md"]))

        tk.Label(
            streak_row,
            text=f"Streak needed to unlock Evaluate:  "
                 f"{config.PRACTICE_PASS_STREAK} correct in a row",
            font=FONTS["small"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_main"],
        ).pack(side="left")

        self._streak_label = tk.Label(
            streak_row,
            text="Streak: 0",
            font=FONTS["small_bold"],
            fg=COLOURS["accent_orange"],
            bg=COLOURS["bg_main"],
        )
        self._streak_label.pack(side="right")

        # Streak dots
        self._dot_frame = tk.Frame(body, bg=COLOURS["bg_main"])
        self._dot_frame.pack(anchor="w", pady=(0, PAD["md"]))
        self._draw_streak_dots(0)

        # ── Question card ───────────────────────────────────────────────────
        self._q_card = tk.Frame(
            body, bg=COLOURS["bg_card"],
            highlightthickness=1,
            highlightbackground=COLOURS["border"],
        )
        self._q_card.pack(fill="x", pady=(0, PAD["md"]))

        self._q_label = tk.Label(
            self._q_card,
            text="",
            font=FONTS["mono_large"],
            fg=COLOURS["text_primary"],
            bg=COLOURS["bg_card"],
            wraplength=600,
            justify="left",
            padx=PAD["lg"], pady=PAD["lg"],
        )
        self._q_label.pack(anchor="w")

        # ── Hint panel ──────────────────────────────────────────────────────
        self._hint_frame = tk.Frame(body, bg=COLOURS["bg_main"])
        self._hint_frame.pack(fill="x", pady=(0, PAD["sm"]))

        self._hint_label = tk.Label(
            self._hint_frame,
            text="",
            font=FONTS["small"],
            fg=COLOURS["accent_gold"],
            bg=COLOURS["bg_highlight"],
            wraplength=600,
            justify="left",
            padx=PAD["md"], pady=PAD["sm"],
        )

        # Hint buttons row
        hint_btn_row = tk.Frame(body, bg=COLOURS["bg_main"])
        hint_btn_row.pack(anchor="w", pady=(0, PAD["md"]))

        self._hint1_btn = make_button(
            hint_btn_row, "💡 Hint 1", lambda: self._show_hint(1),
            variant="ghost", pady=4, padx=10, size="small_bold",
        )
        self._hint1_btn.pack(side="left", padx=(0, PAD["sm"]))

        self._hint2_btn = make_button(
            hint_btn_row, "💡 Hint 2", lambda: self._show_hint(2),
            variant="ghost", pady=4, padx=10, size="small_bold",
        )
        self._hint2_btn.pack(side="left", padx=(0, PAD["sm"]))

        self._hint3_btn = make_button(
            hint_btn_row, "💡 Hint 3", lambda: self._show_hint(3),
            variant="ghost", pady=4, padx=10, size="small_bold",
        )
        self._hint3_btn.pack(side="left", padx=(0, PAD["sm"]))

        self._show_sol_btn = make_button(
            hint_btn_row, "👁 Show Solution",
            self._on_show_solution,
            variant="danger", pady=4, padx=10, size="small_bold",
        )
        self._show_sol_btn.pack(side="left")

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
            highlightcolor=COLOURS["accent_blue"],
            highlightbackground=COLOURS["border"],
            width=16,
        )
        self._answer_entry.pack(side="left", ipady=8)
        self._answer_entry.bind("<Return>", lambda e: self._on_submit())
        self._answer_entry.focus_set()

        self._submit_btn = make_button(
            answer_row, "Check Answer →", self._on_submit,
            variant="primary", pady=8, padx=16,
        )
        self._submit_btn.pack(side="left", padx=(PAD["sm"], 0))

        # ── Feedback panel ──────────────────────────────────────────────────
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
            wraplength=600,
            justify="left",
            padx=PAD["md"], pady=PAD["sm"],
        )
        self._feedback_label.pack(anchor="w")

        self._explanation_label = tk.Label(
            self._feedback_frame,
            text="",
            font=FONTS["mono_small"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_main"],
            wraplength=600,
            justify="left",
            padx=PAD["md"],
        )
        self._explanation_label.pack(anchor="w")

    # -----------------------------------------------------------------------
    # Footer
    # -----------------------------------------------------------------------

    def _build_footer(self) -> None:
        footer = tk.Frame(self, bg=COLOURS["bg_header"], height=48)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        self._next_q_btn = make_button(
            footer, "Next Question →", self._on_next_question,
            variant="primary", pady=6, padx=16,
        )
        self._next_q_btn.pack(side="right", padx=PAD["lg"], pady=PAD["sm"])
        self._next_q_btn.config(state="disabled")

        self._status_label = tk.Label(
            footer,
            text="Answer the question above to continue.",
            font=FONTS["small"],
            fg=COLOURS["text_muted"],
            bg=COLOURS["bg_header"],
        )
        self._status_label.pack(side="left", padx=PAD["lg"])

    # -----------------------------------------------------------------------
    # Render current problem
    # -----------------------------------------------------------------------

    def _render_problem(self) -> None:
        """Display the current problem and reset per-question state."""
        p = self._current_problem
        if not p:
            return

        self._answered      = False
        self._used_hint     = False
        self._used_show_sol = False
        self._hint_level    = 0

        self._q_label.config(text=p.get("question", ""))
        self._answer_var.set("")
        self._answer_entry.config(state="normal",
                                  highlightbackground=COLOURS["border"])
        self._answer_entry.focus_set()
        self._submit_btn.config(state="normal")
        self._next_q_btn.config(state="disabled")
        self._feedback_label.config(text="", bg=COLOURS["bg_main"])
        self._explanation_label.config(text="")
        self._feedback_frame.config(highlightbackground=COLOURS["bg_main"],
                                    bg=COLOURS["bg_main"])
        self._hint_label.pack_forget()
        self._status_label.config(text="Answer the question above to continue.")

        # Reset hint buttons
        for btn in (self._hint1_btn, self._hint2_btn,
                    self._hint3_btn, self._show_sol_btn):
            btn.config(state="normal")

    # -----------------------------------------------------------------------
    # Hint display
    # -----------------------------------------------------------------------

    def _show_hint(self, level: int) -> None:
        p = self._current_problem
        if not p or self._answered:
            return

        key = {1: "hint", 2: "hint2", 3: "hint3"}.get(level, "hint")
        hint_text = p.get(key, "No hint available.")

        self._hint_label.config(text=f"💡  {hint_text}")
        self._hint_label.pack(fill="x", pady=(0, PAD["sm"]))

        self._hint_level = max(self._hint_level, level)
        self._used_hint  = True
        self.sm.mark_hint_used()

    # -----------------------------------------------------------------------
    # Show solution
    # -----------------------------------------------------------------------

    def _on_show_solution(self) -> None:
        p = self._current_problem
        if not p:
            return

        self._used_show_sol = True
        self.sm.mark_show_solution_used()

        explanation = p.get("explanation", "No solution available.")
        self._feedback_frame.config(
            bg=COLOURS["bg_card"],
            highlightbackground=COLOURS["accent_orange"],
        )
        self._feedback_label.config(
            text="Solution shown — your streak has been reset.",
            fg=COLOURS["accent_orange"],
            bg=COLOURS["bg_card"],
        )
        self._explanation_label.config(
            text=explanation,
            bg=COLOURS["bg_card"],
        )

        self._answer_entry.config(state="disabled")
        self._submit_btn.config(state="disabled")
        for btn in (self._hint1_btn, self._hint2_btn,
                    self._hint3_btn, self._show_sol_btn):
            btn.config(state="disabled")

        self._next_q_btn.config(state="normal")
        self._answered = True

        # Submit to session manager so streak resets
        result = self.sm.submit_answer("__show_solution__")
        self._update_streak(result.get("streak", 0))

    # -----------------------------------------------------------------------
    # Answer submission
    # -----------------------------------------------------------------------

    def _on_submit(self) -> None:
        if self._answered:
            return

        raw = self._answer_var.get().strip()
        if not raw:
            self._feedback_label.config(
                text="Please enter an answer first.",
                fg=COLOURS["accent_orange"],
                bg=COLOURS["bg_main"],
            )
            return

        result = self.sm.submit_answer(raw)
        self._answered = True

        correct = result["correct"]
        streak  = result["streak"]

        # Colour the card
        bg  = COLOURS["bg_correct"]   if correct else COLOURS["bg_incorrect"]
        hlt = COLOURS["accent_green"] if correct else COLOURS["accent_red"]
        fg  = COLOURS["accent_green"] if correct else COLOURS["accent_red"]

        self._feedback_frame.config(bg=bg, highlightbackground=hlt)
        self._feedback_label.config(
            text=result["feedback"],
            fg=fg, bg=bg,
        )
        self._explanation_label.config(
            text=result.get("explanation", ""),
            bg=bg,
        )

        # Highlight answer entry
        entry_colour = COLOURS["accent_green"] if correct else COLOURS["accent_red"]
        self._answer_entry.config(
            state="disabled",
            highlightbackground=entry_colour,
        )
        self._submit_btn.config(state="disabled")
        for btn in (self._hint1_btn, self._hint2_btn,
                    self._hint3_btn, self._show_sol_btn):
            btn.config(state="disabled")

        self._update_streak(streak)
        self._next_q_btn.config(state="normal")

        # Check if practice is now passed
        if result.get("practice_passed"):
            self._on_practice_passed()

    # -----------------------------------------------------------------------
    # Streak display
    # -----------------------------------------------------------------------

    def _update_streak(self, streak: int) -> None:
        colour = COLOURS["accent_green"] if streak > 0 else COLOURS["text_muted"]
        self._streak_label.config(
            text=f"Streak: {streak} / {config.PRACTICE_PASS_STREAK}",
            fg=colour,
        )
        self._draw_streak_dots(streak)

    def _draw_streak_dots(self, streak: int) -> None:
        for w in self._dot_frame.winfo_children():
            w.destroy()

        tk.Label(
            self._dot_frame,
            text="Progress: ",
            font=FONTS["small"],
            fg=COLOURS["text_muted"],
            bg=COLOURS["bg_main"],
        ).pack(side="left")

        for i in range(config.PRACTICE_PASS_STREAK):
            filled = i < streak
            tk.Label(
                self._dot_frame,
                text="●" if filled else "○",
                font=FONTS["body_bold"],
                fg=COLOURS["accent_green"] if filled else COLOURS["text_muted"],
                bg=COLOURS["bg_main"],
            ).pack(side="left", padx=2)

    # -----------------------------------------------------------------------
    # Navigation
    # -----------------------------------------------------------------------

    def _on_next_question(self) -> None:
        """Load the next problem."""
        from core.problem_engine import get_problem
        difficulty = self.tracker.get_current_difficulty(self.subject, self.topic)
        self._current_problem = get_problem(self.subject, self.topic, difficulty)
        self._render_problem()

    def _on_practice_passed(self) -> None:
        """Show congratulations and navigate to evaluate."""
        self._status_label.config(
            text="🎉  Practice complete! Evaluate phase unlocked!",
            fg=COLOURS["accent_green"],
        )
        self._next_q_btn.config(
            text="Go to Evaluate →",
            command=lambda: self.app.go_problem(self.subject, self.topic),
            state="normal",
        )
        # Restyle next button as gold
        self._next_q_btn.config(
            bg=COLOURS["accent_gold"],
            fg=COLOURS["text_dark"],
        )