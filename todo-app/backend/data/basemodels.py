from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime
import uuid

class TaskModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str
    description: str = ""
    completed: bool = False
    subtasks: List['TaskModel'] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class SectionModel(BaseModel):
    name: str
    tasks: List['TaskModel'] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class TodoModel(BaseModel):
    version: str = "1.0"
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    settings: Dict[str, Any] = Field(default_factory=dict)
    sections: List['SectionModel'] = Field(default_factory=list)
