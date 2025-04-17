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
    author_counts = defaultdict(int)

    # Count how often each author appears in events
    for issue in issues:
        for event in issue.get("events", []):
            if isinstance(event, dict) and "author" in event and event["author"]:
                author_counts[event["author"]] += 1

    # Top 10 authors by participation
    top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    authors, counts = zip(*top_authors) if top_authors else ([], [])

    # Plot bar chart
    bar_chart(
        authors,
        counts,
        "Authors",
        "Participation Time",
        "Active Author",
        color="green",
    )
