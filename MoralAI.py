import MoralAI_Util

game_name = MoralAI_Util.init_game_file()
grid = MoralAI_Util.init_grid()
print(game_name)

MoralAI_Util.print_grid_to_game_file(grid, game_name)
# print(grid_to_str())


