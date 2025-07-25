import gym
import numpy as np

class ChronoTimeWarpEnv(gym.Env):
    def __init__(self):
        super(ChronoTimeWarpEnv, self).__init__()
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)  # 3D state + 1 time
        self.action_space = gym.spaces.Discrete(2)
        self.state = None
        self.time = 0

    def reset(self):
        self.state = np.random.rand(3)
        self.time = 0
        return np.append(self.state, self.time / 100)

    def step(self, action):
        reward = np.random.rand()  # Dummy reward
        self.time += 1
        self.state = np.random.rand(3)
        done = self.time >= 100
        obs = np.append(self.state, self.time / 100)
        return obs, reward, done, {}

