# IMPORTS
import MoralAI_Util, MoralAI_Agent
from MoralAI_Config import GAME_CONFIG

# CONFIGURATION
GAME_CONFIG['powered_moves'] = False
GAME_CONFIG['num_agents'] = 5
GAME_CONFIG['MAX_num_agents'] = 5
GAME_CONFIG['radar_reach'] = 1

# INITIALIZATION
MoralAI_Util.check_game_config_validity(GAME_CONFIG)
agents = MoralAI_Util.populate_N_agents(MoralAI_Util.init_grid(), GAME_CONFIG['num_agents'])
MoralAI_Util.print_all_agents(agents)
game_name = MoralAI_Util.init_game_file()

# print(game_name)
# MoralAI_Util.print_grid_to_game_file(grid, game_name)
# print(MoralAI_Util.grid_to_str(grid))
# print(agent1.agent_to_string())  # Output: Agent A: Position (0, 0), Power level: 100

# agent1 = MoralAI_Agent.Agent('A')
# rnd_x, rnd_y = MoralAI_Util.get_random_empty_cell(grid)
# grid = MoralAI_Util.set_cell(grid, rnd_x, rnd_y, 'X')