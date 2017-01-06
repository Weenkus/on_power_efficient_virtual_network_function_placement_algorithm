import numpy as np


class ExpressionChecker(object):

    @staticmethod
    def constraint_component_has_server(components):
        components_servers_count = map(lambda x: x != 1, np.sum(components, axis=1))
        return not any(components_servers_count)

    @staticmethod
    def are_servers_active(components):
        return map(lambda x: x > 0, np.sum(components, axis=0))

    @staticmethod
    def servers_used_more_resources_then_available(components, arv, ars):
        pass






class Calculator(object):

    @staticmethod
    def fitness(P_min, ys, P_max, ars, arv, xvs, P_node, zn, P_link):
        raise NotImplementedError
