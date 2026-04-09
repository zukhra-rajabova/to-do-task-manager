def edit_task(tasks, task_id, title=None, description=None, status=None):
    """
    Edit an existing task in the task list.

    Args:
        tasks (list):      List of task dictionaries.
        task_id (int):     The ID of the task to edit.
        title (str):       New title (optional).
        description (str): New description (optional).
        status (str):      New status - 'pending', 'in_progress', or 'done' (optional).

    Returns:
        dict: The updated task, or None if not found.
    """
    for task in tasks:
        if task["id"] == task_id:
            if title       is not None: task["title"]       = title
            if description is not None: task["description"] = description
            if status      is not None: task["status"]      = status
            print(f"Task {task_id} updated successfully.")
            return task

    print(f"Task with ID {task_id} not found.")
    return None