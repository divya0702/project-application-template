import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.json_utils import load_json
from utils.plot_utils import bar_chart
from utils.logging_utils import logger


def run():
    """
    Analyze labels from issues in poetry.json and display a bar chart
    showing the count of labels starting with "kind/".
    """
    logger.info("Starting Label Count Analysis...")

    try:
        issues = load_json("poetry.json")
        logger.info(f"Loaded {len(issues)} issues from poetry.json")
    except Exception as e:
        logger.error(f"Error loading JSON: {e}")
        return

    label_count = defaultdict(int)

    for issue in issues:
        if isinstance(issue.get("labels"), list):
            for label in issue["labels"]:
                if isinstance(label, str) and label.startswith("kind/"):
                    label_count[label] += 1

    if not label_count:
        logger.warning("No labels starting with 'kind/' were found.")
    else:
        logger.info(f"Found {len(label_count)} unique 'kind/' labels.")

    bar_chart(
        list(label_count.keys()),
        list(label_count.values()),
        "Label Name",
        "Number of Issues",
        "Number of Issues for Each Label Type Starting with 'kind/'",
    )
