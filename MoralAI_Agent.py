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
        print(f"PRIVATE-MSG: Agent {self.label} is sending {coordinates} to Agent {recipient}")
        private_channel.send_private_msg(self.label, recipient, coordinates)

    def receive_public_msg(self, coordinates):
        self.coordinates_list.extend(coordinates)
        self.remove_duplicate_coordinates()

    def receive_private_msg(self, sender, coordinates):
        self.coordinates_list.extend(coordinates)
        self.remove_duplicate_coordinates()

    def get_shared_coords(self):
        return f"{self.label}: {self.coordinates_list}"

    def remove_duplicate_coordinates(self):
        coordinates_without_duplicates = []
        for coordinates in self.coordinates_list:
            if coordinates not in coordinates_without_duplicates:
                coordinates_without_duplicates.append(coordinates)
        self.coordinates_list = coordinates_without_duplicates
