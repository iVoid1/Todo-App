import datetime
import uuid



class Task:
    def __init__(self, title, section="To Do"):
        self.id = str(uuid.uuid4())
        self.title = title
        self.completed = False
        self.subtasks = []
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.section = section
        
    def update_title(self, new_title):
        self.title = new_title
        return self
    
    def update_timestamp(self):
        self.updated_at = datetime.datetime.now()
        
    def add_subtask(self, subtask):
        if isinstance(subtask, Task):
            self.subtasks.append(subtask)
    
    def get_subtasks(self):
        return self.subtasks
      
    def remove_subtask(self, subtask):
        if isinstance(subtask, Task):
            self.subtasks.remove(subtask)
    
    def complete(self):
        self.completed = True
        return self
    
    def uncompleted(self):
        self.completed = False
        return self
    def change_section(self, new_section):
        self.section = new_section
        return self
            
    def is_fully_complete(self):
        return self.completed and all(subtask.is_fully_complete() for subtask in self.subtasks)

    def progress(self):
        if not self.subtasks:
            return 100 if self.completed else 0
        completed = sum(1 for st in self.subtasks if st.completed)
        return int((completed / len(self.subtasks)) * 100)
    
    def __repr__(self) -> str:
        return f"<Task: title={self.title}, completed={self.completed}, subtasks={self.subtasks}, section={self.section}>"
