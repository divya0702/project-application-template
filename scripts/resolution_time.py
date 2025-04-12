# Import system modules to dynamically adjust the Python import path
import sys
import os

# Add the project root directory to the system path
# This enables importing shared utility modules located in the parent folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import custom utility functions
from utils.json_utils import load_json  # Function to load JSON data from ./data/
from utils.plot_utils import bar_chart  # Reusable function for generating bar charts
from utils.logging_utils import logger

logger.info("Loaded JSON successfully")

# Import regular expressions module
import re

# Load issue data from 'closed_issues.json' located in the data folder
issues = load_json("closed_issues.json")

# Initialize a dictionary to count issues falling into specific resolution time categories
time_range_count = {"Less than 7 days": 0, "8 to 60 days": 0, "More than 60 days": 0}

# Define a regular expression pattern to extract the number of days from 'time_to_close' field
days_pattern = re.compile(r"(\d+)\s+days?")

# Loop through all issues to classify each based on how long it took to close
for issue in issues:
    time_to_close = issue.get(
        "time_to_close", ""
    )  # Get the resolution time string (e.g., "14 days")
    days_match = days_pattern.search(
        time_to_close
    )  # Extract number of days using regex
    days = int(days_match.group(1)) if days_match else 0  # Default to 0 if not found

    # Categorize the issue based on resolution time
    if days < 7:
        time_range_count["Less than 7 days"] += 1
    elif 8 <= days <= 60:
        time_range_count["8 to 60 days"] += 1
    elif days > 60:
        time_range_count["More than 60 days"] += 1

# Generate a bar chart using the categorized resolution time data
bar_chart(
    labels=list(time_range_count.keys()),  # X-axis: resolution time categories
    counts=list(time_range_count.values()),  # Y-axis: count of issues per category
    xlabel="Resolution Time (in Days)",  # Label for X-axis
    ylabel="Number of Issues",  # Label for Y-axis
    title="Number of Issues Based on Time to Close",  # Chart title
    color="lightcoral",  # Bar color
)
