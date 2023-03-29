import os, re, datetime, random, MoralAI_Agent
from MoralAI_Config import GAME_CONFIG

def check_game_config_validity(GAME_CONFIG):
    if GAME_CONFIG['num_agents'] > GAME_CONFIG['MAX_num_agents']:
        print("Number of simulated agents is exceeding 'MAX_num_agents'\nEXITING..")
        exit(1)

    if GAME_CONFIG['num_agents'] <= 0:
        print("Number of simulated agents is less than or equal to zero\nEXITING..")
        exit(1)

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
    print(f"{game_name}\n")
    return game_name

def init_grid():
    GRID_SIZE = GAME_CONFIG['grid_size']
    grid = [['_' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return grid

def grid_to_str():
    global grid
    result = ''
    header = "   "
    if len(grid) == 100:
        for i in range(1, 11):
            header += f"{i:20}"
        header += "\n"
        result += header
    for i, row in enumerate(grid):
        row_str = ' '.join(row)
        row_num_str = str(i+1)
        if i+1 < 10:
            row_num_str = ' ' + row_num_str
        if i == 99:
            result += f'{row_num_str} {row_str} {row_num_str}\n'
        else:
            result += f'{row_num_str}  {row_str} {row_num_str}\n'
    if len(grid) == 100:
        result += header
    return result

def print_grid_to_game_file(grid, game_name):
    with open(game_name, 'a') as f:
        print(grid_to_str(grid), file=f)

def set_cell(x, y, value):
    global grid
    if GAME_CONFIG['verbose']:
        print(f"setting cell {x}, {y}, to {value}")
    grid[y][x] = value

def get_random_empty_cell(grid):
    GRID_SIZE = GAME_CONFIG['grid_size']
    while True:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if grid[x][y] == '_':
            return (x, y)

def populate_N_agents(N_agents):
    global grid
    grid = init_grid()
    agents = []
    for x in range(N_agents):
        agent_dict = []
        for i in range(26):
            agent_dict.append(chr(ord('A') + i))
        rnd_x, rnd_y = get_random_empty_cell(grid)
        new_agent = MoralAI_Agent.Agent(agent_dict[x], rnd_x, rnd_y)
        agents.append(new_agent)
    return agents

def populate_agent_targets(agents, num_targets_per_agent):
    global grid
    white_space = GAME_CONFIG['white_space']
    
    for agent_num, agent in enumerate(agents):
        print(f"\nAgent {agent.get_agent_label()} Target's:")
        for i in range(num_targets_per_agent):
            target_name = f"T{agent.get_agent_label()}{i+1}"
            rnd_x, rnd_y = get_random_empty_cell(grid)
            print(f"{white_space}Setting target={target_name} at {rnd_x} {rnd_y}")
            set_cell(rnd_x, rnd_y, target_name) # replace (0,0) with the desired target location

def print_all_agents(agents):
    for x in agents:
        print(x.agent_to_string())

    