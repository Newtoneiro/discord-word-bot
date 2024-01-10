import os

DATABASE = os.environ['STORAGE_PATH']
COMMAND_PREFIX = ">"
TIMEOUT = 20  # s
MAX_WRONG_ANSWERS = 3
FIELDS = ['word', 'translation', 'timestamp']
