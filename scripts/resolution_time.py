import json
import matplotlib.pyplot as plt
from collections import defaultdict
import re
import os
import sys

# Adjust path if needed (e.g., if using utils or configs)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class Feature1TimeToClose:
    def run(self):
        # Load JSON data
        with open("data/poetry.json", "r") as file:
            issues = json.load(file)

        time_range_count = {
            "Less than 7 days": 0,
            "8 to 60 days": 0,
            "More than 60 days": 0
        }

        days_pattern = re.compile(r"(\\d+)\\s+days?")

        for issue in issues:
            time_to_close = issue.get("time_to_close", "")
            days_match = days_pattern.search(time_to_close)
            days = int(days_match.group(1)) if days_match else 0

            if days < 7:
                time_range_count["Less than 7 days"] += 1
            elif 8 <= days <= 60:
                time_range_count["8 to 60 days"] += 1
            elif days > 60:
                time_range_count["More than 60 days"] += 1

        categories = list(time_range_count.keys())
        counts = list(time_range_count.values())

        plt.figure(figsize=(10, 6))
        plt.bar(categories, counts, color='lightcoral')
        plt.xlabel("Resolution Time (in Days)")
        plt.ylabel("Number of Issues")
        plt.title("Number of Issues Based on Time to Close")
        plt.tight_layout()
        plt.show()

# ✅ Function required by run.py to call this as feature 2
def run():
    Feature1TimeToClose().run()
