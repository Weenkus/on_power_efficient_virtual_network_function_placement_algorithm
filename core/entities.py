from utils.exceptions import OutOfCapacityException


class Edge(object):

    def __init__(self, from_node, to_node, delay, capacity, power_usage):
        assert from_node != to_node, 'Link is between two different nodes.'
        for node in [from_node, to_node]:
            assert isinstance(node, Node), 'Nodes should be an instance of Node.'

        self.delay = delay
        self.capacity = capacity
        self.capacity_used = 0
        self.power_usage = power_usage
        self.start_node = from_node
        self.end_node = to_node

    def has_node(self, node):
        assert isinstance(node, Node), 'Node should be an instance of Node.'
        return node.node_id in [self.start_node.node_id, self.end_node.node_id]

    def get_available_capacity(self):
        return self.capacity - self.capacity_used

    def add_capacity(self, capacity):
        if capacity > self.get_available_capacity():
            raise OutOfCapacityException

        self.capacity_used += capacity

    def __str__(self):
        return 'Start_node: {0}, end_node: {1}, delay: {2}, capacity: {3}, power_usage: {4}'.format(
            self.start_node, self.end_node, self.delay, self.capacity, self.power_usage
        )


class Link(object):

    def __init__(self, start_component, end_component):
        for component in [start_component, end_component]:
            assert isinstance(component, Component), 'Components should be instances of Component.'

        self.start_component = start_component
        self.end_component = end_component
        self.edges = []
        self.nodes = []

    def add_route(self, nodes):
        for node in nodes:
            assert isinstance(node, Node), 'Nodes should be instances of Node.'
        self.nodes = nodes

    def has_edge(self, edge):
        assert isinstance(edge, Edge), 'Edge should be an instance of Edge.'
        return edge in self.edges

    def has_node(self, node):
        assert isinstance(node, Node), 'Node should be an instance of Node.'
        return any([edge.has_node(node) for edge in self.edges])

    def __str__(self):
        return '[{0} || {1}]'.format(self.start_component, self.end_component)


class LinkDemand(object):

    def __init__(self, link, throughput):
        assert isinstance(link, Link), 'Link should be an instance of Link.'

        self.link = link
        self.throughput = throughput

    def get_route_length(self):
        return len(self.link.edges)

    def __str__(self):
        return self.link.__str__()


class ServiceChain(object):

    def __init__(self, components, max_delay):
        for component in components:
            assert isinstance(component, Component), 'Components should be instances of Component.'

        self.components = components
        self.max_delay = max_delay
        self.links = []

    def get_delay(self):
        delay = 0
        for link in self.links:
            for edge in link.edges:
                delay += edge.delay

        return delay

    def link_delays_are_within_max_delay(self):
        return self.max_delay > self.get_delay()


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
        self.max_resources = resources_available
        self.node_id = node_id
        self.min_power = min_power
        self.max_power = max_power

        assert self.__has_needed_resources(), 'Server does not have the necessary resources for all components.'

    def is_active(self):
        return len(self.components) > 0

    def __has_needed_resources(self):
        resources_needed = sum([component.resources_needed() for component in self.components])
        return resources_needed < self.max_resources

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
        return resources_used > self.max_resources

    def get_available_resources(self):
        resources_used = sum([component.resources_needed for component in self.components])
        available_resources = self.max_resources - resources_used

        assert available_resources >= 0, 'Server can not use more resources than is has.'
        return available_resources

    def __str__(self):
        return 'ID: {0}, active: {1}, min_power: {2}, max_power: {3}, res_available: {4}'.format(
            self.server_id, self.is_active, self.min_power, self.max_power, self.max_resources
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
