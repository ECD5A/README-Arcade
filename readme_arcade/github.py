"""GitHub contribution calendar helpers."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request


QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""


def fetch_calendar(login: str, token: str | None) -> dict | None:
    if not token:
        return None

    payload = json.dumps({"query": QUERY, "variables": {"login": login}}).encode("utf-8")
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "readme-arcade",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"warning: GitHub API unavailable, using deterministic seed: {exc}", file=sys.stderr)
        return None

    if data.get("errors"):
        print(f"warning: GitHub API returned errors: {data['errors']}", file=sys.stderr)
        return None

    user = data.get("data", {}).get("user")
    if not user:
        print(f"warning: GitHub user {login!r} was not found, using deterministic seed", file=sys.stderr)
        return None

    return user["contributionsCollection"]["contributionCalendar"]


def counts_from_calendar(calendar: dict | None, width: int, height: int) -> tuple[list[list[int]], int]:
    counts = [[0 for _ in range(width)] for _ in range(height)]
    total = 0

    if not calendar:
        return counts, total

    total = int(calendar.get("totalContributions") or 0)
    weeks = calendar.get("weeks", [])[-width:]
    x_offset = width - len(weeks)
    for x, week in enumerate(weeks, start=x_offset):
        days = week.get("contributionDays", [])[:height]
        for y, day in enumerate(days):
            counts[y][x] = int(day.get("contributionCount") or 0)

    return counts, total
