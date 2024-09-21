from platformdirs import user_data_dir
from .task_item import TaskItem
from pathlib import Path
from . import cmds
import argparse
import json


def main():
    path = user_data_dir("pymembercli", "mekumotoki")
    tasks = load_file(path)
    tasks = do_everything(tasks)
    # save before exit
    with open(path+'/tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4, default=vars)


def load_file(path) -> list:
    """Loads the tasks.json file and returns it as an object."""
    tasks = []
    Path(path).mkdir(parents=True, exist_ok=True)
    # TODO pull out into 'atomic function'?
    try:
        open(path+'/tasks.json', 'x')
    except FileExistsError:
        with open(path+'/tasks.json') as file:
            data = json.load(file)
            for d in data:
                # TODO cant i just pass the json object around?
                # do i really need objects here?
                t = TaskItem(id=d['id'], name=d['name'], desc=d['desc'],
                             status=d['status'], start_date=d['start_date'])
                tasks.append(t)
    return tasks


# TODO add shell

def do_everything(tasks: list) -> list:
    """Do Everything"""
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
    del_task.add_argument('taskid', type=int, help='taskid to delete')

    args = parser.parse_args()

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
        tasks = cmds.delete_task(args.taskid, tasks=tasks)

    return tasks
