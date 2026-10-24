import argparse
import json
from datetime import datetime
from pathlib import Path

TASKS_FILE = Path("tasks.json")


def load_tasks() -> list[dict]:
    """Load tasks from JSON, creating the file if necessary."""
    if not TASKS_FILE.exists():
        save_tasks([])

    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            "tasks.json contains invalid JSON. "
            "Please repair the file before continuing."
        ) from error

    if not isinstance(tasks, list):
        raise ValueError("tasks.json must contain a list of tasks.")

    return tasks


def save_tasks(tasks: list[dict]) -> None:
    """Save all tasks to the JSON file."""
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)



from datetime import datetime


def add_task(description: str) -> dict:
    """Create and save a new task."""
    description = description.strip()

    if not description:
        raise ValueError("Task description cannot be empty.")

    tasks = load_tasks()

    # Generate the next ID.
    next_id = max(
        (task["id"] for task in tasks),
        default=0
    ) + 1

    # Record the current time.
    now = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    task = {
        "id": next_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now,
    }

    tasks.append(task)
    save_tasks(tasks)

    return task


def list_tasks(status: str | None = None) -> list[dict]:
    """Return all tasks or filter them by status."""
    tasks = load_tasks()

    if status is not None:
        tasks = [
            task for task in tasks
            if task["status"] == status
        ]

    return tasks


def update_task(task_id: int, description: str) -> bool:
    """Update a task's description and timestamp."""
    description = description.strip()

    if not description:
        raise ValueError("Task description cannot be empty.")

    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = datetime.now().astimezone().isoformat(
                timespec="seconds"
            )

            save_tasks(tasks)
            return True

    return False


def delete_task(task_id: int) -> bool:
    """Delete a task by its ID."""
    tasks = load_tasks()

    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[index]
            save_tasks(tasks)
            return True

    return False


def mark_task(task_id: int, status: str) -> bool:
    """Change a task's status."""
    allowed_statuses = {"todo", "in-progress", "done"}

    if status not in allowed_statuses:
        raise ValueError(
            "Invalid status. Use todo, in-progress, or done."
        )

    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().astimezone().isoformat(
                timespec="seconds"
            )

            save_tasks(tasks)
            return True

    return False



def main() -> None:
    parser = argparse.ArgumentParser(
        description="A simple task tracker."
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # add command
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("description")

    # list command
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument(
        "status",
        nargs="?",
        choices=["todo", "in-progress", "done"]
    )

    # update command
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("description")

    # delete command
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("id", type=int)

    # mark-in-progress command
    progress_parser = subparsers.add_parser("mark-in-progress")
    progress_parser.add_argument("id", type=int)

    # mark-done command
    done_parser = subparsers.add_parser("mark-done")
    done_parser.add_argument("id", type=int)

    args = parser.parse_args()

    try:
        if args.command == "add":
            task = add_task(args.description)
            print(f"Task added successfully (ID: {task['id']})")

        elif args.command == "list":
            tasks = list_tasks(args.status)
            for task in tasks:
                print(
                    f"{task['id']}: {task['description']} "
                    f"[{task['status']}]"
                )
            if not tasks:
                print("No tasks found.")

        elif args.command == "update":
            if update_task(args.id, args.description):
                print("Task updated successfully.")
            else:
                print(f"Task with ID {args.id} not found.")

        elif args.command == "delete":
            if delete_task(args.id):
                print("Task deleted successfully.")
            else:
                print(f"Task with ID {args.id} not found.")

        elif args.command == "mark-in-progress":
            if mark_task(args.id, "in-progress"):
                print("Task marked as in-progress.")
            else:
                print(f"Task with ID {args.id} not found.")

        elif args.command == "mark-done":
            if mark_task(args.id, "done"):
                print("Task marked as done.")
            else:
                print(f"Task with ID {args.id} not found.")

    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
