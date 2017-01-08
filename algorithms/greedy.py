from algorithms import Algorithm


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
        raise NotImplementedError
