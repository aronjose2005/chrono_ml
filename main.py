from core.chrono_env import ChronoTimeWarpEnv
from agents.dqn_agent import train_dqn

env = ChronoTimeWarpEnv()
train_dqn(env)

