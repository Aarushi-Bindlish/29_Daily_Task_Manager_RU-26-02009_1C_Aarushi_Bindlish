"""Daily Task Manager - PS 29
Concepts: Lists, Dictionaries, Functions, File Handling
Tasks are stored in tasks.txt as: ID|Title|Priority|Due|Status
"""
from datetime import datetime

FILENAME = "tasks.txt"
PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def load_tasks():
    """Load tasks from file into a list of dictionaries."""
    tasks = []
    try:
        with open(FILENAME, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 5:
                    tasks.append({"id": parts[0], "title": parts[1],
                                  "priority": parts[2], "due": parts[3],
                                  "status": parts[4]})
    except FileNotFoundError:
        pass
    return tasks


def save_tasks(tasks):
    """Write all tasks to file (called after every change)."""
    with open(FILENAME, "w") as f:
        for t in tasks:
            f.write(f"{t['id']}|{t['title']}|{t['priority']}|{t['due']}|{t['status']}\n")


def next_id(tasks):
    """Generate the next unique task ID, starting from T101."""
    nums = [int(t["id"][1:]) for t in tasks if t["id"][1:].isdigit()]
    return "T" + str(max(nums) + 1 if nums else 101)


def valid_priority(p):
    for name in PRIORITY_ORDER:
        if p.lower() == name.lower():
            return name
    return None


def valid_date(d):
    try:
        datetime.strptime(d, "%Y-%m-%d")
        return len(d) == 10
    except ValueError:
        return False


def add_task(tasks):
    title = input("Title: ").strip().replace("|", "/")
    priority = valid_priority(input("Priority: ").strip())
    if priority is None:
        print("Invalid priority. Enter High, Medium or Low.")
        return
    due = input("Due: ").strip()
    if not valid_date(due):
        print("Invalid date. Use YYYY-MM-DD.")
        return
    if not title:
        print("Title cannot be empty.")
        return
    task = {"id": next_id(tasks), "title": title, "priority": priority,
            "due": due, "status": "Pending"}
    tasks.append(task)
    save_tasks(tasks)
    print("Task added.")
    print(f"{task['id']} | {task['title']} | {task['priority']} | {task['due']} | {task['status']}")


def view_by_priority(tasks):
    if not tasks:
        print("No tasks found.")
        return
    for t in sorted(tasks, key=lambda x: (PRIORITY_ORDER[x["priority"]], x["due"])):
        print(f"{t['id']} | {t['title']} | {t['priority']} | {t['due']}")


def show_pending(tasks):
    pending = [t for t in tasks if t["status"] == "Pending"]
    if not pending:
        print("No pending tasks. You are all caught up!")
        return
    for t in pending:
        print(f"{t['id']} | {t['title']} | {t['priority']} | {t['due']} | {t['status']}")


def complete_task(tasks):
    tid = input("Task ID: ").strip().upper()
    for t in tasks:
        if t["id"] == tid:
            t["status"] = "Done"
            save_tasks(tasks)
            pending = sum(1 for x in tasks if x["status"] == "Pending")
            print(f"Task {tid} marked as done. Pending tasks: {pending}")
            return
    print(f"Task {tid} not found.")


def main():
    tasks = load_tasks()
    while True:
        print("\n1 Add\n2 View by priority\n3 Show pending\n4 Complete\n5 Exit")
        choice = input("Menu option: ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_by_priority(tasks)
        elif choice == "3":
            show_pending(tasks)
        elif choice == "4":
            complete_task(tasks)
        elif choice == "5":
            break
        else:
            print("Invalid option. Choose 1-5.")


if __name__ == "__main__":
    main()
