# =============================================================================
# gui/screens/learn_screen.py
# Phase 1 — LEARN screen.
#
# The most important screen in the app. Student must:
#   1. Read through all concept cards (one at a time, Next to advance)
#   2. Reveal all steps of every worked example (tap to reveal each step)
#   3. Only then does "I'm Ready to Practice →" appear
#
# Layout (two-panel):
#   ┌─────────────┬───────────────────────────────────┐
#   │  LEFT PANEL │  RIGHT PANEL                      │
#   │  Contents   │  Active content area              │
#   │  sidebar:   │  (concept card / worked example / │
#   │  · Concepts │   common mistakes / vocabulary)   │
#   │  · Examples │                                   │
#   │  · Mistakes │                                   │
#   │  · Vocab    │                                   │
#   └─────────────┴───────────────────────────────────┘
#   [ Progress bar ]  [ Next / Reveal Step / Ready btn ]
#
# Transitions to: practice_screen (on completion)
# =============================================================================

import tkinter as tk
from tkinter import ttk
import importlib
import logging

import config
from gui.styles import COLOURS, FONTS, PAD, make_button

logger = logging.getLogger(__name__)

# Sidebar section keys
_SEC_CONCEPTS  = "concepts"
_SEC_EXAMPLES  = "examples"
_SEC_MISTAKES  = "mistakes"
_SEC_VOCAB     = "vocab"

_SECTION_LABELS = {
    _SEC_CONCEPTS: "📖  Concepts",
    _SEC_EXAMPLES: "✏️  Worked Examples",
    _SEC_MISTAKES: "⚠️  Common Mistakes",
    _SEC_VOCAB:    "📝  Vocabulary",
}


class LearnScreen(tk.Frame):

    def __init__(self, parent: tk.Widget, app,
                 subject: str = "algebra",
                 topic: str = "linear_equations",
                 **kwargs):
        super().__init__(parent, bg=COLOURS["bg_main"])
        self.app     = app
        self.tracker = app.tracker
        self.subject = subject
        self.topic   = topic

        # Load content module
        self._content = self._load_content()

        # State tracking
        self._current_section   = _SEC_CONCEPTS
        self._card_index        = 0          # which concept card we're on
        self._example_index     = 0          # which worked example we're on
        self._step_index        = 0          # which step within the example
        self._cards_completed   = False
        self._examples_completed = False

        # Track which cards + examples have been fully viewed
        self._cards_seen   = set()
        self._examples_seen = set()

        self._build()
        self._show_section(_SEC_CONCEPTS)

    # -----------------------------------------------------------------------
    # Content loading
    # -----------------------------------------------------------------------

    def _load_content(self):
        """Dynamically load the content module for this topic."""
        module_path = f"content.{self.subject}.{self.topic}"
        try:
            mod = importlib.import_module(module_path)
            logger.info("Loaded content module: %s", module_path)
            return mod
        except ImportError as e:
            logger.error("Could not load content module %s: %s", module_path, e)
            return None

    # -----------------------------------------------------------------------
    # Main layout
    # -----------------------------------------------------------------------

    def _build(self) -> None:
        self._build_header()

        # Body: sidebar + content panel
        body = tk.Frame(self, bg=COLOURS["bg_main"])
        body.pack(fill="both", expand=True)

        self._build_sidebar(body)
        self._build_content_panel(body)
        self._build_footer()

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
            text=f"📖  Learn — {topic_label}",
            font=FONTS["subheading"],
            fg=COLOURS["accent_blue"],
            bg=COLOURS["bg_header"],
        ).pack(side="left", padx=PAD["sm"])

        # Phase badge
        tk.Label(
            header,
            text="PHASE 1 OF 3",
            font=FONTS["tiny"],
            fg=COLOURS["accent_blue"],
            bg=COLOURS["bg_header"],
        ).pack(side="right", padx=PAD["lg"])

    # -----------------------------------------------------------------------
    # Sidebar
    # -----------------------------------------------------------------------

    def _build_sidebar(self, parent: tk.Widget) -> None:
        self._sidebar = tk.Frame(
            parent, bg=COLOURS["bg_sidebar"], width=200
        )
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        tk.Label(
            self._sidebar,
            text="CONTENTS",
            font=FONTS["tiny"],
            fg=COLOURS["text_muted"],
            bg=COLOURS["bg_sidebar"],
        ).pack(anchor="w", padx=PAD["md"], pady=(PAD["lg"], PAD["sm"]))

        self._sidebar_buttons = {}

        sections = [
            _SEC_CONCEPTS,
            _SEC_EXAMPLES,
            _SEC_MISTAKES,
            _SEC_VOCAB,
        ]

        for sec in sections:
            btn = tk.Button(
                self._sidebar,
                text=_SECTION_LABELS[sec],
                command=lambda s=sec: self._show_section(s),
                font=FONTS["small"],
                fg=COLOURS["text_primary"],
                bg=COLOURS["bg_sidebar"],
                activebackground=COLOURS["bg_card"],
                activeforeground=COLOURS["text_white"],
                relief="flat", bd=0,
                padx=PAD["md"], pady=10,
                anchor="w", cursor="hand2",
            )
            btn.pack(fill="x")
            self._sidebar_buttons[sec] = btn

        # Completion indicators
        tk.Frame(self._sidebar, bg=COLOURS["border"], height=1).pack(
            fill="x", pady=PAD["md"]
        )

        self._progress_label = tk.Label(
            self._sidebar,
            text="",
            font=FONTS["tiny"],
            fg=COLOURS["text_muted"],
            bg=COLOURS["bg_sidebar"],
            wraplength=170,
            justify="left",
        )
        self._progress_label.pack(anchor="w", padx=PAD["md"])
        self._update_sidebar_progress()

    def _update_sidebar_progress(self) -> None:
        """Update the sidebar completion status text."""
        c = len(self._cards_seen)
        total_c = len(getattr(self._content, "CONCEPT_CARDS", []))
        e = len(self._examples_seen)
        total_e = len(getattr(self._content, "WORKED_EXAMPLES", []))

        lines = [
            f"Concepts:  {c}/{total_c}",
            f"Examples:  {e}/{total_e}",
        ]
        self._progress_label.config(text="\n".join(lines))

        # Highlight active section button
        for sec, btn in self._sidebar_buttons.items():
            if sec == self._current_section:
                btn.config(bg=COLOURS["bg_card"], fg=COLOURS["accent_blue"])
            else:
                btn.config(bg=COLOURS["bg_sidebar"], fg=COLOURS["text_primary"])

    # -----------------------------------------------------------------------
    # Content panel
    # -----------------------------------------------------------------------

    def _build_content_panel(self, parent: tk.Widget) -> None:
        self._content_frame = tk.Frame(parent, bg=COLOURS["bg_main"])
        self._content_frame.pack(side="left", fill="both", expand=True)

    def _clear_content(self) -> None:
        for widget in self._content_frame.winfo_children():
            widget.destroy()

    # -----------------------------------------------------------------------
    # Footer (progress bar + navigation buttons)
    # -----------------------------------------------------------------------

    def _build_footer(self) -> None:
        self._footer = tk.Frame(self, bg=COLOURS["bg_header"], height=64)
        self._footer.pack(fill="x", side="bottom")
        self._footer.pack_propagate(False)

        # Progress bar
        bar_frame = tk.Frame(self._footer, bg=COLOURS["bg_header"])
        bar_frame.pack(side="top", fill="x", padx=PAD["lg"], pady=(PAD["sm"], 0))

        self._progress_var = tk.DoubleVar(value=0)
        ttk.Progressbar(
            bar_frame,
            variable=self._progress_var,
            maximum=100,
            style="Green.Horizontal.TProgressbar",
            length=400,
        ).pack(side="left", fill="x", expand=True)

        self._pct_label = tk.Label(
            bar_frame,
            text="0%",
            font=FONTS["small_bold"],
            fg=COLOURS["accent_green"],
            bg=COLOURS["bg_header"],
        )
        self._pct_label.pack(side="left", padx=(PAD["sm"], 0))

        # Button row
        btn_row = tk.Frame(self._footer, bg=COLOURS["bg_header"])
        btn_row.pack(side="bottom", fill="x", padx=PAD["lg"], pady=(0, PAD["sm"]))

        self._prev_btn = make_button(
            btn_row, "← Previous", self._on_prev,
            variant="ghost", pady=6, padx=14, size="small_bold",
        )
        self._prev_btn.pack(side="left")

        # Next / Reveal / Ready button (right side)
        self._next_btn = make_button(
            btn_row, "Next →", self._on_next,
            variant="primary", pady=6, padx=14, size="small_bold",
        )
        self._next_btn.pack(side="right")

        self._ready_btn = make_button(
            btn_row, "I'm Ready to Practice →", self._on_ready,
            variant="success", pady=6, padx=14, size="small_bold",
        )
        # Hidden until all content viewed
        self._ready_btn_visible = False

    def _update_footer(self) -> None:
        """Refresh progress bar and button states."""
        pct = self._completion_percent()
        self._progress_var.set(pct)
        self._pct_label.config(text=f"{int(pct)}%")

        all_done = self._is_all_content_viewed()

        # Show/hide ready button
        if all_done and not self._ready_btn_visible:
            self._ready_btn.pack(side="right", padx=(PAD["sm"], 0))
            self._ready_btn_visible = True
            self._next_btn.pack_forget()
        elif not all_done:
            if self._ready_btn_visible:
                self._ready_btn.pack_forget()
                self._next_btn.pack(side="right")
                self._ready_btn_visible = False

    def _completion_percent(self) -> float:
        """Calculate overall learn completion as a percentage."""
        cards    = getattr(self._content, "CONCEPT_CARDS",   []) if self._content else []
        examples = getattr(self._content, "WORKED_EXAMPLES", []) if self._content else []
        total = len(cards) + len(examples)
        if total == 0:
            return 100.0
        done = len(self._cards_seen) + len(self._examples_seen)
        return (done / total) * 100

    def _is_all_content_viewed(self) -> bool:
        """True when all cards and all examples have been fully viewed."""
        cards    = getattr(self._content, "CONCEPT_CARDS",   []) if self._content else []
        examples = getattr(self._content, "WORKED_EXAMPLES", []) if self._content else []
        return (
            len(self._cards_seen)    >= len(cards) and
            len(self._examples_seen) >= len(examples)
        )

    # -----------------------------------------------------------------------
    # Section display
    # -----------------------------------------------------------------------

    def _show_section(self, section: str) -> None:
        self._current_section = section
        self._clear_content()
        self._update_sidebar_progress()

        if section == _SEC_CONCEPTS:
            self._show_concept_card()
        elif section == _SEC_EXAMPLES:
            self._show_worked_example()
        elif section == _SEC_MISTAKES:
            self._show_mistakes()
        elif section == _SEC_VOCAB:
            self._show_vocabulary()

        self._update_footer()

    # -----------------------------------------------------------------------
    # Concept cards
    # -----------------------------------------------------------------------

    def _show_concept_card(self) -> None:
        cards = getattr(self._content, "CONCEPT_CARDS", []) if self._content else []
        if not cards:
            self._show_placeholder("No concept cards available for this topic.")
            return

        idx   = self._card_index
        card  = cards[idx]
        total = len(cards)

        # Mark this card as seen
        self._cards_seen.add(idx)

        # Scrollable wrapper
        outer, content = self._scrollable_panel()

        # Card number
        tk.Label(
            content,
            text=f"Concept  {idx + 1}  of  {total}",
            font=FONTS["small_bold"],
            fg=COLOURS["text_muted"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["sm"]))

        # Card box
        card_frame = tk.Frame(
            content, bg=COLOURS["bg_card"],
            highlightthickness=1,
            highlightbackground=COLOURS["accent_blue"],
        )
        card_frame.pack(fill="x", pady=(0, PAD["md"]))

        # Title bar
        title_bar = tk.Frame(card_frame, bg=COLOURS["accent_blue"])
        title_bar.pack(fill="x")
        tk.Label(
            title_bar,
            text=card.get("title", ""),
            font=FONTS["subheading"],
            fg=COLOURS["text_white"],
            bg=COLOURS["accent_blue"],
            padx=PAD["md"], pady=PAD["sm"],
        ).pack(anchor="w")

        # Body text
        tk.Label(
            card_frame,
            text=card.get("body", ""),
            font=FONTS["body"],
            fg=COLOURS["text_primary"],
            bg=COLOURS["bg_card"],
            wraplength=500,
            justify="left",
            padx=PAD["md"], pady=PAD["md"],
        ).pack(anchor="w")

        # Formula box
        formula = card.get("formula")
        if formula:
            fbox = tk.Frame(
                card_frame, bg=COLOURS["bg_highlight"],
                highlightthickness=1,
                highlightbackground=COLOURS["accent_blue"],
            )
            fbox.pack(fill="x", padx=PAD["md"], pady=(0, PAD["sm"]))
            tk.Label(
                fbox,
                text=formula,
                font=FONTS["mono_large"],
                fg=COLOURS["accent_gold"],
                bg=COLOURS["bg_highlight"],
                padx=PAD["md"], pady=PAD["sm"],
            ).pack()

        # Example
        example = card.get("example")
        if example:
            tk.Label(
                card_frame,
                text=example,
                font=FONTS["mono_small"],
                fg=COLOURS["text_secondary"],
                bg=COLOURS["bg_card"],
                justify="left",
                padx=PAD["md"], pady=(0, PAD["md"]),
            ).pack(anchor="w")

        # Seen all check mark
        if len(self._cards_seen) >= total:
            tk.Label(
                content,
                text="✓  All concept cards read",
                font=FONTS["small_bold"],
                fg=COLOURS["accent_green"],
                bg=COLOURS["bg_main"],
            ).pack(anchor="w", pady=(PAD["sm"], 0))

        self._update_footer()

    # -----------------------------------------------------------------------
    # Worked examples
    # -----------------------------------------------------------------------

    def _show_worked_example(self) -> None:
        examples = getattr(self._content, "WORKED_EXAMPLES", []) if self._content else []
        if not examples:
            self._show_placeholder("No worked examples available for this topic.")
            return

        idx     = self._example_index
        example = examples[idx]
        total   = len(examples)
        steps   = example.get("steps", [])

        outer, content = self._scrollable_panel()

        tk.Label(
            content,
            text=f"Worked Example  {idx + 1}  of  {total}",
            font=FONTS["small_bold"],
            fg=COLOURS["text_muted"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["sm"]))

        # Problem statement
        prob_frame = tk.Frame(
            content, bg=COLOURS["bg_card"],
            highlightthickness=1,
            highlightbackground=COLOURS["accent_orange"],
        )
        prob_frame.pack(fill="x", pady=(0, PAD["md"]))

        tk.Label(
            prob_frame,
            text="Problem",
            font=FONTS["small_bold"],
            fg=COLOURS["accent_orange"],
            bg=COLOURS["bg_card"],
            padx=PAD["md"], pady=PAD["sm"],
        ).pack(anchor="w")

        tk.Label(
            prob_frame,
            text=example.get("problem", ""),
            font=FONTS["mono_large"],
            fg=COLOURS["text_primary"],
            bg=COLOURS["bg_card"],
            padx=PAD["md"], pady=(0, PAD["md"]),
        ).pack(anchor="w")

        # Steps — revealed one at a time
        steps_shown = self._step_index  # how many steps revealed so far

        for i, (desc, working) in enumerate(steps):
            if i >= steps_shown:
                break

            step_frame = tk.Frame(
                content, bg=COLOURS["bg_card"],
                highlightthickness=1,
                highlightbackground=COLOURS["border"],
            )
            step_frame.pack(fill="x", pady=(0, PAD["sm"]))

            # Step header
            step_hdr = tk.Frame(step_frame, bg=COLOURS["bg_highlight"])
            step_hdr.pack(fill="x")
            tk.Label(
                step_hdr,
                text=f"Step {i + 1}  —  {desc}",
                font=FONTS["small_bold"],
                fg=COLOURS["text_secondary"],
                bg=COLOURS["bg_highlight"],
                padx=PAD["sm"], pady=4,
            ).pack(anchor="w")

            tk.Label(
                step_frame,
                text=working,
                font=FONTS["mono_large"],
                fg=COLOURS["accent_gold"],
                bg=COLOURS["bg_card"],
                padx=PAD["md"], pady=PAD["sm"],
            ).pack(anchor="w")

        # Check line (shown only when all steps revealed)
        all_steps_shown = steps_shown >= len(steps)
        if all_steps_shown:
            check_frame = tk.Frame(
                content, bg=COLOURS["bg_correct"],
                highlightthickness=1,
                highlightbackground=COLOURS["accent_green"],
            )
            check_frame.pack(fill="x", pady=(0, PAD["md"]))
            tk.Label(
                check_frame,
                text=example.get("check", ""),
                font=FONTS["mono"],
                fg=COLOURS["accent_green"],
                bg=COLOURS["bg_correct"],
                padx=PAD["md"], pady=PAD["sm"],
            ).pack(anchor="w")

            notes = example.get("notes")
            if notes:
                tk.Label(
                    content,
                    text=f"💡  {notes}",
                    font=FONTS["small"],
                    fg=COLOURS["text_secondary"],
                    bg=COLOURS["bg_main"],
                    wraplength=500,
                    justify="left",
                ).pack(anchor="w", pady=(0, PAD["sm"]))

            self._examples_seen.add(idx)

        # Reveal next step button or example navigation
        if not all_steps_shown:
            make_button(
                content,
                f"Reveal Step {steps_shown + 1} of {len(steps)} →",
                self._on_reveal_step,
                variant="warning", pady=8,
            ).pack(anchor="w", pady=(PAD["sm"], 0))
        else:
            if idx + 1 < total:
                make_button(
                    content,
                    f"Next Example ({idx + 2} of {total}) →",
                    self._on_next_example,
                    variant="primary", pady=8,
                ).pack(anchor="w", pady=(PAD["sm"], 0))
            else:
                tk.Label(
                    content,
                    text="✓  All worked examples completed",
                    font=FONTS["small_bold"],
                    fg=COLOURS["accent_green"],
                    bg=COLOURS["bg_main"],
                ).pack(anchor="w", pady=(PAD["sm"], 0))

        self._update_footer()

    # -----------------------------------------------------------------------
    # Common mistakes
    # -----------------------------------------------------------------------

    def _show_mistakes(self) -> None:
        mistakes = getattr(self._content, "COMMON_MISTAKES", []) if self._content else []
        outer, content = self._scrollable_panel()

        tk.Label(
            content,
            text="Common Mistakes to Avoid",
            font=FONTS["heading"],
            fg=COLOURS["accent_red"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["md"]))

        if not mistakes:
            self._show_placeholder("No mistakes listed for this topic.", parent=content)
            return

        for m in mistakes:
            frame = tk.Frame(
                content, bg=COLOURS["bg_card"],
                highlightthickness=1,
                highlightbackground=COLOURS["accent_red"],
            )
            frame.pack(fill="x", pady=(0, PAD["sm"]))

            # Mistake header
            hdr = tk.Frame(frame, bg=COLOURS["bg_incorrect"])
            hdr.pack(fill="x")
            tk.Label(
                hdr,
                text=f"✗  {m.get('mistake', '')}",
                font=FONTS["body_bold"],
                fg=COLOURS["accent_red"],
                bg=COLOURS["bg_incorrect"],
                padx=PAD["md"], pady=PAD["sm"],
                wraplength=520,
                justify="left",
            ).pack(anchor="w")

            # Example
            tk.Label(
                frame,
                text=f"Example:  {m.get('example', '')}",
                font=FONTS["mono_small"],
                fg=COLOURS["text_secondary"],
                bg=COLOURS["bg_card"],
                padx=PAD["md"], pady=PAD["sm"],
                wraplength=520,
                justify="left",
            ).pack(anchor="w")

            # Fix
            tk.Label(
                frame,
                text=f"✓  Fix:  {m.get('fix', '')}",
                font=FONTS["small"],
                fg=COLOURS["accent_green"],
                bg=COLOURS["bg_card"],
                padx=PAD["md"], pady=(0, PAD["sm"]),
                wraplength=520,
                justify="left",
            ).pack(anchor="w")

    # -----------------------------------------------------------------------
    # Vocabulary
    # -----------------------------------------------------------------------

    def _show_vocabulary(self) -> None:
        vocab = getattr(self._content, "KEY_VOCABULARY", {}) if self._content else {}
        outer, content = self._scrollable_panel()

        tk.Label(
            content,
            text="Key Vocabulary",
            font=FONTS["heading"],
            fg=COLOURS["accent_gold"],
            bg=COLOURS["bg_main"],
        ).pack(anchor="w", pady=(0, PAD["md"]))

        if not vocab:
            self._show_placeholder("No vocabulary for this topic.", parent=content)
            return

        for term, definition in vocab.items():
            row = tk.Frame(
                content, bg=COLOURS["bg_card"],
                highlightthickness=1,
                highlightbackground=COLOURS["border"],
            )
            row.pack(fill="x", pady=(0, PAD["sm"]))

            tk.Label(
                row,
                text=term,
                font=FONTS["body_bold"],
                fg=COLOURS["accent_gold"],
                bg=COLOURS["bg_card"],
                padx=PAD["md"], pady=PAD["sm"],
                anchor="w",
            ).pack(anchor="w")

            tk.Label(
                row,
                text=definition,
                font=FONTS["body"],
                fg=COLOURS["text_primary"],
                bg=COLOURS["bg_card"],
                padx=PAD["md"], pady=(0, PAD["sm"]),
                wraplength=520,
                justify="left",
            ).pack(anchor="w")

    # -----------------------------------------------------------------------
    # Navigation actions
    # -----------------------------------------------------------------------

    def _on_next(self) -> None:
        """Advance within current section."""
        if self._current_section == _SEC_CONCEPTS:
            cards = getattr(self._content, "CONCEPT_CARDS", []) if self._content else []
            if self._card_index < len(cards) - 1:
                self._card_index += 1
                self._show_concept_card()
            else:
                # All cards done — move to examples
                self._show_section(_SEC_EXAMPLES)

        elif self._current_section == _SEC_EXAMPLES:
            self._on_reveal_step()

    def _on_prev(self) -> None:
        """Go back within current section."""
        if self._current_section == _SEC_CONCEPTS:
            if self._card_index > 0:
                self._card_index -= 1
                self._show_concept_card()
        elif self._current_section == _SEC_EXAMPLES:
            if self._example_index > 0:
                self._example_index -= 1
                self._step_index = 0
                self._show_worked_example()

    def _on_reveal_step(self) -> None:
        """Reveal the next step of the current worked example."""
        examples = getattr(self._content, "WORKED_EXAMPLES", []) if self._content else []
        if not examples:
            return
        steps = examples[self._example_index].get("steps", [])
        if self._step_index < len(steps):
            self._step_index += 1
        self._show_worked_example()

    def _on_next_example(self) -> None:
        """Move to the next worked example."""
        examples = getattr(self._content, "WORKED_EXAMPLES", []) if self._content else []
        if self._example_index < len(examples) - 1:
            self._example_index += 1
            self._step_index = 0
            self._show_worked_example()

    def _on_ready(self) -> None:
        """Student has viewed all content — mark Learn complete and go to Practice."""
        self.tracker.complete_learn(self.subject, self.topic)
        logger.info("Learn phase complete: %s / %s", self.subject, self.topic)
        self.app.go_practice(self.subject, self.topic)

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _scrollable_panel(self) -> tuple:
        """
        Create a scrollable canvas+frame inside the content panel.
        Returns (canvas_outer_frame, inner_content_frame).
        """
        outer = tk.Frame(self._content_frame, bg=COLOURS["bg_main"])
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=COLOURS["bg_main"], highlightthickness=0)
        sb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=COLOURS["bg_main"])
        win   = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _resize_canvas(e):
            canvas.itemconfig(win, width=e.width)
        canvas.bind("<Configure>", _resize_canvas)

        def _update_scroll(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner.bind("<Configure>", _update_scroll)

        def _mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _mousewheel)

        # Actual content frame with padding
        content = tk.Frame(inner, bg=COLOURS["bg_main"])
        content.pack(fill="both", expand=True, padx=PAD["lg"], pady=PAD["md"])

        return outer, content

    def _show_placeholder(self, msg: str, parent=None) -> None:
        target = parent or self._content_frame
        tk.Label(
            target,
            text=msg,
            font=FONTS["body"],
            fg=COLOURS["text_muted"],
            bg=COLOURS["bg_main"],
        ).pack(expand=True)