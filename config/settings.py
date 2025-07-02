# This file store the app-wide constants eg: DB paths, modes, timezone
"""
Neuro_Sync -Application settings
This is the central configurationn file for our application...
"""

import os
from pathlib import Path
from datetime import datetime, timezone
import pytz # MOre concerned about timezone handling

# PROJECT PATHS
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
BACKUP_DIR = PROJECT_ROOT / "backup"
CACHE_DIR = PROJECT_ROOT / "cache"

# Create directories if they do not exist
for directory in [DATA_DIR, LOGS_DIR, BACKUP_DIR, CACHE_DIR]:
    directory.mkdir(exist_ok=True)

# DATABASE SETTINGS
DATABASE_PATH = DATA_DIR /"neuro_sync.db"
BACKUP_DATABASE_PATH = BACKUP_DIR / f"neuro_sync_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

# APPLICATION MODES
class AppModes:
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

# Current mode - can be overridden by the environment variable
APP_MODE = os.getenv("APP_MODE", AppModes.DEVELOPMENT)

#TIMEZONE AND DATE SETTINGS
DEFAULT_TIMEZONE = pytz.timezone("Africa/Nairobi")
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# AI SETTINGS
class AISettings:
    # Claude AI
    CLAUDE_MODEL= "claude-3-sonnet-20240229"
    CLAUDE_MAX_TOKENS = 1000
    CLAUDE_TEMPERATURE = 0.7

    # OpenAI GPT
    OPENAI_MODEL = "gpt-4"
    OPENAI_MAX_TOKENS = 1000
    OPENAI_TEMPERATURE = 0.7

    # Response caching
    CACHE_AI_RESPONSES = True
    CACHE_DURATION_HOURS = 24

# Gamification Settings
class GameSettings:
    # XP points
    TASK_COMPLETION_XP = 50
    HABIT_COMPLETE_XP = 5
    STREAK_BONUS_MULTIPLIER = 2
    CHALLENGE_COMPLETION_XP = 500

# NOTIFICATION SETTINGS
class NotificationSettings:
    EMAIL_REMINDER_HOURS = [4,6,9,11,13,15,17,19,21,23,24]
    DESKTOP_NOTIFICATION_DURATION = 5
    TELEGRAM_PARSE_MODE = "Markdown"
    DAILY_SUMMARY_TIME = "20.00" #8pm


#Schedule settings
class ScheduleSettings:
    DEFAULT_TASK_DURATION = 60
    POMODORO_DURATION = 30
    SHORT_BREAK = 5
    LONG_BREAK = 15

    # Back up frequency
    AUTO_BACKUP_HOURS = 6
    CLOUD_SYNC_MINUTES = 30


# LOGGING SETTINGS
class LogSettings:
    LOG_LEVEL = "INFO" if APP_MODE == AppModes.PRODUCTION else "DEBUG" # Simply do not debug during production
    LOG_FILE = LOGS_DIR /"neuro_sync.log"
    ERROR_LOG_FILE = LOGS_DIR / "error.log"
    AI_LOG_FILE = LOGS_DIR / "ai_operations.log"

    # Log rotation settings
    MAX_LOG_SIZE_MB = 10
    BACKUP_COUNT = 5

#WEB INTERFACE SETTINGS
class WebSettings:
    HOST = "127.0.0.1"
    PORT = 5000
    DEBUG = APP_MODE = AppModes.DEVELOPMENT
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "neuro-sync-dev-change-in-production")
#File limits
class FileLimits:
    MAX_EXPORT_RECORDS = 10000
    MAX_CACHE_SIZE_MB = 100
    MAX_BACKUP_FILES = 30

#Feature Flags
class Features:
    ENABLE_AI = True
    ENABLE_GAMIFICATION = True
    ENABLE_EMAIL_NOTIFICATIONS = True
    ENABLE_WEB_INTERFACE = True
    ENABLE_TELEGRAM_BOT = True
    ENABLE_GOOGLE_SYNC = True
    ENABLE_ANALYTICS = True

#Validation Rule
class validationRules:
    MIN_TASK_TITLE_LENGTH = 3
    MAX_TASK_TITLE_LENGTH = 100
    MIN_HABIT_TITLE_LENGTH = 3
    MAX_HABIT_TITLE_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 500

#Environment variables
def is_development():
    return APP_MODE == AppModes.DEVELOPMENT

def is_production():
    return APP_MODE == AppModes.PRODUCTION

def is_testing():
    return APP_MODE == AppModes.TESTING

def get_current_time():
    return datetime.now(DEFAULT_TIMEZONE)

def get_today_date():
    return get_current_time().date()


#CONFIGURATION VALIDATION
def validate_settings():
    #Validate configuration settings
    errors = []
    if not DATA_DIR.exists():
        errors.append(f"Data directory {DATA_DIR} does not exist.")

    if Features.ENABLE_AI and not (os.getenv("CLAUDE_API_KEY") or os.getenv("OPENAI_API_KEY")):
        errors.append("AI features enabled but no API keys found")
    if Features.ENABLE_TELEGRAM_BOT and not os.getenv("TELEGRAM_BOT_TOKEN"):
        errors.append("Telegram bot enabled but no token found")

    return errors
    


