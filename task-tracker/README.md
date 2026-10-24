# Task Tracker CLI

A simple command-line task management application built with Python. Tasks are saved locally in a JSON file.

## Features

- Add new tasks
- List all tasks or filter by status
- Update task descriptions
- Delete tasks
- Mark tasks as in-progress or done
- Assign unique task IDs
- Track creation and update timestamps
- Store tasks between program runs

## Requirements

- Python 3.10 or later
- Python standard library only

## Usage

Run commands from the `task-tracker` directory.

### Add a task

```bash
python3 task_cli.py add "Finish my project"
```

### List tasks

```bash
python3 task_cli.py list
python3 task_cli.py list todo
python3 task_cli.py list in-progress
python3 task_cli.py list done
```

### Update a task

```bash
python3 task_cli.py update 1 "Review my project"
```

### Change task status

```bash
python3 task_cli.py mark-in-progress 1
python3 task_cli.py mark-done 1
```

### Delete a task

```bash
python3 task_cli.py delete 1
```

### View help

```bash
python3 task_cli.py --help
```

## Data Storage

The application creates `tasks.json` automatically when needed. Task data is stored locally and excluded from Git.

## Running the Application

Navigate into the project directory and run the desired command using Python 3.
