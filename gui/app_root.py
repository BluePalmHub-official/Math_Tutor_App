# =============================================================================
# gui/app_root.py
# Main application window and screen manager.
#
# Responsibilities:
#   - Own the single Tk root window
#   - Hold one instance each of ProgressTracker and SessionManager
#   - Manage screen transitions (show_screen replaces the current frame)
#   - Pass shared resources (tracker, session_manager, show_screen) to screens
#
# Screen lifecycle:
#   Each screen is a tk.Frame subclass.
#   show_screen() destroys the old frame and creates a fresh one.
#   This keeps memory clean and ensures each screen always re-reads
#   the latest progress data when it opens.
# =============================================================================

import tkinter as tk
import logging

from config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from gui.styles import COLOURS, configure_ttk_styles
from core.progress_tracker import ProgressTracker
from core.session_manager import SessionManager

logger = logging.getLogger(__name__)


class AppRoot:
    """
    The top-level application controller.

    Created once in main.py and passed the Tk root window.
    All screens receive a reference to this object so they can
    call self.app.show_screen(...) to navigate.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self._setup_window()

        # Shared backend objects — one instance for the entire app lifetime
        self.tracker         = ProgressTracker()
        self.tracker.load()
        self.session_manager = SessionManager(self.tracker)

        # Container frame that fills the window — screens are placed inside it
        self.container = tk.Frame(self.root, bg=COLOURS["bg_main"])
        self.container.pack(fill="both", expand=True)

        self._current_screen = None   # reference to the active screen frame

        # Start on the welcome screen
        self.show_screen("welcome")

        logger.info("AppRoot initialised — showing welcome screen")

    # -----------------------------------------------------------------------
    # Window setup
    # -----------------------------------------------------------------------

    def _setup_window(self) -> None:
        """Configure the root Tk window."""
        self.root.title(APP_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.root.configure(bg=COLOURS["bg_main"])
        self.root.resizable(True, True)

        # Centre the window on the screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - WINDOW_WIDTH)  // 2
        y = (self.root.winfo_screenheight() - WINDOW_HEIGHT) // 2
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

        # Configure ttk dark styles
        configure_ttk_styles(self.root)

        # Handle window close gracefully
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # -----------------------------------------------------------------------
    # Screen navigation
    # -----------------------------------------------------------------------

    def show_screen(self, screen_name: str, **kwargs) -> None:
        """
        Switch to a named screen.

        Destroys the current screen frame (if any), imports the new screen
        module, instantiates it, and packs it into the container.

        Parameters:
            screen_name : one of the keys in SCREEN_MAP below
            **kwargs    : passed directly to the screen's __init__
                          e.g. show_screen("topic", subject="algebra")
        """
        # Lazy imports — screens are only imported when first needed.
        # This keeps startup fast and avoids circular import issues.
        SCREEN_MAP = {
            "welcome":  self._import_welcome,
            "home":     self._import_home,
            "topic":    self._import_topic,
            "learn":    self._import_learn,
            "practice": self._import_practice,
            "problem":  self._import_problem,
            "result":   self._import_result,
            "progress": self._import_progress,
        }

        factory = SCREEN_MAP.get(screen_name)
        if factory is None:
            logger.error("show_screen: unknown screen '%s'", screen_name)
            return

        # Destroy the current screen
        if self._current_screen is not None:
            self._current_screen.destroy()
            self._current_screen = None

        # Build the new screen
        try:
            ScreenClass = factory()
            screen = ScreenClass(
                parent=self.container,
                app=self,
                **kwargs,
            )
            screen.pack(fill="both", expand=True)
            self._current_screen = screen
            logger.info("Navigated to screen: %s", screen_name)
        except Exception as e:
            logger.error("show_screen: failed to load '%s': %s", screen_name, e, exc_info=True)
            self._show_error_screen(screen_name, e)

    # -----------------------------------------------------------------------
    # Lazy screen importers
    # Each returns the Screen class — imported only when called.
    # -----------------------------------------------------------------------

    def _import_welcome(self):
        from gui.screens.welcome_screen import WelcomeScreen
        return WelcomeScreen

    def _import_home(self):
        from gui.screens.home_screen import HomeScreen
        return HomeScreen

    def _import_topic(self):
        from gui.screens.topic_screen import TopicScreen
        return TopicScreen

    def _import_learn(self):
        from gui.screens.learn_screen import LearnScreen
        return LearnScreen

    def _import_practice(self):
        from gui.screens.practice_screen import PracticeScreen
        return PracticeScreen

    def _import_problem(self):
        from gui.screens.problem_screen import ProblemScreen
        return ProblemScreen

    def _import_result(self):
        from gui.screens.result_screen import ResultScreen
        return ResultScreen

    def _import_progress(self):
        from gui.screens.progress_screen import ProgressScreen
        return ProgressScreen

    # -----------------------------------------------------------------------
    # Convenience navigation methods (called by screens)
    # -----------------------------------------------------------------------

    def go_home(self) -> None:
        """Navigate to the home dashboard."""
        self.show_screen("home")

    def go_welcome(self) -> None:
        """Navigate to the welcome / name entry screen."""
        self.show_screen("welcome")

    def go_topic(self, subject: str) -> None:
        """Navigate to the topic list for a subject."""
        self.show_screen("topic", subject=subject)

    def go_learn(self, subject: str, topic: str) -> None:
        """Navigate to the Learn phase screen."""
        self.show_screen("learn", subject=subject, topic=topic)

    def go_practice(self, subject: str, topic: str) -> None:
        """Navigate to the Practice phase screen."""
        self.show_screen("practice", subject=subject, topic=topic)

    def go_problem(self, subject: str, topic: str) -> None:
        """Navigate to the Evaluate phase screen."""
        self.show_screen("problem", subject=subject, topic=topic)

    def go_result(self, result_data: dict) -> None:
        """Navigate to the result summary screen."""
        self.show_screen("result", result_data=result_data)

    def go_progress(self) -> None:
        """Navigate to the overall progress dashboard."""
        self.show_screen("progress")

    # -----------------------------------------------------------------------
    # Error fallback screen
    # -----------------------------------------------------------------------

    def _show_error_screen(self, screen_name: str, error: Exception) -> None:
        """Show a minimal error message if a screen fails to load."""
        frame = tk.Frame(self.container, bg=COLOURS["bg_main"])
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Something went wrong",
            font=("Helvetica", 20, "bold"),
            fg=COLOURS["accent_red"],
            bg=COLOURS["bg_main"],
        ).pack(pady=(80, 8))

        tk.Label(
            frame,
            text=f"Screen '{screen_name}' failed to load.\n{error}",
            font=("Helvetica", 12),
            fg=COLOURS["text_secondary"],
            bg=COLOURS["bg_main"],
            wraplength=500,
            justify="center",
        ).pack(pady=(0, 32))

        from gui.styles import make_button
        make_button(
            frame, "Go to Home", self.go_home, variant="primary"
        ).pack()

        self._current_screen = frame

    # -----------------------------------------------------------------------
    # Window close
    # -----------------------------------------------------------------------

    def _on_close(self) -> None:
        """Save progress and exit cleanly when the window is closed."""
        logger.info("Window closing — saving progress")
        self.tracker.save()
        self.root.destroy()