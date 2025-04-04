import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random

class GridWorld:
    def __init__(self, size=5, start=(0, 0), goal=(4, 4)):
        self.size = size
        self.start = start
        self.goal = goal
        self.agent_pos = start
        self.grid = np.zeros((size, size))
        self.grid[goal] = 2  # Goal
        self.grid[start] = 1  # Agent

    def reset(self):
        self.agent_pos = self.start
        self.grid = np.zeros((self.size, self.size))
        self.grid[self.goal] = 2
        self.grid[self.agent_pos] = 1
        return self.get_state()

    def get_state(self):
        return np.array([self.agent_pos[0], self.agent_pos[1], self.goal[0], self.goal[1]])

    def step(self, action):
        x, y = self.agent_pos
        if action == 0:  # Up
            new_x, new_y = max(0, x - 1), y
        elif action == 1:  # Down
            new_x, new_y = min(self.size - 1, x + 1), y
        elif action == 2:  # Left
            new_x, new_y = x, max(0, y - 1)
        elif action == 3:  # Right
            new_x, new_y = x, min(self.size - 1, y + 1)
        else:
            raise ValueError("Invalid action")

        self.agent_pos = (new_x, new_y)

        reward = 10 if self.agent_pos == self.goal else -1
        done = self.agent_pos == self.goal

        self.grid = np.zeros((self.size, self.size))
        self.grid[self.goal] = 2
        self.grid[self.agent_pos] = 1

        return self.get_state(), reward, done

class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, output_size)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        return self.fc2(x)

def train_dqn(env, model, optimizer, loss_fn, episodes=1000, gamma=0.9, epsilon=0.1, batch_size=32):
    replay_buffer = []
    for episode in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0

        while not done:
            if random.random() < epsilon:
                action = random.randint(0, 3)
            else:
                state_tensor = torch.FloatTensor(state).unsqueeze(0)
                q_values = model(state_tensor)
                action = torch.argmax(q_values).item()

            next_state, reward, done = env.step(action)
            replay_buffer.append((state, action, reward, next_state, done))
            state = next_state
            total_reward += reward

            if len(replay_buffer) > batch_size:
                batch = random.sample(replay_buffer, batch_size)
                states, actions, rewards, next_states, dones = zip(*batch)

                states_tensor = torch.FloatTensor(states)
                actions_tensor = torch.LongTensor(actions).unsqueeze(1)
                rewards_tensor = torch.FloatTensor(rewards)
                next_states_tensor = torch.FloatTensor(next_states)
                dones_tensor = torch.FloatTensor(dones)

                q_values = model(states_tensor).gather(1, actions_tensor).squeeze(1)
                next_q_values = model(next_states_tensor).max(1)[0]
                target_q_values = rewards_tensor + gamma * next_q_values * (1 - dones_tensor)

                loss = loss_fn(q_values, target_q_values)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        if episode % 100 == 0:
            print(f"Episode {episode}, Total Reward: {total_reward}")

# Main
env = GridWorld()
input_size = 4  # Agent_x, Agent_y, Goal_x, Goal_y
output_size = 4  # Up, Down, Left, Right
model = DQN(input_size, output_size)
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.MSELoss()

train_dqn(env, model, optimizer, loss_fn)

# Example of using the trained model
state = env.reset()
done = False
while not done:
    state_tensor = torch.FloatTensor(state).unsqueeze(0)
    q_values = model(state_tensor)
    action = torch.argmax(q_values).item()
    state, _, done = env.step(action)
    print(env.grid)