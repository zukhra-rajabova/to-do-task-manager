class Task:
    def __init__(self, task_id, title, description, priority, due_date, status="Pending"):
        self.id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.status = status

def add_task(task_list, next_id, title, description, priority, due_date):

    if not isinstance(task_list, list):
        raise AttributeError("task_list must be a list")

    if not isinstance(next_id, int):
        raise TypeError("next_id must be integer")

    if not isinstance(title, str):
        raise TypeError("title must be string")

    if title.strip() == "":
        raise ValueError("title cannot be empty")

    new_task = Task(next_id, title, description, priority, due_date)
    task_list.append(new_task)
    return new_task, next_id + 1