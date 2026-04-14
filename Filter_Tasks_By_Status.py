def filter_tasks_by_status(tasks, status):
    """
    Filter tasks by their status.

    :param tasks: list of task dicts
    :param status: "pending", "in_progress", or "completed"
    :return: list of matching tasks
    """
    valid_statuses = ["pending", "in_progress", "completed"]

    if status not in valid_statuses:
        print(f"Invalid status. Choose from: {valid_statuses}")
        return []

    return [task for task in tasks if task["status"] == status]