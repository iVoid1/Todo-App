from task import Task

class Section:
    def __init__(self, name):
        self.name = name
        self.tasks = []
    
    def add_task(self, task):
        if isinstance(task, Task):
            self.tasks.append(task)
    
    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
    
    def get_tasks(self):
        return self.tasks
    
    def get_completed_tasks(self):
        return [task for task in self.tasks if task.completed]
    
    def get_pending_tasks(self):
        return [task for task in self.tasks if not task.completed]
    
    def __repr__(self):
        return f"<Section: {self.name} ({len(self.tasks)} tasks)>"
    
    
