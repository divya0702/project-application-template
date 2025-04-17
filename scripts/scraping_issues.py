import asyncio
import aiohttp
import json

# GitHub repository and API setup
GITHUB_TOKEN = "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"
REPO = "python-poetry/poetry"
ISSUES_API_URL = f"https://api.github.com/repos/{REPO}/issues"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Fetch all issues asynchronously
async def fetch_issues(session):
    issues = []
    page = 1
    while True:
        url = f"{ISSUES_API_URL}?state=all&per_page=100&page={page}"
        async with session.get(url, headers=HEADERS) as response:
            if response.status == 200:
                data = await response.json()
                if not data:
                    break
                issues.extend(data)
                page += 1
            else:
                print(f"❌ Failed to fetch issues: {response.status}, {await response.text()}")
                break
    return issues

# Fetch issue events asynchronously
async def fetch_issue_events(session, issue):
    events = []
    if "events_url" in issue:
        async with session.get(issue["events_url"], headers=HEADERS) as response:
            if response.status == 200:
                events = await response.json()
            else:
                print(f"❌ Failed to fetch events for issue {issue['number']}: {response.status}")
    

    body_text = issue.get("body", "")
    # Only call replace if body_text is not None
    if body_text is not None:
        body_text = body_text.replace("\r", "")
    else:
        body_text = ""
    # Format the issue with the new structure
    formatted_issue = {
        "url": issue.get("html_url"),
        "creator": issue.get("user", {}).get("login"),
        "labels": [label["name"] for label in issue.get("labels", [])],
        "state": issue.get("state"),
        "assignees": [assignee["login"] for assignee in issue.get("assignees", [])],
        "title": issue.get("title"),
        "text": body_text,
        "number": issue.get("number"),
        "created_date": issue.get("created_at"),
        "updated_date": issue.get("updated_at"),
        "timeline_url": f"https://api.github.com/repos/python-poetry/poetry/issues/{issue.get('number')}/timeline",
        "events": [
            {
                "event_type": event.get("event"),
                "author": (event.get("actor") or {}).get("login", "Unknown"),
                "event_date": event.get("created_at", ""),
                "comment": event.get("body", "") if event.get("event") == "commented" else ""
            } for event in events
        ]
    }
    
    return formatted_issue

# Main function to fetch all issues with events concurrently
async def fetch_issues_with_events():
    async with aiohttp.ClientSession() as session:
        issues = await fetch_issues(session)

        # Fetch events concurrently for all issues
        tasks = [fetch_issue_events(session, issue) for issue in issues]
        formatted_issues = await asyncio.gather(*tasks)

    return formatted_issues

# Save data to a JSON file
def save_issues_to_file(filename="test_issues.json"):
    issues_data = asyncio.run(fetch_issues_with_events())
    with open(filename, "w") as json_file:
        json.dump(issues_data, json_file, indent=4)
    print(f"✅ Issues with events saved to {filename}")

# Run the function
if __name__ == "__main__":
    save_issues_to_file()