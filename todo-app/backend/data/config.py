import json
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime
from data import ConfigModel
from classes import Task, Section

class Config:
    def __init__(self, file_path: str = "todo_data.json"):
        self.file_path = Path(file_path)
        self.data = ConfigModel()
        # Indexes for fast lookup
        self.task_index: Dict[str, Task] = {}
        self.section_index: Dict[str, Section] = {}
        
        self.load_from_file()
        self._build_indexes()


#======= file operations ========

    def load_from_file(self):
        """Load data from JSON file"""
        try:
            # Check if file exists
            if not self.file_path.exists():
                print(f"File not found, creating: {self.file_path}")
                self._create_default_file()
                return True
            
            # Check if file is empty
            if self.file_path.stat().st_size == 0:
                print("File is empty, creating default data")
                self._create_default_file()
                return True
            
            # Read file
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Check if JSON is empty or null
                if not data:
                    print("Data is empty, creating default data")
                    self._create_default_file()
                    return True
                
                self.data = ConfigModel.model_validate(data)
                print("Data loaded successfully")
            return True
            
        except json.JSONDecodeError as e:
            print(f"JSON format error: {e}")
            print("Creating new file with default data")
            self._create_default_file()
            return True
            
        except Exception as e:
            print(f"Error loading file: {e}")
            print("Creating new file with default data")
            self._create_default_file()
            return True
    
    def _build_indexes(self):
        """Build indexes for fast lookup"""
        self.task_index.clear()
        self.section_index.clear()
        
        for section_data in self.data.sections:
            section = Section.model_validate(section_data.model_dump())
            self.section_index[section.name] = section
            
            for task in section.tasks:
                self.task_index[task.id] = Task.model_validate(task.model_dump())
                # Index subtasks too
                for subtask in task.subtasks:
                    self.task_index[subtask.id] = Task.model_validate(subtask.model_dump())
    
    def _create_default_file(self):
        """Create file with default data"""
        try:
            # Create default data
            self.data = ConfigModel()
            self._update_timestamp()
            
            # Create directory if it doesn't exist
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save default data
            self.save_to_file()
            print(f"Created new file: {self.file_path}")
            
        except Exception as e:
            print(f"Error creating default file: {e}")
    
    def save_to_file(self):
        """Save data to JSON file"""
        try:
            # Create directory if it doesn't exist
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data.model_dump(), f, ensure_ascii=False, indent=4, default=str)
            self.reload()  # Rebuild indexes after save
            self._update_timestamp()
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
# ======= data manipulation methods ========

    def create_task(self, title: str, section_name: str, description: str = "") -> Task:
        """Create a new task"""
        
        task = Task(title=title, description=description)
        self.add_task_to_section(task, section_name)
        return task
    
    def create_section(self, name: str) -> Section:
        """Create a new section (if it doesn't exist)"""
        if name in self.section_index:
            print(f"Section '{name}' already exists.")
            return self.section_index[name]
        
        section = Section(name=name)
        self.add_section(section)
        return section
    
    def add_task_to_section(self, task: Task, section_name: str):
        """Add task to a specific section"""
        section = self.get_section_by_name(section_name) or self.create_section(section_name)
        
        if not section:
            print(f"Section '{section_name}' not found and couldn't be created")
            return False
        
        section.add_task(task)
        
        self.add_section(section)
        self.save_to_file()
        return True
    
    def add_section(self, section: Section):
        """Add a new section"""
        self.data.sections.append(section)
        self.save_to_file()
    
    def remove_task_by_id(self, task_id: str) -> bool:
        """Remove task by ID"""
        # 1. Get task from index
        task = self.task_index.get(task_id)
        if not task:
            print(f"Task with ID {task_id} not found")
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
        section = self.section_index.get(section_name)
        if not section:
            print(f"Section '{section_name}' not found")
            return False
        # 2. Remove section from data
        self.data.sections.remove(section)
        self.save_to_file()
        print(f"Removed section: {section_name}")
        return True
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return self.task_index.get(task_id)
    
    def get_section_by_name(self, name: str) -> Optional[Section]:
        """Get section by name"""
        return self.section_index.get(name)
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return list(self.task_index.values())
    
    def get_all_sections(self) -> List[Section]:
        """Get all sections"""
        return list(self.section_index.values())
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks"""
        return [task for task in self.task_index.values() if task.completed]
    
    def _update_timestamp(self):
        """Update last modified timestamp"""
        self.data.last_updated = datetime.now()
    
    def reload(self):
        """Reload data from file"""
        self.load_from_file()
        self._build_indexes()
    
    def reset_to_default(self):
        """Reset data to default state"""
        self._create_default_file()
        self._build_indexes()