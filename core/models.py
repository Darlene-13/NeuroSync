"""
Neuro_SYnc - Database Models
Core data structure for Tasks, Habiys, Users, Finance and Gamification.
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
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

#USER MODELS
@dataclass
class User:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str 
    email: str
    created_at:datetime = field(default_factory=datetime.now())
    last_active: datetime = field(default_factory=datetime.now())
    timezone: str = "Africa/Nairobi"

    def __post_init__(self):
        self.created_at = datetime.now() if self.created_at is None else self.created_at
        self.last_active = datetime.now() if self.last_active is None else self.last_active
        self.timezone = self.timezone if self.timezone else "Africa/Nairobi"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "timezone": self.timezone
        }
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=data.get("id"),
            name=data["name"],
            email=data["email"],
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            last_active=datetime.fromisoformat(data["last_active"]) if data.get("last_active") else None,
            timezone=data.get("timezone", "Africa/Nairobi")
        )
    def is_active(self):
        return (datetime.now() - self.last_active) < timedelta(days=30)

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
@dataclass
class Habit:
    id: str = field(default_factory=lambda: str (uuid.uuid4()))
    user_id: str
    title: str
    description: Optional[str] = None
    frequency: HabitFrequency = HabitFrequency.DAILY
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now())
    updated_at: datetime = field(default_factory=datetime.now())
    target_streak: int = 0
    current_streak: int = 0
    best_streak: int = 0
    last_completed: Optional[datetime] = None

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.start_date is None:
            self.start_date = datetime.now()
        if self.end_date is None:
            self.end_date = datetime.now() + timedelta(days=365)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "frequency": self.frequency.value,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "target_streak": self.target_streak,
            "current_streak": self.current_streak,
            "best_streak": self.best_streak,
            "last_completed": self.last_completed.isoformat() if self.last_completed else None
        }
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=data.get("id"),
            user_id=data["user_id"],
            title=data["title"],
            description=data.get("description"),
            frequency=HabitFrequency(data["frequency"]),
            start_date=datetime.fromisoformat(data["start_date"]) if data.get("start_date") else None,
            end_date=datetime.fromisoformat(data["end_date"]) if data.get("end_date") else None,
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            target_streak=data.get("target_streak", 0),
            current_streak=data.get("current_streak", 0),
            best_streak=data.get("best_streak", 0),
            last_completed=datetime.fromisoformat(data["last_completed"]) if data.get("last_completed") else None
        )
    def complete(self):
        """ Mark habit as completed for the day and updating streaks."""
        if self.last_completed and self.last_completed.date() == datetime.now().date():
            return
        self.last_completed = datetime.now()
        self.current_streak += 1
        if self.current_streak > self.best_streak:
            self.best_streak = self.current_streak
        self.updated_at = datetime.now()

# FINANCE MODELS
@dataclass
class FinanceRecord:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    amount: float
    category: FinanceCategory
    description: Optional[str] = None
    source: str = ""
    date: datetime = field(default_factory=datetime.now())
    created_at: datetime = field(default_factory=datetime.now())
    amount: float = 0.0
    transaction_date: datetime = field(default_factory=datetime.now())
    is_income: bool = False
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.transactiom_date is None:
            self.transaction_date = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "category": self.category.value,
            "description": self.description,
            "date": self.date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "transaction_date": self.transaction_date.isoformat(),
            "is_income": self.is_income,
            "tags": json.dumps(self.tags)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls (
            id=data.get("id"),
            user_id=data["user_id"],
            amount=data["amount"],
            category=FinanceCategory(data["category"]),
            description=data.get("description"),
            date=datetime.fromisoformat(data["date"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            transaction_date=datetime.fromisoformat(data["transaction_date"]),
            is_income=data.get("is_income", False),
            tags=json.loads(data.get("tags", "[]"))
        )
    
    def is_recent(self):
        # Check if the record is within the last 30 days
        return self.transaction.date >= datetime.now() - timedelta(days =30)
    
    def is_income(self):
        return self.category ==FinanceCategory.INCOME
    
#XP MODELS
@dataclass
class XPEntry:
    id: str = field(default_factory=lambda: str(uuid.uuuid4))
    description: str
    user_id: str
    source: XPSource
    points: int
    earned_date: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now
        if self.earned_date is None:
            self.earned_date = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "user_id": self.user_id,
            "source": self.source.value,
            "points": self.points,
            "earned_date": self.earned_date.isoformat(),
            "created_at": self.created_at.isoformat()
        }
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=data.get("id"),
            description=data["description"],
            user_id=data["user_id"],
            source=XPSource(data["source"]),
            points=data["points"],
            earned_date=datetime.fromisoformat(data["earned_date"]),
            created_at=datetime.fromisoformat(data["created_at"])
        )
    def is_recent(self):
        return self.earned_date >= datetime.now() - timedelta(days=30)

# ACHIEVEMENT MODELS  
@dataclass
class Achievement:
    id: str = field(default_category=lambda: str(uuid.uuid4))
    user_id: str
    title: str
    description: Optional[str] = None
    points: int = 0
    date_earned: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    unlock_condition: Optional[str] = None
    is_unlocked: bool = False

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.date_earned is None:
            self.date_earned = datetime.now()
        if self.unlock_condition is None:
            self.unlock_condition = "Default Condition"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "points": self.points,
            "date_earned": self.date_earned.isoformat(),
            "created_at": self.created_at.isoformat(),
            "unlock_condition": self.unlock_condition,
            "is_unlocked": self.is_unlocked
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=data.get("id"),
            user_id=data["user_id"],
            title=data["title"],
            description=data.get("description"),
            points=data.get("points", 0),
            date_earned=datetime.fromisoformat(data["date_earned"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            unlock_condition=data.get("unlock_condition", "Default Condition"),
            is_unlocked=data.get("is_unlocked", False)
        )
    def unlock(self):
        """ Mark achievement as unlocked."""
        self.is_unlocked = True
        self.date_earned = datetime.now()
        self.created_at = datetime.now()    
    def is_recent(self):
        """ Check if the achievement was earned within the last 30 days."""
        return self.date_earned >= datetime.now() - timedelta(days=30)
    
if __name__ == "__main__":
    print(" Neuro Sync Model Configuration and testing")
    # Example usage
    user = User(name= "Darlene Wendie", email = "darlenewendie@gmail.com")
    print("User Created:", user.to_dict())
    task = Task(user_id=user.id, title="Complete Jerry's Work", description="Finish the assignment before due date")
    print("Task Created:", task.to_dict())
    habit = Habit(user_id=user.id, title="Daily Meditation", frequency=HabitFrequency.DAILY)
    print("Habit Created:", habit.to_dict())
    finance_record = FinanceRecord(user_id=user.id, amount=100.0, category=FinanceCategory.INCOME, description="Freelance Work")
    print("Finance Record Created:", finance_record.to_dict())
    xp_entry = XPEntry(user_id=user.id, description="Completed Task", source=XPSource.TASK_COMPLETION, points=10)
    print("XP Entry Created:", xp_entry.to_dict())
    achievement = Achievement(user_id=user.id, title="First Task Completed", description="Awarded for completing the first task.")
    print("Achievement Created:", achievement.to_dict())

    # Example 2 with a different user
    user2 = User(name= "Stacy Phanince", email = "stacyjuma018@gmail.com")
    print("User 2 created:", user2.to_dict())
    task2 = Task(user_id=user2.id, title= 'Complete KRA Certification', description="Finish the KRA certification before the deadline")
    print("Task 2 Created:", task2.to_dict())
    habit2 = Habit(user_id=user2.id, title="Weekly Review", frequency=HabitFrequency.WEEKLY)
    print("Habit 2 Created:", habit2.to_dict())
    finance_record2 = FinanceRecord(user_id=user2.id, amount=200.0,category=FinanceCategory.EXPENSE, description="Monthly Subscription")
    print("Finance Record 2 Created:", finance_record2.to_dict())
    xp_entry2 = XPEntry(user_id=user2.id, description="Habit Completed", source=XPSource.HABIT_COMPLETION, points=5)
    print("XP Entry 2 created:", xp_entry2.to_dict())
    achievement2 = Achievement(user_id=user2.id, title="First Habit Completed", description="Awarded for completing the first habit.")
    print("Achievement 2 Created:", achievement2.to_dict())


    print("ALl model created successfully!")

