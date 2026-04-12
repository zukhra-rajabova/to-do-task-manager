from datetime import datetime

def sort_tasks_by_due_date(tasks):
    return sorted(
        tasks,
        key=lambda task: datetime.strptime(task["due_date"], "%Y-%m-%d")
    )