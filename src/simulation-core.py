import numpy as np
import redstone_components as rc

# Block types TODO: as enum, categorize all possible blocks
AIR = 0
REDSTONE_WIRE = 1
REDSTONE_TORCH = 2

class Simulation:
    def __init__(self, 
                 max_simulation_ticks, 
                 simulation_matrix_size,
                 redstone_schematics,
                 blocks_orientation):
        
        self.max_simulation_ticks = max_simulation_ticks
        self.simulation_matrix_size = simulation_matrix_size
        self.simulation_block_matrix = redstone_schematics
        self.simulation_block_orientation_matrix = blocks_orientation
        self.simulation_redstone_power_matrix = np.zeros((simulation_matrix_size, simulation_matrix_size, simulation_matrix_size), dtype=int)

        self.initial_setup()

    def initial_setup(self):
        for y in range(self.simulation_matrix_size):
            for x in range(self.simulation_matrix_size):
                for z in range(self.simulation_matrix_size):
                    self.set_initial_power_levels(self.simulation_block_matrix[x][z][y], [x, z, y])
                    self.create_dependency_graph([x, z, y])

    def set_initial_power_levels(self, block, indexes): 
        current_x = indexes[0]
        current_z = indexes[1]
        current_y = indexes[2]
        if block == rc.RedstoneComponentUniqueID.REDSTONE_BLOCK.value:
            self.simulation_redstone_power_matrix[current_x][current_z][current_y] = rc.RedstoneConstants.MAX_POWER.value

    def create_dependency_graph(self, indexes):
        current_x = indexes[0]
        current_z = indexes[1]
        current_y = indexes[2]
        redstone_block = self.create_redstone_object(   self.simulation_block_matrix[current_x][current_z][current_y], 
                                                        self.simulation_block_orientation_matrix[current_x][current_z][current_y])
        
        area_of_dependency_matrix = self.simulation_block_matrix[   current_x - redstone_block.area_of_effect:current_x + redstone_block.area_of_effect, 
                                                                    current_z - redstone_block.area_of_effect:current_z + redstone_block.area_of_effect,
                                                                    current_y - redstone_block.area_of_effect:current_y + redstone_block.area_of_effect]
        print("OK")

    def create_redstone_object(self, block_id, block_orientation):
        #TODO: extend for all possible redstone blocks
        if block_id == rc.RedstoneComponentUniqueID.REDSTONE_BLOCK.value:
            return rc.RedstoneBlock()
        elif block_id == rc.RedstoneComponentUniqueID.REDSTONE_REPEATER.value:
            return rc.Repeater(orientation=block_orientation)

    def run(self):
        for tick in range(1, self.max_simulation_ticks):
            pass
        # Copy the state from the last tick
        # current_block_matrix = time_series_blocks[tick - 1].copy()
        # current_power_matrix = time_series_power[tick - 1].copy()

        # # Update the state for the current tick
        # for y in range(HEIGHT):
        #     for x in range(WIDTH):
        #         for z in range(DEPTH):
        #             update_power_level(current_block_matrix, current_power_matrix, x, y, z)

        # # Store the state in the time series
        # time_series_blocks.append(current_block_matrix)
        # time_series_power.append(current_power_matrix)


# TEST
test_size_x_z = 5
# test_size_y = 1 keep it simple for the first test
redstone_test_schematic = np.zeros((test_size_x_z, test_size_x_z, test_size_x_z), dtype=int)
redstone_test_schematic_block_orientation = np.zeros((test_size_x_z, test_size_x_z, test_size_x_z), dtype=int)

redstone_test_schematic[0][0][0] = rc.RedstoneComponentUniqueID.REDSTONE_BLOCK.value
redstone_test_schematic_block_orientation[0][0][0] = rc.OrizontalSpaceOrientation.DONT_CARE.value
redstone_test_schematic[0][1][0] = rc.RedstoneComponentUniqueID.REDSTONE_REPEATER.value
redstone_test_schematic_block_orientation[0][1][0] = rc.OrizontalSpaceOrientation.SOUTH.value

model = Simulation(100, 5, redstone_test_schematic, redstone_test_schematic_block_orientation)