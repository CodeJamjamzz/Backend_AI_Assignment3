def get_initial_tasks():
    return [
        {"id": 1, "title": "Buy groceries", "done": False},
        {"id": 2, "title": "Clean the house", "done": True},
        {"id": 3, "title": "Finish Assignment 1", "done": False},
    ]

# In-memory storage
tasks_db = get_initial_tasks()
next_id = 4

def reset_db():
    global tasks_db, next_id
    tasks_db.clear()
    tasks_db.extend(get_initial_tasks())
    next_id = 4
