import gym
from gym import error, spaces, utils, logger
from gym.utils import seeding
import cityflow
import numpy as np

class CityFlow_1x1_LowTraffic(gym.Env):
    """
    Description:
        A single intersection with low traffic.
        8 roads, 1 intersection (plus 4 virtual intersections).

    State:
        The total number of vehicles -- whether waiting or not -- on each lane.

    Actions:
        Type: Discrete(9)
        index of one of 9 light phases.

        Note:
            Below is a snippet from "roadnet.json" file which defines lightphases for "intersection_1_1".

            "lightphases": [
              {"time": 5, "availableRoadLinks": []},
              {"time": 30, "availableRoadLinks": [ 0, 4 ] },
              {"time": 30, "availableRoadLinks": [ 2, 7 ] },
              {"time": 30, "availableRoadLinks": [ 1, 5 ] },
              {"time": 30,"availableRoadLinks": [3,6]},
              {"time": 30,"availableRoadLinks": [0,1]},
              {"time": 30,"availableRoadLinks": [4,5]},
              {"time": 30,"availableRoadLinks": [2,3]},
              {"time": 30,"availableRoadLinks": [6,7]}
            ]

    Reward:
        The total amount of time -- in seconds -- that all the vehicles in the intersection
        waitied for.

        Todo: as a way to enssure fairness -- i.e. not a single lane gets green lights for too long --
        instead of simply summing up the waiting time, we could weigh the waiting time of each car by how
        much it had waited so far.
    """

    metadata = {'render.modes':['human']}
    def __init__(self):

        # hardcoded settings from "config.json" file
        self.cityflow = cityflow.Engine("1x1_config/config.json", thread_num=1)
        self.intersection_id = "intersection_1_1"
        self.num_lane = 8
        self.sec_per_step = 1.0
        self.action_space = spaces.Discrete(9)

        self.steps_per_episode = 1500
        self.current_step = 0
        self.is_done = False

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))


        self.cityflow.set_tl_phase(self.intersection_id, action)
        self.cityflow.next_step()

        state = self._get_state()
        reward = self._get_reward()

        self.current_step += 1

        if self.is_done:
            logger.warn("You are calling 'step()' even though this environment has already returned done = True. "
                        "You should always call 'reset()' once you receive 'done = True' "
                        "-- any further steps are undefined behavior.")
            reward = 0.0

        if self.current_step + 1 == self.steps_per_episode:
            self.is_done = True

        return state, reward, self.is_done, {}


    def reset(self):
        self.cityflow.reset()
        self.is_done = False
        return self._get_state()

    def render(self, mode='human'):
        print("Current time: " + self.cityflow.get_current_time())

    #def close(self):
    #    del self.cityflow

    def _get_state(self):
        lane_vehicles_dict = self.cityflow.get_lane_vehicle_count()
        lane_waiting_vehicles_dict = self.cityflow.get_lane_waiting_vehicle_count()
        state = np.zeroes(self.num_lane, 2)
        for i in range(self.num_lane):
            state[i][0] = lane_vehicles_dict[i]
            state[i][1] = lane_waiting_vehicles_dict[i]
        return state

    def _get_reward(self):
        lane_waiting_vehicles_dict = self.cityflow.get_lane_waiting_vehicle_count()
        reward = 0.0

        for _ in lane_waiting_vehicles_dict:
            reward -= self.sec_per_step
        return reward
