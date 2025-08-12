from classes import Task
from data import SectionModel


class Section(SectionModel):
    
    def add_task(self, task):
        if isinstance(task, Task):
            self.tasks.append(task)
    
    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
    
    def get_completed_tasks(self):
        return [task for task in self.tasks if task.completed]
    
    def get_pending_tasks(self):
        return [task for task in self.tasks if not task.completed]
    
    

    