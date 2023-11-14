from enum import Enum, auto
import numpy as np

class RedstoneConstants(Enum):
    MAX_POWER = 15
    INPUT_POWER_UNKNOWN = -1
    REPEATER_STANDARD_TICKS_DELAY = 2
    STANDARD_AOE = 1

#define the orientation of the redstone component inputs and outputs. 
# A redstone component is oriented in the direction of its output.
# Its inputs are oriented relative to its output.
# Example:  A repeater which output is facing NORTH is oriented NORTH
#           Its inputs are SOUTH (main input) and EAST or WEST (repetear or comparator locking the repeater)
class OrizontalSpaceOrientation(Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3
    DONT_CARE = 4

# Source: https://minecraft.fandom.com/wiki/Redstone_components
class RedstoneComponentUniqueID(Enum):
    # DEFAULT
    INVALID_ID = auto()

    # Power components
    REDSTONE_BLOCK = auto()
    STONE_BUTTON = auto()
    WOOD_BUTTON = auto()
    CALIBRATED_SCULK_SENSOR = auto()
    CHISELED_BOOKSHELF = auto()
    DAYLIGHT_DETECTOR = auto()
    DETECTOR_RAIL = auto()
    JUKEBOX = auto()
    LECTERN = auto()
    LEVER = auto()
    LIGHTNING_ROD = auto()
    OBSERVER = auto()
    PRESSURE_PLATE = auto()
    REDSTONE_TORCH = auto()
    SCULK_SENSOR = auto()
    TARGET_BLOCK = auto()
    TRAPPER_CHEST = auto()
    TRIPWIRE_HOOK = auto()

    # Transmission components
    REDSTONE_DUST = auto()
    REDSTONE_REPEATER = auto()
    REDSTONE_COMPARATOR = auto()

    # Mechanism components
    ACTIVATOR_RAIL = auto()
    BELL = auto()
    DISPENSER = auto()
    DOOR = auto()
    DRAGON_HEAD = auto()
    DROPPER = auto()
    FENCE_GATE = auto()
    HOPPER = auto()
    NOTE_BLOCK = auto()
    PISTON = auto()
    POWERED_RAIL = auto()
    RAIL = auto()
    REDSTONE_LAMP = auto()
    TNT = auto()
    TRAPDOOR = auto()
    COMMAND_BLOCK = auto()
    STRUCTURE_BLOCK = auto()

    # Mobile components
    MINECART = auto()
    MINECART_WITH_CHEST = auto()
    MINECART_WITH_COMMAND_BLOCK = auto()
    MINECART_WITH_FURNACE = auto()
    MINECART_WITH_HOPPER = auto()
    MINECART_WITH_TNT = auto()

class RedstoneComponent:
    def __init__(   self, 
                    area_of_effect=RedstoneConstants.STANDARD_AOE.value, 
                    orientation=OrizontalSpaceOrientation.DONT_CARE, 
                    component_id=RedstoneComponentUniqueID.INVALID_ID):
        
        # a redstone component affecting only the blocks directly next to him will have an area of effect of 1
        # the area of effect is represented by a matrix of size area_of_effect*2+1 = 3x3
        # the matrix is centered around the component. For a Repeater oriented NORTH, the output matrix will be:
        # 0 15 0
        # 0 0 0
        # 0 0 0
        area_of_effect_matrix_size = area_of_effect*2+1
        self.input_power = np.zeros((area_of_effect_matrix_size, area_of_effect_matrix_size), dtype=int)
        self.input_component_id = np.zeros((area_of_effect_matrix_size, area_of_effect_matrix_size), dtype=int)
        self.output_power = np.zeros((area_of_effect_matrix_size, area_of_effect_matrix_size), dtype=int)
        self.orientation = orientation
        self.component_id = component_id
        self.area_of_effect = area_of_effect
        self.aoe_size = area_of_effect_matrix_size

        self.configure_input_matrix()
        self.configure_output_matrix()

    def configure_input_matrix(self):
        pass


    def configure_output_matrix(self):
        if self.orientation == OrizontalSpaceOrientation.DONT_CARE or self.orientation == OrizontalSpaceOrientation.NORTH:
            for dz in range(0, self.area_of_effect):
                self.output_power[dz][self.area_of_effect] = RedstoneConstants.MAX_POWER.value

        if self.orientation == OrizontalSpaceOrientation.DONT_CARE or self.orientation == OrizontalSpaceOrientation.SOUTH:
            for dz in range(self.area_of_effect + 1, self.aoe_size):
                self.output_power[dz][self.area_of_effect] = RedstoneConstants.MAX_POWER.value
        
        if self.orientation == OrizontalSpaceOrientation.DONT_CARE or self.orientation == OrizontalSpaceOrientation.WEST:
            for dx in range(0, self.area_of_effect):
                self.output_power[self.area_of_effect][dx] = RedstoneConstants.MAX_POWER.value

        if self.orientation == OrizontalSpaceOrientation.DONT_CARE or self.orientation == OrizontalSpaceOrientation.EAST:
            for dx in range(self.area_of_effect + 1, self.aoe_size):
                self.output_power[self.area_of_effect][dx] = RedstoneConstants.MAX_POWER.value

    def set_input(self, power_level):
        """ Set the input power level for the component. """
        self.input_power = power_level

    def update(self):
        """ Update the component state for each tick. """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_output(self):
        """ Get the current output power level of the component. """
        return self.output_power

class RedstoneBlock(RedstoneComponent):
    def __init__(self):
        super().__init__(orientation=OrizontalSpaceOrientation.DONT_CARE, component_id=RedstoneComponentUniqueID.REDSTONE_BLOCK)


class Repeater(RedstoneComponent):
    def __init__(self, orientation, delay_ticks=RedstoneConstants.REPEATER_STANDARD_TICKS_DELAY):
        super().__init__(   orientation=orientation, 
                            component_id=RedstoneComponentUniqueID.REDSTONE_REPEATER
                        )

        self.delay_ticks = delay_ticks
        self.timer = delay_ticks

        self.configure_input_matrix()

    def configure_input_matrix(self):
        input_matrix = np.zeros((3, 3), dtype=int)

        if self.orientation == OrizontalSpaceOrientation.NORTH:
            input_matrix[2][1] = RedstoneConstants.INPUT_POWER_UNKNOWN.value
        elif self.orientation == OrizontalSpaceOrientation.SOUTH:
            input_matrix[0][1] = RedstoneConstants.INPUT_POWER_UNKNOWN.value
        elif self.orientation == OrizontalSpaceOrientation.WEST:
            input_matrix[1][2] = RedstoneConstants.INPUT_POWER_UNKNOWN.value
        elif self.orientation == OrizontalSpaceOrientation.EAST:
            input_matrix[1][0] = RedstoneConstants.INPUT_POWER_UNKNOWN.value

        super().configure_input_matrix()
    

    def update(self):
        pass

    def set_input(self, power_level):
        super().set_input(power_level)
        self.timer = self.delay_ticks
        
        
# repeater_test_north = Repeater(OrizontalSpaceOrientation.NORTH)
# repetear_test_south = Repeater(OrizontalSpaceOrientation.SOUTH)
# repeater_test_west = Repeater(OrizontalSpaceOrientation.WEST)
# repeater_test_east = Repeater(OrizontalSpaceOrientation.EAST)

# redstone_block = RedstoneBlock()

# print("OK")