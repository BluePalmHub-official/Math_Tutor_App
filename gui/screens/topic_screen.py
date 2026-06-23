# =============================================================================
# gui/screens/topic_screen.py
# Topic list screen — shows all topics within a subject (Algebra or Geometry)
# with phase status indicators for each.
#
# Layout:
#   ┌─────────────────────────────────────────────┐
#   │  HEADER  — back button + subject title       │
#   ├─────────────────────────────────────────────┤
#   │  Intro text                                  │
#   │                                              │
#   │  ┌─ Topic Card ──────────────────────────┐  │
#   │  │  Topic Name          [●LEARN][●PRAC][○EVAL]│
#   │  │  Status label                    [→ btn]  │
#   │  └──────────────────────────────────────────┘│
#   │  ... (one card per topic)                    │
#   └─────────────────────────────────────────────┘
#
# Transitions to: learn_screen, practice_screen, problem_screen (per phase)
# =============================================================================

import tkinter as tk
import logging

import config
from gui.styles import (
    COLOURS, FONTS, PAD, make_button,
    phase_colour, phase_dot,
)

logger = logging.getLogger(__name__)

# Phase display labels and order
_PHASE_LABELS = {
    config.PHASE_LEARN:    "LEARN",
    config.PHASE_PRACTICE: "PRACTICE",
    config.PHASE_EVALUATE: "EVALUATE",
}


class TopicScreen(tk.Frame):

    def __init__(self, parent: tk.Widget, app, subject: str = "algebra", **kwargs):
        super().__init__(parent, bg=COLOURS["bg_main"])
        self.app     = app
        self.tracker = app.tracker
        self.subject = subject
        self._build()

    # -----------------------------------------------------------------------
    # Layout
    # -----------------------------------------------------------------------

    def _build(self) -> None:
        self._build_header()
        self._build_body()

    def _build_header(self) -> None:
        header = tk.Frame(self, bg=COLOURS["bg_header"], height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        make_button(
            header, "← Home", self.app.go_home,
            variant="ghost", pady=4, padx=12, size="small_bold",
        ).pack(side="left", padx=PAD["md"])

        subject_label = config.TOPIC_LABELS.get(
            self.subject,
            self.subject.title()
        )
        _ICONS = {
            config.SUBJECT_ALGEBRA:  "📐",
            config.SUBJECT_GEOMETRY: "📏",
            config.SUBJECT_ADVANCED: "🎓",
        }
        icon = _ICONS.get(self.subject, "📚")

        tk.Label(
            header,
            text=f"{icon}  {self.subject.title()} — Topics",
            font=FONTS["subheading"],
            fg=COLOURS["accent_gold"],
            bg=COLOURS["bg_header"],
        ).pack(side="left", padx=PAD["sm"])

        # Student name top-right
        tk.Label(
            header,
            text=f"{self.tracker.get_student_name()}  ",
            font=FONTS["small"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_header"],
        ).pack(side="right")

    def _build_body(self) -> None:
        # Scrollable area for topic cards
        canvas = tk.Canvas(self, bg=COLOURS["bg_main"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Inner frame inside the canvas
        inner = tk.Frame(canvas, bg=COLOURS["bg_main"])
        canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")

        # Make inner frame stretch to canvas width
        def on_canvas_resize(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", on_canvas_resize)

        # Update scroll region when inner frame changes size
        def on_inner_resize(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner.bind("<Configure>", on_inner_resize)

        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Content inside inner frame
        content = tk.Frame(inner, bg=COLOURS["bg_main"])
        content.pack(fill="both", expand=True, padx=PAD["xl"], pady=PAD["lg"])

        # Intro
        subject_name = self.subject.title()
        tk.Label(
            content,
            text=f"{subject_name} Topics",
            font=FONTS["heading"],
            fg=COLOURS["text_primary"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, 4))

        tk.Label(
            content,
            text=(
                "Complete each topic in order: Learn → Practice → Evaluate.\n"
                "You must finish all three phases to master a topic."
            ),
            font=FONTS["small"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_main"],
            justify="left",
        ).pack(anchor="w", pady=(0, PAD["lg"]))

        # Phase legend
        self._build_legend(content)

        # Divider
        tk.Frame(content, bg=COLOURS["border"], height=1).pack(
            fill="x", pady=(0, PAD["md"])
        )

        # Topic cards
        _TOPICS = {
            config.SUBJECT_ALGEBRA:  config.ALGEBRA_TOPICS,
            config.SUBJECT_GEOMETRY: config.GEOMETRY_TOPICS,
            config.SUBJECT_ADVANCED: config.ADVANCED_TOPICS,
        }
        topics = _TOPICS.get(self.subject, config.ALGEBRA_TOPICS)

        for i, topic in enumerate(topics):
            summary = self.tracker.get_topic_summary(self.subject, topic)
            self._build_topic_card(content, topic, summary, i)

    def _build_legend(self, parent: tk.Widget) -> None:
        """Phase legend row shown above the topic list."""
        row = tk.Frame(parent, bg=COLOURS["bg_main"])
        row.pack(anchor="w", pady=(0, PAD["sm"]))

        tk.Label(
            row, text="Phase status:  ",
            font=FONTS["small"],
            fg=COLOURS["text_muted"],
            bg=COLOURS["bg_main"],
        ).pack(side="left")

        legend_items = [
            ("● Complete",     COLOURS["accent_green"]),
            ("◑ In Progress",  COLOURS["accent_orange"]),
            ("○ Not Started",  COLOURS["text_muted"]),
            ("○ Locked",       COLOURS["phase_locked"]),
        ]
        for text, colour in legend_items:
            tk.Label(
                row, text=f"  {text}",
                font=FONTS["small"],
                fg=colour,
                bg=COLOURS["bg_main"],
            ).pack(side="left")

    # -----------------------------------------------------------------------
    # Topic card
    # -----------------------------------------------------------------------

    def _build_topic_card(
        self, parent: tk.Widget, topic: str, summary: dict, index: int
    ) -> None:
        """Build one topic row card with phase indicators and action button."""

        is_locked   = summary.get("locked", False)
        is_mastered = summary.get("mastered", False)

        card = tk.Frame(
            parent,
            bg=COLOURS["bg_card"],
            highlightthickness=1,
            highlightbackground=(
                COLOURS["accent_gold"] if is_mastered
                else COLOURS["border"]
            ),
        )
        card.pack(fill="x", pady=(0, PAD["sm"]))

        # Inner padding frame
        inner = tk.Frame(card, bg=COLOURS["bg_card"])
        inner.pack(fill="x", padx=PAD["md"], pady=PAD["sm"])

        # ── Left side: index + topic name + status ──────────────────────────
        left = tk.Frame(inner, bg=COLOURS["bg_card"])
        left.pack(side="left", fill="x", expand=True)

        # Topic number + name row
        name_row = tk.Frame(left, bg=COLOURS["bg_card"])
        name_row.pack(anchor="w")

        # Index number badge
        tk.Label(
            name_row,
            text=f" {index + 1} ",
            font=FONTS["small_bold"],
            fg=COLOURS["bg_main"],
            bg=COLOURS["text_muted"] if is_locked else COLOURS["accent_blue"],
        ).pack(side="left", padx=(0, PAD["sm"]))

        # Topic name
        topic_colour = COLOURS["text_muted"] if is_locked else COLOURS["text_primary"]
        if is_mastered:
            topic_colour = COLOURS["accent_gold"]

        tk.Label(
            name_row,
            text=summary["label"],
            font=FONTS["body_bold"],
            fg=topic_colour,
            bg=COLOURS["bg_card"],
        ).pack(side="left")

        if is_mastered:
            tk.Label(
                name_row,
                text="  ★ MASTERED",
                font=FONTS["small_bold"],
                fg=COLOURS["accent_gold"],
                bg=COLOURS["bg_card"],
            ).pack(side="left")

        # Status line
        status_text = self._status_text(summary)
        tk.Label(
            left,
            text=status_text,
            font=FONTS["small"],
            fg=COLOURS["text_muted"],
            bg=COLOURS["bg_card"],
        ).pack(anchor="w", pady=(2, 0))

        # ── Middle: phase indicator dots ────────────────────────────────────
        phases_frame = tk.Frame(inner, bg=COLOURS["bg_card"])
        phases_frame.pack(side="left", padx=PAD["lg"])

        for phase in config.PHASES_IN_ORDER:
            status = summary.get(phase, config.STATUS_LOCKED)
            col    = phase_colour(status)
            dot    = phase_dot(status)
            label  = _PHASE_LABELS[phase]

            phase_col = tk.Frame(phases_frame, bg=COLOURS["bg_card"])
            phase_col.pack(side="left", padx=PAD["sm"])

            tk.Label(
                phase_col,
                text=dot,
                font=FONTS["body_bold"],
                fg=col,
                bg=COLOURS["bg_card"],
            ).pack()

            tk.Label(
                phase_col,
                text=label,
                font=FONTS["tiny"],
                fg=col,
                bg=COLOURS["bg_card"],
            ).pack()

        # ── Right side: action button ───────────────────────────────────────
        right = tk.Frame(inner, bg=COLOURS["bg_card"])
        right.pack(side="right")

        btn_text, btn_cmd, btn_variant = self._button_config(topic, summary)
        make_button(
            right, btn_text, btn_cmd,
            variant=btn_variant, size="small_bold",
            pady=6, padx=14,
        ).pack()

        # Best score (if any evaluate attempts)
        best = summary.get("best_score", 0)
        if best > 0:
            tk.Label(
                right,
                text=f"Best: {best}%",
                font=FONTS["tiny"],
                fg=COLOURS["text_muted"],
                bg=COLOURS["bg_card"],
            ).pack(pady=(2, 0))

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _status_text(self, summary: dict) -> str:
        """Return a one-line status description for a topic."""
        if summary.get("locked"):
            return "🔒 Locked — complete prerequisite topics first"
        if summary.get("mastered"):
            diff = summary.get("difficulty", "easy").title()
            return f"Mastered ✓  |  Now playing: {diff} difficulty"
        learn    = summary.get("learn",    config.STATUS_NOT_STARTED)
        practice = summary.get("practice", config.STATUS_LOCKED)
        evaluate = summary.get("evaluate", config.STATUS_LOCKED)

        if learn == config.STATUS_NOT_STARTED:
            return "Start here — begin with the Learn phase"
        if learn == config.STATUS_IN_PROGRESS:
            return "In progress — finish reading all concept cards"
        if learn == config.STATUS_COMPLETE and practice in (
            config.STATUS_LOCKED, config.STATUS_NOT_STARTED
        ):
            return "Learn complete ✓ — ready for Practice"
        if practice == config.STATUS_IN_PROGRESS:
            streak = summary.get("best_streak", 0)
            return f"Practising — streak: {streak} / {config.PRACTICE_PASS_STREAK} needed"
        if practice == config.STATUS_COMPLETE and evaluate in (
            config.STATUS_LOCKED, config.STATUS_NOT_STARTED
        ):
            return "Practice complete ✓ — ready to Evaluate"
        if evaluate == config.STATUS_IN_PROGRESS:
            best = summary.get("best_score", 0)
            return f"Evaluating — best score so far: {best}%  (need {config.MASTERY_SCORE_PERCENT}%)"
        return "In progress"

    def _button_config(self, topic: str, summary: dict) -> tuple:
        """
        Return (button_text, command, variant) for the topic's action button.
        Directs to the correct phase based on current progress.
        """
        if summary.get("locked"):
            return ("🔒 Locked", lambda: None, "ghost")

        learn    = summary.get("learn",    config.STATUS_NOT_STARTED)
        practice = summary.get("practice", config.STATUS_LOCKED)
        evaluate = summary.get("evaluate", config.STATUS_LOCKED)

        # Determine which phase to open
        if learn != config.STATUS_COMPLETE:
            return (
                "Start Learning →",
                lambda t=topic: self.app.go_learn(self.subject, t),
                "primary",
            )

        if practice not in (config.STATUS_COMPLETE, config.STATUS_MASTERED):
            return (
                "Go to Practice →",
                lambda t=topic: self.app.go_practice(self.subject, t),
                "warning",
            )

        if not summary.get("mastered"):
            return (
                "Go to Evaluate →",
                lambda t=topic: self.app.go_problem(self.subject, t),
                "danger",
            )

        # Mastered — offer replay at higher difficulty
        return (
            "Replay ↺",
            lambda t=topic: self.app.go_problem(self.subject, t),
            "gold",
        )