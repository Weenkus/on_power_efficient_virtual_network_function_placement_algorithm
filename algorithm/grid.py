from algorithm.entities import Component, Link, Node, Server
import numpy as np


class GridFactory(object):

    def __init__(self, data):
        self.data = data
        self.grid = None

    def create_grid(self):
        servers = self.__create_servers(self.data)
        components = self.__create_components(self.data)
        nodes = self.__create_nodes(self.data, servers)
        layout = self.__create_layout(self.data, nodes)

        self.grid = Grid(servers, components, nodes, layout)

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

    def __create_nodes(self, data, servers):
        server_num = data['numServers']
        node_num = data['numNodes']
        power_usages = data['P']

        assert server_num == len(servers), 'Mismatch in server numbers.'

        nodes = []
        for node_id, power_usage in zip(range(node_num), power_usages):

            current_node_servers = [server for server in servers if server.node_id == node_id]
            node = Node(servers=current_node_servers, power_usage=power_usage)
            nodes.append(node)

        assert node_num == len(nodes), 'Mismatch in node numbers.'
        return nodes

    def __create_layout(self, data, nodes):
        edges = data['Edges']
        num_nodes = data['numNodes']

        layout = [[None] * num_nodes] * num_nodes
        for edge in edges:
            first_node_id, second_node_id, capacity, power_usage, delay = edge
            first_node_id, second_node_id = int(first_node_id) - 1, int(second_node_id) - 1

            first_node = nodes[first_node_id]
            second_node = nodes[second_node_id]

            new_edge = Edge(first_node, second_node, delay, capacity, power_usage)
            self.__set_edges(first_node_id, second_node_id, layout, new_edge, nodes)

        return layout

    def __set_edges(self, first_node_id, second_node_id, layout, new_edge, nodes):
        layout[first_node_id][second_node_id] = new_edge
        layout[second_node_id][first_node_id] = new_edge

        nodes[first_node_id].add_adjacent_node(nodes[second_node_id])
        nodes[second_node_id].add_adjacent_node(nodes[first_node_id])

    def get_grid(self):
        assert self.grid is not None, 'You must call build_grid before this method!'

        return self.grid


class Edge(object):

    def __init__(self, from_node, to_node, delay, capacity, power_usage):
        assert from_node != to_node, 'Link is between two different nodes.'
        for node in [from_node, to_node]:
            assert isinstance(node, Node), 'Nodes should be an instance of Node.'

        self.delay = delay
        self.capacity = capacity
        self.power_usage = power_usage


class Grid(object):

    def __init__(self, servers, components, nodes, layout):
        self.servers = servers
        self.components = components
        self.nodes = nodes
        self.layout = layout
