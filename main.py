# =============================================================================
# main.py
# Application entry point for the Math Learning App.
# =============================================================================

import multiprocessing
multiprocessing.freeze_support()

# --- Logging first -----------------------------------------------------------
from utils.logger import setup_logger
log = setup_logger()
log.info("=" * 60)
log.info("Math Learning App starting up")

# --- Initialise save data ----------------------------------------------------
from utils.file_io import (
    initialise_progress_if_missing,
    initialise_session_log_if_missing,
)
initialise_progress_if_missing()
initialise_session_log_if_missing()

# --- Launch GUI --------------------------------------------------------------
import tkinter as tk
from gui.app_root import AppRoot


def main():
    root = tk.Tk()
    AppRoot(root)
    log.info("Entering main loop")
    root.mainloop()
    log.info("App exited cleanly")


if __name__ == "__main__":
    main()