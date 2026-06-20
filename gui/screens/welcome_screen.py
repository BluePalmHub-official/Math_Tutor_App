# =============================================================================
# gui/screens/welcome_screen.py
# Welcome screen — first thing the student sees.
# =============================================================================

import tkinter as tk
import logging

from gui.styles import COLOURS, FONTS, PAD, make_button

logger = logging.getLogger(__name__)


class WelcomeScreen(tk.Frame):

    def __init__(self, parent: tk.Widget, app, **kwargs):
        super().__init__(parent, bg=COLOURS["bg_main"])
        self.app = app

        existing_name = self.app.tracker.get_student_name()

        if existing_name:
            self._build_returning(existing_name)
        else:
            self._build_new_student()

    # -----------------------------------------------------------------------
    # New student layout
    # -----------------------------------------------------------------------

    def _build_new_student(self) -> None:
        outer = tk.Frame(self, bg=COLOURS["bg_main"])
        outer.pack(expand=True)

        # App title
        tk.Label(
            outer,
            text="Math Foundation Builder",
            font=FONTS["title"],
            fg=COLOURS["accent_gold"],
            bg=COLOURS["bg_main"],
        ).pack(pady=(0, 4))

        tk.Label(
            outer,
            text="Algebra & Geometry — Grade 12 Prep",
            font=FONTS["body"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_main"],
        ).pack(pady=(0, PAD["xl"]))

        # Card
        card = tk.Frame(
            outer,
            bg=COLOURS["bg_card"],
            highlightthickness=1,
            highlightbackground=COLOURS["border"],
        )
        card.pack(fill="x", ipadx=PAD["lg"], ipady=PAD["lg"])

        tk.Label(
            card,
            text="Welcome! What is your name?",
            font=FONTS["subheading"],
            fg=COLOURS["text_primary"],
            bg=COLOURS["bg_card"],
        ).pack(pady=(PAD["lg"], PAD["md"]))

        # Name entry
        self._name_var = tk.StringVar()
        self._entry = tk.Entry(
            card,
            textvariable=self._name_var,
            font=FONTS["heading"],
            bg=COLOURS["bg_input"],
            fg=COLOURS["text_primary"],
            insertbackground=COLOURS["text_primary"],
            relief="flat",
            bd=0,
            highlightthickness=2,
            highlightcolor=COLOURS["accent_blue"],
            highlightbackground=COLOURS["border"],
            justify="center",
            width=24,
        )
        self._entry.pack(ipady=10, pady=(0, PAD["sm"]), padx=PAD["lg"])
        self._entry.focus_set()
        self._entry.bind("<Return>", lambda e: self._on_start())

        # Error label
        self._error_var = tk.StringVar()
        tk.Label(
            card,
            textvariable=self._error_var,
            font=FONTS["small"],
            fg=COLOURS["accent_red"],
            bg=COLOURS["bg_card"],
        ).pack()

        make_button(
            card, "Start Learning  →", self._on_start,
            variant="success", width=22,
        ).pack(pady=(PAD["sm"], PAD["lg"]))

        tk.Label(
            outer,
            text="Your progress is saved automatically.",
            font=FONTS["small"],
            fg=COLOURS["text_muted"],
            bg=COLOURS["bg_main"],
        ).pack(pady=(PAD["sm"], 0))

    # -----------------------------------------------------------------------
    # Returning student layout
    # -----------------------------------------------------------------------

    def _build_returning(self, name: str) -> None:
        outer = tk.Frame(self, bg=COLOURS["bg_main"])
        outer.pack(expand=True)

        tk.Label(
            outer,
            text="Math Foundation Builder",
            font=FONTS["title"],
            fg=COLOURS["accent_gold"],
            bg=COLOURS["bg_main"],
        ).pack(pady=(0, 4))

        tk.Label(
            outer,
            text="Algebra & Geometry — Grade 12 Prep",
            font=FONTS["body"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_main"],
        ).pack(pady=(0, PAD["xl"]))

        card = tk.Frame(
            outer,
            bg=COLOURS["bg_card"],
            highlightthickness=1,
            highlightbackground=COLOURS["border"],
        )
        card.pack(ipadx=PAD["lg"], ipady=PAD["md"])

        tk.Label(
            card,
            text="Welcome back,",
            font=FONTS["body"],
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_card"],
        ).pack(pady=(PAD["lg"], 2))

        tk.Label(
            card,
            text=name,
            font=FONTS["title"],
            fg=COLOURS["accent_gold"],
            bg=COLOURS["bg_card"],
        ).pack(pady=(0, PAD["md"]))

        # Progress summary
        overall = self.app.tracker.get_overall_progress()
        geo_line = (
            "Geometry: 🔒 Unlock by mastering all Algebra topics"
            if overall["geometry_locked"]
            else f"Geometry: {overall['geometry_mastered']} / {overall['geometry_total']} mastered"
        )
        summary = (
            f"Algebra:  {overall['algebra_mastered']} / {overall['algebra_total']} topics mastered\n"
            f"{geo_line}\n"
            f"Overall progress: {overall['percent_overall']}%"
        )

        tk.Label(
            card,
            text=summary,
            font=FONTS["body"],
            fg=COLOURS["text_primary"],
            bg=COLOURS["bg_card"],
            justify="center",
        ).pack(pady=(0, PAD["lg"]))

        make_button(
            card, "Continue Learning  →", self._on_continue,
            variant="success", width=24,
        ).pack(pady=(0, PAD["sm"]))

        make_button(
            card, "Switch Student", self._on_new_student,
            variant="ghost", width=24, pady=6,
        ).pack(pady=(0, PAD["lg"]))

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    def _on_start(self) -> None:
        name = self._name_var.get().strip()
        if not name:
            self._error_var.set("Please enter your name to continue.")
            self._entry.focus_set()
            return
        if len(name) < 2:
            self._error_var.set("Please enter at least 2 characters.")
            self._entry.focus_set()
            return
        self.app.tracker.set_student_name(name)
        logger.info("New student started: %s", name)
        self.app.show_screen("home")

    def _on_continue(self) -> None:
        self.app.show_screen("home")

    def _on_new_student(self) -> None:
        self.app.tracker.set_student_name("")
        self.app.show_screen("welcome")