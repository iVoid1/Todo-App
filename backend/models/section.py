from . import SectionModel, TaskModel


class Section(SectionModel):
    
    def add_task(self, task: TaskModel):
        self.tasks.append(task)
    
    def remove_task(self, task: TaskModel):
        if task in self.tasks:
            self.tasks.remove(task)
    
    def get_completed_tasks(self):
        return [task for task in self.tasks if task.completed]
    
    def get_pending_tasks(self):
        return [task for task in self.tasks if not task.completed]
    
    

    