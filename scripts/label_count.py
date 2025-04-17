import sys
import os
from collections import defaultdict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.json_utils import load_json
from utils.plot_utils import bar_chart
from utils.logging_utils import logger

def run():
    logger.info("Loaded JSON successfully")

    # Load issues from poetry.json
    issues = load_json("poetry.json")
    label_count = defaultdict(int)

    # Count labels starting with "kind/"
    for issue in issues:
        if isinstance(issue.get("labels"), list):
            for label in issue["labels"]:
                if isinstance(label, str) and label.startswith("kind/"):
                    label_count[label] += 1

    # Plot bar chart
    bar_chart(
        list(label_count.keys()),
        list(label_count.values()),
        "Label Name",
        "Number of Issues",
        "Number of Issues for Each Label Type Starting with 'kind/'",
    )
