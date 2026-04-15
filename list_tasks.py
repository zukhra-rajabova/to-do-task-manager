def lines_for_task(task):
    """
    Build printable lines for one task (used by list and search).

    Args:
        task (dict): Task fields such as id, title, description, status;
            optional: priority, due_date, category, categories.

    Returns:
        list: Lines of text to print (no trailing newlines).
    """
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
    cats = task.get("categories")
    if isinstance(cats, list) and cats:
        lines.append(f"  Categories: {', '.join(str(c) for c in cats)}")

    return lines


def list_all_tasks(tasks):
    """
    Print every task in the list.

    Args:
        tasks (list): List of task dictionaries.

    Returns:
        list: The same tasks list (unchanged).
    """
    if not tasks:
        print("No tasks yet.")
        return tasks

    print(f"Tasks ({len(tasks)} total)\n")

    for task in tasks:
        print("\n".join(lines_for_task(task)))
        print("-" * 40)

    return tasks
