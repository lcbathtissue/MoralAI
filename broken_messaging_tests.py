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
        coordinates = [tuple(map(int, c.split(','))) for c in coordinates]
        self.coordinates_list.extend(coordinates)
        for observer in self.observers:
            observer.receive_public_msg(coordinates)

class PrivateChannel:
    # Mediator object
    def __init__(self):
        self.channels = {}

    def add_channel(self, agent1, agent2):
        channel_id = f"{agent1.label}_{agent2.label}"
        self.channels[channel_id] = []
        agent1.private_channels.append(channel_id)
        agent2.private_channels.append(channel_id)

    def send_msg(self, sender, receiver, coordinates):
        channel_id = f"{sender.label}_{receiver.label}"
        if channel_id in self.channels:
            self.channels[channel_id].append(coordinates)
            sender.receive_private_msg(channel_id, coordinates)
            receiver.receive_private_msg(channel_id, coordinates)

class Agent(Observer):
    def __init__(self, label):
        self.label = label
        self.private_channels = []
        public_channel.subscribe_agent(self)

    def send_public_msg(self, coordinates):
        print(f"PUBLIC SEND: Agent {self.label} is sending {coordinates}")
        public_channel.send_all(coordinates)

    def send_private_msg(self, receiver, coordinates):
        print(f"PRIVATE SEND: Agent {self.label} is sending {coordinates} to Agent {receiver.label}")
        private_channel.send_msg(self, receiver, coordinates)

    def receive_public_msg(self, coordinates):
        public_channel.coordinates_list.extend([tuple(c) for c in coordinates])

    def receive_private_msg(self, channel_id, coordinates):
        public_channel.coordinates_list.extend([tuple(c) for c in coordinates])

    def get_shared_coords(self):
        return f"{self.label}: {list(set(public_channel.coordinates_list))}"

private_channel = PrivateChannel()
public_channel = PublicChannel()
agents = [Agent('A'), Agent('B'), Agent('C')]

private_channel.add_channel(agents[0], agents[1])  # Agents A and B share a private channel

agents[0].send_public_msg(["1, 2"])  # Agent A sends public message
agents[1].send_public_msg(["3, 4"])  # Agent B sends public message

agents[0].send_private_msg(agents[1], ["5, 6"])  # Agent A sends private message to Agent B
agents[1].send_private_msg(agents[2], ["7, 8"])  # Agent B sends private message to Agent C

for agent in agents:
    print(agent.get_shared_coords())

