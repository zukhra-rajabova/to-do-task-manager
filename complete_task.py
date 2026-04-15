def mark_task_completed(task_list, task_id):
    for task in task_list:
        if task.id == task_id:
            task.status = "Completed"
            return True
    return False