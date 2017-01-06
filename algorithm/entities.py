
class Link(object):

    def __init__(self, from_component, to_component, throughput):
        for component in [from_component, to_component]:
            assert isinstance(component, Component), 'Components should be an instance of Component.'
        assert from_component != to_component, 'From and to components should be different.'

        self.from_component = from_component
        self.to_component = to_component
        self.throughput = throughput


class Edge(object):

    def __init__(self, from_node, to_node, delay, throughput, power_usage):
        assert from_node != to_node, 'Link is between two different nodes.'
        for node in [from_node, to_node]:
            assert isinstance(node, Node), 'Nodes should be an instance of Node.'

        self.delay = delay
        self.throughput = throughput
        self.power_usage = power_usage


class Node(object):

    def __init__(self, servers, power_usage):
        for server in servers:
            assert isinstance(server, Server), "Servers should be instance of Server."

        self.servers = servers
        self.power_usage = power_usage

    def number_of_servers(self):
        return len(self.servers)


class Server(object):

    def __init__(self, node_id, components, min_power, max_power, resources_available):
        assert max_power > min_power, 'Max power should be higher then min power.'
        assert node_id > -1, 'Node ID should be a greater then -1.'
        for component in components:
            assert isinstance(component, Component), 'Components should be an instance of Component.'

        self.resources_available = resources_available
        self.node_id = node_id
        self.components = components
        self.min_power = min_power
        self.max_power = max_power
        self.is_active = self.__is_active()

        assert self.__has_needed_resources(), 'Server does not have the necessary resources for all components.'

        print('Server {0} has no components and is inactive'.format(self.node_id))

    def __is_active(self):
        return len(self.components) > 0

    def __has_needed_resources(self):
        resources_needed = sum([component.resources_needed() for component in self.components])
        return resources_needed < self.resources_available

    def number_of_components(self):
        return len(self.components)

    def add_component(self, component):
        assert isinstance(component, Component), 'Component should be an instance of Component'
        self.components.append(component)

    def add_components(self, components):
        for component in components:
            self.add_component(component)


class Component(object):

    def __init__(self, server_id, resources_needed):
        assert server_id > -1, 'Every component needs to have a server (server ID should be greater then -1).'

        self.resources_needed = resources_needed
        self.server_id = server_id

    def resources_needed(self):
        return self.resources_needed


