def delete_task(tasks, task_id):
    for i, task in enumerate(tasks):
        if task.get("id") == task_id:
            del tasks[i]
            return True
    return False
