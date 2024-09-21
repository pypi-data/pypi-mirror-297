from .task_item import TaskItem
from datetime import datetime
from .util import colorize


def list_tasks(listarg, tasks):
    if len(tasks) == 0:
        print("You have no todos!")
        return
    tolist = ''
    match (listarg):
        case 'all':
            for t in tasks:
                print(t)
        case 'todo':
            tolist = 'todo'
        case 'doing':
            tolist = 'doing'
        case 'done':
            tolist = 'done'
    for t in tasks:
        if t.status == tolist:
            print(t)


def add_task(name: str, tasks: list, desc: str = ''):
    date = datetime.now()
    newdate = str(date.month) + "/" + str(date.day) + "/" + str(date.year)
    if len(tasks) == 0:
        newid = 0
    else:
        newid = tasks[-1].id + 1
    t = TaskItem(id=newid, name=name, desc=desc,
                 status="todo", start_date=newdate)
    tasks.append(t)
    print("added", t)


# TODO allow you to delete multiple tasks at once
def delete_task_by_id(taskid, tasks: list) -> list:
    newlist = []
    for t in tasks:
        if t.id != taskid:
            if t.id > taskid:
                t.id -= 1
            newlist.append(t)
        else:
            print(colorize("deleted", 'underline'), t)
    return newlist


def delete_task_by_set(taskset, tasks: list) -> list:
    newlist = []
    if taskset == 'all':
        pass
    else:
        for t in tasks:
            if t.status != taskset:
                newlist.append(t)
    print(colorize(colorize('deleted', 'underline'), 'red'), 'all in', taskset)
    return newlist


# TODO allow you to set multiple tasks at once
def set_mark(taskid, mark, tasks: list):
    color = ''
    match mark:
        case 'todo':
            color = 'red'
        case 'doing':
            color = 'yellow'
        case 'done':
            color = 'green'
    for t in tasks:
        if t.id == taskid:
            t.status = mark
            print("marked", t.name, "as", colorize(mark, color))


# TODO let you update tasks
