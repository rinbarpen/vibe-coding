import unittest

from vibe_tool.update import build_update_command, filter_managed_submodule_paths


class UpdateCommandTests(unittest.TestCase):
    def test_batch_update_excludes_unmanaged_submodules(self):
        paths = [
            "skills/ai-skills",
            "skills/agent-skills",
            "skills/ai-investment-advisor",
            "workflows/writing-agent",
        ]

        managed = filter_managed_submodule_paths(paths)

        self.assertEqual(
            managed,
            ["skills/ai-skills", "workflows/writing-agent"],
        )

    def test_update_command_contains_only_managed_paths(self):
        command = build_update_command(
            [
                "skills/agent-skills",
                "skills/anthropics",
                "skills/ai-investment-advisor",
            ]
        )

        self.assertEqual(
            command,
            [
                "git",
                "submodule",
                "update",
                "--remote",
                "--merge",
                "--",
                "skills/anthropics",
            ],
        )


if __name__ == "__main__":
    unittest.main()
