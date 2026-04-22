import unittest

def delete_task(tasks, task_id):
    if not isinstance(task_id, int):
        raise TypeError("ID must be int")
    if task_id not in tasks:
        raise ValueError("Task not found")
    tasks.remove(task_id)
    return tasks


class TestDeleteTask(unittest.TestCase):

    # 正常删除
    def test_delete_normal(self):
        tasks = [1, 2, 3]
        result = delete_task(tasks, 2)
        self.assertEqual(result, [1, 3])

    # index shift 检查
    def test_delete_order(self):
        tasks = [1, 2, 3]
        result = delete_task(tasks, 1)
        self.assertEqual(result, [2, 3])

    # 空列表
    def test_empty_list(self):
        tasks = []
        with self.assertRaises(ValueError):
            delete_task(tasks, 1)

    # 删除最后一个
    def test_delete_last(self):
        tasks = [1]
        result = delete_task(tasks, 1)
        self.assertEqual(result, [])

    # 不存在的ID
    def test_invalid_id(self):
        tasks = [1, 2]
        with self.assertRaises(ValueError):
            delete_task(tasks, 5)

    # 类型错误
    def test_wrong_type(self):
        tasks = [1, 2]
        with self.assertRaises(TypeError):
            delete_task(tasks, "a")


if __name__ == '__main__':
    unittest.main()