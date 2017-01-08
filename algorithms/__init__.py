
class Algorithm(object):

    def __init__(self, problem):
        self.problem = problem

    def deploy_components(self):
        raise NotImplementedError

    def route_components(self):
        raise NotImplementedError