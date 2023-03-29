class Observer:
    # Observer object
    def receive_public_msg(self, PublicChannel):
        pass

class PublicChannel:
    # Subject object
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

public_channel = PublicChannel()
class Agent(Observer):
    def __init__(self, label):
        self.label = label
        public_channel.subscribe_agent(self)

    def send_public_msg(self, coordinates):
        print(f"Agent {self.label} is sending {coordinates} on the public channel..")
        public_channel.send_all(coordinates)

    def get_shared_coords(self):
        return f"{self.label}: {public_channel.coordinates_list}"

agents = [Agent('A'), Agent('B'), Agent('C')]
agents[0].send_public_msg(["1, 2"])
agents[1].send_public_msg(["3, 4"])

for agent in agents:
    print(agent.get_shared_coords())
