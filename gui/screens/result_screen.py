# =============================================================================
# gui/screens/result_screen.py
# Result screen — shown after completing an Evaluate session.
#
# Shows:
#   - Score (X / 10) and percentage
#   - Pass / Fail status (mastered or not)
#   - Per-question answer review (correct / incorrect)
#   - Buttons: Replay, Back to Practice, Back to Topics
# =============================================================================

import tkinter as tk
from tkinter import ttk
import logging

import config
from gui.styles import COLOURS, FONTS, PAD, make_button

logger = logging.getLogger(__name__)


class ResultScreen(tk.Frame):

    def __init__(self, parent: tk.Widget, app,
                 result_data: dict = None, **kwargs):
        super().__init__(parent, bg=COLOURS["bg_main"])
        self.app         = app
        self.result_data = result_data or {}
        self._build()

    # -----------------------------------------------------------------------
    # Layout
    # -----------------------------------------------------------------------

    def _build(self) -> None:
        self._build_header()

        # Scrollable body
        canvas = tk.Canvas(self, bg=COLOURS["bg_main"], highlightthickness=0)
        sb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=COLOURS["bg_main"])
        win   = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _resize(e):
            canvas.itemconfig(win, width=e.width)
        canvas.bind("<Configure>", _resize)

        def _scroll_update(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner.bind("<Configure>", _scroll_update)

        def _mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _mousewheel)

        body = tk.Frame(inner, bg=COLOURS["bg_main"])
        body.pack(fill="both", expand=True, padx=PAD["xl"], pady=PAD["lg"])

        self._build_score_panel(body)
        self._build_action_buttons(body)
        self._build_answer_review(body)

    # -----------------------------------------------------------------------
    # Header
    # -----------------------------------------------------------------------

    def _build_header(self) -> None:
        header = tk.Frame(self, bg=COLOURS["bg_header"], height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        topic_label = config.TOPIC_LABELS.get(
            self.result_data.get("topic", ""),
            self.result_data.get("topic", ""),
        )
        tk.Label(
            header,
            text=f"📊  Results — {topic_label}",
            font=FONTS["subheading"],
            fg=COLOURS["accent_gold"],
            bg=COLOURS["bg_header"],
        ).pack(side="left", padx=PAD["lg"])

        elapsed = self.result_data.get("elapsed_seconds", 0)
        mins    = elapsed // 60
        secs    = elapsed % 60
        tk.Label(
            header,
            text=f"Time: {mins}:{secs:02d}  ",
            font=FONTS["small"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_header"],
        ).pack(side="right")

    # -----------------------------------------------------------------------
    # Score panel
    # -----------------------------------------------------------------------

    def _build_score_panel(self, parent: tk.Widget) -> None:
        summary        = self.result_data.get("summary", {})
        tracker_result = self.result_data.get("tracker_result", {})

        score_pct   = summary.get("score_percent", 0)
        correct     = summary.get("total_correct", 0)
        total       = config.PROBLEMS_PER_ROUND
        passed      = summary.get("passed", False)
        mastered    = tracker_result.get("mastered", False)
        geo_unlock  = tracker_result.get("geometry_unlocked", False)
        best_score  = tracker_result.get("best_score", score_pct)
        streak      = summary.get("best_streak", 0)

        # Main result card
        border_colour = COLOURS["accent_gold"] if mastered else (
            COLOURS["accent_green"] if passed else COLOURS["accent_red"]
        )
        card = tk.Frame(
            parent, bg=COLOURS["bg_card"],
            highlightthickness=2,
            highlightbackground=border_colour,
        )
        card.pack(fill="x", pady=(0, PAD["lg"]))

        # Result banner
        if mastered:
            banner_bg   = COLOURS["accent_gold"]
            banner_text = "🌟  MASTERED!"
            banner_fg   = COLOURS["text_dark"]
        elif passed:
            banner_bg   = COLOURS["accent_green"]
            banner_text = "✓  PASSED"
            banner_fg   = COLOURS["text_dark"]
        else:
            banner_bg   = COLOURS["accent_red"]
            banner_text = "✗  NOT YET — Keep Practising"
            banner_fg   = COLOURS["text_white"]

        banner = tk.Frame(card, bg=banner_bg)
        banner.pack(fill="x")
        tk.Label(
            banner,
            text=banner_text,
            font=FONTS["heading"],
            fg=banner_fg,
            bg=banner_bg,
            pady=PAD["sm"],
        ).pack()

        # Score breakdown row
        stats_row = tk.Frame(card, bg=COLOURS["bg_card"])
        stats_row.pack(fill="x", padx=PAD["lg"], pady=PAD["lg"])

        stats = [
            (f"{score_pct}%",     "Score",              COLOURS["accent_blue"]),
            (f"{correct}/{total}", "Correct Answers",   COLOURS["accent_green"]),
            (f"{best_score}%",    "Personal Best",      COLOURS["accent_gold"]),
            (f"{streak}",         "Best Streak",        COLOURS["accent_orange"]),
        ]

        for value, label, colour in stats:
            tile = tk.Frame(stats_row, bg=COLOURS["bg_main"])
            tile.pack(side="left", expand=True)

            tk.Label(
                tile,
                text=value,
                font=FONTS["title"],
                fg=colour,
                bg=COLOURS["bg_main"],
            ).pack()

            tk.Label(
                tile,
                text=label,
                font=FONTS["tiny"],
                fg=COLOURS["text_secondary"],
                bg=COLOURS["bg_main"],
            ).pack()

        # Progress bar
        bar_frame = tk.Frame(card, bg=COLOURS["bg_card"])
        bar_frame.pack(fill="x", padx=PAD["lg"], pady=(0, PAD["md"]))

        bar_style = "Gold.Horizontal.TProgressbar" if mastered \
                    else "Green.Horizontal.TProgressbar"
        pv = tk.DoubleVar(value=score_pct)
        ttk.Progressbar(
            bar_frame,
            variable=pv,
            maximum=100,
            style=bar_style,
        ).pack(fill="x")

        tk.Label(
            bar_frame,
            text=f"Need {config.MASTERY_SCORE_PERCENT}% to master this topic",
            font=FONTS["tiny"],
            fg=COLOURS["text_muted"],
            bg=COLOURS["bg_card"],
        ).pack(anchor="e")

        # Feedback message
        if mastered:
            msg = (
                "Outstanding! You've mastered this topic. "
                "The difficulty level has increased for your next attempt."
            )
            msg_colour = COLOURS["accent_gold"]
        elif passed:
            msg = (
                f"Well done — you scored {score_pct}%! "
                "Review any mistakes below before your next attempt."
            )
            msg_colour = COLOURS["accent_green"]
        else:
            msg = (
                f"You scored {score_pct}% — you need {config.MASTERY_SCORE_PERCENT}% "
                "to master this topic. Review the mistakes below, "
                "then go back to Practice before trying again."
            )
            msg_colour = COLOURS["text_secondary"]

        tk.Label(
            card,
            text=msg,
            font=FONTS["body"],
            fg=msg_colour,
            bg=COLOURS["bg_card"],
            wraplength=580,
            justify="center",
            pady=PAD["sm"],
        ).pack(padx=PAD["lg"], pady=(0, PAD["md"]))

        # Geometry unlock announcement
        if geo_unlock:
            unlock_frame = tk.Frame(
                parent, bg=COLOURS["accent_green"],
                highlightthickness=0,
            )
            unlock_frame.pack(fill="x", pady=(0, PAD["md"]))
            tk.Label(
                unlock_frame,
                text="🔓  Geometry module unlocked! All Algebra topics mastered!",
                font=FONTS["subheading"],
                fg=COLOURS["text_dark"],
                bg=COLOURS["accent_green"],
                pady=PAD["sm"],
            ).pack()

    # -----------------------------------------------------------------------
    # Action buttons
    # -----------------------------------------------------------------------

    def _build_action_buttons(self, parent: tk.Widget) -> None:
        summary        = self.result_data.get("summary", {})
        tracker_result = self.result_data.get("tracker_result", {})
        subject        = self.result_data.get("subject", config.SUBJECT_ALGEBRA)
        topic          = self.result_data.get("topic", "")
        passed         = summary.get("passed", False)

        btn_row = tk.Frame(parent, bg=COLOURS["bg_main"])
        btn_row.pack(fill="x", pady=(0, PAD["lg"]))

        # Always show: back to topics
        make_button(
            btn_row, "← Back to Topics",
            lambda: self.app.go_topic(subject),
            variant="ghost", pady=8, padx=16,
        ).pack(side="left")

        if passed:
            # Replay at current (possibly higher) difficulty
            make_button(
                btn_row, "Try Again ↺",
                lambda: self.app.go_problem(subject, topic),
                variant="primary", pady=8, padx=16,
            ).pack(side="right", padx=(PAD["sm"], 0))
        else:
            # Failed — nudge back to practice
            make_button(
                btn_row, "Back to Practice →",
                lambda: self.app.go_practice(subject, topic),
                variant="warning", pady=8, padx=16,
            ).pack(side="right", padx=(PAD["sm"], 0))

            make_button(
                btn_row, "Try Evaluate Again ↺",
                lambda: self.app.go_problem(subject, topic),
                variant="ghost", pady=8, padx=16,
            ).pack(side="right", padx=(PAD["sm"], 0))

        # Home button
        make_button(
            btn_row, "🏠 Home",
            self.app.go_home,
            variant="ghost", pady=8, padx=16,
        ).pack(side="right", padx=(PAD["sm"], 0))

    # -----------------------------------------------------------------------
    # Answer review
    # -----------------------------------------------------------------------

    def _build_answer_review(self, parent: tk.Widget) -> None:
        summary     = self.result_data.get("summary", {})
        answer_log  = summary.get("answer_log", [])

        if not answer_log:
            return

        tk.Frame(parent, bg=COLOURS["border"], height=1).pack(
            fill="x", pady=(0, PAD["md"])
        )

        tk.Label(
            parent,
            text="Question Review",
            font=FONTS["subheading"],
            fg=COLOURS["text_primary"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["sm"]))

        tk.Label(
            parent,
            text="Review each question to understand what went well and what to improve.",
            font=FONTS["small"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["md"]))

        for entry in answer_log:
            correct = entry.get("correct", False)
            bg      = COLOURS["bg_correct"]   if correct else COLOURS["bg_incorrect"]
            hlt     = COLOURS["accent_green"] if correct else COLOURS["accent_red"]
            icon    = "✓" if correct else "✗"

            row = tk.Frame(
                parent, bg=bg,
                highlightthickness=1,
                highlightbackground=hlt,
            )
            row.pack(fill="x", pady=(0, PAD["sm"]))

            # Question line
            q_row = tk.Frame(row, bg=bg)
            q_row.pack(fill="x", padx=PAD["md"], pady=(PAD["sm"], 0))

            tk.Label(
                q_row,
                text=f"{icon}  Q{entry.get('q_number', '?')}:",
                font=FONTS["small_bold"],
                fg=hlt,
                bg=bg,
            ).pack(side="left")

            tk.Label(
                q_row,
                text=entry.get("question", ""),
                font=FONTS["mono_small"],
                fg=COLOURS["text_primary"],
                bg=bg,
                wraplength=500,
                justify="left",
            ).pack(side="left", padx=(PAD["sm"], 0))

            # Answer line
            ans_row = tk.Frame(row, bg=bg)
            ans_row.pack(fill="x", padx=PAD["md"], pady=(2, PAD["sm"]))

            student_ans  = entry.get("student_input", "—")
            expected_ans = entry.get("expected_answer", "—")

            if correct:
                ans_text = f"Your answer: {student_ans}  ✓"
                ans_fg   = COLOURS["accent_green"]
            else:
                ans_text = (
                    f"Your answer: {student_ans}   |   "
                    f"Correct answer: {expected_ans}"
                )
                ans_fg = COLOURS["accent_red"]

            tk.Label(
                ans_row,
                text=ans_text,
                font=FONTS["small"],
                fg=ans_fg,
                bg=bg,
            ).pack(side="left")

            # Hint used / show solution flag
            flags = []
            if entry.get("used_hint"):
                flags.append("hint used")
            if entry.get("used_show_solution"):
                flags.append("solution shown")
            if flags:
                tk.Label(
                    ans_row,
                    text=f"  [{', '.join(flags)}]",
                    font=FONTS["tiny"],
                    fg=COLOURS["text_muted"],
                    bg=bg,
                ).pack(side="left")