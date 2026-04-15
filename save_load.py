import json

def save_tasks(task_list, filename="tasks.json"):
    data = []
    for task in task_list:
        data.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "due_date": task.due_date,
            "status": task.status
        })

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_tasks(TaskClass, filename="tasks.json"):
    task_list = []
    next_id = 1

    try:
        with open(filename, "r") as file:
            data = json.load(file)

            for item in data:
                task = TaskClass(
                    item["id"],
                    item["title"],
                    item["description"],
                    item["priority"],
                    item["due_date"],
                    item["status"]
                )
                task_list.append(task)

            if task_list:
                next_id = max(task.id for task in task_list) + 1

    except FileNotFoundError:
        pass

    return task_list, next_id