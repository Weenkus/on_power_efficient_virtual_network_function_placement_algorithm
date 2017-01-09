from algorithms import Algorithm
from utils.exceptions import OutOfCapacityException
from random import shuffle
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

    def deploy_routes(self):
        link_demands = sorted(self.problem.grid.link_demands, key=lambda x: x.throughput, reverse=False)

        for link_demand in link_demands:
            link = link_demand.link
            routes = self.problem.grid.get_routes(link.start_component, link.end_component)
            if len(routes) > 0:
                routes = sorted(routes, key=lambda x: len(x), reverse=False)

                for route in routes:
                    try:
                        self.problem.grid.add_link_route(link, route, link_demand.throughput)
                        break
                    except OutOfCapacityException:
                        continue
