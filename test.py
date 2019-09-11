import gym
import gym_cityflow
import numpy as np

if __name__ == "__main__":
    env = gym.make('gym_cityflow:CityFlow-1x1-LowTraffic-v0')
    env.set_save_replay(False)

    is_done = False
    state = env.reset()

    while not is_done:
        action = np.random.randint(low=0, high=9)
        state, reward, is_done, _ = env.step(action)