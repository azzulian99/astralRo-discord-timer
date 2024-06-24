import logging

# Log configuration
LOG_LEVEL = logging.INFO
LOG_FILE = 'bot.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Exception codes
EXCEPTION_CODES = {
    'INVALID_FORMAT': 'Error 1001: Invalid format. Expected: -mvp add {code} {currentDeathTime} {coordinateX} {coordinateY} {optional int}',
    'INVALID_MVP_CODE': 'Error 1002: Invalid MVP code.',
    'COORDINATES_OUT_OF_BOUNDS': 'Error 1003: Coordinates must be between 0 and 499.',
    'INVALID_TIME_FORMAT': 'Error 1004: Invalid time format. Expected hh:mm or hh:mm:ss.',
    'INVALID_INDEX': 'Error 1005: Invalid index.'
}

COORDINATE_BOUNDS = 500

MVP_DATA_FILE = 'mvp_data.csv'
MVP_SCHED_FILE = 'mvp_sched.csv'
INTRO_MESSAGE = "Hello! I am (name TBD), your MVP bot timer."
