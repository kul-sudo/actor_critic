from torch.nn import Module, Linear, ReLU
from torch.optim import SGD, Adam
from common.config import *


class Actor(Module):
    def __init__(self):
        super().__init__()
        self.fc1 = Linear(2, 512)
        self.relu1 = ReLU()
        self.fc2 = Linear(512, 512)
        self.relu2 = ReLU()
        self.fc3 = Linear(512, N_DIRECTIONS)

        self.optimizer = SGD(self.parameters(), lr=0.01)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x


class Critic(Module):
    def __init__(self):
        super().__init__()
        self.fc1 = Linear(2, 512)
        self.relu1 = ReLU()
        self.fc2 = Linear(512, 512)
        self.relu2 = ReLU()
        self.fc3 = Linear(512, 1)

        self.optimizer = Adam(self.parameters(), lr=0.01)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x
