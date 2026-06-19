# =============================================================================
# main.py
# Application entry point for the Math Learning App.
#
# Startup sequence:
#   1. Set up logging (before any other import that might log)
#   2. Initialise save-data files if this is the first launch
#   3. Create the Tk root window
#   4. Launch the GUI (app_root handles all screen management)
# =============================================================================

import sys
import multiprocessing

# PyInstaller + multiprocessing safety (no-op on macOS but required for Windows)
multiprocessing.freeze_support()

# --- Logging must be configured before any other app module is imported ------
from utils.logger import setup_logger
log = setup_logger()
log.info("=" * 60)
log.info("Math Learning App starting up")

# --- Initialise save-data files on first launch ------------------------------
from utils.file_io import (
    initialise_progress_if_missing,
    initialise_session_log_if_missing,
)
initialise_progress_if_missing()
initialise_session_log_if_missing()

# --- Launch the GUI ----------------------------------------------------------
import tkinter as tk
from config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT

def main():
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

    # Centre the window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth()  - WINDOW_WIDTH)  // 2
    y = (root.winfo_screenheight() - WINDOW_HEIGHT) // 2
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    # TODO: Replace this placeholder with app_root.AppRoot(root) once built
    # -------------------------------------------------------------------------
    placeholder = tk.Label(
        root,
        text="Math Learning App\n\nFoundation files loaded successfully.\nGUI coming next.",
        font=("Helvetica", 18),
        fg="#2C3E50",
        bg="#F5F5F0",
        justify="center",
    )
    placeholder.pack(expand=True)
    root.configure(bg="#F5F5F0")
    # -------------------------------------------------------------------------

    log.info("Tkinter root window created — entering main loop")
    root.mainloop()
    log.info("App exited cleanly")


if __name__ == "__main__":
    main()