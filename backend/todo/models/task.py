from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class TaskModel(BaseModel):
    title: str
    description: str = ""
    completed: bool = False
    subtasks: List['Task'] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    
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
   
    def mark_task(self, complete: bool = True):
        self.completed = complete
        self.update_timestamp()
           
    def is_fully_complete(self) -> bool:
        return self.completed and all(subtask.completed for subtask in self.subtasks)
    
    def progress(self) -> int:
        if not self.subtasks:
            return 100 if self.completed else 0
        completed = sum(1 for st in self.subtasks if st.completed)
        return int((completed / len(self.subtasks)) * 100)
    