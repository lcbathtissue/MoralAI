import MoralAI_Util
from MoralAI_Config import GAME_CONFIG

class Agent:
    def __init__(self, label, x, y):
        self.label = label
        self.public_channel = []
        self.private_channel = {}
        self.received_coordinates = [] 
        self.power_level = 100
        self.x = x
        self.y = y
        self.radar_reach = GAME_CONFIG['radar_reach']
        MoralAI_Util.set_cell(x, y, label)
        if GAME_CONFIG['verbose']:
            print(f"New agent: {label}, {x}, {y}")
    
    def send_coordinates(self, coordinates, recipient=None):
        print(f"send_coordinates: {coordinates} (recipient={recipient})")
        if recipient is None:
            self.public_channel.append(coordinates)
        else:
            if recipient not in self.private_channel:
                self.private_channel[recipient] = []
            self.private_channel[recipient].append(coordinates)
    
    def receive_coordinates(self, sender):
        print(f"receive_coordinates: {self.receiver} sender={sender}")
        coordinates = []
        if sender is None:
            coordinates = self.public_channel
        else:
            if sender in self.private_channel:
                coordinates = self.private_channel[sender]
        # add received coordinates to own list of received coordinates
        self.received_coordinates.extend(coordinates)
        # clear the private channel after receiving coordinates
        if sender in self.private_channel:
            self.private_channel[sender] = []
        print(f"AGENT {self.label}'S COMMS\n{coordinates}")

    def get_agent_label(self):
        return self.label
    
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
