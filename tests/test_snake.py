import unittest

from readme_arcade.modes.snake import choose_step, motion_key


class MotionKeyTests(unittest.TestCase):
    def test_same_daily_seed_is_reproducible(self) -> None:
        self.assertEqual(
            motion_key("octocat", "2026-07-26"),
            motion_key("octocat", "2026-07-26"),
        )

    def test_daily_seed_changes_route_key(self) -> None:
        self.assertNotEqual(
            motion_key("octocat", "2026-07-26"),
            motion_key("octocat", "2026-07-27"),
        )


class ActorSeparationTests(unittest.TestCase):
    def test_actor_avoids_step_too_close_to_other_actor(self) -> None:
        body = [(2, 2), (1, 2), (0, 2)]
        other_actor = {(4, 2)}

        next_head = choose_step(
            user="octocat:route:2026-07-26",
            frame=1,
            actor="snake",
            head=body[0],
            target=(3, 2),
            body=body,
            width=7,
            height=5,
            food={(3, 2): 1},
            theme_name="dark",
            blocked=other_actor,
            min_actor_distance=3,
        )

        self.assertNotEqual(next_head, (3, 2))
        self.assertGreaterEqual(
            min(abs(next_head[0] - x) + abs(next_head[1] - y) for x, y in other_actor),
            3,
        )


if __name__ == "__main__":
    unittest.main()
