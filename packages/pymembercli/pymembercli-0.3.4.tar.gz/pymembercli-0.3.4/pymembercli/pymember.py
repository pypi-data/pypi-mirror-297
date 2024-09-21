from platformdirs import user_data_dir
from .task_item import TaskItem
from pathlib import Path
from . import cmds
import argparse
import json


def main():
    path = user_data_dir("pymembercli", "mekumotoki")
    tasks = load_file(path)
    args = make_parser()
    tasks = handle_args(tasks, args)
    # save before exit
    with open(path+'/tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4, default=vars)


def load_file(path) -> list:
    """Loads the tasks.json file and returns it as an object."""
    tasks = []
    Path(path).mkdir(parents=True, exist_ok=True)
    # check if file already exists
    try:
        open(path+'/tasks.json', 'x')
    except FileExistsError:
        with open(path+'/tasks.json') as file:
            data = json.load(file)
            for d in data:
                t = TaskItem(id=d['id'], name=d['name'], desc=d['desc'],
                             status=d['status'], start_date=d['start_date'])
                tasks.append(t)
    return tasks


def make_parser() -> argparse.Namespace:
    """Setup the CLI"""
    parser = argparse.ArgumentParser(
        description="A tool for todo-list keeping and helpful reminders.",
        prog="pymember")
    parser.add_argument('--debug', action='store_true',
                        help='print debug info')

    subparsers = parser.add_subparsers(dest='command')

    ls = subparsers.add_parser(
        'ls', help='list tasks')
    ls.add_argument('lstype', type=str, choices=[
        'all', 'todo', 'doing', 'done'], default='all', nargs='?')

    add = subparsers.add_parser('add', help='add a task to the list')
    add.add_argument('taskname', type=str, help='name of task')
    add.add_argument('-d', '--desc', type=str, help='set a description')

    set_state = subparsers.add_parser(
        'set', help='set the status of a task')
    set_state.add_argument(
        'taskid', type=int, help='taskid to set')
    set_state.add_argument(
        'status', type=str, choices=['todo', 'doing', 'done'])

    del_task = subparsers.add_parser('del', help='delete a task')
    del_task.add_argument('-id', dest='taskid', type=int,
                          help='taskid to delete')
    del_task.add_argument('-set', dest='taskset', type=str,
                          choices=['all', 'todo', 'doing', 'done'],
                          help='taskset to delete')

    subparsers.add_parser('clear', help='clear all tasks')

    return parser.parse_args()


def handle_args(tasks, args) -> list:
    if args.command == 'ls':
        cmds.list_tasks(args.lstype, tasks)

    elif args.command == 'add':
        if args.desc is not None:
            cmds.add_task(name=args.taskname, desc=args.desc, tasks=tasks)
        else:
            cmds.add_task(name=args.taskname, tasks=tasks)

    elif args.command == 'set':
        cmds.set_mark(taskid=args.taskid,
                      mark=args.status, tasks=tasks)

    elif args.command == 'del':
        if args.taskid is not None:
            tasks = cmds.delete_task_by_id(args.taskid, tasks=tasks)
        if args.taskset is not None:
            tasks = cmds.delete_task_by_set(args.taskset, tasks=tasks)

    elif args.command == 'clear':
        tasks = cmds.delete_task_by_set('all', tasks=tasks)

    return tasks
