import MoralAI_Util
from MoralAI_Config import GAME_CONFIG

class Observer:
    def receive_public_msg(self, coordinates):
        pass

    def receive_private_msg(self, sender, coordinates):
        pass

class PublicChannel:
    # [public] 'Subject' object
    def __init__(self):
        self.observers = []
        self.coordinates_list = []

    def subscribe_agent(self, observer):
        self.observers.append(observer)

    def send_all(self, coordinates):
        coordinates = [list(map(int, c.split(','))) for c in coordinates]
        self.coordinates_list.extend(coordinates)
        for observer in self.observers:
            observer.receive_public_msg(coordinates)

class PrivateChannel:
    # [private] 'Subject' object
    def __init__(self):
        self.observers = {}
    
    def subscribe_agent(self, agent):
        self.observers[agent.label] = agent

    def send_private_msg(self, sender, recipient, coordinates):
        coordinates = [list(map(int, c.split(','))) for c in coordinates]
        if recipient in self.observers:
            self.observers[recipient].receive_private_msg(sender, coordinates)

public_channel = PublicChannel()
private_channel = PrivateChannel()
class Agent:
    def __init__(self, label, x, y):
        self.label = label
        self.collected_targets = 0
        self.coordinates_list = []
        public_channel.subscribe_agent(self)
        private_channel.subscribe_agent(self)
        self.power_level = 100
        self.x = x
        self.y = y
        self.radar_reach = GAME_CONFIG['radar_reach']
        MoralAI_Util.set_cell(x, y, label)
        if GAME_CONFIG['verbose']:
            print(f"New agent: {label}, {x}, {y}")

    def get_agent_label(self):
        return self.label

    def get_agent_collected_targets(self):
        return self.collected_targets

    def add_agent_collected_target_count(self):
        self.collected_targets += 1
    
    def move_agent(self, direction):
        valid_move = True
        if GAME_CONFIG['powered_moves']:
            if self.power_level == 0:
                valid_move = False
                print(f"AGENT {self.label} ATTEMPTED TO MOVE BUT IS OUT OF POWER!")
                return
        if direction == 'UP':
            if self.y > 0:
                self.y -= 1
            else:
                valid_move = False
        elif direction == 'DOWN':
            if self.y < GAME_CONFIG['grid_size']-1:
                self.y += 1
            else:
                valid_move = False
        elif direction == 'LEFT':
            if self.x > 0:
                self.x -= 1
            else:
                valid_move = False
        elif direction == 'RIGHT':
            if self.x < GAME_CONFIG['grid_size']-1:
                self.x += 1
            else:
                valid_move = False
        if valid_move and GAME_CONFIG['powered_moves']:
            self.power_level -= 1
        if not valid_move:
            print(f"'AGENT {self.label}' ATTEMPTED AN INVALID MOVE IN DIRECTION '{direction}' FROM POS '{self.x}, {self.y}'!")

    
    def get_position(self):
        return self.x, self.y
    
    def agent_radar(self):
        nearby_cells = []
        for i in range(self.x - self.radar_reach, self.x + self.radar_reach + 1):
            for j in range(self.y - self.radar_reach, self.y + self.radar_reach + 1):
                if i < 0 or i > 99 or j < 0 or j > 99:
                    continue
                nearby_cells.append((i, j))
        return nearby_cells

    def agent_to_string(self):
        white_space = GAME_CONFIG['white_space']
        if GAME_CONFIG['powered_moves']:
            return f"Agent {self.label}:\n{white_space}Position ({self.x}, {self.y}),\n{white_space}Power level: {self.power_level}"
        else:
            return f"Agent {self.label}:\n{white_space}Position ({self.x}, {self.y})"

    def send_public_msg(self, coordinates):
        print(f"PUBLIC-MSG: Agent {self.label} is sending {coordinates}")
        public_channel.send_all(coordinates)

    def send_private_msg(self, recipient, coordinates):
        private_comms_enabled = MoralAI_Util.get_private_comms_state()
        if private_comms_enabled:
            print(f"PRIVATE-MSG: Agent {self.label} is sending {coordinates} to Agent {recipient}")
            private_channel.send_private_msg(self.label, recipient, coordinates)
        else:
            print(f"BLOCKED: Agent {self.label} attempted to send on the private channel but because of game rules it was blocked.")

    def receive_public_msg(self, coordinates):
        self.coordinates_list.extend(coordinates)
        self.remove_duplicate_coordinates()

    def receive_private_msg(self, sender, coordinates):
        private_comms_enabled = MoralAI_Util.get_private_comms_state()
        if private_comms_enabled:
            self.coordinates_list.extend(coordinates)
            self.remove_duplicate_coordinates()
        else:
            print(f"BLOCKED: Agent {self.label} attempted to send on the private channel but because of game rules it was blocked.")


    def get_shared_coords(self):
        return f"{self.label}: {self.coordinates_list}"

    def remove_duplicate_coordinates(self):
        coordinates_without_duplicates = []
        for coordinates in self.coordinates_list:
            if coordinates not in coordinates_without_duplicates:
                coordinates_without_duplicates.append(coordinates)
        self.coordinates_list = coordinates_without_duplicates

    def observation_matrix(self, grid, radius):
        # define the observable space around the agent, 
        # 'X' out of range, 'A' is agent at centre, '0' is reachable cell in radius 
        center = radius  
        matrix = [[0.0 for x in range(2*radius+1)] for y in range(2*radius+1)]

        for i in range(2*radius+1):
            # perform distance calculations 
            for j in range(2*radius+1):
                dist = math.sqrt((i-center)**2 + (j-center)**2) 
                matrix[i][j] = round(dist, 2) 

        for i in range(len(matrix)):
            # exclude any cells out of radius threshold
            for j in range(len(matrix[0])):
                if matrix[i][j] > radius:
                    matrix[i][j] = 'X'
                else:
                    matrix[i][j] = '0'

        center_row = len(matrix) // 2
        center_col = len(matrix[0]) // 2
        matrix[self.y][self.x] = 'A'

        # translate the observable space into relative 
        # coordinates based off agent position
        coords = []
        num_rows, num_cols = len(matrix), len(matrix[0])
        offset_x, offset_y = self.y - (num_rows // 2), self.x - (num_cols // 2)
        for i in range(num_rows):
            row = []
            for j in range(num_cols):
                if matrix[i][j] == '0':
                    row.append([j + offset_y, i + offset_x])
                elif matrix[i][j] == 'A' or matrix[i][j] == 'X':
                    row.append(matrix[i][j])
            coords.append(row)

        # using the matrix of relative coordinates and the values
        # in the grid parameter, replace observable cells with
        # the values found in grid, excluding cells outside of
        # the border of the grid which also will become 'X'
        num_rows, num_cols = len(grid), len(grid[0])
        values_matrix = [['X' for j in range(len(coords[0]))] for i in range(len(coords))]
        for i in range(len(coords)):
            for j in range(len(coords[0])):
                if coords[i][j] == 'A' or coords[i][j] == 'X':
                    values_matrix[i][j] = coords[i][j]
                else:
                    x, y = coords[i][j]
                    if x < 0 or x >= num_cols or y < 0 or y >= num_rows:
                        values_matrix[i][j] = 'X'
                    else:
                        values_matrix[i][j] = grid[y][x]
        return values_matrix