class GlobalConfig:
    _instance = None

    DATABASE = None
    COMMAND_PREFIX = ">"
    TIMEOUT = 20  # s
    MAX_WRONG_ANSWERS = 3
    FIELDS = ['word', 'translation', 'timestamp']

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def init_database(self, database: str) -> None:
        self.DATABASE = database
