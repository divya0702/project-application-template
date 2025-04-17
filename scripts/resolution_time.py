import tkinter as tk
from utils.json_utils import load_json
from gui.flexible_bucket_gui import FlexibleXUnitApp
from utils.logging_utils import logger


def run():
    """
    Launches a Tkinter-based GUI to visualize issue resolution times
    using customizable time buckets.
    """
    logger.info("Launching Resolution Time GUI...")

    try:
        issues = load_json("closed_issues.json")
        logger.info(f"Loaded {len(issues)} issues from closed_issues.json")
    except Exception as e:
        logger.error(f"Failed to load JSON data: {e}")
        return

    # Start the interactive bucket-based visualization
    root = tk.Tk()
    app = FlexibleXUnitApp(root, issues)
    root.mainloop()


if __name__ == "__main__":
    run()
