import unittest

from readme_arcade.github import counts_from_calendar


class CountsFromCalendarTests(unittest.TestCase):
    def test_empty_calendar_returns_zero_grid(self) -> None:
        counts, total = counts_from_calendar(None, width=3, height=2)

        self.assertEqual(counts, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(total, 0)

    def test_recent_weeks_are_right_aligned_and_height_is_bounded(self) -> None:
        calendar = {
            "totalContributions": 10,
            "weeks": [
                {"contributionDays": [{"contributionCount": 9}]},
                {
                    "contributionDays": [
                        {"contributionCount": 1},
                        {"contributionCount": 2},
                        {"contributionCount": 99},
                    ]
                },
                {
                    "contributionDays": [
                        {"contributionCount": 3},
                        {"contributionCount": 4},
                    ]
                },
            ],
        }

        counts, total = counts_from_calendar(calendar, width=2, height=2)

        self.assertEqual(counts, [[1, 3], [2, 4]])
        self.assertEqual(total, 10)

    def test_short_history_is_padded_on_the_left(self) -> None:
        calendar = {
            "totalContributions": 5,
            "weeks": [{"contributionDays": [{"contributionCount": 5}]}],
        }

        counts, _ = counts_from_calendar(calendar, width=3, height=1)

        self.assertEqual(counts, [[0, 0, 5]])


if __name__ == "__main__":
    unittest.main()
