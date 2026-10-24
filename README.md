# Task Tracker CLI

A simple command-line application built with Python to manage tasks and track their progress. Tasks are stored in a JSON file, so they persist between runs.

## Features

- Add, update, and delete tasks
- Mark tasks as in-progress or done
- List all tasks
- Filter tasks by status
- Store tasks in JSON
- Automatically assign task IDs and timestamps

## Requirements

- Python 3.10 or later
- No external libraries required

## Usage

Add a task:

`python3 task_cli.py add "Buy groceries"`

List all tasks:

`python3 task_cli.py list`

List tasks by status:

`python3 task_cli.py list todo`

`python3 task_cli.py list in-progress`

`python3 task_cli.py list done`

Update a task:

`python3 task_cli.py update 1 "Buy groceries and cook dinner"`

Delete a task:

`python3 task_cli.py delete 1`

Mark a task in progress:

`python3 task_cli.py mark-in-progress 1`

Mark a task as done:

`python3 task_cli.py mark-done 1`

View available commands:

`python3 task_cli.py --help`

## Storage

Tasks are stored in `tasks.json`, which is created automatically when needed.

Each task contains an ID, description, status, creation timestamp, and last-update timestamp.

## Learning outcomes

This project demonstrates Python functions, command-line arguments, JSON serialization, filesystem operations, input validation, and error handling.