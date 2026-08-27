# =============================================================================
# gui/screens/cat_result_screen.py
# Result screen for a completed CAT session (pre-test or final exam).
#
# Shows: result banner, score tiles, difficulty journey visual, topic
# breakdown by strength, study/review recommendations, recent CAT
# history for this mode, and mode-appropriate action buttons.
# =============================================================================

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import logging

import config
from gui.styles import COLOURS, FONTS, PAD, make_button
from utils.file_io import read_json, get_progress_path

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Banner presentation — mode + pass_fail -> (bg colour, text)
# ---------------------------------------------------------------------------

_PRETEST_BANNERS = {
    "pass":       ("#17A398", "✅  Strong Foundation Detected"),
    "borderline": (COLOURS["accent_orange"], "⚠️  Adequate Foundation — See Recommendations"),
    "fail":       (COLOURS["accent_blue"], "📋  Diagnostic Complete — Study Plan Below"),
}
_FINAL_BANNERS = {
    "pass":       (COLOURS["accent_gold"], "🌟  PASSED — Competency Confirmed"),
    "fail":       (COLOURS["accent_red"], "✗  Not Yet — Keep Studying"),
    "borderline": (COLOURS["accent_orange"], "⚠️  Borderline — Almost There"),
}

# Difficulty-journey square colours: (correct, difficulty) -> hex
_JOURNEY_COLOURS = {
    (True,  config.DIFFICULTY_EASY):   "#5DADE2",
    (True,  config.DIFFICULTY_MEDIUM): "#F39C12",
    (True,  config.DIFFICULTY_HARD):   "#27AE60",
    (False, config.DIFFICULTY_EASY):   "#2471A3",
    (False, config.DIFFICULTY_MEDIUM): "#D35400",
    (False, config.DIFFICULTY_HARD):   "#922B21",
}

_STRENGTH_BAR_COLOUR = {
    "strong":   COLOURS["accent_green"],
    "adequate": COLOURS["accent_orange"],
    "weak":     COLOURS["accent_red"],
}


class CATResultScreen(tk.Frame):

    def __init__(self, parent: tk.Widget, app, summary: dict = None, **kwargs):
        super().__init__(parent, bg=COLOURS["bg_main"])
        self.app     = app
        self.tracker = app.tracker
        self.summary = summary or {}
        self.mode    = self.summary.get("mode", config.CAT_MODE_PRETEST)
        self._build()

    # -----------------------------------------------------------------------
    # Layout
    # -----------------------------------------------------------------------

    def _build(self) -> None:
        self._build_header()

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

        self._build_banner(body)
        self._build_score_tiles(body)
        self._build_result_message(body)
        self._build_difficulty_journey(body)
        self._build_topic_breakdown(body)
        self._build_recommendations(body)
        self._build_history(body)
        self._build_action_buttons(body)

    def _build_header(self) -> None:
        header = tk.Frame(self, bg=COLOURS["bg_header"], height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = "📋  Pre-Test Results" if self.mode == config.CAT_MODE_PRETEST else "🎓  Final Exam Results"
        tk.Label(
            header, text=title,
            font=FONTS["subheading"],
            fg=COLOURS["accent_gold"],
            bg=COLOURS["bg_header"],
        ).pack(side="left", padx=PAD["lg"])

    # -----------------------------------------------------------------------
    # Section 1 — Result banner
    # -----------------------------------------------------------------------

    def _build_banner(self, parent: tk.Widget) -> None:
        pass_fail = self.summary.get("pass_fail", "fail")
        table = _PRETEST_BANNERS if self.mode == config.CAT_MODE_PRETEST else _FINAL_BANNERS
        bg, text = table.get(pass_fail, (COLOURS["accent_blue"], "Assessment Complete"))

        banner = tk.Frame(parent, bg=bg)
        banner.pack(fill="x", pady=(0, PAD["lg"]))
        tk.Label(
            banner, text=text,
            font=FONTS["heading"],
            fg=COLOURS["text_dark"],
            bg=bg, pady=PAD["md"],
        ).pack()

    # -----------------------------------------------------------------------
    # Section 2 — Score tiles
    # -----------------------------------------------------------------------

    def _build_score_tiles(self, parent: tk.Widget) -> None:
        row = tk.Frame(parent, bg=COLOURS["bg_main"])
        row.pack(fill="x", pady=(0, PAD["lg"]))

        elapsed = self.summary.get("elapsed_seconds", 0)
        mins, secs = divmod(elapsed, 60)

        tiles = [
            (f"{self.summary.get('score_percent', 0)}%", "Score", COLOURS["accent_blue"]),
            (f"{self.summary.get('total_correct', 0)}/{self.summary.get('total_answered', 0)}",
             "Correct / Total", COLOURS["accent_green"]),
            (f"{self.summary.get('hard_streak_peak', 0)}", "Peak Hard Streak", COLOURS["accent_gold"]),
            (f"{mins}:{secs:02d}", "Time", COLOURS["accent_orange"]),
        ]

        for value, label, colour in tiles:
            tile = tk.Frame(
                row, bg=COLOURS["bg_card"],
                highlightthickness=1,
                highlightbackground=COLOURS["border"],
            )
            tile.pack(side="left", expand=True, fill="x", padx=(0, PAD["sm"]),
                      ipadx=PAD["md"], ipady=PAD["sm"])
            tk.Label(tile, text=value, font=FONTS["title"], fg=colour, bg=COLOURS["bg_card"]).pack()
            tk.Label(tile, text=label, font=FONTS["tiny"], fg=COLOURS["text_secondary"],
                     bg=COLOURS["bg_card"]).pack()

    # -----------------------------------------------------------------------
    # Section 3 — Result message
    # -----------------------------------------------------------------------

    def _build_result_message(self, parent: tk.Widget) -> None:
        tk.Label(
            parent,
            text=self.summary.get("result_message", ""),
            font=FONTS["body"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_main"],
            wraplength=640,
            justify="left",
        ).pack(anchor="w", pady=(0, PAD["lg"]))

    # -----------------------------------------------------------------------
    # Section 4 — Difficulty journey
    # -----------------------------------------------------------------------

    def _build_difficulty_journey(self, parent: tk.Widget) -> None:
        tk.Label(
            parent, text="Your Difficulty Journey",
            font=FONTS["subheading"], fg=COLOURS["text_primary"], bg=COLOURS["bg_main"],
        ).pack(anchor="w")
        tk.Label(
            parent, text="Each square = one question",
            font=FONTS["small"], fg=COLOURS["text_muted"], bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["sm"]))

        answer_log = self.summary.get("answer_log", [])
        sq_w, sq_h, gap, per_row = 14, 22, 2, 20
        cols = min(per_row, len(answer_log)) or 1
        rows = (len(answer_log) + per_row - 1) // per_row or 1
        canvas_w = 580
        canvas_h = max(sq_h, rows * (sq_h + gap))

        canvas = tk.Canvas(parent, width=canvas_w, height=canvas_h,
                            bg=COLOURS["bg_main"], highlightthickness=0)
        canvas.pack(anchor="w", pady=(0, PAD["sm"]))

        for i, record in enumerate(answer_log):
            row_i = i // per_row
            col_i = i % per_row
            x0 = col_i * (sq_w + gap)
            y0 = row_i * (sq_h + gap)
            colour = _JOURNEY_COLOURS.get(
                (record.get("correct", False), record.get("difficulty", config.DIFFICULTY_EASY)),
                COLOURS["text_muted"],
            )
            canvas.create_rectangle(x0, y0, x0 + sq_w, y0 + sq_h, fill=colour, outline="")

        # Legend
        legend = tk.Frame(parent, bg=COLOURS["bg_main"])
        legend.pack(anchor="w", pady=(0, PAD["lg"]))
        legend_items = [
            ("Correct · Easy",   _JOURNEY_COLOURS[(True, config.DIFFICULTY_EASY)]),
            ("Correct · Medium", _JOURNEY_COLOURS[(True, config.DIFFICULTY_MEDIUM)]),
            ("Correct · Hard",   _JOURNEY_COLOURS[(True, config.DIFFICULTY_HARD)]),
            ("Wrong · Easy",     _JOURNEY_COLOURS[(False, config.DIFFICULTY_EASY)]),
            ("Wrong · Medium",   _JOURNEY_COLOURS[(False, config.DIFFICULTY_MEDIUM)]),
            ("Wrong · Hard",     _JOURNEY_COLOURS[(False, config.DIFFICULTY_HARD)]),
        ]
        for label, colour in legend_items:
            item = tk.Frame(legend, bg=COLOURS["bg_main"])
            item.pack(side="left", padx=(0, PAD["md"]))
            tk.Frame(item, bg=colour, width=12, height=12).pack(side="left", padx=(0, 4))
            tk.Label(item, text=label, font=FONTS["tiny"], fg=COLOURS["text_secondary"],
                     bg=COLOURS["bg_main"]).pack(side="left")

    # -----------------------------------------------------------------------
    # Section 5 — Topic breakdown
    # -----------------------------------------------------------------------

    def _build_topic_breakdown(self, parent: tk.Widget) -> None:
        tk.Label(
            parent, text="Performance by Topic",
            font=FONTS["subheading"], fg=COLOURS["text_primary"], bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["sm"]))

        breakdown = list(self.summary.get("topic_breakdown", {}).values())
        strong   = sorted([e for e in breakdown if e.get("strength") == "strong"],
                           key=lambda e: -e.get("percent", 0))
        adequate = sorted([e for e in breakdown if e.get("strength") == "adequate"],
                           key=lambda e: -e.get("percent", 0))
        weak     = sorted([e for e in breakdown if e.get("strength") == "weak"],
                           key=lambda e: e.get("percent", 0))

        columns = tk.Frame(parent, bg=COLOURS["bg_main"])
        columns.pack(fill="x", pady=(0, PAD["lg"]))

        self._topic_column(columns, "✅  Strong", strong, COLOURS["accent_green"])
        self._topic_column(columns, "⚠️  Adequate", adequate, COLOURS["accent_orange"])
        self._topic_column(columns, "❌  Weak", weak, COLOURS["accent_red"])

    def _topic_column(self, parent, title, entries, header_colour) -> None:
        col = tk.Frame(parent, bg=COLOURS["bg_main"])
        col.pack(side="left", fill="both", expand=True, padx=(0, PAD["sm"]))

        tk.Label(
            col, text=title, font=FONTS["small_bold"],
            fg=header_colour, bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["sm"]))

        if not entries:
            tk.Label(
                col, text="—", font=FONTS["small"],
                fg=COLOURS["text_muted"], bg=COLOURS["bg_main"],
            ).pack(anchor="w")
            return

        for entry in entries:
            row = tk.Frame(col, bg=COLOURS["bg_card"], highlightthickness=1,
                            highlightbackground=COLOURS["border"])
            row.pack(fill="x", pady=(0, PAD["sm"]))

            tk.Label(
                row,
                text=f"{entry['label']}  {entry['correct']}/{entry['attempted']}  {entry['percent']}%",
                font=FONTS["small_bold"], fg=COLOURS["text_primary"], bg=COLOURS["bg_card"],
                anchor="w",
            ).pack(fill="x", padx=PAD["sm"], pady=(PAD["sm"], 4))

            bar_bg = tk.Frame(row, bg=COLOURS["bar_bg"], height=6)
            bar_bg.pack(fill="x", padx=PAD["sm"], pady=(0, PAD["sm"]))
            bar_bg.pack_propagate(False)
            pct = entry.get("percent", 0)
            if pct > 0:
                tk.Frame(bar_bg, bg=_STRENGTH_BAR_COLOUR.get(entry.get("strength"), COLOURS["accent_blue"]),
                         height=6).place(relwidth=min(pct, 100) / 100, relheight=1)

    # -----------------------------------------------------------------------
    # Section 6 — Recommendations
    # -----------------------------------------------------------------------

    def _build_recommendations(self, parent: tk.Widget) -> None:
        weak_pairs = self.summary.get("weak_topic_pairs", [])
        if not weak_pairs:
            return

        panel = tk.Frame(
            parent, bg=COLOURS["bg_card"],
            highlightthickness=1, highlightbackground=COLOURS["accent_gold"],
        )
        panel.pack(fill="x", pady=(0, PAD["lg"]))

        if self.mode == config.CAT_MODE_PRETEST:
            tk.Label(
                panel, text="📚 Recommended Study Order",
                font=FONTS["subheading"], fg=COLOURS["accent_gold"], bg=COLOURS["bg_card"],
            ).pack(anchor="w", padx=PAD["md"], pady=(PAD["md"], 4))
            tk.Label(
                panel,
                text="Based on your diagnostic results, focus on these topics first:",
                font=FONTS["small"], fg=COLOURS["text_secondary"], bg=COLOURS["bg_card"],
                wraplength=600, justify="left",
            ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["sm"]))

            for i, (subject, topic) in enumerate(weak_pairs, start=1):
                label = config.TOPIC_LABELS.get(topic, topic)
                tk.Label(
                    panel, text=f"{i}. {label}  ({subject.title()})",
                    font=FONTS["body"], fg=COLOURS["text_primary"], bg=COLOURS["bg_card"],
                ).pack(anchor="w", padx=PAD["lg"], pady=(0, 2))

            tk.Label(
                panel,
                text="These topics have been highlighted in your topic screens for easy access.",
                font=FONTS["tiny"], fg=COLOURS["text_muted"], bg=COLOURS["bg_card"],
                wraplength=600, justify="left",
            ).pack(anchor="w", padx=PAD["md"], pady=(PAD["sm"], PAD["sm"]))

            first_subject, first_topic = weak_pairs[0]
            first_label = config.TOPIC_LABELS.get(first_topic, first_topic)
            make_button(
                panel, f"Start with {first_label} →",
                lambda s=first_subject, t=first_topic: self.app.go_learn(s, t),
                variant="gold", pady=8, padx=16,
            ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["md"]))

        else:
            tk.Label(
                panel, text="📚 Topics to Review",
                font=FONTS["subheading"], fg=COLOURS["accent_gold"], bg=COLOURS["bg_card"],
            ).pack(anchor="w", padx=PAD["md"], pady=(PAD["md"], 4))
            tk.Label(
                panel,
                text="Before your next attempt, go back to Practice and Evaluate these topics:",
                font=FONTS["small"], fg=COLOURS["text_secondary"], bg=COLOURS["bg_card"],
                wraplength=600, justify="left",
            ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["sm"]))

            for subject, topic in weak_pairs:
                label = config.TOPIC_LABELS.get(topic, topic)
                tk.Label(
                    panel, text=f"•  {label}  ({subject.title()})",
                    font=FONTS["body"], fg=COLOURS["text_primary"], bg=COLOURS["bg_card"],
                ).pack(anchor="w", padx=PAD["lg"], pady=(0, 2))

            tk.Frame(panel, bg=COLOURS["bg_card"], height=PAD["sm"]).pack()

    # -----------------------------------------------------------------------
    # Section 7 — CAT history
    # -----------------------------------------------------------------------

    def _build_history(self, parent: tk.Widget) -> None:
        title = "Previous Pre-Test Results" if self.mode == config.CAT_MODE_PRETEST else "Previous Exam Results"

        tk.Frame(parent, bg=COLOURS["border"], height=1).pack(fill="x", pady=(0, PAD["md"]))
        tk.Label(
            parent, text=title,
            font=FONTS["subheading"], fg=COLOURS["text_primary"], bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["sm"]))

        data = read_json(get_progress_path())
        history = data.get("cat_history", {}).get(self.mode, [])
        recent = list(reversed(history[-3:]))

        if not recent:
            tk.Label(
                parent, text="No previous results yet.",
                font=FONTS["small"], fg=COLOURS["text_muted"], bg=COLOURS["bg_main"],
            ).pack(anchor="w", pady=(0, PAD["lg"]))
            return

        for entry in recent:
            row = tk.Frame(parent, bg=COLOURS["bg_card"], highlightthickness=1,
                            highlightbackground=COLOURS["border"])
            row.pack(fill="x", pady=(0, PAD["sm"]))
            inner = tk.Frame(row, bg=COLOURS["bg_card"])
            inner.pack(fill="x", padx=PAD["md"], pady=PAD["sm"])

            date_str = _format_date(entry.get("date", ""))
            score    = entry.get("score_percent", 0)
            result   = str(entry.get("pass_fail", "")).title()
            elapsed  = entry.get("elapsed_seconds", 0)
            mins, secs = divmod(elapsed, 60)

            tk.Label(inner, text=date_str, font=FONTS["small"], fg=COLOURS["text_secondary"],
                     bg=COLOURS["bg_card"], width=14, anchor="w").pack(side="left")
            tk.Label(inner, text=f"{score}%", font=FONTS["small_bold"], fg=COLOURS["accent_blue"],
                     bg=COLOURS["bg_card"], width=6, anchor="w").pack(side="left")
            tk.Label(inner, text=result, font=FONTS["small_bold"], fg=COLOURS["text_primary"],
                     bg=COLOURS["bg_card"], width=12, anchor="w").pack(side="left")
            tk.Label(inner, text=f"{mins}:{secs:02d}", font=FONTS["small"], fg=COLOURS["text_muted"],
                     bg=COLOURS["bg_card"]).pack(side="left")

        tk.Frame(parent, bg=COLOURS["bg_main"], height=PAD["md"]).pack()

    # -----------------------------------------------------------------------
    # Section 8 — Action buttons
    # -----------------------------------------------------------------------

    def _build_action_buttons(self, parent: tk.Widget) -> None:
        row = tk.Frame(parent, bg=COLOURS["bg_main"])
        row.pack(fill="x", pady=(0, PAD["lg"]))

        make_button(
            row, "← Home", self.app.go_home,
            variant="ghost", pady=8, padx=16,
        ).pack(side="left")

        if self.mode == config.CAT_MODE_PRETEST:
            make_button(
                row, "Take Pre-Test Again",
                lambda: self.app.go_cat(mode=config.CAT_MODE_PRETEST),
                variant="ghost", pady=8, padx=16,
            ).pack(side="right", padx=(PAD["sm"], 0))
            make_button(
                row, "Start Studying →", self.app.go_home,
                variant="primary", pady=8, padx=16,
            ).pack(side="right", padx=(PAD["sm"], 0))
        else:
            weak_pairs = self.summary.get("weak_topic_pairs", [])
            if weak_pairs:
                first_subject = weak_pairs[0][0]
                make_button(
                    row, "Review Topics",
                    lambda s=first_subject: self.app.go_topic(s),
                    variant="warning", pady=8, padx=16,
                ).pack(side="right", padx=(PAD["sm"], 0))
            make_button(
                row, "Try Exam Again",
                lambda: self.app.go_cat(mode=config.CAT_MODE_FINAL),
                variant="gold", pady=8, padx=16,
            ).pack(side="right", padx=(PAD["sm"], 0))


def _format_date(iso_str: str) -> str:
    """Format an ISO datetime string as 'Jun 22, 2026'. Falls back to the raw string."""
    if not iso_str:
        return "—"
    try:
        dt = datetime.fromisoformat(iso_str)
        return f"{dt.strftime('%b')} {dt.day}, {dt.year}"
    except (ValueError, TypeError):
        return iso_str[:10]
