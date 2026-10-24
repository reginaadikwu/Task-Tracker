
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import task_cli


class TaskTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tasks_file = Path(self.temp_dir.name) / "tasks.json"
        self.file_patcher = patch.object(task_cli, "TASKS_FILE", self.tasks_file)
        self.file_patcher.start()

    def tearDown(self):
        self.file_patcher.stop()
        self.temp_dir.cleanup()

    def test_add_task(self):
        task = task_cli.add_task("Learn Python")

        self.assertEqual(task["id"], 1)
        self.assertEqual(task["description"], "Learn Python")
        self.assertEqual(task["status"], "todo")

    def test_empty_description_is_rejected(self):
        with self.assertRaises(ValueError):
            task_cli.add_task("   ")

    def test_update_task(self):
        task = task_cli.add_task("Old description")

        result = task_cli.update_task(task["id"], "New description")

        self.assertTrue(result)
        self.assertEqual(
            task_cli.list_tasks()[0]["description"],
            "New description",
        )

    def test_delete_task(self):
        task = task_cli.add_task("Temporary task")

        result = task_cli.delete_task(task["id"])

        self.assertTrue(result)
        self.assertEqual(task_cli.list_tasks(), [])

    def test_mark_task_done(self):
        task = task_cli.add_task("Finish homework")

        result = task_cli.mark_task(task["id"], "done")

        self.assertTrue(result)
        self.assertEqual(task_cli.list_tasks()[0]["status"], "done")

    def test_missing_task_returns_false(self):
        self.assertFalse(task_cli.update_task(999, "Missing"))
        self.assertFalse(task_cli.delete_task(999))
        self.assertFalse(task_cli.mark_task(999, "done"))

    def test_list_filters_by_status(self):
        task_cli.add_task("First task")
        second = task_cli.add_task("Second task")
        task_cli.mark_task(second["id"], "in-progress")

        tasks = task_cli.list_tasks("in-progress")

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "Second task")

    def test_tasks_are_saved_as_json(self):
        task_cli.add_task("Saved task")

        with self.tasks_file.open("r", encoding="utf-8") as file:
            saved_tasks = json.load(file)

        self.assertEqual(saved_tasks[0]["description"], "Saved task")


if __name__ == "__main__":
    unittest.main()
