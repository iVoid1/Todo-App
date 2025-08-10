
class Task:
    def __init__(self, title, section="To Do"):
        self.title = title
        self.completed = False
        self.subtasks = []
        self.section = section
    
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
