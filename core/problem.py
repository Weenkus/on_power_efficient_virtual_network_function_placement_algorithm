from core.grid import GridFactory
from core.parser import Parser


class Problem(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.grid = None
        self.constraint_service = None

    def init(self):
        parser = Parser(self.file_path)
        parser.parse()

        grid_factory = GridFactory(parser.get_parsed_data())
        grid_factory.create_grid()
        self.grid = grid_factory.get_grid()

        self.constraint_service = ConstraintService(self.grid)

    def fitness(self):
        edges_power_costs = [edge.power_usage for edge in self.grid.edges if self.grid.is_active_edge(edge)]
        nodes_power_costs = [node.power_usage for node in self.grid.nodes if self.grid.is_active_node(node)]
        servers_power_costs = [self.__get_server_power_usage(server) for server in self.grid.servers]

        return sum(edges_power_costs) + sum(nodes_power_costs) + sum(servers_power_costs)

    def __get_server_power_usage(self, server):
        if server.is_active():
            server_components_power_usage = sum([component.resources_needed for component in server.components])
            average_server_power = (server.max_power - server.min_power) * server.resources_available
            server_power = server.min_power + average_server_power * server_components_power_usage
            return server_power
        else:
            return 0


class ConstraintService(object):

    def __init__(self, grid):
        self.grid = grid

    def components_are_deployed(self):
        for component in self.grid.components:
            if not component.is_deployed_on_server():
                return False
        return True

    def servers_are_active(self):
        for server in self.grid.servers:
            if not server.is_active():
                return False
        return True

    def servers_did_not_use_more_resources_then_they_have(self):
        for server in self.grid.servers:
            if server.is_using_more_resources_then_available():
                return False
        return True

