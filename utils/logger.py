# =============================================================================
# utils/logger.py
# Centralised logging for the Math Learning App.
#
# Why logging instead of print():
#   - With PyInstaller --windowed there is no console, so print() output
#     disappears silently. Logging writes to a file instead.
#   - Log file location: <data_dir>/app.log
#   - All modules import `logger` from here and call logger.info() / error()
# =============================================================================

import logging
import os


def setup_logger() -> logging.Logger:
    """
    Configure and return the root application logger.

    - Writes to <data_dir>/app.log  (always)
    - Also writes to the console    (development only, when not frozen)
    - Log level: DEBUG in development, INFO in packaged app

    Call this ONCE from main.py before importing any other app module.
    Returns the configured logger so main.py can hold a reference.
    """
    # Import here to avoid circular imports at module load time
    from utils.file_io import get_log_path
    import sys

    log_path = get_log_path()

    # Root logger for the entire app
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --- File handler (always active) ---
    try:
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except OSError as e:
        # If we can't open the log file, continue — don't crash the app
        print(f"Warning: could not open log file {log_path}: {e}")

    # --- Console handler (development only) ---
    if not getattr(sys, "frozen", False):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    return logging.getLogger("MathApp")


# Module-level logger for other modules that do:
#   from utils.logger import logger
# Note: this logger is only useful AFTER setup_logger() has been called
# from main.py. Importing before that will still work but output may not
# go to the file until handlers are attached.
logger = logging.getLogger("MathApp")