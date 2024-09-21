from .color import Style

s = Style()
class ALineError(Exception):
    """
    Main class exception
    """

class PrintModeNotFoundError(ALineError):
    def __init__(self, mode: str):

        super().__init__(f"Unexpected {s.color_arg(mode, s.CYAN)} in infos print-mode")