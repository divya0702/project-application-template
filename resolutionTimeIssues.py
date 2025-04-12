import json
import matplotlib.pyplot as plt
from collections import defaultdict
import re

# Load JSON data from 'closed_issues.json'
with open("closed_issues.json", "r") as file:
    issues = json.load(file)

# Initialize counters for each time_to_close range
time_range_count = {
    "Less than 7 days": 0,
    "8 to 60 days": 0,
    "More than 60 days": 0
}

# Regular expression to extract days from 'time_to_close' field
days_pattern = re.compile(r"(\d+)\s+days?")

# Iterate through the issues to categorize them based on 'time_to_close'
for issue in issues:
    time_to_close = issue.get("time_to_close", "")
    
    # Extract the number of days from the 'time_to_close' field
    days_match = days_pattern.search(time_to_close)
    if days_match:
        days = int(days_match.group(1))
    else:
        days = 0  # Handle cases where 'time_to_close' is less than 1 day or does not have "days"

    # Categorize based on the number of days
    if days < 7:
        time_range_count["Less than 7 days"] += 1
    elif 8 <= days <= 60:
        time_range_count["8 to 60 days"] += 1
    elif days > 60:
        time_range_count["More than 60 days"] += 1

# Prepare data for the bar chart
categories = list(time_range_count.keys())
counts = list(time_range_count.values())

# Create a bar plot
plt.figure(figsize=(10, 6))
plt.bar(categories, counts, color='lightcoral')

# Add labels and title
plt.xlabel("Resolution Time (in Days)")
plt.ylabel("Number of Issues")
plt.title("Number of Issues Based on Time to Close")

# Display the graph
plt.tight_layout()  # Adjust layout to prevent label cut-off
plt.show()
