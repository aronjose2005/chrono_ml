import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
import pandas as pd

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, output_dim)
        )

    def forward(self, x):
        return self.net(x)

def train_dqn(env):
    model = DQN(env.observation_space.shape[0], env.action_space.n)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.MSELoss()

    gamma = 0.99
    epsilon = 1.0
    decay = 0.995
    min_epsilon = 0.01
    memory = []
    max_memory = 10000
    batch_size = 64
    reward_history = []

    for episode in range(300):
        state = env.reset()
        total_reward = 0

        for step in range(100):
            if random.random() < epsilon:
                action = env.action_space.sample()
            else:
                with torch.no_grad():
                    q_vals = model(torch.tensor(state, dtype=torch.float32))
                    action = torch.argmax(q_vals).item()

            next_state, reward, done, _ = env.step(action)
            memory.append((state, action, reward, next_state, done))
            if len(memory) > max_memory:
                memory.pop(0)

            if len(memory) >= batch_size:
                batch = random.sample(memory, batch_size)
                states, actions, rewards, next_states, dones = zip(*batch)
                states = torch.tensor(states, dtype=torch.float32)
                actions = torch.tensor(actions, dtype=torch.long)
                rewards = torch.tensor(rewards, dtype=torch.float32)
                next_states = torch.tensor(next_states, dtype=torch.float32)
                dones = torch.tensor(dones, dtype=torch.bool)

                q_values = model(states).gather(1, actions.unsqueeze(1)).squeeze()
                with torch.no_grad():
                    q_next = model(next_states).max(1)[0]
                    q_target = rewards + gamma * q_next * (~dones)

                loss = loss_fn(q_values, q_target)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            state = next_state
            total_reward += reward
            if done:
                break

        epsilon = max(min_epsilon, epsilon * decay)
        reward_history.append(total_reward)
        if episode % 10 == 0:
            print(f"Episode {episode}, Reward: {total_reward:.2f}")

    # Save rewards for dashboard
    df = pd.DataFrame({'episode': list(range(len(reward_history))), 'reward': reward_history})
    df.to_csv("training_rewards.csv", index=False)

