# Import standard libraries for system and path manipulation
import sys
import os

# Add the project root directory to the Python path so we can import from 'utils'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import required modules
from collections import defaultdict
from utils.json_utils import load_json  # Custom function to load JSON data from ./data/
from utils.plot_utils import bar_chart  # Custom function to create a reusable bar chart
from utils.logging_utils import logger

logger.info("Loaded JSON successfully")

# Load issue data from poetry.json
issues = load_json("poetry.json")

# Dictionary to count how many times each author appears in events
author_counts = defaultdict(int)

# Iterate over each issue and its events to count authors
for issue in issues:
    for event in issue.get("events", []):  # Use .get with default empty list for safety
        if isinstance(event, dict) and "author" in event and event["author"]:
            author_counts[event["author"]] += 1

# Get the top 10 most active authors based on participation count
top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:10]

# Unzip into separate lists for plotting
authors, counts = zip(*top_authors)

# Create a bar chart of the top 10 active authors
bar_chart(
    authors,
    counts,
    "Authors",  # X-axis label
    "Participation Time",  # Y-axis label
    "Active Author",  # Chart title
    color="green",  # Bar color
)
