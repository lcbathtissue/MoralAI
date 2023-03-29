from MoralAI_Config import GAME_CONFIG

class Agent:
    def __init__(self, label, x, y):
        self.label = label
        self.power_level = 100
        self.x = x
        self.y = y
        self.radar_reach = 1
        # print(f"New agent: {label}, {x}, {y}")
    
    def move_agent(self, direction):
        if GAME_CONFIG['powered_moves']:
            if self.power_level == 0:
                return
        if direction == 'UP' and self.y > 0:
            self.y -= 1
        elif direction == 'DOWN' and self.y < 99:
            self.y += 1
        elif direction == 'LEFT' and self.x > 0:
            self.x -= 1
        elif direction == 'RIGHT' and self.x < 99:
            self.x += 1
    
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
        white_space = "    "
        if GAME_CONFIG['powered_moves']:
            return f"Agent {self.label}:\n{white_space}Position ({self.x}, {self.y}),\n{white_space}Power level: {self.power_level}"
        else:
            return f"Agent {self.label}:\n{white_space}Position ({self.x}, {self.y})"
