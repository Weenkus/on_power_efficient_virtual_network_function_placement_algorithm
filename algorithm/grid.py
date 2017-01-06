from algorithm.entities import Component, Edge, Link, Node, Server
import numpy as np


class GridFactory(object):

    def __init__(self, data):
        self.data = data
        self.grid = None

    def create_grid(self):
        servers = self.__create_servers(self.data)
        components = self.__create_components(self.data)

        self.grid = Grid(servers, components)

    def __create_servers(self, data):
        min_powers = data['P_min']
        max_powers = data['P_max']
        servers_available_resources = data['av']
        node_server_location = data['al']

        servers = []
        server_id = 0
        for min_power, max_power, available_resources in zip(min_powers, max_powers, servers_available_resources[0]):
            node_id = np.argmax(node_server_location[server_id])

            server = Server(
                server_id=server_id,
                node_id=node_id,
                min_power=min_power,
                max_power=max_power,
                resources_available=available_resources
            )

            server_id += 1
            servers.append(server)

        return np.array(servers)

    def __create_components(self, data):
        resources_needed = data['req']
        processor_resources_needed = resources_needed[0]

        components = []
        for component_id, resources_needed in enumerate(processor_resources_needed):
            component = Component(resources_needed)
            components.append(component)

        return components

    def get_grid(self):
        assert self.grid is not None, 'You must call build_grid before this method!'

        return self.grid


class Grid(object):

    def __init__(self, servers, components):
        self.servers = servers
        self.components = components