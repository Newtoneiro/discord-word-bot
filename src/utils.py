from dataclasses import dataclass


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


@dataclass
class Word:
    word_eng: str
    word_pl: str
    timestamp: float
    no_correct: int
    no_wrong: int

    def __hash__(self):
        # Creating a hash based on the hash of the concatenated values
        return hash(
            (
                self.word_eng,
                self.word_pl,
                self.timestamp,
                self.no_correct,
                self.no_wrong
            )
        )


def get_word_weight(word: Word) -> int:
    """
    Returns the weight of the word.
    """
    weight = (word.no_wrong + 1) / (word.no_correct + 1)
    return weight
