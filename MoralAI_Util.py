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

def generate_summary_csv(input_file, output_file):
    scenarios = set()
    with open(input_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)
        for row in rows:
            scenarios.add(row['Scenario number (1,2 or 3)'])

    with open(output_file, mode='w', newline='') as summary_csv_file:
        fieldnames = ['Scenario number (1,2 or 3)', 'Average happiness in each iteration', 'Average competitiveness in each iteration']
        csv_writer = csv.DictWriter(summary_csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for scenario in scenarios:
            happiness_sum = 0
            competitiveness_sum = 0
            iteration_count = 0
            for row in rows:
                if row['Scenario number (1,2 or 3)'] == scenario and row['Average happiness in each iteration']:
                    happiness_sum += float(row['Average happiness in each iteration'])
                    competitiveness_sum += float(row['k: Agent competitiveness: k=(f-h)/(g-h)'])
                    iteration_count += 1
            if iteration_count > 0:
                avg_happiness = happiness_sum / iteration_count
                avg_competitiveness = competitiveness_sum / iteration_count
                csv_writer.writerow({'Scenario number (1,2 or 3)': scenario, 
                                    'Average happiness in each iteration': avg_happiness, 
                                    'Average competitiveness in each iteration': avg_competitiveness})

def check_game_config_validity(GAME_CONFIG):
    if GAME_CONFIG['num_agents'] > GAME_CONFIG['MAX_num_agents']:
        print("Number of simulated agents is exceeding 'MAX_num_agents'\nEXITING..")
        exit(1)

    if GAME_CONFIG['num_agents'] <= 0:
        print("Number of simulated agents is less than or equal to zero\nEXITING..")
        exit(1)

def check_game_end_conditions(GAME_CONFIG, agents):
    end_game_flag = False
    game_modes = ["Competition", "Collaboration", "Compassion"]
    white_space = GAME_CONFIG['white_space']
    num_agents = GAME_CONFIG['num_agents']
    num_targets = GAME_CONFIG['num_targets_per_agent']
    game_mode_num = GAME_CONFIG['scenario_number']
    game_mode = game_modes[game_mode_num-1]
    print(f"[GAME-END-CHECK: game_mode={game_mode}] There are {num_targets} targets per agent..")
    if GAME_CONFIG['scenario_number'] == 1 or GAME_CONFIG['scenario_number'] == 3:
        print(f"{white_space}game ends when ANY agent has captured {num_targets} targets..")
        captures = get_agents_target_captures(agents, num_targets)
        for i, capture in enumerate(captures):
            if capture == num_targets:
                end_game_flag = True
                winner = agents[i].get_agent_label()
    elif GAME_CONFIG['scenario_number'] == 2:
        print(f"{white_space}game ends when ALL {num_agents} agents have captured all {(num_agents*num_targets)} targets ({num_targets} per agent)..")
        captures = get_agents_target_captures(agents, num_targets)
        agents_completed = []
        for capture in captures:
            if capture == num_targets:
                agents_completed.append(True)
            else:
                agents_completed.append(False)
        if all(agents_completed):
            end_game_flag = True
            winner = None

    if end_game_flag:
        end_game(winner)

def get_agents_target_captures(agents, num_targets):
    target_captures = []
    for agent in agents:
        collected_count = agent.get_agent_collected_targets()
        target_captures.append(collected_count)
    return target_captures

def end_game(winner):
    if winner is not None:
        print(f"\nThe game has ended! The winner is Agent {winner}\nEXITING..")
    else:
        print("\nThe game has ended! All agents collected their targets!\nEXITING..")
    exit(0)

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
    global grid, show_initial_positions
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

def populate_agent_targets(agents, num_targets_per_agent, show_initial_positions):
    global grid
    white_space = GAME_CONFIG['white_space']
    
    for agent_num, agent in enumerate(agents):
        if show_initial_positions:
            print(f"\nAgent {agent.get_agent_label()} Target's:")
        for i in range(num_targets_per_agent):
            target_name = f"T{agent.get_agent_label()}{i+1}"
            rnd_x, rnd_y = get_random_empty_cell(grid)
            if show_initial_positions:
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

def enable_private_comms_if_allowed(GAME_CONFIG):
    global private_comms_enabled
    if GAME_CONFIG['scenario_number'] == 1:
        print("Blocking private communication channels..")
        private_comms_enabled = False
    else:
        print("Enabling private communication channels..")
        private_comms_enabled = True

def get_private_comms_state():
    global private_comms_enabled
    if GAME_CONFIG['scenario_number'] == 1:
        return False
    else:
        return True