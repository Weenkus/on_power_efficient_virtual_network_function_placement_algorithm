

class Edge(object):

    def __init__(self, from_node, to_node, delay, capacity, power_usage):
        assert from_node != to_node, 'Link is between two different nodes.'
        for node in [from_node, to_node]:
            assert isinstance(node, Node), 'Nodes should be an instance of Node.'

        self.delay = delay
        self.capacity = capacity
        self.power_usage = power_usage
        self.start_node = from_node
        self.end_node = to_node

    def has_node(self, node):
        assert isinstance(node, Node), 'Node should be an instance of Node.'
        return node.node_id in [self.start_node.node_id, self.end_node.node_id]

    def __str__(self):
        return 'Start_node: {0}, end_node: {1}, delay: {2}, capacity: {3}, power_usage: {4}'.format(
            self.start_node, self.end_node, self.delay, self.capacity, self.power_usage
        )


class Link(object):

    def __init__(self, start_component, end_component, throughput):
        for component in [start_component, end_component]:
            assert isinstance(component, Component), 'Components should be instances of Component.'

        self.start_component = start_component
        self.end_component = end_component
        self.throughput = throughput


class ServiceChain(object):

    def __init__(self, components):
        for component in components:
            assert isinstance(component, Component), 'Components should be instances of Component.'

        self.components = components
        self.route = []

    def add_route(self, edges):
        for edge in edges:
            assert isinstance(edge, Edge), 'Edges should be instances of Edge.'

        self.route = edges

    def add_edge(self, edge):
        assert isinstance(edge, Edge), 'Edge should be an instance of Edge.'
        self.route.append(edge)

    def clear_route(self):
        self.route = []

    def has_edge(self, edge):
        assert isinstance(edge, Edge), 'Edge should be an instance of Edge.'
        return edge in self.route

    def has_node(self, node):
        assert isinstance(node, Node), 'Node should be an instance of Node.'
        return any([edge.has_node(node) for edge in self.route])

    def __str__(self):
        return '\n'.join(self.route) + '\n'


class Node(object):

    def __init__(self, node_id, servers, power_usage):
        for server in servers:
            assert isinstance(server, Server), "Servers should be an instance of Server."

        self.node_id = node_id
        self.servers = servers
        self.power_usage = power_usage
        self.adjacent_nodes = []

    def number_of_servers(self):
        return len(self.servers)

    def add_adjacent_node(self, node):
        assert isinstance(node, Node), 'Node should be an instance of Node.'
        self.adjacent_nodes.append(node)

    def __str__(self):
        return 'ID: {0}, power_usage: {1}'.format(self.node_id, self.power_usage)


class Server(object):

    def __init__(self, server_id, node_id, min_power, max_power, resources_available):
        assert max_power > min_power, 'Max power should be higher then min power.'
        assert node_id > -1, 'Node ID should be a greater then -1.'

        self.components = []
        self.server_id = server_id
        self.resources_available = resources_available
        self.node_id = node_id
        self.min_power = min_power
        self.max_power = max_power

        assert self.__has_needed_resources(), 'Server does not have the necessary resources for all components.'

    def is_active(self):
        return len(self.components) > 0

    def __has_needed_resources(self):
        resources_needed = sum([component.resources_needed() for component in self.components])
        return resources_needed < self.resources_available

    def number_of_components(self):
        return len(self.components)

    def add_component(self, component):
        assert isinstance(component, Component), 'Component should be an instance of Component'
        component.add_server_id(server_id=self.server_id)
        self.components.append(component)

    def add_components(self, components):
        for component in components:
            self.add_component(component)

    def is_using_more_resources_then_available(self):
        resources_used = sum([component.resources_needed for component in self.components])
        return resources_used > self.resources_available

    def __str__(self):
        return 'ID: {0}, active: {1}, min_power: {2}, max_power: {3}, res_available: {4}'.format(
            self.server_id, self.is_active, self.min_power, self.max_power, self.resources_available
        )


class Component(object):

    def __init__(self, resources_needed, server_id=None):
        self.resources_needed = resources_needed
        self.server_id = server_id

    def resources_needed(self):
        return self.resources_needed

    def add_server_id(self, server_id):
        assert server_id > -1, 'Every component needs to have a server (server ID should be greater then -1).'
        self.server_id = server_id

    def is_deployed_on_server(self):
        return self.server_id is not None

    def __str__(self):
        return 'Server ID: {0}, resources needed: {1}'.format(self.server_id, self.resources_needed)
