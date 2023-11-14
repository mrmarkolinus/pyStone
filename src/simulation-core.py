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
                 redstone_schematics):
        
        self.max_simulation_ticks = max_simulation_ticks
        self.simulation_matrix_size = simulation_matrix_size
        self.simulation_block_matrix = redstone_schematics
        self.simulation_redstone_power_matrix = np.zeros((simulation_matrix_size, simulation_matrix_size, simulation_matrix_size), dtype=int)

        self.set_initial_power_levels()

    def set_initial_power_levels(self):
        for y in range(self.simulation_matrix_size):
            for x in range(self.simulation_matrix_size):
                for z in range(self.simulation_matrix_size):
                    if self.simulation_block_matrix[x][z][y] == rc.RedstoneComponentUniqueID.REDSTONE_BLOCK.value:
                        self.simulation_redstone_power_matrix[x][z][y] = rc.RedstoneConstants.MAX_POWER.value

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
redstone_test = np.zeros((5, 5, 5), dtype=int)
redstone_test[0][0][0] = rc.RedstoneComponentUniqueID.REDSTONE_BLOCK.value
redstone_test[0][1][0] = rc.RedstoneComponentUniqueID.REDSTONE_REPEATER.value

model = Simulation(100, 5, redstone_test)