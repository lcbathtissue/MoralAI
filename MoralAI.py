# IMPORTS
import MoralAI_Util, MoralAI_Agent
from MoralAI_Config import GAME_CONFIG

# CONFIGURATION
GAME_CONFIG['verbose'] = False  # toggles extra print statements to see simulations internal state
GAME_CONFIG['white_space'] = "    "  # sets the indentation for print statements with 'tabs'
GAME_CONFIG['scenario_number'] = 2  # 1= 'Competition', 2= 'Collaboration', 3= 'Compassionate'
GAME_CONFIG['grid_size'] = 100  # 1 m = 100 cm (square grid)
GAME_CONFIG['num_agents'] = 5  # N
GAME_CONFIG['MAX_num_agents'] = 5  # MAX N
GAME_CONFIG['num_targets_per_agent'] = 5  # M
GAME_CONFIG['radar_reach'] = 1  # 3x3 grid ??
GAME_CONFIG['powered_moves'] = False

GAME_CONFIG['show_initial_positions'] = False

test_simulation = False

# INITIALIZATION
private_comms_enabled = None
show_initial_positions = GAME_CONFIG['show_initial_positions']
MoralAI_Util.enable_private_comms_if_allowed(GAME_CONFIG)
grid = None  # create a global variable for the grid that will be accessible by all required functions using 'global grid'
game_name = MoralAI_Util.init_game_file()  # create a unique name & file for the simulation
MoralAI_Util.check_game_config_validity(GAME_CONFIG)  # check validity of configuration, stop program if required
if not test_simulation:
    agents = MoralAI_Util.populate_N_agents(GAME_CONFIG['num_agents'])  # create N number of agents based off configuration 
    if show_initial_positions:
        MoralAI_Util.print_all_agents(agents)  # get the status of all initialized agents
    MoralAI_Util.populate_agent_targets(agents, GAME_CONFIG['num_targets_per_agent'], show_initial_positions)  # create NxM number of agents based off configuration 

    # print("\nMESSAGING TEST")
    agents[0].send_public_msg(["1, 2"])
    agents[1].send_public_msg(["3, 4"])
    agents[0].send_private_msg('B', ['5, 6'])
    agents[1].send_private_msg('C', ['7, 8'])

    # for agent in agents:
    #     print(agent.get_shared_coords())
else:
    grid = MoralAI_Util.init_grid()
    print(grid)

    test_agent = MoralAI_Agent.Agent('T', 99, 99)
    # print(test_agent.agent_to_string())

    # agent_a = MoralAI_Agent.Agent('A', 0, 0)
    # print(agent_a.agent_to_string())
    # agent_b = MoralAI_Agent.Agent('B', 5, 5)
    # print(agent_b.agent_to_string())

    # # agent A sends coordinates to agent B through private channel
    # agent_a.send_coordinates((1, 1), recipient='B')

    # # agent A sends coordinates to all agents through public channel
    # agent_a.send_coordinates((2, 2))

    # # agent B sends coordinates to agent A through private channel
    # agent_b.send_coordinates((6, 6), recipient='A')

    # # agent A receives coordinates from agent B's private channel
    # agent_a.receive_coordinates(sender='B')

    # # agent B receives coordinates from agent A's public channel
    # agent_b.receive_coordinates(sender=None)



# MoralAI_Util.print_grid_to_game_file(grid, game_name)
# print(MoralAI_Util.grid_to_str())
# MoralAI_Util.save_csv_file(None, f"{game_name}.csv")
# MoralAI_Util.generate_summary_csv("example_test_csv.csv", "test_csv_summary.csv")