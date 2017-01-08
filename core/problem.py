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

        print(sum(edges_power_costs), sum(nodes_power_costs), sum(servers_power_costs))
        return sum(edges_power_costs) + sum(nodes_power_costs) + sum(servers_power_costs)

    def __get_server_power_usage(self, server):
        node = self.grid.get_servers_node(server)

        if server.is_active() and self.grid.is_active_node(node):
            server_components_power_usage = sum([component.resources_needed for component in server.components])
            average_server_power = (server.max_power - server.min_power) / server.max_resources
            server_power = server.min_power + average_server_power * server_components_power_usage

            return server_power
        else:
            return 0

    def active_servers(self):
        return [server for server in self.grid.servers if server.is_active()]


class ConstraintService(object):

    def __init__(self, grid):
        self.grid = grid

        self.constraints = [
            (self.components_are_deployed, 'Every component is deployed.'),
            (
                self.servers_did_not_use_more_resources_then_they_have,
                'Servers are not using more resources then they have.'
            ),
            (self.edge_traffic_is_lower_then_edge_capacity, 'Edge traffic is lower then edge capacity.'),
            (self.service_chains_are_within_max_delay_range, 'Service chains are within max delay range.'),
            (self.every_link_demand_is_met, 'Ever link demand is not met.')
        ]

    def print_al_constraints(self):
        for constraint in self.constraints:
            constraint_function, constraint_description = constraint
            print('[{0}] {1}'.format(constraint_function(), constraint_description))

    def check_all(self):
        for constraint in self.constraints:
            constraint_function, constraint_description = constraint
            if not constraint_function():
                return False
        return True

    def components_are_deployed(self):
        for component in self.grid.components:
            if not component.is_deployed_on_server():
                return False
        return True

    def servers_did_not_use_more_resources_then_they_have(self):
        for server in self.grid.servers:
            if server.is_using_more_resources_then_available():
                return False
        return True

    def edge_traffic_is_lower_then_edge_capacity(self):
        for edge in self.grid.edges:
            total_edge_traffic = self.grid.throughput_on_edge(edge)
            if total_edge_traffic > edge.capacity:
                return False
        return True

    def service_chains_are_within_max_delay_range(self):
        for service_chain in self.grid.service_chains:
            if not service_chain.link_delays_are_within_max_delay():
                return False
        return True

    def every_link_demand_is_met(self):
        for link_demand in self.grid.link_demands:
            components_are_on_same_server = self.grid.link_has_both_components_on_same_server(link_demand.link)
            if link_demand.get_route_length() == 0 and not components_are_on_same_server:
                return False
        return True
