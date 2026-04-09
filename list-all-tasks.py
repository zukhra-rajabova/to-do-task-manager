def list_all_tasks(tasks):
    # prints the whole list. each task is a dict like edit_task uses
    if not tasks:
        print("No tasks yet.")
        return tasks

    print(f"Tasks ({len(tasks)} total)\n")

    for task in tasks:
        task_id = task.get("id", "?")
        title = task.get("title", "")
        description = task.get("description", "")
        status = task.get("status", "")

        lines = [
            f"  ID: {task_id}",
            f"  Title: {title}",
            f"  Description: {description}",
            f"  Status: {status}",
        ]

        if "priority" in task:
            lines.append(f"  Priority: {task['priority']}")
        if "due_date" in task:
            lines.append(f"  Due date: {task['due_date']}")
        if "category" in task:
            lines.append(f"  Category: {task['category']}")

        print("\n".join(lines))
        print("-" * 40)

    return tasks

