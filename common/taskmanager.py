from light_progress.commandline import ProgressBar
from light_progress import widget


class TaskManager(object):
    def __init__(self, tasks):
        self.tasks = tasks
        widgets = [widget.Bar(bar='*', tip='>'),
                   widget.Percentage(),
                   widget.Num(),
                   widget.ElapsedSeconds(),
                   widget.FinishedAt()]
        self.pb = ProgressBar(len(self.tasks), widgets=widgets)

    def start(self):
        self.pb.start()
        self.execute()

    def pop(self):
        if len(self.tasks) == 0:
            return
        task = self.tasks.pop()
        self.pb.forward()
        return task

    def execute(self):
        t = self.pop()
        if not t:
            return
        t.execute()
        if len(self.tasks) > 0:
            self.execute()
        else:
            self.pb.finish()
