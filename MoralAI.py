import MoralAI_Util, MoralAI_Agent
from MoralAI_Config import GAME_CONFIG
GAME_CONFIG['powered_moves'] = True

game_name = MoralAI_Util.init_game_file()
grid = MoralAI_Util.init_grid()

# print(game_name)
# MoralAI_Util.print_grid_to_game_file(grid, game_name)
# print(MoralAI_Util.grid_to_str(grid))

agent1 = MoralAI_Agent.Agent('A')
print(agent1.agent_to_string())  # Output: Agent A: Position (0, 0), Power level: 100
