import unittest


def edit_task(tasks, task_id, title=None, description=None, status=None):
    for task in tasks:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title
            if description is not None:
                task["description"] = description
            if status is not None:
                task["status"] = status
            return task
    return None


def filter_tasks_by_priority(tasks, priority):
    return [task for task in tasks if task["priority"] == priority]


def filter_tasks_by_status(tasks, status):
    valid_statuses = ["pending", "in_progress", "completed"]
    if status not in valid_statuses:
        print(f"Invalid status. Choose from: {valid_statuses}")
        return []
    return [task for task in tasks if task["status"] == status]


class TestEditTask(unittest.TestCase):

    def test_tc1_update_title_only(self):
        tasks = [{"id": 1, "title": "Task1", "description": "Desc1", "status": "pending"}]
        result = edit_task(tasks, 1, title="Updated Task1")
        self.assertEqual(result["title"], "Updated Task1")
        self.assertEqual(result["description"], "Desc1")
        self.assertEqual(result["status"], "pending")

    def test_tc2_update_description_only(self):
        tasks = [{"id": 1, "title": "Task1", "description": "Old Desc", "status": "pending"}]
        result = edit_task(tasks, 1, description="New Desc")
        self.assertEqual(result["description"], "New Desc")
        self.assertEqual(result["title"], "Task1")
        self.assertEqual(result["status"], "pending")

    def test_tc3_update_status_to_done(self):
        tasks = [{"id": 1, "title": "Task1", "description": "Desc1", "status": "pending"}]
        result = edit_task(tasks, 1, status="done")
        self.assertEqual(result["status"], "done")

    def test_tc4_update_all_fields(self):
        tasks = [{"id": 1, "title": "Old", "description": "Old Desc", "status": "pending"}]
        result = edit_task(tasks, 1, title="New Title", description="New Desc", status="done")
        self.assertEqual(result["title"], "New Title")
        self.assertEqual(result["description"], "New Desc")
        self.assertEqual(result["status"], "done")

    def test_tc5_multiple_tasks_update_one(self):
        tasks = [
            {"id": 1, "title": "Task1", "description": "D1", "status": "pending"},
            {"id": 2, "title": "Task2", "description": "D2", "status": "pending"},
        ]
        result = edit_task(tasks, 2, title="Updated Task2")
        self.assertEqual(result["title"], "Updated Task2")
        self.assertEqual(tasks[0]["title"], "Task1")

    def test_tc6_no_optional_args_task_unchanged(self):
        tasks = [{"id": 1, "title": "Task1", "description": "Desc1", "status": "pending"}]
        result = edit_task(tasks, 1)
        self.assertEqual(result, {"id": 1, "title": "Task1", "description": "Desc1", "status": "pending"})

    def test_ec1_empty_task_list(self):
        result = edit_task([], 1, title="X")
        self.assertIsNone(result)

    def test_ec2_nonexistent_task_id(self):
        tasks = [{"id": 1, "title": "Task1", "description": "D", "status": "pending"}]
        result = edit_task(tasks, 999, title="X")
        self.assertIsNone(result)

    def test_ec3_very_large_task_id(self):
        tasks = [{"id": 1, "title": "Task1", "description": "D", "status": "pending"}]
        result = edit_task(tasks, 10 ** 18, title="X")
        self.assertIsNone(result)

    def test_ec4_empty_string_values(self):
        tasks = [{"id": 1, "title": "Task1", "description": "Desc1", "status": "pending"}]
        result = edit_task(tasks, 1, title="", description="", status="")
        self.assertEqual(result["title"], "")
        self.assertEqual(result["description"], "")
        self.assertEqual(result["status"], "")

    def test_ec5_invalid_status_value_updated_anyway(self):
        tasks = [{"id": 1, "title": "Task1", "description": "Desc1", "status": "pending"}]
        result = edit_task(tasks, 1, status="flying")
        self.assertEqual(result["status"], "flying")

    def test_eh1_tasks_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            edit_task(None, 1, title="X")

    def test_eh2_task_id_as_string_returns_none(self):
        tasks = [{"id": 1, "title": "Task1", "description": "D", "status": "pending"}]
        result = edit_task(tasks, "1", title="X")
        self.assertIsNone(result)

    def test_eh3_missing_id_key_raises_key_error(self):
        tasks = [{"title": "Task1", "description": "D", "status": "pending"}]
        with self.assertRaises(KeyError):
            edit_task(tasks, 1, title="X")

    def test_eh4_non_dict_task_raises_type_error(self):
        tasks = ["not_a_dict"]
        with self.assertRaises(TypeError):
            edit_task(tasks, 1, title="X")

    def test_eh5_invalid_type_for_title_updated_anyway(self):
        tasks = [{"id": 1, "title": "Task1", "description": "D", "status": "pending"}]
        result = edit_task(tasks, 1, title=12345)
        self.assertEqual(result["title"], 12345)


class TestFilterTasksByPriority(unittest.TestCase):

    def test_tc1_filter_low_from_mixed(self):
        tasks = [{"id": 1, "priority": "low"}, {"id": 2, "priority": "high"}]
        result = filter_tasks_by_priority(tasks, "low")
        self.assertEqual(result, [{"id": 1, "priority": "low"}])

    def test_tc2_filter_medium_all_match(self):
        tasks = [{"id": 1, "priority": "medium"}, {"id": 2, "priority": "medium"}]
        result = filter_tasks_by_priority(tasks, "medium")
        self.assertEqual(result, tasks)

    def test_tc3_filter_high_partial_match(self):
        tasks = [
            {"id": 1, "priority": "high"},
            {"id": 2, "priority": "low"},
            {"id": 3, "priority": "high"},
        ]
        result = filter_tasks_by_priority(tasks, "high")
        self.assertEqual(result, [{"id": 1, "priority": "high"}, {"id": 3, "priority": "high"}])

    def test_tc4_no_match_returns_empty(self):
        tasks = [{"id": 1, "priority": "low"}, {"id": 2, "priority": "medium"}]
        result = filter_tasks_by_priority(tasks, "high")
        self.assertEqual(result, [])

    def test_tc5_single_task_matches(self):
        tasks = [{"id": 1, "priority": "low"}]
        result = filter_tasks_by_priority(tasks, "low")
        self.assertEqual(result, [{"id": 1, "priority": "low"}])

    def test_tc6_single_medium_from_three(self):
        tasks = [
            {"id": 1, "priority": "low"},
            {"id": 2, "priority": "medium"},
            {"id": 3, "priority": "high"},
        ]
        result = filter_tasks_by_priority(tasks, "medium")
        self.assertEqual(result, [{"id": 2, "priority": "medium"}])

    def test_ec1_empty_task_list(self):
        result = filter_tasks_by_priority([], "low")
        self.assertEqual(result, [])

    def test_ec2_all_tasks_match(self):
        tasks = [{"id": 1, "priority": "high"}, {"id": 2, "priority": "high"}]
        result = filter_tasks_by_priority(tasks, "high")
        self.assertEqual(result, tasks)

    def test_ec3_case_sensitive_no_match(self):
        tasks = [{"id": 1, "priority": "low"}]
        result = filter_tasks_by_priority(tasks, "Low")
        self.assertEqual(result, [])

    def test_ec4_extra_fields_preserved(self):
        tasks = [{"id": 1, "priority": "medium", "title": "Task"}]
        result = filter_tasks_by_priority(tasks, "medium")
        self.assertEqual(result, [{"id": 1, "priority": "medium", "title": "Task"}])

    def test_ec5_large_list_all_match(self):
        tasks = [{"id": i, "priority": "low"} for i in range(1000)]
        result = filter_tasks_by_priority(tasks, "low")
        self.assertEqual(len(result), 1000)
        self.assertEqual(result, tasks)

    def test_eh1_unknown_priority_returns_empty(self):
        tasks = [{"id": 1, "priority": "low"}]
        result = filter_tasks_by_priority(tasks, "urgent")
        self.assertEqual(result, [])

    def test_eh2_tasks_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            filter_tasks_by_priority(None, "low")

    def test_eh3_missing_priority_key_raises_key_error(self):
        tasks = [{"id": 1}]
        with self.assertRaises(KeyError):
            filter_tasks_by_priority(tasks, "low")

    def test_eh4_non_dict_task_raises_type_error(self):
        tasks = ["not_a_dict"]
        with self.assertRaises(TypeError):
            filter_tasks_by_priority(tasks, "low")

    def test_eh5_priority_none_returns_empty(self):
        tasks = [{"id": 1, "priority": "low"}]
        result = filter_tasks_by_priority(tasks, None)
        self.assertEqual(result, [])


class TestFilterTasksByStatus(unittest.TestCase):

    def test_tc1_filter_pending(self):
        tasks = [
            {"id": 1, "status": "pending"},
            {"id": 2, "status": "completed"},
        ]
        result = filter_tasks_by_status(tasks, "pending")
        self.assertEqual(result, [{"id": 1, "status": "pending"}])

    def test_tc2_filter_in_progress(self):
        tasks = [
            {"id": 1, "status": "in_progress"},
            {"id": 2, "status": "in_progress"},
            {"id": 3, "status": "pending"},
        ]
        result = filter_tasks_by_status(tasks, "in_progress")
        self.assertEqual(result, [{"id": 1, "status": "in_progress"}, {"id": 2, "status": "in_progress"}])

    def test_tc3_filter_completed(self):
        tasks = [
            {"id": 1, "status": "pending"},
            {"id": 2, "status": "completed"},
            {"id": 3, "status": "completed"},
        ]
        result = filter_tasks_by_status(tasks, "completed")
        self.assertEqual(result, [{"id": 2, "status": "completed"}, {"id": 3, "status": "completed"}])

    def test_tc4_no_match_returns_empty(self):
        tasks = [{"id": 1, "status": "pending"}, {"id": 2, "status": "pending"}]
        result = filter_tasks_by_status(tasks, "completed")
        self.assertEqual(result, [])

    def test_tc5_single_task_matches(self):
        tasks = [{"id": 1, "status": "in_progress"}]
        result = filter_tasks_by_status(tasks, "in_progress")
        self.assertEqual(result, [{"id": 1, "status": "in_progress"}])

    def test_tc6_all_three_statuses_present(self):
        tasks = [
            {"id": 1, "status": "pending"},
            {"id": 2, "status": "in_progress"},
            {"id": 3, "status": "completed"},
        ]
        result = filter_tasks_by_status(tasks, "in_progress")
        self.assertEqual(result, [{"id": 2, "status": "in_progress"}])

    def test_ec1_empty_task_list(self):
        result = filter_tasks_by_status([], "pending")
        self.assertEqual(result, [])

    def test_ec2_all_tasks_match(self):
        tasks = [{"id": 1, "status": "completed"}, {"id": 2, "status": "completed"}]
        result = filter_tasks_by_status(tasks, "completed")
        self.assertEqual(result, tasks)

    def test_ec3_case_sensitive_no_match(self):
        tasks = [{"id": 1, "status": "pending"}]
        result = filter_tasks_by_status(tasks, "Pending")
        self.assertEqual(result, [])

    def test_ec4_extra_fields_preserved(self):
        tasks = [{"id": 1, "status": "pending", "title": "Do laundry", "priority": "low"}]
        result = filter_tasks_by_status(tasks, "pending")
        self.assertEqual(result, [{"id": 1, "status": "pending", "title": "Do laundry", "priority": "low"}])

    def test_ec5_large_list_all_match(self):
        tasks = [{"id": i, "status": "pending"} for i in range(1000)]
        result = filter_tasks_by_status(tasks, "pending")
        self.assertEqual(len(result), 1000)
        self.assertEqual(result, tasks)

    def test_eh1_invalid_status_returns_empty(self):
        tasks = [{"id": 1, "status": "pending"}]
        result = filter_tasks_by_status(tasks, "archived")
        self.assertEqual(result, [])

    def test_eh2_tasks_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            filter_tasks_by_status(None, "pending")

    def test_eh3_missing_status_key_raises_key_error(self):
        tasks = [{"id": 1, "title": "No status here"}]
        with self.assertRaises(KeyError):
            filter_tasks_by_status(tasks, "pending")

    def test_eh4_non_dict_task_raises_type_error(self):
        tasks = ["not_a_dict"]
        with self.assertRaises(TypeError):
            filter_tasks_by_status(tasks, "pending")

    def test_eh5_status_none_returns_empty(self):
        tasks = [{"id": 1, "status": "pending"}]
        result = filter_tasks_by_status(tasks, None)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
