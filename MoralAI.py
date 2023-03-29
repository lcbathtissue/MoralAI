# IMPORTS
import MoralAI_Util, MoralAI_Agent
from MoralAI_Config import GAME_CONFIG

# CONFIGURATION
GAME_CONFIG['verbose'] = False  # toggles extra print statements to see simulations internal state
GAME_CONFIG['white_space'] = "    "  # sets the indentation for print statements with 'tabs'
GAME_CONFIG['grid_size'] = 100  # 1 m = 100 cm (square grid)
GAME_CONFIG['num_agents'] = 5  # N
GAME_CONFIG['MAX_num_agents'] = 5  # MAX N
GAME_CONFIG['num_targets_per_agent'] = 5  # M
GAME_CONFIG['radar_reach'] = 1  # 3x3 grid ??
GAME_CONFIG['powered_moves'] = False

# INITIALIZATION
grid = None  # create a global variable for the grid that will be accessible by all required functions using 'global grid'
game_name = MoralAI_Util.init_game_file()  # create a unique name & file for the simulation
MoralAI_Util.check_game_config_validity(GAME_CONFIG)  # check validity of configuration, stop program if required
agents = MoralAI_Util.populate_N_agents(GAME_CONFIG['num_agents'])  # create N number of agents based off configuration 
MoralAI_Util.print_all_agents(agents)  # get the status of all initialized agents
MoralAI_Util.populate_agent_targets(agents, GAME_CONFIG['num_targets_per_agent'])  # create NxM number of agents based off configuration 

# test_agent = MoralAI_Agent.Agent('T', 99, 99)
# print(test_agent.agent_to_string())

# MoralAI_Util.print_grid_to_game_file(grid, game_name)
# print(MoralAI_Util.grid_to_str())

