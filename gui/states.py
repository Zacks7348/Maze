from enum import Enum

class AppState(Enum):
    HOME = 0
    GENERATING = 1
    MAZE = 2
    SOLVING = 3