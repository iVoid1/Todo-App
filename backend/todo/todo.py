import json
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field


from todo.models.section import Section, SectionModel
from todo.models.task import Task, TaskModel


class TodoModel(BaseModel):
    version: str = "1.0"
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    sections: List['SectionModel'] = Field(default_factory=list)
    
    
class Todo:
    def __init__(self, file_path: str|Path = ""):
        self.file_path = Path(file_path)
        self.model = TodoModel()
        # Indexes for fast lookup
        self.section_index: Dict[str, Section] = {}
        self.task_index: Dict[str, Task] = {}
        self.load_from_file(file_path)

# ======= file operations ========

    def load_from_file(self, file_path: str|Path):
        """Load data from JSON file"""
        file_path = Path(file_path)
        # Read file
        self._read_file(file_path)
        # Build indexes
        self._build_indexes()
        # Update timestamp
        self._update_timestamp()

    def _read_file(self, file_path: Path):
        """Read file content and load into model"""
        if not file_path.exists():
            self._default_file(file_path)
            return
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
                self.model = TodoModel.model_validate_json(json.dumps(data))
                print("Data loaded successfully")
                return
        except json.JSONDecodeError as e: 
            print(f"the data in the file is not valid json: {e}")
            self._default_file(file_path)
            return
    def _build_indexes(self):
        """Build indexes for fast lookup"""
        self.task_index.clear()
        self.section_index.clear()
        
        for section_data in self.model.sections:
            section = Section.model_validate(section_data.model_dump())
            self.section_index[section.name] = section
            
            for task in section.tasks:
                self.task_index[task.title] = task
                # Index subtasks too
                for subtask in task.subtasks:
                    self.task_index[subtask.title] = subtask

    def _default_file(self, file_path: Path):
        """Get or create default section"""
        general_section = Section(name="General")
        self.model.sections.append(general_section)
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(self.model.model_dump(), f, ensure_ascii=False, indent=4, default=str)

    def save_to_file(self):
        """Save data to JSON file"""
        try:
            self.model.sections = list(self.section_index.values())
            print(self.model.sections)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.model.model_dump(), f, ensure_ascii=False, indent=4, default=str)
                
            self._update_timestamp()
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
# ======= data manipulation methods ========

    def create_task(self, title: str, section_name: str, description: str = "") -> Task:
        """Create a new task"""
        if title in self.task_index:
            print(f"Task '{title}' already exists.")
            return self.task_index[title]
        
        task = Task(title=title, description=description)
        self.add_task_to_section(task, section_name)
        return task
    
    def create_subtask(self, parent_title: str, title: str, description: str = "") -> Optional[Task]:
        """Create a subtask under a parent task"""
        parent_task = self.task_index.get(parent_title)
        if not parent_task:
            print("❌ مالقيت المهمة الأم!")
            return
        if title in self.task_index:
            print(f"Subtask '{title}' already exists.")
            return self.task_index[title]
        new_subtask = Task(title=title)
        parent_task.add_subtask(new_subtask)
        self.task_index[new_subtask.title] = new_subtask
        self.save_to_file()
        return new_subtask

    def create_section(self, name: str) -> Section:
        """Create a new section (if it doesn't exist)"""
        if name in self.section_index:
            print(f"Section '{name}' already exists.")
            return self.section_index[name]
        
        section = Section(name=name)
        self.section_index[section.name] = section
        self.save_to_file()
        return section
    
    def add_task_to_section(self, task: Task, section_name: str):
        """Add task to a specific section"""
        section = self.get_section(section_name)
        
        if not section:
            print(f"Section '{section_name}' not found and couldn't be created")
            return False
        
        section.add_task(task)
        self.task_index[task.title] = task
        self.save_to_file()
        return True
    
    def remove_task_by_title(self, task_title: str) -> bool:
        """Remove task by ID"""
        # 1. Get task from index
        task = self.task_index.get(task_title)
        if not task:
            print(f"Task with ID {task_title} not found")
            return False
        for section in self.section_index.values():
            if task in section.tasks:
                section.remove_task(task)
                break
        self.save_to_file()
        print(f"Removed task: {task.title}")
        return True
    
    def remove_section_by_name(self, section_name: str) -> bool:
        """Remove section by name"""
        # 1. Check if section exists
        section = self.get_section(section_name)
        if not section:
            print(f"Section '{section_name}' not found")
            return False
        # 2. Remove section from data
        self.model.sections.remove(section)
        self.save_to_file()
        print(f"Removed section: {section_name}")
        return True
    
    def get_task(self, task_title: str):
        """Get task by title"""
        print(self.task_index)
        return self.task_index.get(task_title)
    
    def get_section(self, section_name: str):
        """Get section by name"""
        return self.section_index.get(section_name)
    @property
    def get_all_tasks(self) -> List[TaskModel]:
        """Get all tasks"""
        return list(self.task_index.values())
    @property
    def get_root_tasks(self) -> List[Task]:
        """Get all root-level tasks (excluding subtasks)"""
        root_tasks = []
        for section in self.section_index.values():
            root_tasks.extend(section.tasks)
        return root_tasks
    @property
    def get_all_sections(self) -> List[Section]:
        """Get all sections"""
        return list(self.section_index.values())
    @property
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks"""
        return [task for task in self.task_index.values() if task.completed]
    
    def _update_timestamp(self):
        """Update last modified timestamp"""
        self.model.last_updated = datetime.now()
    
    # def reload(self):
    #     """Reload data from file"""
    #     self.load_from_file()
    #     self._build_indexes()
    
    # def reset_to_default(self):
    #     """Reset data to default state"""
    #     self._create_default_file()
    #     self._build_indexes()