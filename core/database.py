"""
Database module for Neuro_Sync, providing an interface to interact with the underlying data storage.
This module defines the core data structures and enums used throughout the application.
"""
import json
from dataclasses import dataclass, field # This import is neccessary for tasks and other structure definitions
from datetime import datetime, timedelta
from enum import Enum
import sqlite3
from typing import Optional, List, Dict, Any
import uuid
from pathlib import Path
from contextlib import contextmanager # This import is important in managing database connections

from .models import Task, Habit, User, FinanceRecord, Achievement, XPEntry

#DATABASE SCHEMA
SCHEMA_SQL = """
--Users table
CREATE TABLE IF NOT EXISTS users (
    id TEST PRIMARY KEY,
    name TEST NOT NULL,
    email TEXT
    timezone TEXT NOT NULL,
    created_at TEXT NOT NULL,
    lat_active TEXT NOT NULL,
    );   
    
--Tasks table (
CREATE TABLE IF NOT EXISTS tasks
    id TEXT PRIMARY KEY, 
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    due_date TEXT,
    status TEST NOT NULL DEFAULT 'pending'
    priority TEXT NOT NULL DEFAULT 'medium'
    due_dat TEXT,
    created_at TEXT NOT NULL,
    estimated_duration INTEGER,
    actual_duration INTEGER,
    complete_at TEXT,
    );

--Habits table(
CREATE TABLE IF NOT EXISTS habits (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,)
)
    
    
    
    """
