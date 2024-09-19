from dataclasses import dataclass
from .util import colorize


@dataclass
class TaskItem:
    """Represents a todo item."""
    id: int
    name: str
    desc: str
    status: str
    start_date: str

    def __repr__(self):
        newname = self.name
        newstatus = self.status
        newdesc = colorize(self.desc, 'dark_gray')
        newdate = colorize(self.start_date, 'purple')
        if self.status == 'todo':
            newname = colorize(newname, 'red')
            newstatus = colorize(newstatus, 'red')
        elif self.status == 'inprog':
            newname = colorize(newname, 'yellow')
            newstatus = colorize(newstatus, 'yellow')
        elif self.status == 'done':
            newname = colorize(newname, 'green')
            newstatus = colorize(newstatus, 'green')
        reprstr = str(self.id) + ". " + newname + " |  " + newdesc + \
            "\n" + newstatus + "  added: " + newdate
        return reprstr
