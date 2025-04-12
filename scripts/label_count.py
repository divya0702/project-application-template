# Import system modules to adjust the import path
import sys
import os

# Add the project root directory to the Python path
# This allows importing utility modules from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import standard and custom libraries
from collections import defaultdict
from utils.json_utils import load_json  # Custom utility to load JSON files from ./data/
from utils.plot_utils import bar_chart  # Reusable bar chart function
from utils.logging_utils import logger

logger.info("Loaded JSON successfully")

# Load issue data from 'poetry.json'
issues = load_json("poetry.json")

# Dictionary to count the number of issues for each label
label_count = defaultdict(int)

# Loop through each issue and extract labels
for issue in issues:
    # Ensure the 'labels' field is a list
    if isinstance(issue.get("labels"), list):
        for label in issue["labels"]:
            # We're interested only in string labels starting with "kind/"
            if isinstance(label, str) and label.startswith("kind/"):
                label_count[label] += 1

# Generate a bar chart using the label frequency data
bar_chart(
    list(label_count.keys()),  # X-axis: label names
    list(label_count.values()),  # Y-axis: count of each label
    "Label Name",  # X-axis label
    "Number of Issues",  # Y-axis label
    "Number of Issues for Each Label Type Starting with 'kind/'",  # Chart title
)
