class Observer:
    # Observer object
    def receive_public_msg(self, coordinates):
        pass

    def receive_private_msg(self, sender, coordinates):
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


class PrivateChannel:
    # Subject object
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


class Agent(Observer):
    def __init__(self, label):
        self.label = label
        self.coordinates_list = []
        public_channel.subscribe_agent(self)
        private_channel.subscribe_agent(self)

    def send_public_msg(self, coordinates):
        print(f"Agent {self.label} is sending {coordinates} on the public channel..")
        public_channel.send_all(coordinates)

    def send_private_msg(self, recipient, coordinates):
        print(f"Agent {self.label} is sending a private coordinates to {recipient}: {coordinates}")
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

agents = [Agent('A'), Agent('B'), Agent('C')]

agents[0].send_public_msg(["1, 2"])
agents[1].send_public_msg(["3, 4"])
# agents[1].send_public_msg(["3, 4"])  # duplicates handled by remove_duplicate_coordinates function

agents[0].send_private_msg('B', ['5, 6'])
agents[1].send_private_msg('C', ['7, 8'])
# agents[1].send_private_msg('C', ['7, 8'])  # duplicates handled by remove_duplicate_coordinates function

for agent in agents:
    print(agent.get_shared_coords())
