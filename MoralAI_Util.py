import os, re, datetime

def init_game_file():
    if not os.path.exists('games'):
        os.makedirs('games')
    game_name = f"games/game_{datetime.datetime.now().strftime('%m-%d_%H-%M')}.txt"
    while os.path.exists(game_name):
        suffix_match = re.search(r"_(\d+)\.", game_name)
        if suffix_match:
            suffix = int(suffix_match.group(1)) + 1
            game_name = re.sub(r"_(\d+)\.", f"_{suffix}.", game_name)
        else:
            game_name = re.sub(r"\.", "_2.", game_name)
    with open(game_name, 'w'):
        pass
    return game_name

def init_grid():
    GRID_SIZE = 100  # 1 m = 100 cm (square grid)
    grid = [['_' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return grid

def set_cell(x, y, value):
    grid[y-1][x-1] = value

def grid_to_str(grid):
    result = ''
    header = "   "
    for i in range(1, 11):
        header += f"{i:20}"
    header += "\n"
    result += header
    # add rows
    for i, row in enumerate(grid):
        row_str = ' '.join(row)
        # pad row number with whitespace
        row_num_str = str(i+1)
        if i+1 < 10:
            row_num_str = ' ' + row_num_str
        if i == 99:
            result += f'{row_num_str} {row_str} {row_num_str}\n'
        else:
            result += f'{row_num_str}  {row_str} {row_num_str}\n'
    result += header
    return result

def print_grid_to_game_file(grid, game_name):
    with open(game_name, 'a') as f:
        print(grid_to_str(grid), file=f)