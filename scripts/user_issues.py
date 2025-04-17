import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.json_utils import load_json
from utils.plot_utils import bar_chart
from utils.logging_utils import logger


def run():
    """
    Analyze author activity from poetry.json and plot top 10 authors
    by number of event contributions.
    """
    logger.info("Starting Author Activity Analysis...")

    try:
        issues = load_json("poetry.json")
        logger.info(f"Loaded {len(issues)} issues from poetry.json")
    except Exception as e:
        logger.error(f"Error loading JSON: {e}")
        return

    author_counts = defaultdict(int)

    for issue in issues:
        for event in issue.get("events", []):
            if isinstance(event, dict) and "author" in event and event["author"]:
                author_counts[event["author"]] += 1

    if not author_counts:
        logger.warning("No author events found in the dataset.")
        return

    top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    authors, counts = zip(*top_authors) if top_authors else ([], [])

    logger.info(f"Top 10 authors extracted. Rendering chart...")

    bar_chart(
        authors,
        counts,
        "Authors",
        "Participation Time",
        "Active Author",
        color="green",
    )
