def filter_tasks_by_priority(tasks, priority):
    """
    Filter tasks by their priority.

    :param tasks: list of task dicts
    :param priority: "low", "medium", or "high"
    :return: list of matching tasks
    """
    valid_priorities = ["low", "medium", "high"]

    if priority not in valid_priorities:
        print(f"Invalid priority. Choose from: {valid_priorities}")
        return []

    return [task for task in tasks if task["priority"] == priority]