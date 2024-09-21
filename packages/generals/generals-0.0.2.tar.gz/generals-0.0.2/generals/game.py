import numpy as np
import gymnasium as gym
from typing import Dict, List
from generals.config import PASSABLE, MOUNTAIN, GENERAL
from generals.config import UP, DOWN, LEFT, RIGHT
from generals.config import INCREMENT_RATE

from scipy.ndimage import maximum_filter


class Game:
    def __init__(self, map: np.ndarray, agents: List[str]):
        self.agents = agents
        self.agent_id = {agent: i for i, agent in enumerate(agents)}
        self.time = 0

        spatial_dim = (map.shape[0], map.shape[1])
        self.map = map
        self.grid_size = spatial_dim[0]  # Grid shape should be square

        self.general_positions = {
            agent: np.argwhere(map == chr(ord(GENERAL) + self.agent_id[agent]))[0]
            for agent in self.agents
        }

        valid_generals = ["A", "B"]  # because generals are represented as letters

        # Initialize channels
        # Army - army size in each cell
        # General - general mask (1 if general is in cell, 0 otherwise)
        # Mountain - mountain mask (1 if cell is mountain, 0 otherwise)
        # City - city mask (1 if cell is city, 0 otherwise)
        # Passable - passable mask (1 if cell is passable, 0 otherwise)
        # Ownership_i - ownership mask for player i (1 if player i owns cell, 0 otherwise)
        # Ownerhsip_0 - ownership mask for neutral cells that are passable (1 if cell is neutral, 0 otherwise)
        # Initialize channels
        self.channels = {
            "army": np.where(np.isin(map, valid_generals), 1, 0).astype(np.float32),
            "general": np.where(np.isin(map, valid_generals), 1, 0).astype(bool),
            "mountain": np.where(map == MOUNTAIN, 1, 0).astype(bool),
            "city": np.where(np.char.isdigit(map), 1, 0).astype(bool),
            "passable": (map != MOUNTAIN).astype(bool),
            "ownership_neutral": ((map == PASSABLE) | (np.char.isdigit(map))).astype(
                bool
            ),
            **{
                f"ownership_{agent}": np.where(
                    map == chr(ord(GENERAL) + id), 1, 0
                ).astype(bool)
                for id, agent in enumerate(self.agents)
            },
        }

        # City costs are 40 + digit in the cell
        base_cost = 40
        city_costs = np.where(np.char.isdigit(map), map, '0').astype(np.float32)
        self.channels["army"] += base_cost * self.channels["city"] + city_costs

        box = gym.spaces.Box(low=0, high=1, shape=spatial_dim, dtype=np.float32)
        self.observation_space = gym.spaces.Dict(
            {
                "army": gym.spaces.Box(
                    low=0, high=np.inf, shape=spatial_dim, dtype=np.int32
                ),
                "general": box,
                "city": box,
                "ownership": box,
                "ownership_opponent": box,
                "ownership_neutral": box,
                "mountain": box,
            }
        )

        self.action_space = gym.spaces.MultiDiscrete(
            [self.grid_size, self.grid_size, 4]
        )

    def action_mask(self, agent: str) -> np.ndarray:
        """
        Function to compute valid actions from a given ownership mask.

        Args:
            agent_id: str

        Returns:
            np.ndarray: an NxNx4 array, where each channel is a boolean mask
            of valid actions (UP, DOWN, LEFT, RIGHT) for each cell in the grid.

            I.e. valid_action_mask[i, j, k] is 1 if action k is valid in cell (i, j).
        """

        ownership_channel = self.channels[f"ownership_{agent}"]

        owned_cells_indices = self.channel_to_indices(ownership_channel)
        valid_action_mask = np.zeros(
            (self.grid_size, self.grid_size, 4), dtype=np.float32
        )

        if self.is_done():
            return valid_action_mask

        for channel_index, direction in enumerate([UP, DOWN, LEFT, RIGHT]):
            destinations = owned_cells_indices + direction

            # check if destination is in grid bounds
            in_first_boundary = np.all(destinations >= 0, axis=1)
            in_second_boundary = np.all(destinations < self.grid_size, axis=1)
            destinations = destinations[in_first_boundary & in_second_boundary]

            # check if destination is road
            passable_cell_indices = (
                self.channels["passable"][destinations[:, 0], destinations[:, 1]] == 1.0
            )
            action_destinations = destinations[passable_cell_indices]

            # get valid action mask for a given direction
            valid_source_indices = action_destinations - direction
            valid_action_mask[
                valid_source_indices[:, 0], valid_source_indices[:, 1], channel_index
            ] = 1.0

        return valid_action_mask

    def channel_to_indices(self, channel: np.ndarray) -> np.ndarray:
        """
        Returns a list of indices of cells from specified a channel.

        Expected channels are ownership, general, city, mountain.

        Args:
            channel: one channel of the game grid

        Returns:
            np.ndarray: list of indices of cells with non-zero values.
        """
        return np.argwhere(channel != 0)

    def visibility_channel(self, ownership_channel: np.ndarray) -> np.ndarray:
        """
        Returns a binary channel of visible cells from the perspective of the given player.

        Args:
            agent_id: int
        """
        return maximum_filter(ownership_channel, size=3)

    def step(self, actions: Dict[str, np.ndarray]):
        """
        Perform one step of the game

        Args:
            actions: dictionary of agent_id to action (this will be reworked)
        """
        done_before_actions = self.is_done()
        directions = np.array([UP, DOWN, LEFT, RIGHT])

        # Agent with smaller army to move is prioritized
        armies = [
            (self.channels["army"][actions[agent][0]][actions[agent][1]], agent)
            for agent in list(actions.keys())
        ]
        # If only half of the army is sent, update the army size
        armies = [
            (army, agent) if actions[agent][3] == 0 else (army // 2, agent) for army, agent in armies
        ]
        agents = [agent for _, agent in sorted(armies)]

        for agent in agents:
            source = actions[agent][:2]  # x,y indices of a source cell
            direction = actions[agent][2]  # 0,1,2,3

            si, sj = source[0], source[1]  # source indices
            di, dj = (
                source[0] + directions[direction][0],
                source[1] + directions[direction][1],
            )  # destination indices

            send_half = actions[agent][3]
            if send_half:
                army_to_move = self.channels["army"][si, sj] // 2
                army_to_stay = self.channels["army"][si, sj] - army_to_move
            else:
                army_to_move = self.channels["army"][si, sj] - 1 # Send all but one army
                army_to_stay = 1

            # Check if the current player owns the source cell and has atleast 2 army size
            if army_to_move < 1 or self.channels[f"ownership_{agent}"][si, sj] == 0:
                continue

            target_square_army = self.channels["army"][di, dj]
            target_square_owner_idx = np.argmax(
                [
                    self.channels[f"ownership_{agent}"][di, dj]
                    for agent in ["neutral"] + self.agents
                ]
            )
            target_square_owner = (["neutral"] + self.agents)[target_square_owner_idx]

            if target_square_owner == agent:
                self.channels["army"][di, dj] += army_to_move
                self.channels["army"][si, sj] = army_to_stay
            else:
                # Calculate resulting army, winner and update channels
                remaining_army = np.abs(target_square_army - army_to_move)
                square_winner = (
                    agent
                    if target_square_army < army_to_move
                    else target_square_owner
                )
                self.channels["army"][di, dj] = remaining_army
                self.channels["army"][si, sj] = army_to_stay
                self.channels[f"ownership_{square_winner}"][di, dj] = 1
                if square_winner != target_square_owner:
                    self.channels[f"ownership_{target_square_owner}"][di, dj] = 0

        if not done_before_actions:
            self.time += 1

        if self.is_done():
            # Give all cells of loser to winner
            winner = (
                self.agents[0] if self.agent_won(self.agents[0]) else self.agents[1]
            )
            loser = self.agents[1] if winner == self.agents[0] else self.agents[0]
            self.channels[f"ownership_{winner}"] += self.channels[f"ownership_{loser}"]
            self.channels[f"ownership_{loser}"] = self.channels["passable"] * 0
        else:
            self._global_game_update()

        observations = {agent: self._agent_observation(agent) for agent in self.agents}
        infos = self.get_infos()
        return observations, infos

    def get_all_observations(self):
        """
        Returns observations for all agents.
        """
        return {agent: self._agent_observation(agent) for agent in self.agents}

    def _global_game_update(self):
        """
        Update game state globally.
        """

        owners = self.agents

        # every TICK_RATE steps, increase army size in each cell
        if self.time % INCREMENT_RATE == 0:
            for owner in owners:
                self.channels["army"] += self.channels[f"ownership_{owner}"]

        # Increment armies on general and city cells, but only if they are owned by player
        if self.time % 2 == 0 and self.time > 0:
            update_mask = self.channels["general"] + self.channels["city"]
            for owner in owners:
                self.channels["army"] += (
                    update_mask * self.channels[f"ownership_{owner}"]
                )

    def is_done(self):
        """
        Returns True if the game is over, False otherwise.
        """
        return any(self.agent_won(agent) for agent in self.agents)

    def get_infos(self):
        """
        Returns a dictionary of player statistics.
        Keys and values are as follows:
        - army: total army size
        - land: total land size
        """
        players_stats = {}
        for agent in self.agents:
            army_size = np.sum(
                self.channels["army"] * self.channels[f"ownership_{agent}"]
            ).astype(np.int32)
            land_size = np.sum(self.channels[f"ownership_{agent}"]).astype(np.int32)
            players_stats[agent] = {
                "army": army_size,
                "land": land_size,
                "is_winner": self.agent_won(agent),
            }
        return players_stats

    def _agent_observation(self, agent: str) -> Dict[str, np.ndarray]:
        """
        Returns an observation for a given agent.
        Args:
            agent: str

        Returns:
            np.ndarray: observation for the given agent
        """
        info = self.get_infos()
        opponent = self.agents[0] if agent == self.agents[1] else self.agents[1]
        visibility = self.visibility_channel(self.channels[f"ownership_{agent}"])
        observation = {
            "visibility": visibility,
            "army": self.channels["army"] * visibility,
            "general": self.channels["general"] * visibility,
            "city": self.channels["city"] * visibility,
            "ownership": self.channels[f"ownership_{agent}"] * visibility,
            "ownership_opponent": self.channels[f"ownership_{opponent}"] * visibility,
            "ownership_neutral": self.channels["ownership_neutral"] * visibility,
            "structure": self.channels["mountain"] + self.channels["city"],
            "action_mask": self.action_mask(agent),
            "n_land": info[agent]["land"],
            "n_army": info[agent]["army"],
            "is_winner": info[agent]["is_winner"],
            "timestep": self.time
        }
        return observation

    def agent_won(self, agent: str) -> bool:
        """
        Returns True if the agent won the game, False otherwise.
        """
        return all(
            self.channels[f"ownership_{agent}"][general[0], general[1]] == 1
            for general in self.general_positions.values()
        )
