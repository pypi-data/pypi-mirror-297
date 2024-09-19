from .TaskItem import TaskItem
from datetime import datetime


def list_tasks(listarg, tasks):
    if len(tasks) == 0:
        print("You have no todos!")
        return
    tolist = ''
    match (listarg):
        case 'a' | 'all':
            for t in tasks:
                print(t)
        case 't' | 'todo':
            tolist = 'todo'
        case 'i' | 'inprog':
            tolist = 'inprog'
        case 'd' | 'done':
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
    # TODO colorize
    print("added", t)


def delete_task(taskid, tasks: list) -> list:
    newlist = []
    for t in tasks:
        if t.id != taskid:
            if t.id > taskid:
                t.id -= 1
            newlist.append(t)
        else:
            # TODO colorize
            print("deleted", t)
    return newlist


def set_mark(taskid, mark, tasks: list):
    for t in tasks:
        if t.id == taskid:
            t.status = mark
    # TODO colorize
    print("marked", t.name, "as", t.status)

# TODO update
