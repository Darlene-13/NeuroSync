"""
Database configuration  settings for the application.
"""

import sqlite3
from pathlib import Path
from .settings import DATABASE_PATH, APP_MODE, AppModes
from datetime import datetime

#DATABASE SETTINGS
class DatabaseConfig:
    # Main database file
    DATABASE_PATH = DATABASE_PATH

    #Connection settings
    TIMEOUT = 30.0
    CHECK_SAME_THREAD = False

    #SQLite pragrams for performance and reliability
    PRAGMAS = {
        "journal_mode": "WAL", # write ahead logging for better accuracy
        "synchronous": "NORMAL", #Balance between safety and speed
        "cache_size": "10000",# 10MB Cache
        "temp_store": "memory", #Store temporary tables in memory
        "mmap_size": "268435456", # 256 memory_mapped I/0
        "foreign_keys": "ON", # Enalbe foreign key contraints
        "auto_vacuum": "FULL"
    }

    # Development vs production settings
    if APP_MODE == AppModes.DEVELOPMENT:
        PRAGMAS["synchronous"] = "OFF"  # Faster writes in development
    elif APP_MODE == AppModes.PRODUCTION:
        PRAGMAS["synchronous"] = "FULL"  # Full safety in production


#CONNECTION HELPERS 
def get_connection_string():
    "'Get SQLite connection string for the database."
    return f"sqlite:///{DATABASE_PATH}"

def get_raw_connection():
    """ Get raw sqlite3 connection with optimized settings"""
    conn = sqlite3.connect(
        DATABASE_PATH,
        timeout=DatabaseConfig.TIMEOUT,
        check_same_thread=DatabaseConfig.CHECK_SAME_THREAD
    )

    # Apply for pragmas for performance
    for pragma, value in DatabaseConfig.PRAGMAS.items():
        conn.execute(f" PRAGMA {pragma} = {value}")
        
    # Enable row factory for dict like access
    conn.row_factory = sqlite3.Row

    return conn

def apply_pragmas(connection):
    """ Apply database pragmas to an existing connection."""

    cursor = connection.cursor()
    for pragma, value in DatabaseConfig.PRAGMAS.items():
        cursor.execute(f"PRAGMA {pragma} = {value}")
    cursor.close()

# DATABASE SCHEMA VERSION
class SchemaConfig:
    """ Datavase schema versioning settings."""
    CURRENT_VERSION = 1
    VERSION_TABLE = "schema_version"

    # Schema migration settings ( for future versions)
    MIGRATIONS = {
        1: "initial_schema.sql",

        # Add future migfrations here...


    }
    
# TABLE DEFINITIONS
class TableDefinitions:
    # Core tables
    USERS = "users"
    TASKS = "tasks"
    HABITS = "habits"
    FINANCE = "finance_entries"

    # Gamification tables
    XP_LOG = "xp_log"
    ACHIEVEMENTS = "achievements"
    CHALLENGES = "challenges"

    # AI Tables
    AI_MODELS = "ai_models" 
    AI_CONVERSATIONS = "ai_conversations"


# QUERY OPTIMIZATION
class QueryConfig:
    # Batch sizes for bulk operations
    BATCH_SIZE = 1000

    # Query timeouts
    DEFAULT_TIMEOUT = 30.0
    BULK_OPERATIONS_TIMEOUT = 60.0

    # Indexing strategy
    INDEXES = [
        # Tasks indexes
        "CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)",
        "CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date)",
        "CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)",
        
        # Habits indexes
        "CREATE INDEX IF NOT EXISTS idx_habits_user_id ON habits(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_habits_active ON habits(is_active)",
        
        # Finance indexes
        "CREATE INDEX IF NOT EXISTS idx_finance_date ON finance_entries(transaction_date)",
        "CREATE INDEX IF NOT EXISTS idx_finance_category ON finance_entries(category)",
        
        # XP indexes
        "CREATE INDEX IF NOT EXISTS idx_xp_user_date ON xp_log(user_id, earned_date)",
        
        # AI cache indexes
        "CREATE INDEX IF NOT EXISTS idx_ai_cache_key ON ai_cache(cache_key)",
        "CREATE INDEX IF NOT EXISTS idx_ai_cache_created ON ai_cache(created_at)",
    ]

# BACKUP CONFIGURATION
class BackupConfig:
    """ Settings for database backups. """
    AUTO_BACKUP_ENABLED = True
    BACK_UP_INTERVAL = 86400 # 24 hours in seconds
    BACKUP_RETENTION_DAYS = 30

    # Backup file naming
    BACKUP_PREFIX = "neuro_sync_backup"
    BACKUP_DIR = Path("backups")

    # Backup triggers
    BACKUP_ON_STARTUP = True
    BACKUP_ON_SHUTDOWN = True
    BACKUP_INTERVAL_HOURS = 6


# Database Utilities
def created_backup_name():
    """ Generate a backup file name with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{BackupConfig.BACKUP_PREFIX}_{timestamp}-{BackupConfig.BACKUP_EXTENSION}"

def get_database_size():
    """ Get the size of the database file in bytes."""
    if DATABASE_PATH.exists():
        size_bytes = DATABASE_PATH.stat().st_size
        return round(size_bytes / (1024*1024), 2) # Convert to MB
    return 0

def check_database_exists():
    return DATABASE_PATH.exists()
def get_database_info():
    """ Get basic information about the database."""
    return {
        "path": str(DATABASE_PATH),
        "exists": check_database_exists(),
        "size_mb": get_database_size(),
        "pragmas": DatabaseConfig.PRAGMAS,
        "schema_version": SchemaConfig.CURRENT_VERSION

    }


#CONNETION TESTING

def test_connection():
    try:
        conn = get_raw_connection
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False
    
if __name__ == "__main__":
    # Database configuration test
    print("Neuro Sync Database Configuration")
    print( "=" * 40)

    info = get_database_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    
    print(f"\nConnection test:{ 'Pass if test_connection() else "FAIL'}")
    print(f"Backup enabled: {'Yes' if BackupConfig.AUTO_BACKUP_ENABLED else 'No'}")