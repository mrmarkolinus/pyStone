from enum import Enum, auto

class MC_BLOCK_TYPE(Enum):
    OPAQUE = auto()
    TRANSPARENT = auto()

class MinecraftBlock:
    def __init__(self, block_type):
        self.block_type = block_type