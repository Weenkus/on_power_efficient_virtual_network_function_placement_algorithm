from core.grid import GridFactory
from core.parser import Parser
import numpy as np


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
            (self.every_link_demand_is_met, 'Ever link demand is met.')
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
        constraint_failed = False
        for link_demand in self.grid.link_demands:
            components_are_on_same_node = self.grid.are_components_on_same_node(
                link_demand.link.start_component, link_demand.link.end_component
            )

            if link_demand.get_route_length() == 0 and not components_are_on_same_node:
                constraint_failed = True

        return not constraint_failed


class WriterService(object):

    def __init__(self, program):
        self.program = program

    def write(self, file_path=None):
        if file_path is None:
            print(self.__generate_output_string())
        else:
            with open(file_path, 'w') as output_file:
                output_file.write(self.__generate_output_string())

    def __generate_output_string(self):
        output_string = 'x={0};\n\nroutes={1};'.format(
            self.__generate_component_server_matrix(),
            self.__generate_routes()
        )
        return output_string

    def __generate_component_server_matrix(self):
        component_server_matrix = []
        server_num = len(self.program.grid.servers)
        for component in self.program.grid.components:
            component_sever_one_hot = [0] * server_num
            component_sever_one_hot[component.server_id] = 1

            row_format = '[{0}]'.format((','.join(map(lambda x: str(x), component_sever_one_hot))))
            component_server_matrix.append(row_format)

        return '[\n{0}\n]'.format('\n'.join(component_server_matrix))

    def __generate_routes(self):
        routes = []
        for link_demand in self.program.grid.link_demands:
            # print(self.program.grid.get_component_node(link_demand.link.start_component))
            # print(self.program.grid.get_component_node(link_demand.link.end_component))
            # print(link_demand)
            # print()

            node_route = link_demand.link.nodes.__str__().replace(' ', '')

            if node_route == '[]':
                node = self.program.grid.get_component_node(link_demand.link.end_component)
                node_route = '[%d]' % (node.node_id + 1)

            route_string = '<{0},{1},{2}>'.format(
                link_demand.link.start_component.component_id + 1,
                link_demand.link.end_component.component_id + 1,
                node_route
            )
            routes.append(route_string)

        return '{\n' + ',\n'.join(routes) + ',\n}'
