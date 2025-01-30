from torch import log as t_log
from .learning_config import *
from common.brains import Critic


class Agent:
    def __init__(self, actor):
        self.actor = actor
        self.critic = Critic()

    def train(self, state, weight, next_state, reward):
        # Critic update
        value = self.critic(state)
        td_error = reward - value
        if next_state is not None:
            next_value = self.critic(next_state)
            td_error += GAMMA * next_value
        critic_loss = td_error.pow(2)

        self.critic.optimizer.zero_grad()
        critic_loss.backward()
        self.critic.optimizer.step()

        # Actor update
        log_prob = t_log(weight)
        actor_loss = -log_prob * td_error.detach()

        self.actor.optimizer.zero_grad()
        actor_loss.backward()
        self.actor.optimizer.step()
