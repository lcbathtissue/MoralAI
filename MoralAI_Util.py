import os, re, csv, datetime, random, MoralAI_Agent
from MoralAI_Config import GAME_CONFIG

def save_csv_file(data, filename):
    data = [
        {
            'Scenario number (1,2 or 3)': 1, 
            'Iteration number': 1, 
            'Agent number': 1, 
            'd: Number of collected targets by the agent': 10, 
            'e: Number of steps taken by the agent at the end of iteration': 20
        },
        {
            'Scenario number (1,2 or 3)': 1, 
            'Iteration number': 1, 
            'Agent number': 1, 
            'd: Number of collected targets by the agent': 10, 
            'e: Number of steps taken by the agent at the end of iteration': 20
        },
    ]
    
    with open(filename, mode='w', newline='') as csv_file:
        fieldnames = [
            'Scenario number (1,2 or 3)', 
            'Iteration number', 
            'Agent number', 
            'd: Number of collected targets by the agent', 
            'e: Number of steps taken by the agent at the end of iteration', 
            'f: Agent happiness: f=d/(e+1)', 
            'g: Maximum happiness in each iteration', 
            'h: Minimum happiness in each iteration', 
            'Average happiness in each iteration', 
            'Standard deviation of happiness in each iteration', 
            'k: Agent competitiveness: k=(f-h)/(g-h)'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in data:
            row['f: Agent happiness: f=d/(e+1)'] = row['d: Number of collected targets by the agent'] / (row['e: Number of steps taken by the agent at the end of iteration'] + 1)  # Calculate happiness
            writer.writerow(row)
        
        iter_data = {} 
        for row in data:
            iter_num = row['Iteration number']
            if iter_num not in iter_data:
                iter_data[iter_num] = []
            iter_data[iter_num].append(row['f: Agent happiness: f=d/(e+1)'])
        
        for iter_num in sorted(iter_data.keys()):
            happiness_values = iter_data[iter_num]
            max_happiness = max(happiness_values)
            min_happiness = min(happiness_values)
            avg_happiness = sum(happiness_values) / len(happiness_values)
            std_dev_happiness = (sum((x - avg_happiness) ** 2 for x in happiness_values) / len(happiness_values)) ** 0.5
            
            # Write happiness statistics row for current iteration
            writer.writerow({
                'Scenario number (1,2 or 3)': '',
                'Iteration number': iter_num,
                'Agent number': '',
                'd: Number of collected targets by the agent': '',
                'e: Number of steps taken by the agent at the end of iteration': '',
                'f: Agent happiness: f=d/(e+1)': max_happiness,
                'g: Maximum happiness in each iteration': '',
                'h: Minimum happiness in each iteration': min_happiness,
                'Average happiness in each iteration': avg_happiness,
                'Standard deviation of happiness in each iteration': std_dev_happiness,
                'k: Agent competitiveness: k=(f-h)/(g-h)': '',
            })

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
    game_name = f"games/game_{datetime.datetime.now().strftime('%m-%d_%H-%M')}"
    while os.path.exists(f"{game_name}.txt"):
        suffix_match = re.search(r"_(\d+)\.", f"{game_name}.txt")
        if suffix_match:
            suffix = int(suffix_match.group(1)) + 1
            game_name = re.sub(r"_(\d+)\.", f"_{suffix}.", f"{game_name}.txt")
        else:
            game_name = re.sub(r"\.", "_2.", f"{game_name}.txt")
    with open(f"{game_name}.txt", 'w'):
        pass
    print(f"{game_name}.txt\n")
    return game_name

def init_grid():
    GRID_SIZE = GAME_CONFIG['grid_size']
    grid = [['_' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return grid

def return_target_num(string):
    for char in string:
        num_str = ''.join(filter(str.isdigit, char))
        if num_str:
            return int(num_str)

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
            print(f"{white_space}'{target_name}' Position ({rnd_x}, {rnd_y})")
            set_cell(rnd_x, rnd_y, target_name)

def print_all_agents(agents):
    for x in agents:
        print(x.agent_to_string())

def show_moves(grids_list):
    grids_list = [
        [[1, 2, 2], [3, 4, 2], [3, 4, 2]], 
        [[5, 6, 2], [7, 8, 2], [3, 4, 2]], 
        [[9, 10, 2], [11, 12, 2], [3, 4, 2]]
    ]

    for i, array in enumerate(grids_list):
        if i > 0:
            input("\nPress Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in array:
            print(" ".join(str(elem) for elem in row))
    