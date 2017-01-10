from algorithms import Algorithm
import random


class GreedyHeuristic(Algorithm):

    def __init__(self, problem):
        super(GreedyHeuristic, self).__init__(problem)

    def deploy_components(self):
        servers = sorted(self.problem.grid.servers, key=lambda x: x.max_power, reverse=True)
        components = sorted(self.problem.grid.components, key=lambda x: x.resources_needed, reverse=True)

        for component in components:
            for server in servers:
                if server.get_available_resources() > component.resources_needed:
                    server.add_component(component)
                    break

        empty_servers = [server.server_id for server in servers if not server.is_active()]
        print('Empty servers: {0} - {1}'.format(len(empty_servers), empty_servers))

    def deploy_routes(self):
        link_demands = sorted(self.problem.grid.link_demands, key=lambda x: x.throughput, reverse=False)

        empty_demands = []
        for link_demand in link_demands:
            link = link_demand.link
            routes = self.problem.grid.get_routes(link.start_component, link.end_component)

            if len(routes) > 0:
                valid_routes = self.__filter_non_valid_routes(routes, link_demand.throughput)

                if len(valid_routes) == 0:
                    empty_demands.append(link_demand)
                    continue

                valid_routes = sorted(valid_routes, key=lambda x: len(x), reverse=False)
                self.problem.grid.add_link_route(link, valid_routes[0], link_demand.throughput)

        print('Empty demands: {0} - {1}'.format(len(empty_demands), empty_demands))

    def __filter_non_valid_routes(self, routes, throughput):
        return list(filter(lambda x: self.problem.grid.min_available_route_capacity(x) > throughput, routes))
