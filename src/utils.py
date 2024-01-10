IS_BUSY = False


class BusyContextManager:
    @staticmethod
    def is_busy():
        return IS_BUSY

    def __enter__(self):
        global IS_BUSY
        if IS_BUSY:
            raise RuntimeError("Resource is already busy.")
        IS_BUSY = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        global IS_BUSY
        IS_BUSY = False
