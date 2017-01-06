from algorithm.entities import Component, Edge, Link, Node, Server
import numpy as np


class GridFactory(object):

    def __init__(self, data):
        self.data = data
        self.grid = None

    def create_grid(self):
        servers = self.__create_servers(self.data)

    def __create_servers(self, data):
        min_powers = data['P_min']
        max_powers = data['P_max']
        servers_available_resources = data['av']

        servers = []
        node_id = 0
        for min_power, max_power, available_resources in zip(min_powers, max_powers, servers_available_resources[0]):
            server = Server(
                node_id=node_id,
                components=None,
                min_power=min_power,
                max_power=max_power,
                resources_available=available_resources
            )

            node_id += 1
            servers.append(server)

        return np.array(servers)

    def get_grid(self):
        assert self.grid is not None, 'You must call build_grid before this method!'

        return self.grid


class Grid(object):

    def __init__(self):
        self.servers