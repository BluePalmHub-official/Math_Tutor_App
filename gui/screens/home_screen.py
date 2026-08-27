# =============================================================================
# gui/screens/home_screen.py
# Home dashboard — shown after login.
# =============================================================================

import tkinter as tk
import logging
from datetime import datetime

import config
from gui.styles import COLOURS, FONTS, PAD, make_button
from utils.file_io import read_json, get_progress_path

logger = logging.getLogger(__name__)

_CAT_TEAL = "#17A398"


class HomeScreen(tk.Frame):

    def __init__(self, parent: tk.Widget, app, **kwargs):
        super().__init__(parent, bg=COLOURS["bg_main"])
        self.app     = app
        self.tracker = app.tracker
        self._build()

    def _build(self) -> None:
        overall = self.tracker.get_overall_progress()
        name    = self.tracker.get_student_name()

        self._build_header(name, overall)

        body = tk.Frame(self, bg=COLOURS["bg_main"])
        body.pack(fill="both", expand=True)

        self._build_sidebar(body)
        self._build_main(body, overall)

    # -----------------------------------------------------------------------
    # Header
    # -----------------------------------------------------------------------

    def _build_header(self, name: str, overall: dict) -> None:
        header = tk.Frame(self, bg=COLOURS["bg_header"], height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="  📚  Math Foundation Builder",
            font=FONTS["subheading"],
            fg=COLOURS["accent_gold"],
            bg=COLOURS["bg_header"],
        ).pack(side="left", padx=PAD["md"])

        tk.Label(
            header,
            text=f"{name}  |  {overall['percent_overall']}% complete  ",
            font=FONTS["small_bold"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_header"],
        ).pack(side="right")

    # -----------------------------------------------------------------------
    # Sidebar
    # -----------------------------------------------------------------------

    def _build_sidebar(self, parent: tk.Widget) -> None:
        sidebar = tk.Frame(parent, bg=COLOURS["bg_sidebar"], width=170)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="MENU",
            font=FONTS["tiny"],
            fg=COLOURS["text_muted"],
            bg=COLOURS["bg_sidebar"],
        ).pack(anchor="w", padx=PAD["md"], pady=(PAD["lg"], PAD["sm"]))

        items = [
            ("🏠  Dashboard",   None),
            ("📊  My Progress", self.app.go_progress),
        ]
        for label, cmd in items:
            tk.Button(
                sidebar,
                text=label,
                command=cmd if cmd else lambda: None,
                font=FONTS["body"],
                fg=COLOURS["text_primary"],
                bg=COLOURS["bg_sidebar"],
                activebackground=COLOURS["bg_card"],
                activeforeground=COLOURS["text_white"],
                relief="flat", bd=0,
                padx=PAD["md"], pady=10,
                anchor="w", cursor="hand2",
            ).pack(fill="x")

    # -----------------------------------------------------------------------
    # Main content
    # -----------------------------------------------------------------------

    def _build_main(self, parent: tk.Widget, overall: dict) -> None:
        main = tk.Frame(parent, bg=COLOURS["bg_main"])
        main.pack(side="left", fill="both", expand=True,
                  padx=PAD["lg"], pady=PAD["lg"])

        tk.Label(
            main,
            text="Choose a Module",
            font=FONTS["heading"],
            fg=COLOURS["text_primary"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, 4))

        tk.Label(
            main,
            text="Complete each module in order — Geometry unlocks after Algebra, "
                 "Advanced unlocks after Geometry.",
            font=FONTS["small"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["lg"]))

        # Module cards
        cards_row = tk.Frame(main, bg=COLOURS["bg_main"])
        cards_row.pack(fill="x", pady=(0, PAD["lg"]))

        self._module_card(
            cards_row, config.SUBJECT_ALGEBRA,
            "📐  Algebra", overall["algebra_mastered"],
            overall["algebra_total"], locked=False,
        )

        tk.Frame(cards_row, bg=COLOURS["bg_main"], width=PAD["lg"]).pack(side="left")

        self._module_card(
            cards_row, config.SUBJECT_GEOMETRY,
            "📏  Geometry", overall["geometry_mastered"],
            overall["geometry_total"], locked=overall["geometry_locked"],
            lock_msg="Complete all Algebra topics to unlock",
        )

        tk.Frame(cards_row, bg=COLOURS["bg_main"], width=PAD["lg"]).pack(side="left")

        self._module_card(
            cards_row, config.SUBJECT_ADVANCED,
            "🎓  Advanced", overall["advanced_mastered"],
            overall["advanced_total"], locked=overall["advanced_locked"],
            lock_msg="Complete all Geometry topics to unlock",
        )

        # Divider
        tk.Frame(main, bg=COLOURS["border"], height=1).pack(fill="x", pady=PAD["md"])

        # Stats
        self._build_stats(main, overall)

        # Divider
        tk.Frame(main, bg=COLOURS["border"], height=1).pack(fill="x", pady=PAD["md"])

        # CAT panels
        self._build_cat_panels(main, overall)

    # -----------------------------------------------------------------------
    # Module card
    # -----------------------------------------------------------------------

    def _module_card(
        self, parent, subject, title, mastered, total, locked,
        lock_msg="Complete prerequisites to unlock",
    ) -> None:
        card = tk.Frame(
            parent, bg=COLOURS["bg_card"],
            highlightthickness=1,
            highlightbackground=COLOURS["border"],
        )
        card.pack(side="left", fill="both", expand=True,
                  ipadx=PAD["md"], ipady=PAD["md"])

        title_colour = COLOURS["text_muted"] if locked else COLOURS["text_primary"]
        tk.Label(
            card, text=title,
            font=FONTS["heading"],
            fg=title_colour, bg=COLOURS["bg_card"],
        ).pack(anchor="w", padx=PAD["md"], pady=(PAD["md"], PAD["sm"]))

        if locked:
            tk.Label(
                card,
                text=f"🔒  {lock_msg}",
                font=FONTS["small"],
                fg=COLOURS["text_muted"],
                bg=COLOURS["bg_card"],
            ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["md"]))

            make_button(
                card, "🔒  Locked", lambda: None,
                variant="ghost", width=18,
            ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["md"]))

        else:
            pct = int((mastered / total) * 100) if total else 0

            tk.Label(
                card,
                text=f"{mastered} of {total} topics mastered",
                font=FONTS["body"],
                fg=COLOURS["text_secondary"],
                bg=COLOURS["bg_card"],
            ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["sm"]))

            # Progress bar
            bar_outer = tk.Frame(card, bg=COLOURS["bar_bg"], height=8)
            bar_outer.pack(fill="x", padx=PAD["md"], pady=(0, PAD["md"]))
            bar_outer.pack_propagate(False)
            if pct > 0:
                tk.Frame(bar_outer, bg=COLOURS["bar_fill"], height=8).place(
                    relwidth=pct / 100, relheight=1
                )

            subject_label = title.split("  ")[1]
            make_button(
                card, f"Open {subject_label}  →",
                lambda s=subject: self.app.go_topic(s),
                variant="primary", width=18,
            ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["md"]))

    # -----------------------------------------------------------------------
    # Stats row
    # -----------------------------------------------------------------------

    def _build_stats(self, parent: tk.Widget, overall: dict) -> None:
        tk.Label(
            parent,
            text="Your Progress at a Glance",
            font=FONTS["subheading"],
            fg=COLOURS["text_primary"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["sm"]))

        row = tk.Frame(parent, bg=COLOURS["bg_main"])
        row.pack(anchor="w")

        stats = [
            ("Algebra Mastered",  f"{overall['algebra_mastered']} / {overall['algebra_total']}",  COLOURS["accent_blue"]),
            ("Geometry Mastered", f"{overall['geometry_mastered']} / {overall['geometry_total']}", COLOURS["accent_orange"]),
            ("Advanced Mastered", f"{overall['advanced_mastered']} / {overall['advanced_total']}", COLOURS["accent_gold"]),
            ("Overall",           f"{overall['percent_overall']}%",                                COLOURS["accent_green"]),
        ]

        for label, value, colour in stats:
            tile = tk.Frame(
                row, bg=COLOURS["bg_card"],
                highlightthickness=1,
                highlightbackground=COLOURS["border"],
            )
            tile.pack(side="left", padx=(0, PAD["sm"]),
                      ipadx=PAD["lg"], ipady=PAD["sm"])

            tk.Label(
                tile, text=value,
                font=FONTS["heading"],
                fg=colour, bg=COLOURS["bg_card"],
            ).pack()

            tk.Label(
                tile, text=label,
                font=FONTS["tiny"],
                fg=COLOURS["text_secondary"],
                bg=COLOURS["bg_card"],
            ).pack()

    # -----------------------------------------------------------------------
    # CAT panels — Diagnostic Pre-Test & Final Adaptive Exam
    # -----------------------------------------------------------------------

    def _build_cat_panels(self, parent: tk.Widget, overall: dict) -> None:
        tk.Label(
            parent,
            text="Assessments",
            font=FONTS["subheading"],
            fg=COLOURS["text_primary"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["sm"]))

        row = tk.Frame(parent, bg=COLOURS["bg_main"])
        row.pack(fill="x")

        self._build_pretest_panel(row)
        tk.Frame(row, bg=COLOURS["bg_main"], width=PAD["lg"]).pack(side="left")
        self._build_final_exam_panel(row, overall)

    def _build_pretest_panel(self, parent: tk.Widget) -> None:
        panel = tk.Frame(
            parent, bg=COLOURS["bg_card"],
            highlightthickness=1, highlightbackground=_CAT_TEAL,
        )
        panel.pack(side="left", fill="both", expand=True, ipadx=PAD["md"], ipady=PAD["md"])

        tk.Label(
            panel, text="📋  Diagnostic Pre-Test",
            font=FONTS["heading"], fg=_CAT_TEAL, bg=COLOURS["bg_card"],
        ).pack(anchor="w", padx=PAD["md"], pady=(PAD["md"], PAD["sm"]))

        tk.Label(
            panel,
            text=("Not sure where to start? Take a quick diagnostic test to "
                  "identify your strong and weak areas before you begin studying."),
            font=FONTS["small"], fg=COLOURS["text_secondary"], bg=COLOURS["bg_card"],
            wraplength=280, justify="left",
        ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["sm"]))

        last_result = self._get_last_cat_result(config.CAT_MODE_PRETEST)
        if last_result:
            tk.Label(
                panel, text=last_result,
                font=FONTS["tiny"], fg=COLOURS["text_muted"], bg=COLOURS["bg_card"],
            ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["sm"]))

        make_button(
            panel, "Take Diagnostic Pre-Test →",
            lambda: self.app.go_cat(mode=config.CAT_MODE_PRETEST),
            variant="primary", width=24,
        ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["md"]))

    def _build_final_exam_panel(self, parent: tk.Widget, overall: dict) -> None:
        all_mastered = (
            overall["algebra_mastered"]  == overall["algebra_total"] and
            overall["geometry_mastered"] == overall["geometry_total"] and
            overall["advanced_mastered"] == overall["advanced_total"] and
            not overall["geometry_locked"] and
            not overall["advanced_locked"]
        )

        border = COLOURS["accent_gold"] if all_mastered else COLOURS["border"]
        panel = tk.Frame(
            parent, bg=COLOURS["bg_card"],
            highlightthickness=1, highlightbackground=border,
        )
        panel.pack(side="left", fill="both", expand=True, ipadx=PAD["md"], ipady=PAD["md"])

        if all_mastered:
            tk.Label(
                panel, text="🎓  Final Adaptive Exam  ✅  READY",
                font=FONTS["heading"], fg=COLOURS["accent_gold"], bg=COLOURS["bg_card"],
            ).pack(anchor="w", padx=PAD["md"], pady=(PAD["md"], PAD["sm"]))

            tk.Label(
                panel,
                text="60 questions · Adaptive difficulty · Tests all topics · Just like NCLEX CAT",
                font=FONTS["small"], fg=COLOURS["text_secondary"], bg=COLOURS["bg_card"],
                wraplength=280, justify="left",
            ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["sm"]))

            last_result = self._get_last_cat_result(config.CAT_MODE_FINAL)
            if last_result:
                tk.Label(
                    panel, text=last_result,
                    font=FONTS["tiny"], fg=COLOURS["text_muted"], bg=COLOURS["bg_card"],
                ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["sm"]))

            make_button(
                panel, "Start Final Exam →",
                lambda: self.app.go_cat(mode=config.CAT_MODE_FINAL),
                variant="gold", width=24,
            ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["md"]))
        else:
            tk.Label(
                panel, text="🎓  Final Adaptive Exam  🔒",
                font=FONTS["heading"], fg=COLOURS["text_muted"], bg=COLOURS["bg_card"],
            ).pack(anchor="w", padx=PAD["md"], pady=(PAD["md"], PAD["sm"]))

            tk.Label(
                panel,
                text="Complete all topics in Algebra, Geometry, and Advanced to unlock the Final Exam.",
                font=FONTS["small"], fg=COLOURS["text_muted"], bg=COLOURS["bg_card"],
                wraplength=280, justify="left",
            ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["sm"]))

            tk.Label(
                panel,
                text=(f"Algebra: {overall['algebra_mastered']}/{overall['algebra_total']}  ·  "
                      f"Geometry: {overall['geometry_mastered']}/{overall['geometry_total']}  ·  "
                      f"Advanced: {overall['advanced_mastered']}/{overall['advanced_total']}"),
                font=FONTS["tiny"], fg=COLOURS["text_muted"], bg=COLOURS["bg_card"],
            ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["sm"]))

            make_button(
                panel, "🔒  Locked", lambda: None,
                variant="ghost", width=24,
            ).pack(anchor="w", padx=PAD["md"], pady=(0, PAD["md"]))

    def _get_last_cat_result(self, mode: str):
        """Return a formatted one-line summary of the most recent CAT result for this mode, or None."""
        data = read_json(get_progress_path())
        history = data.get("cat_history", {}).get(mode, [])
        if not history:
            return None

        entry = history[-1]
        score = entry.get("score_percent", 0)
        when  = self._relative_date(entry.get("date", ""))

        if mode == config.CAT_MODE_PRETEST:
            weak_count = len(entry.get("weak_topics", []))
            noun = "weak topic" if weak_count == 1 else "weak topics"
            return f"Last result: {score}% · {weak_count} {noun} · {when}"

        result = str(entry.get("pass_fail", "")).title()
        return f"Last result: {score}% · {result} · {when}"

    def _relative_date(self, iso_str: str) -> str:
        """Return a human-friendly 'N days ago' string from an ISO date, or ''."""
        if not iso_str:
            return ""
        try:
            dt = datetime.fromisoformat(iso_str)
        except (ValueError, TypeError):
            return ""
        days = (datetime.now() - dt).days
        if days <= 0:
            return "today"
        if days == 1:
            return "1 day ago"
        return f"{days} days ago"