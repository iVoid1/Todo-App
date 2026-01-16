from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

from todo.models.task import Task


class SectionModel(BaseModel):
    name: str
    tasks: List['Task'] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    
class Section(SectionModel):
    
    def add_task(self, task: Task):
        self.tasks.append(task)
    
    def remove_task(self, task: Task):
        if task in self.tasks:
            self.tasks.remove(task)
            
    @property
    def completed_tasks(self):
        return [task for task in self.tasks if task.completed]
    @property
    def pending_tasks(self):
        return [task for task in self.tasks if not task.completed]
    
    

    