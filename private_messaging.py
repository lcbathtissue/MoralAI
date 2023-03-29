class Observer:
    # Observer object
    def receive_private_msg(self, sender, message):
        pass


class PrivateChannel:
    def __init__(self):
        self.agent_channels = {}

    def subscribe_agent(self, agent):
        self.agent_channels[agent.label] = agent

    def send_private_msg(self, sender, recipient, message):
        if recipient in self.agent_channels:
            self.agent_channels[recipient].receive_private_msg(sender, message)


private_channel = PrivateChannel()


class Agent(Observer):
    def __init__(self, label):
        self.label = label
        self.coordinates_list = []
        private_channel.subscribe_agent(self)

    def send_private_msg(self, recipient, message):
        print(f"Agent {self.label} is sending a private message to {recipient}: {message}")
        private_channel.send_private_msg(self.label, recipient, message)

    def receive_private_msg(self, sender, message):
        self.coordinates_list.extend(message)

    def get_shared_coords(self):
        return f"{self.label}: {self.coordinates_list}"


agents = [Agent('A'), Agent('B'), Agent('C')]

agents[0].send_private_msg('B', ['1, 2'])
agents[1].send_private_msg('C', ['3, 4'])

for agent in agents:
    print(agent.get_shared_coords())

