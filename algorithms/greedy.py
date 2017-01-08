from algorithms import Algorithm


class GreedyHeuristic(Algorithm):

    def __init__(self, problem):
        super(GreedyHeuristic, self).__init__(problem)

    def deploy_components(self):
        for component in self.problem.grid.components:
            for server in self.problem.grid.servers:
                if server.get_available_resources() > component.resources_needed:
                    server.add_component(component)
                    break
