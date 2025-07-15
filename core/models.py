"""
Neuro_SYnc - Database Models
Core data structure for Tasks, Habiys, Users, Finance and Gamification.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
import uuid
import json

# ENUMS FOR STATUS VALUES
class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PAUSED = "paused"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class HabitFrequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    CUSTOM = "custom"

class FinanceCategory(Enum):
    INCOME = "income"
    EXPENSE = "expense"
    FOOD = "food"
    INVESTMENT = "investment"
    ENTERTAINMENT = "entertainment"
    EDUCATION = "education"
    HEALTH = "health"
    TRANSPORT = "transport"
    UTILITIES = "utilities"
    MISCELLANEOUS = "miscellaneous"
    SAVINGS = "savings"
    DEBT = "debt"
    OTHER = "other"

class XPSource(Enum):
    TASK_COMPLETION = "task_completion"
    HABIT_COMPLETION = "habit_completion"
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    CHALLENGE_COMPLETED = "challenge_completed"
    STREAK_BONUS = "streak_bonus"


# TASK MODELS
@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    estimated_duration: Optional[int] = None  # in minutes
    actual_duration: Optional[int] = None
    completed_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now
        if self.tags is None:
            self.tags = []

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "estimated_duration": self.estimated_duration,
            "actual_duration": self.actual_duration,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "tags": json.dumps(self.tags)
        }
    
    @classmethod
    def from_dict(cls, data:Dict[str, Any]):
        return cls(
            id=data.get("id"),
            user_id=data["user_id"],
            title=data["title"],
            description=data.get("description"),
            status=TaskStatus(data["status"]),
            priority=TaskPriority(data["priority"]),
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            estimated_duration=data.get("estimated_duration"),
            actual_duration=data.get("actual_duration"),
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
            tags=json.loads("tags", [])
        )
    
    def is_overdue(self):
        """ Check if the task is overdue based on the due date."""
        if self.due_date and self.status != TaskStatus.COMPLETED:
            return datetime.now() > self.due_date
        return False
    
    def complete(self):
        """ Mark task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()

#HABIT MODELS