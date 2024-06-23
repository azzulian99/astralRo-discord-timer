import logging

# Log configuration
LOG_LEVEL = logging.DEBUG
LOG_FILE = 'bot.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Exception codes
EXCEPTION_CODES = {
    'INVALID_FORMAT': 1001,
    'INVALID_MVP_CODE': 1002,
    'COORDINATES_OUT_OF_BOUNDS': 1003,
    'INVALID_TIME_FORMAT': 1004,
    'INVALID_INDEX': 1005
}

MVP_DATA_FILE = 'mvp_data.csv'
MVP_SCHED_FILE = 'mvp_sched.csv'
INTRO_MESSAGE = "Hello! I am RAGNAROK-HUNTER, your MVP timer bot."
