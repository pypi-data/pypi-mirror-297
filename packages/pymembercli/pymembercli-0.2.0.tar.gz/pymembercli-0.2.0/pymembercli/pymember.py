from platformdirs import user_data_dir
from .task_item import TaskItem
from pathlib import Path
from . import cmds
import argparse
import json


def main():
    parser = make_parser()
    args = parser.parse_args()
    path = user_data_dir("pymembercli", "mekumotoki")
    tasks = load_file(path)
    tasks = handle_args(args, tasks)
    # save before exit
    with open(path+'/tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4, default=vars)


def load_file(path) -> list:
    """Loads the tasks.json file and returns it as an object."""
    tasks = []
    Path(path).mkdir(parents=True, exist_ok=True)
    try:
        open(path+'/tasks.json', 'x')
    except:
        with open(path+'/tasks.json') as file:
            data = json.load(file)
            for d in data:
                t = TaskItem(id=d['id'], name=d['name'], desc=d['desc'],
                             status=d['status'], start_date=d['start_date'])
                tasks.append(t)
    return tasks


def handle_args(args: argparse.Namespace, tasks: list) -> list:
    """Handle all the arguments."""
    if args.list != None:
        cmds.list_tasks(args.list, tasks)
    if args.add != None:
        if args.desc != None:
            cmds.add_task(name=args.add, desc=args.desc, tasks=tasks)
        else:
            cmds.add_task(name=args.add, tasks=tasks)
    if args.mt != None:
        cmds.set_mark(args.mt, 'todo', tasks)
    if args.mi != None:
        cmds.set_mark(args.mi, 'inprog', tasks)
    if args.md != None:
        cmds.set_mark(args.md, 'done', tasks)
    if args.delete != None:
        tasks = cmds.delete_task(args.delete, tasks)
    return tasks


def make_parser() -> argparse.ArgumentParser:
    """Setup the CLI."""
    parser = argparse.ArgumentParser(
        description="A tool for todo-list keeping and helpful reminders.",
        prog="pymember")
    parser.add_argument('-l', '--list', type=str,
                        help="List either 'a'll, 't'odo, 'i'nprog or 'd'one.")
    parser.add_argument('-a', '--add', type=str, nargs='?',
                        help="Add an item to the list.")
    # parser.add_argument('-u', '--update', nargs='+', dest='upd',
    # help="Update an item on the list.")
    parser.add_argument('-d', '--desc', type=str,
                        dest='desc', help="Add a description, when adding or updating an item.")
    parser.add_argument('-mt', '--markt', type=int, dest='mt',
                        help="Mark an item as 't'odo.")
    parser.add_argument('-mi', '--marki', type=int, dest='mi',
                        help="Mark an item as 'i'n progress.")
    parser.add_argument('-md', '--markd', type=int, dest='md',
                        help="Mark an item as 'd'one")
    parser.add_argument('-del', type=int, dest='delete',
                        help="Delete an item.")
    return parser
