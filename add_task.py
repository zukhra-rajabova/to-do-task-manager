tasks = []
task_id_counter = 1

def add_task(title, description, priority, due_date):
    global task_id_counter

    task = {
        "id": task_id_counter,
        "title": title,
        "description": description,
        "priority": priority,  # e.g., Low / Medium / High
        "due_date": due_date,  # format: YYYY-MM-DD
        "status": "Pending"    # default status
    }

    tasks.append(task)
    task_id_counter += 1

    print(f"✅ Task '{title}' added successfully!")