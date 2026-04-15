def add_category(task, category):
    """
    Add a category label to a task (stored in task['categories']).

    Args:
        task (dict): The task to update.
        category (str): Label to add; blank strings are ignored.

    Returns:
        dict: The same task dict (updated in place).
    """
    if category is None or str(category).strip() == "":
        return task
    label = str(category).strip()
    if "categories" not in task:
        task["categories"] = []
    elif not isinstance(task["categories"], list):
        task["categories"] = [str(task["categories"])]
    if label not in task["categories"]:
        task["categories"].append(label)
    return task
