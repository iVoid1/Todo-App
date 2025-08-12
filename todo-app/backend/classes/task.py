from datetime import datetime

from data import TaskModel


class Task(TaskModel):  
          
    def update_title(self, new_title: str):
        self.title = new_title
        self.update_timestamp()
        return self

    def add_subtask(self, subtask: 'Task'):
        if isinstance(subtask, Task):
            self.subtasks.append(subtask)
            self.update_timestamp()
    
    def update_timestamp(self):
        self.updated_at = datetime.now()
   
    def complete(self):
        self.completed = True
        self.update_timestamp()
        return self
   
    def incomplete(self):
        self.completed = False
        self.update_timestamp()
        return self
           
    def is_fully_complete(self) -> bool:
        return self.completed and all(subtask.completed for subtask in self.subtasks)
    
    def progress(self) -> int:
        if not self.subtasks:
            return 100 if self.completed else 0
        completed = sum(1 for st in self.subtasks if st.completed)
        return int((completed / len(self.subtasks)) * 100)
    