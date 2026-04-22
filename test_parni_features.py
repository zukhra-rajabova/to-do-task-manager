import io
import importlib.util
import pathlib
import unittest
from contextlib import redirect_stdout

from add_categories import add_category
from list_tasks import list_all_tasks
from search_tasks import search_tasks_by_keyword


def _load_legacy_list_function():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    legacy_path = repo_root / "to-do-task-manager-main-2" / "list-all-tasks.py"
    if not legacy_path.exists():
        return None

    spec = importlib.util.spec_from_file_location("legacy_list_module", legacy_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except (SyntaxError, ImportError):
        return None
    return getattr(module, "list_all_tasks", None)


class TestParniListAllTasks(unittest.TestCase):
    def test_l1_empty_list(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = list_all_tasks([])
        self.assertEqual(result, [])
        self.assertIn("No tasks yet.", buf.getvalue())

    def test_l2_single_complete_task(self):
        tasks = [{"id": 1, "title": "Read", "description": "Ch.2", "status": "pending"}]
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = list_all_tasks(tasks)
        output = buf.getvalue()
        self.assertIs(result, tasks)
        self.assertIn("ID: 1", output)
        self.assertIn("Title: Read", output)
        self.assertIn("Description: Ch.2", output)
        self.assertIn("Status: pending", output)

    def test_l3_multiple_tasks_count_and_separator(self):
        tasks = [
            {"id": 1, "title": "A", "description": "d1", "status": "pending"},
            {"id": 2, "title": "B", "description": "d2", "status": "done"},
        ]
        buf = io.StringIO()
        with redirect_stdout(buf):
            list_all_tasks(tasks)
        output = buf.getvalue()
        self.assertIn("Tasks (2 total)", output)
        self.assertGreaterEqual(output.count("----------------------------------------"), 2)

    def test_l4_optional_fields_visible(self):
        tasks = [
            {
                "id": 7,
                "title": "Task",
                "description": "Desc",
                "status": "in_progress",
                "priority": "high",
                "due_date": "2026-04-22",
                "category": "school",
            }
        ]
        buf = io.StringIO()
        with redirect_stdout(buf):
            list_all_tasks(tasks)
        output = buf.getvalue()
        self.assertIn("Priority: high", output)
        self.assertIn("Due date: 2026-04-22", output)
        self.assertIn("Category: school", output)

    def test_l5_categories_list_visible(self):
        tasks = [
            {
                "id": 1,
                "title": "Task",
                "description": "Desc",
                "status": "pending",
                "categories": ["school", "urgent"],
            }
        ]
        buf = io.StringIO()
        with redirect_stdout(buf):
            list_all_tasks(tasks)
        self.assertIn("Categories: school, urgent", buf.getvalue())

    def test_l6_missing_key_robustness(self):
        tasks = [{"id": 3, "description": "Only desc", "status": "pending"}]
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = list_all_tasks(tasks)
        self.assertIs(result, tasks)
        self.assertIn("ID: 3", buf.getvalue())

    def test_l7_none_tasks_behaves_like_empty(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = list_all_tasks(None)
        self.assertIsNone(result)
        self.assertIn("No tasks yet.", buf.getvalue())

    def test_legacy_list_file_matches_core_behavior(self):
        legacy_fn = _load_legacy_list_function()
        if legacy_fn is None:
            self.skipTest("Legacy list file not found")
        tasks = [{"id": 1, "title": "Read", "description": "Ch.2", "status": "pending"}]
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = legacy_fn(tasks)
        output = buf.getvalue()
        self.assertIs(result, tasks)
        self.assertIn("ID: 1", output)
        self.assertIn("Title: Read", output)


class TestParniAddCategories(unittest.TestCase):
    def test_c1_add_first_category(self):
        task = {"id": 1}
        result = add_category(task, "school")
        self.assertIs(result, task)
        self.assertEqual(task["categories"], ["school"])

    def test_c2_add_second_distinct_category(self):
        task = {"id": 1, "categories": ["school"]}
        add_category(task, "urgent")
        self.assertEqual(task["categories"], ["school", "urgent"])

    def test_c3_duplicate_prevention(self):
        task = {"id": 1, "categories": ["school"]}
        add_category(task, "school")
        self.assertEqual(task["categories"], ["school"])

    def test_c4_whitespace_normalization(self):
        task = {"id": 1}
        add_category(task, "  school  ")
        self.assertEqual(task["categories"], ["school"])

    def test_c5_blank_category_rejection(self):
        task = {"id": 1, "categories": ["school"]}
        before = list(task["categories"])
        result_empty = add_category(task, "")
        result_spaces = add_category(task, "   ")
        self.assertIs(result_empty, task)
        self.assertIs(result_spaces, task)
        self.assertEqual(task["categories"], before)

    def test_c6_non_list_legacy_categories_value(self):
        task = {"id": 1, "categories": "old"}
        add_category(task, "new")
        self.assertEqual(task["categories"], ["old", "new"])

    def test_c7_invalid_task_object_raises(self):
        with self.assertRaises(TypeError):
            add_category(None, "school")


class TestParniSearchByKeyword(unittest.TestCase):
    def test_s1_match_by_title(self):
        tasks = [{"id": 1, "title": "Math Exam", "description": "", "status": "pending"}]
        result = search_tasks_by_keyword(tasks, "exam")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)

    def test_s2_match_by_description(self):
        tasks = [{"id": 1, "title": "Task", "description": "chapter 2", "status": "pending"}]
        result = search_tasks_by_keyword(tasks, "chapter")
        self.assertEqual(len(result), 1)

    def test_s3_match_by_status(self):
        tasks = [
            {"id": 1, "title": "A", "description": "", "status": "pending"},
            {"id": 2, "title": "B", "description": "", "status": "done"},
        ]
        result = search_tasks_by_keyword(tasks, "pending")
        self.assertEqual([t["id"] for t in result], [1])

    def test_s4_match_by_category_field(self):
        tasks = [{"id": 1, "title": "A", "description": "", "status": "pending", "category": "school"}]
        result = search_tasks_by_keyword(tasks, "school")
        self.assertEqual(len(result), 1)

    def test_s5_match_by_categories_list(self):
        tasks = [{"id": 1, "title": "A", "description": "", "status": "pending", "categories": ["group", "urgent"]}]
        result = search_tasks_by_keyword(tasks, "urgent")
        self.assertEqual(len(result), 1)

    def test_s6_case_insensitive(self):
        tasks = [{"id": 1, "title": "A", "description": "", "status": "pending", "categories": ["school"]}]
        result = search_tasks_by_keyword(tasks, "SCHOOL")
        self.assertEqual(len(result), 1)

    def test_s7_no_results(self):
        tasks = [{"id": 1, "title": "A", "description": "", "status": "pending"}]
        result = search_tasks_by_keyword(tasks, "zzz")
        self.assertEqual(result, [])

    def test_s8_blank_keyword_validation(self):
        tasks = [{"id": 1, "title": "A", "description": "", "status": "pending"}]
        self.assertEqual(search_tasks_by_keyword(tasks, ""), [])
        self.assertEqual(search_tasks_by_keyword(tasks, "   "), [])

    def test_s9_invalid_tasks_object_raises(self):
        with self.assertRaises(TypeError):
            search_tasks_by_keyword(None, "a")


if __name__ == "__main__":
    unittest.main()
