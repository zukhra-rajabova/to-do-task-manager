def add_category(task, category):
    if "categories" not in task:
        task["categories"] = []
    if category not in task["categories"]:
        task["categories"].append(category)
    return task