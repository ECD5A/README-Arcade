import json
import tempfile
import unittest
from pathlib import Path

from readme_arcade.config import DEFAULT_CONFIG, load_config, output_base_name


class LoadConfigTests(unittest.TestCase):
    def write_config(self, directory: str, data: object) -> Path:
        path = Path(directory) / "config.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_missing_file_returns_independent_defaults(self) -> None:
        first = load_config(Path("missing-config.json"))
        first["lifegrid"]["width"] = 1

        second = load_config(Path("missing-config.json"))

        self.assertEqual(second["lifegrid"]["width"], DEFAULT_CONFIG["lifegrid"]["width"])

    def test_nested_override_preserves_other_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_config(directory, {"lifegrid": {"width": 40}})

            config = load_config(path)

        self.assertEqual(config["lifegrid"]["width"], 40)
        self.assertEqual(config["lifegrid"]["height"], DEFAULT_CONFIG["lifegrid"]["height"])

    def test_explicit_duration_wins_over_speed_preset(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_config(
                directory,
                {"speed": "turbo", "snake": {"duration": "12s"}},
            )

            config = load_config(path)

        self.assertEqual(config["snake"]["duration"], "12s")
        self.assertEqual(config["matrix"]["duration"], "22s")

    def test_unknown_speed_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_config(directory, {"speed": "warp"})

            with self.assertRaisesRegex(ValueError, "unknown speed"):
                load_config(path)

    def test_top_level_json_value_must_be_an_object(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_config(directory, ["snake"])

            with self.assertRaisesRegex(ValueError, "must contain a JSON object"):
                load_config(path)


class OutputBaseNameTests(unittest.TestCase):
    def test_accepts_portable_filename_stems(self) -> None:
        config = {"output": {"baseName": "profile_arcade-v2.1"}}

        self.assertEqual(output_base_name(config), "profile_arcade-v2.1")

    def test_rejects_parent_directory_traversal(self) -> None:
        config = {"output": {"baseName": "../profile"}}

        with self.assertRaisesRegex(ValueError, "output.baseName"):
            output_base_name(config)

    def test_rejects_path_separators(self) -> None:
        for value in ("nested/profile", r"nested\profile"):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "output.baseName"):
                    output_base_name({"output": {"baseName": value}})

    def test_rejects_empty_and_overlong_names(self) -> None:
        for value in ("", "a" * 129):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "output.baseName"):
                    output_base_name({"output": {"baseName": value}})


if __name__ == "__main__":
    unittest.main()
