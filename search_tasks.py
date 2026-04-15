from list_tasks import lines_for_task


def search_tasks_by_keyword(tasks, keyword):
    """
    Find tasks whose title, description, status, category, or categories contain the keyword.

    Args:
        tasks (list): List of task dictionaries.
        keyword (str): Substring to search for (case-insensitive).

    Returns:
        list: Tasks that match; empty if none or keyword is blank.
    """
    if keyword is None or str(keyword).strip() == "":
        print("Need a keyword to search.")
        return []

    needle = str(keyword).strip()
    q = needle.lower()
    matches = []

    for task in tasks:
        chunks = []
        for key in ("title", "description", "status", "category"):
            if key in task and task[key] is not None:
                chunks.append(str(task[key]))
        cats = task.get("categories")
        if isinstance(cats, list):
            chunks.extend(str(c) for c in cats)
        elif cats is not None:
            chunks.append(str(cats))
        haystack = " ".join(chunks).lower()
        if q in haystack:
            matches.append(task)

    if not matches:
        print(f"No tasks match '{needle}'.")
        return matches

    print(f"Matches for '{needle}' ({len(matches)} task(s))\n")
    for task in matches:
        print("\n".join(lines_for_task(task)))
        print("-" * 40)

    return matches
