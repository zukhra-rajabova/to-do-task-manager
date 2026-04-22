import unittest
from add_task import add_task, Task


class TestAddTask(unittest.TestCase):

    def test_add_task_basic(self):
        tasks = []
        task, next_id = add_task(tasks, 1, "Study", "Math revision", "High", "2026-04-20")

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Study")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(next_id, 2)

    def test_add_second_task(self):
        tasks = []
        task1, next_id = add_task(tasks, 1, "Task1", "Desc", "High", "2026-04-20")
        task2, next_id = add_task(tasks, next_id, "Task2", "Desc", "Low", "2026-04-21")

        self.assertEqual(task2.id, 2)
        self.assertEqual(len(tasks), 2)
        self.assertEqual(next_id, 3)

    def test_priority_low(self):
        tasks = []
        task, _ = add_task(tasks, 1, "Task", "Desc", "Low", "2026-04-20")

        self.assertEqual(task.priority, "Low")

    def test_empty_description(self):
        tasks = []
        task, _ = add_task(tasks, 1, "Task", "", "High", "2026-04-20")

        self.assertEqual(task.description, "")

    def test_empty_title(self):
        tasks = []
        task, _ = add_task(tasks, 1, "", "Desc", "High", "2026-04-20")

        self.assertEqual(task.title, "")

    def test_long_title(self):
        tasks = []
        long_title = "A" * 1000

        task, _ = add_task(tasks, 1, long_title, "Desc", "High", "2026-04-20")

        self.assertEqual(task.title, long_title)

    def test_past_due_date(self):
        tasks = []
        task, _ = add_task(tasks, 1, "Task", "Desc", "High", "1900-01-01")

        self.assertEqual(task.due_date, "1900-01-01")

    def test_large_next_id(self):
        tasks = []
        task, next_id = add_task(tasks, 999999, "Task", "Desc", "High", "2026-04-20")

        self.assertEqual(task.id, 999999)
        self.assertEqual(next_id, 1000000)

    def test_title_none(self):
        with self.assertRaises(TypeError):
            add_task([], 1, None, "Desc", "High", "2026-04-20")

    def test_task_list_none(self):
        with self.assertRaises(AttributeError):
            add_task(None, 1, "Task", "Desc", "High", "2026-04-20")

    def test_next_id_string(self):
        with self.assertRaises(TypeError):
            add_task([], "one", "Task", "Desc", "High", "2026-04-20")

    def test_missing_arguments(self):
        with self.assertRaises(TypeError):
            add_task([])  # missing parameters

if __name__ == "__main__":
    unittest.main()