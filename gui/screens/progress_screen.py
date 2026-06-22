# =============================================================================
# gui/screens/progress_screen.py
# Overall progress dashboard.
#
# Shows:
#   - Overall completion percentage and progress bar
#   - Per-subject breakdown (Algebra / Geometry)
#   - Per-topic phase status for every topic
#   - Mastery badges for completed topics
# =============================================================================

import tkinter as tk
from tkinter import ttk
import logging

import config
from gui.styles import COLOURS, FONTS, PAD, make_button, phase_colour, phase_dot

logger = logging.getLogger(__name__)


class ProgressScreen(tk.Frame):

    def __init__(self, parent: tk.Widget, app, **kwargs):
        super().__init__(parent, bg=COLOURS["bg_main"])
        self.app     = app
        self.tracker = app.tracker
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

        def _scroll(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner.bind("<Configure>", _scroll)

        def _wheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _wheel)

        body = tk.Frame(inner, bg=COLOURS["bg_main"])
        body.pack(fill="both", expand=True, padx=PAD["xl"], pady=PAD["lg"])

        overall = self.tracker.get_overall_progress()
        self._build_overall_panel(body, overall)
        self._build_subject_section(body, config.SUBJECT_ALGEBRA, overall)
        self._build_subject_section(body, config.SUBJECT_GEOMETRY, overall)

    # -----------------------------------------------------------------------
    # Header
    # -----------------------------------------------------------------------

    def _build_header(self) -> None:
        header = tk.Frame(self, bg=COLOURS["bg_header"], height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        make_button(
            header, "← Home", self.app.go_home,
            variant="primary", pady=4, padx=12, size="small_bold",
        ).pack(side="left", padx=PAD["md"])

        tk.Label(
            header,
            text="My Progress",
            font=FONTS["subheading"],
            fg=COLOURS["accent_gold"],
            bg=COLOURS["bg_header"],
        ).pack(side="left", padx=PAD["sm"])

        name = self.tracker.get_student_name()
        tk.Label(
            header,
            text=f"{name}  ",
            font=FONTS["small"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_header"],
        ).pack(side="right")

    # -----------------------------------------------------------------------
    # Overall panel
    # -----------------------------------------------------------------------

    def _build_overall_panel(self, parent: tk.Widget, overall: dict) -> None:
        card = tk.Frame(
            parent, bg=COLOURS["bg_card"],
            highlightthickness=1,
            highlightbackground=COLOURS["accent_gold"],
        )
        card.pack(fill="x", pady=(0, PAD["lg"]))

        # Title
        tk.Label(
            card,
            text="Overall Completion",
            font=FONTS["heading"],
            fg=COLOURS["accent_gold"],
            bg=COLOURS["bg_card"],
        ).pack(anchor="w", padx=PAD["lg"], pady=(PAD["md"], PAD["sm"]))

        # Big percentage
        pct = overall["percent_overall"]
        tk.Label(
            card,
            text=f"{pct}%",
            font=("Helvetica", 48, "bold"),
            fg=COLOURS["accent_gold"],
            bg=COLOURS["bg_card"],
        ).pack(padx=PAD["lg"])

        # Progress bar
        bar_frame = tk.Frame(card, bg=COLOURS["bg_card"])
        bar_frame.pack(fill="x", padx=PAD["lg"], pady=(0, PAD["sm"]))

        pv = tk.DoubleVar(value=pct)
        ttk.Progressbar(
            bar_frame,
            variable=pv,
            maximum=100,
            style="Gold.Horizontal.TProgressbar",
        ).pack(fill="x")

        # Stats row
        stats_row = tk.Frame(card, bg=COLOURS["bg_card"])
        stats_row.pack(fill="x", padx=PAD["lg"], pady=(PAD["sm"], PAD["md"]))

        total_mastered = overall["algebra_mastered"] + overall["geometry_mastered"]
        total_topics   = overall["algebra_total"]    + overall["geometry_total"]

        stats = [
            ("Topics Mastered",    f"{total_mastered} / {total_topics}", COLOURS["accent_green"]),
            ("Algebra Mastered",   f"{overall['algebra_mastered']} / {overall['algebra_total']}", COLOURS["accent_blue"]),
            ("Geometry Mastered",  f"{overall['geometry_mastered']} / {overall['geometry_total']}", COLOURS["accent_orange"]),
        ]

        for label, value, colour in stats:
            tile = tk.Frame(
                stats_row, bg=COLOURS["bg_main"],
                highlightthickness=1,
                highlightbackground=COLOURS["border"],
            )
            tile.pack(side="left", expand=True, fill="x",
                      padx=(0, PAD["sm"]), ipadx=PAD["md"], ipady=PAD["sm"])

            tk.Label(
                tile, text=value,
                font=FONTS["heading"],
                fg=colour,
                bg=COLOURS["bg_main"],
            ).pack()

            tk.Label(
                tile, text=label,
                font=FONTS["tiny"],
                fg=COLOURS["text_secondary"],
                bg=COLOURS["bg_main"],
            ).pack()

    # -----------------------------------------------------------------------
    # Subject section
    # -----------------------------------------------------------------------

    def _build_subject_section(
        self, parent: tk.Widget, subject: str, overall: dict
    ) -> None:
        is_locked = self.tracker.is_subject_locked(subject)
        topics    = (config.ALGEBRA_TOPICS if subject == config.SUBJECT_ALGEBRA
                     else config.GEOMETRY_TOPICS)

        icon  = "📐" if subject == config.SUBJECT_ALGEBRA else "📏"
        title = f"{icon}  {subject.title()}"
        if is_locked:
            title += "  🔒"

        # Section heading
        tk.Label(
            parent,
            text=title,
            font=FONTS["heading"],
            fg=COLOURS["text_muted"] if is_locked else COLOURS["text_primary"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["sm"]))

        if is_locked:
            tk.Label(
                parent,
                text="Complete all Algebra topics to unlock Geometry.",
                font=FONTS["small"],
                fg=COLOURS["text_muted"],
                bg=COLOURS["bg_main"],
            ).pack(anchor="w", pady=(0, PAD["md"]))
            return

        # Mastered count
        mastered_key = f"{subject}_mastered"
        total_key    = f"{subject}_total"
        mastered_count = overall.get(mastered_key, 0)
        total_count    = overall.get(total_key, len(topics))

        tk.Label(
            parent,
            text=f"{mastered_count} of {total_count} topics mastered",
            font=FONTS["small"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["md"]))

        # Topic rows
        for topic in topics:
            summary = self.tracker.get_topic_summary(subject, topic)
            self._build_topic_row(parent, subject, topic, summary)

        tk.Frame(parent, bg=COLOURS["border"], height=1).pack(
            fill="x", pady=PAD["md"]
        )

    # -----------------------------------------------------------------------
    # Topic row
    # -----------------------------------------------------------------------

    def _build_topic_row(
        self, parent: tk.Widget, subject: str, topic: str, summary: dict
    ) -> None:
        is_mastered = summary.get("mastered", False)
        best_score  = summary.get("best_score", 0)

        border = COLOURS["accent_gold"] if is_mastered else COLOURS["border"]
        row = tk.Frame(
            parent, bg=COLOURS["bg_card"],
            highlightthickness=1,
            highlightbackground=border,
        )
        row.pack(fill="x", pady=(0, PAD["sm"]))

        inner = tk.Frame(row, bg=COLOURS["bg_card"])
        inner.pack(fill="x", padx=PAD["md"], pady=PAD["sm"])

        # Left — topic name + status
        left = tk.Frame(inner, bg=COLOURS["bg_card"])
        left.pack(side="left", fill="x", expand=True)

        name_colour = (COLOURS["accent_gold"] if is_mastered
                       else COLOURS["text_primary"])
        name_row = tk.Frame(left, bg=COLOURS["bg_card"])
        name_row.pack(anchor="w")

        tk.Label(
            name_row,
            text=summary["label"],
            font=FONTS["body_bold"],
            fg=name_colour,
            bg=COLOURS["bg_card"],
        ).pack(side="left")

        if is_mastered:
            tk.Label(
                name_row,
                text="  MASTERED",
                font=FONTS["small_bold"],
                fg=COLOURS["accent_gold"],
                bg=COLOURS["bg_card"],
            ).pack(side="left")

        if best_score > 0:
            tk.Label(
                left,
                text=f"Best score: {best_score}%",
                font=FONTS["small"],
                fg=COLOURS["text_muted"],
                bg=COLOURS["bg_card"],
            ).pack(anchor="w")

        # Middle — phase dots
        phases_frame = tk.Frame(inner, bg=COLOURS["bg_card"])
        phases_frame.pack(side="left", padx=PAD["lg"])

        for phase in config.PHASES_IN_ORDER:
            status = summary.get(phase, config.STATUS_LOCKED)
            col    = phase_colour(status)
            dot    = phase_dot(status)
            label  = phase.upper()

            col_frame = tk.Frame(phases_frame, bg=COLOURS["bg_card"])
            col_frame.pack(side="left", padx=PAD["sm"])

            tk.Label(
                col_frame, text=dot,
                font=FONTS["body_bold"],
                fg=col, bg=COLOURS["bg_card"],
            ).pack()

            tk.Label(
                col_frame, text=label,
                font=FONTS["tiny"],
                fg=col, bg=COLOURS["bg_card"],
            ).pack()

        # Right — Go button
        right = tk.Frame(inner, bg=COLOURS["bg_card"])
        right.pack(side="right")

        if not summary.get("locked"):
            learn_done    = summary.get("learn") == config.STATUS_COMPLETE
            practice_done = summary.get("practice") == config.STATUS_COMPLETE

            if not learn_done:
                cmd = lambda s=subject, t=topic: self.app.go_learn(s, t)
                btn_text = "Learn"
            elif not practice_done:
                cmd = lambda s=subject, t=topic: self.app.go_practice(s, t)
                btn_text = "Practice"
            else:
                cmd = lambda s=subject, t=topic: self.app.go_problem(s, t)
                btn_text = "Evaluate" if not is_mastered else "Replay"

            make_button(
                right, f"{btn_text} →", cmd,
                variant="primary", pady=4, padx=10, size="small_bold",
            ).pack()