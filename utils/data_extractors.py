from collections import defaultdict
import re


# ✅ Move UNIT_MAP here
UNIT_MAP = {
    "minutes": 1,
    "minute": 1,
    "hours": 60,
    "hour": 60,
    "days": 1440,
    "day": 1440,
}


def extract_label_counts(issues, prefix="kind/"):
    label_count = defaultdict(int)
    for issue in issues:
        if isinstance(issue.get("labels"), list):
            for label in issue["labels"]:
                if isinstance(label, str) and label.startswith(prefix):
                    label_count[label] += 1
    return label_count


def extract_author_counts(issues, top_n=10):
    author_counts = defaultdict(int)
    for issue in issues:
        for event in issue.get("events", []):
            if isinstance(event, dict) and "author" in event and event["author"]:
                author_counts[event["author"]] += 1
    sorted_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_authors[:top_n])


def parse_time_to_minutes(time_str):
    match = re.search(r"(\d+)\s*(minutes?|hours?|days?)", time_str)
    if match:
        value, unit = int(match.group(1)), match.group(2).lower()
        return value * UNIT_MAP.get(unit, 1)
    return 0


def extract_minutes_from_issues(issues):
    return [parse_time_to_minutes(issue.get("time_to_close", "")) for issue in issues]


def bucket_values(values, ranges):
    counts = [0] * len(ranges)
    for v in values:
        for i, (start, end) in enumerate(ranges):
            if start <= v <= end:
                counts[i] += 1
                break
    return counts
