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
import importlib
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

        # Review Lesson popup state
        self._review_win     = None
        self._review_content = None

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

        # ── Review Lesson trigger ───────────────────────────────────────────
        tk.Label(
            body,
            text="Stuck? Review the lesson without losing your progress.",
            font=FONTS["small"],
            fg=COLOURS["text_muted"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, 2))

        self._review_btn = tk.Button(
            body,
            text="📖 Review Lesson",
            command=self._show_review_panel,
            font=FONTS["small_bold"],
            fg=COLOURS["accent_blue"],
            bg=COLOURS["bg_card"],
            activebackground=COLOURS["bg_highlight"],
            activeforeground=COLOURS["accent_blue"],
            relief="flat", bd=0,
            highlightthickness=1,
            highlightbackground=COLOURS["accent_blue"],
            padx=12, pady=6,
            cursor="hand2",
        )
        self._review_btn.pack(anchor="w", pady=(0, PAD["md"]))

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
                    self._hint3_btn, self._show_sol_btn, self._review_btn):
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
                    self._hint3_btn, self._show_sol_btn, self._review_btn):
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
                    self._hint3_btn, self._show_sol_btn, self._review_btn):
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
        """Load the next problem from the session manager."""
        self._current_problem = self.sm.next_practice_problem()
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

    # -----------------------------------------------------------------------
    # Review Lesson popup
    #
    # A read-only reference popup (tk.Toplevel) — never navigates away from
    # this screen and never touches session_manager / tracker state, so the
    # practice session (streak, current problem, answer entry) is completely
    # unaffected by opening or closing it.
    # -----------------------------------------------------------------------

    def _show_review_panel(self) -> None:
        """Open the lesson review popup for the current subject/topic."""
        if self._review_win is not None and self._review_win.winfo_exists():
            self._review_win.lift()
            self._review_win.focus_force()
            return

        try:
            self._review_content = importlib.import_module(
                f"content.{self.subject}.{self.topic}"
            )
        except ImportError:
            self._review_content = None

        self._review_card_idx    = 0
        self._review_example_idx = 0

        topic_label = config.TOPIC_LABELS.get(self.topic, self.topic)

        win = tk.Toplevel(self)
        win.title(f"Lesson Review — {topic_label}")
        win.configure(bg=COLOURS["bg_card"])
        win.geometry("600x700")
        win.transient(self.winfo_toplevel())
        win.protocol("WM_DELETE_WINDOW", self._close_review_panel)
        self._review_win = win

        # Dim the practice screen underneath to signal the panel is active.
        self.configure(bg="#111820")

        # ── Tab bar ──────────────────────────────────────────────────────────
        tab_bar = tk.Frame(win, bg=COLOURS["bg_header"])
        tab_bar.pack(fill="x")

        self._review_tab_buttons = {}
        for key, label in (
            ("concepts", "Concept Cards"),
            ("examples", "Worked Examples"),
            ("vocab",    "Key Vocabulary"),
        ):
            btn = tk.Button(
                tab_bar,
                text=label,
                command=lambda k=key: self._set_review_tab(k),
                font=FONTS["small_bold"],
                fg=COLOURS["text_primary"],
                bg=COLOURS["bg_header"],
                activebackground=COLOURS["bg_card"],
                activeforeground=COLOURS["accent_blue"],
                relief="flat", bd=0,
                padx=PAD["md"], pady=10,
                cursor="hand2",
            )
            btn.pack(side="left", fill="x", expand=True)
            self._review_tab_buttons[key] = btn

        # ── Content area (rebuilt per tab) ──────────────────────────────────
        self._review_content_frame = tk.Frame(win, bg=COLOURS["bg_card"])
        self._review_content_frame.pack(fill="both", expand=True)

        # ── Close button ─────────────────────────────────────────────────────
        make_button(
            win, "Close Review", self._close_review_panel,
            variant="primary", pady=10, padx=20,
        ).pack(side="bottom", pady=PAD["md"])

        self._set_review_tab("concepts")

        win.focus_force()
        # Delay the click-away binding slightly so the initial focus-in from
        # creating the window doesn't immediately trigger a close.
        win.after(300, lambda: win.bind("<FocusOut>", self._on_review_focus_out))

    def _on_review_focus_out(self, event) -> None:
        """Close the popup when focus moves entirely away from it (click away)."""
        win = self._review_win
        if win is not None and win.winfo_exists() and win.focus_get() is None:
            self._close_review_panel()

    def _close_review_panel(self) -> None:
        """Destroy the popup only — the practice screen is left untouched."""
        win = self._review_win
        if win is not None and win.winfo_exists():
            win.destroy()
        self._review_win = None

        self.configure(bg=COLOURS["bg_main"])
        if not self._answered:
            self._review_btn.config(state="normal")

    def _set_review_tab(self, tab: str) -> None:
        for key, btn in self._review_tab_buttons.items():
            active = key == tab
            btn.config(
                bg=COLOURS["bg_card"] if active else COLOURS["bg_header"],
                fg=COLOURS["accent_blue"] if active else COLOURS["text_primary"],
            )

        for w in self._review_content_frame.winfo_children():
            w.destroy()

        if tab == "concepts":
            self._render_review_concepts()
        elif tab == "examples":
            self._render_review_examples()
        else:
            self._render_review_vocab()

    def _review_scrollable_panel(self, parent: tk.Widget) -> tk.Widget:
        """Build a scrollable canvas+frame inside `parent`, return the inner content frame."""
        canvas = tk.Canvas(parent, bg=COLOURS["bg_card"], highlightthickness=0)
        sb = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=COLOURS["bg_card"])
        win = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _resize(e):
            canvas.itemconfig(win, width=e.width)
        canvas.bind("<Configure>", _resize)

        def _scroll(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner.bind("<Configure>", _scroll)

        def _wheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind("<MouseWheel>", _wheel)

        content = tk.Frame(inner, bg=COLOURS["bg_card"])
        content.pack(fill="both", expand=True, padx=PAD["lg"], pady=PAD["md"])
        return content

    # -- Tab 1: Concept Cards -------------------------------------------------

    def _render_review_concepts(self) -> None:
        cards = getattr(self._review_content, "CONCEPT_CARDS", []) if self._review_content else []
        content = self._review_scrollable_panel(self._review_content_frame)

        if not cards:
            tk.Label(
                content, text="No concept cards available for this topic.",
                font=FONTS["body"], fg=COLOURS["text_muted"], bg=COLOURS["bg_card"],
            ).pack(pady=PAD["lg"])
            return

        self._review_card_idx = max(0, min(self._review_card_idx, len(cards) - 1))
        idx   = self._review_card_idx
        card  = cards[idx]
        total = len(cards)

        tk.Label(
            content, text=f"Card {idx + 1} of {total}",
            font=FONTS["small_bold"], fg=COLOURS["text_muted"], bg=COLOURS["bg_card"],
        ).pack(anchor="w", pady=(0, PAD["sm"]))

        card_frame = tk.Frame(
            content, bg=COLOURS["bg_highlight"],
            highlightthickness=1, highlightbackground=COLOURS["accent_blue"],
        )
        card_frame.pack(fill="x", pady=(0, PAD["md"]))

        tk.Label(
            card_frame, text=card.get("title", ""),
            font=FONTS["subheading"], fg=COLOURS["accent_blue"], bg=COLOURS["bg_highlight"],
            padx=PAD["md"], pady=PAD["sm"],
        ).pack(anchor="w")

        tk.Label(
            card_frame, text=card.get("body", ""),
            font=FONTS["body"], fg=COLOURS["text_primary"], bg=COLOURS["bg_highlight"],
            wraplength=500, justify="left", padx=PAD["md"], pady=PAD["md"],
        ).pack(anchor="w")

        formula = card.get("formula")
        if formula:
            fbox = tk.Frame(
                card_frame, bg=COLOURS["bg_main"],
                highlightthickness=1, highlightbackground=COLOURS["accent_gold"],
            )
            fbox.pack(fill="x", padx=PAD["md"], pady=(0, PAD["sm"]))
            tk.Label(
                fbox, text=formula,
                font=FONTS["mono_large"], fg=COLOURS["accent_gold"], bg=COLOURS["bg_main"],
                padx=PAD["md"], pady=PAD["sm"],
            ).pack()

        example = card.get("example")
        if example:
            tk.Label(
                card_frame, text=example,
                font=FONTS["mono_small"], fg=COLOURS["text_secondary"], bg=COLOURS["bg_highlight"],
                justify="left", padx=PAD["md"], pady=PAD["md"],
            ).pack(anchor="w")

        nav_row = tk.Frame(content, bg=COLOURS["bg_card"])
        nav_row.pack(fill="x", pady=(PAD["sm"], 0))

        prev_btn = make_button(
            nav_row, "← Previous", lambda: self._review_card_nav(-1),
            variant="ghost", pady=6, padx=12, size="small_bold",
        )
        prev_btn.pack(side="left")
        if idx == 0:
            prev_btn.config(state="disabled")

        next_btn = make_button(
            nav_row, "Next →", lambda: self._review_card_nav(1),
            variant="ghost", pady=6, padx=12, size="small_bold",
        )
        next_btn.pack(side="right")
        if idx == total - 1:
            next_btn.config(state="disabled")

    def _review_card_nav(self, delta: int) -> None:
        cards = getattr(self._review_content, "CONCEPT_CARDS", []) if self._review_content else []
        if not cards:
            return
        self._review_card_idx = max(0, min(self._review_card_idx + delta, len(cards) - 1))
        for w in self._review_content_frame.winfo_children():
            w.destroy()
        self._render_review_concepts()

    # -- Tab 2: Worked Examples ------------------------------------------------

    def _render_review_examples(self) -> None:
        examples = getattr(self._review_content, "WORKED_EXAMPLES", []) if self._review_content else []
        content = self._review_scrollable_panel(self._review_content_frame)

        if not examples:
            tk.Label(
                content, text="No worked examples available for this topic.",
                font=FONTS["body"], fg=COLOURS["text_muted"], bg=COLOURS["bg_card"],
            ).pack(pady=PAD["lg"])
            return

        self._review_example_idx = max(0, min(self._review_example_idx, len(examples) - 1))
        idx     = self._review_example_idx
        example = examples[idx]
        total   = len(examples)
        steps   = example.get("steps", [])

        tk.Label(
            content, text=f"Example {idx + 1} of {total}",
            font=FONTS["small_bold"], fg=COLOURS["text_muted"], bg=COLOURS["bg_card"],
        ).pack(anchor="w", pady=(0, PAD["sm"]))

        prob_frame = tk.Frame(
            content, bg=COLOURS["bg_highlight"],
            highlightthickness=2, highlightbackground=COLOURS["accent_orange"],
        )
        prob_frame.pack(fill="x", pady=(0, PAD["md"]))
        tk.Label(
            prob_frame, text="Problem",
            font=FONTS["small_bold"], fg=COLOURS["accent_orange"], bg=COLOURS["bg_highlight"],
            padx=PAD["md"], pady=PAD["sm"],
        ).pack(anchor="w")
        tk.Label(
            prob_frame, text=example.get("problem", ""),
            font=FONTS["mono_large"], fg=COLOURS["text_primary"], bg=COLOURS["bg_highlight"],
            padx=PAD["md"], pady=PAD["md"],
        ).pack(anchor="w")

        # All steps shown at once — this is review, not first-time reveal mode.
        for i, (desc, working) in enumerate(steps):
            step_frame = tk.Frame(
                content, bg=COLOURS["bg_highlight"],
                highlightthickness=1, highlightbackground=COLOURS["border"],
            )
            step_frame.pack(fill="x", pady=(0, PAD["sm"]))

            tk.Label(
                step_frame, text=f"Step {i + 1}  —  {desc}",
                font=FONTS["small_bold"], fg=COLOURS["text_secondary"], bg=COLOURS["bg_highlight"],
                padx=PAD["sm"], pady=4,
            ).pack(anchor="w")
            tk.Label(
                step_frame, text=working,
                font=FONTS["mono_large"], fg=COLOURS["accent_gold"], bg=COLOURS["bg_highlight"],
                padx=PAD["md"], pady=PAD["sm"],
            ).pack(anchor="w")

        check_frame = tk.Frame(
            content, bg=COLOURS["bg_correct"],
            highlightthickness=1, highlightbackground=COLOURS["accent_green"],
        )
        check_frame.pack(fill="x", pady=(0, PAD["md"]))
        tk.Label(
            check_frame, text=example.get("check", ""),
            font=FONTS["mono"], fg=COLOURS["accent_green"], bg=COLOURS["bg_correct"],
            padx=PAD["md"], pady=PAD["sm"],
        ).pack(anchor="w")

        notes = example.get("notes")
        if notes:
            tk.Label(
                content, text=f"💡  {notes}",
                font=FONTS["small"], fg=COLOURS["text_secondary"], bg=COLOURS["bg_card"],
                wraplength=500, justify="left",
            ).pack(anchor="w", pady=(0, PAD["sm"]))

        nav_row = tk.Frame(content, bg=COLOURS["bg_card"])
        nav_row.pack(fill="x", pady=(PAD["sm"], 0))

        prev_btn = make_button(
            nav_row, "← Previous", lambda: self._review_example_nav(-1),
            variant="ghost", pady=6, padx=12, size="small_bold",
        )
        prev_btn.pack(side="left")
        if idx == 0:
            prev_btn.config(state="disabled")

        next_btn = make_button(
            nav_row, "Next →", lambda: self._review_example_nav(1),
            variant="ghost", pady=6, padx=12, size="small_bold",
        )
        next_btn.pack(side="right")
        if idx == total - 1:
            next_btn.config(state="disabled")

    def _review_example_nav(self, delta: int) -> None:
        examples = getattr(self._review_content, "WORKED_EXAMPLES", []) if self._review_content else []
        if not examples:
            return
        self._review_example_idx = max(0, min(self._review_example_idx + delta, len(examples) - 1))
        for w in self._review_content_frame.winfo_children():
            w.destroy()
        self._render_review_examples()

    # -- Tab 3: Key Vocabulary --------------------------------------------------

    def _render_review_vocab(self) -> None:
        vocab = getattr(self._review_content, "KEY_VOCABULARY", {}) if self._review_content else {}
        content = self._review_scrollable_panel(self._review_content_frame)

        if not vocab:
            tk.Label(
                content, text="No vocabulary for this topic.",
                font=FONTS["body"], fg=COLOURS["text_muted"], bg=COLOURS["bg_card"],
            ).pack(pady=PAD["lg"])
            return

        for term, definition in vocab.items():
            row = tk.Frame(
                content, bg=COLOURS["bg_highlight"],
                highlightthickness=1, highlightbackground=COLOURS["border"],
            )
            row.pack(fill="x", pady=(0, PAD["sm"]))

            tk.Label(
                row, text=term,
                font=FONTS["body_bold"], fg=COLOURS["accent_gold"], bg=COLOURS["bg_highlight"],
                padx=PAD["md"], pady=PAD["sm"], anchor="w",
            ).pack(anchor="w")

            tk.Label(
                row, text=definition,
                font=FONTS["body"], fg=COLOURS["text_white"], bg=COLOURS["bg_highlight"],
                padx=PAD["md"], pady=PAD["sm"], wraplength=500, justify="left",
            ).pack(anchor="w")