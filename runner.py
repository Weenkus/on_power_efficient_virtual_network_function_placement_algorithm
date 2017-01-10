from core.problem import Problem
from algorithms.greedy import GreedyHeuristic


def main():
    problem = Problem(file_path='data/instance.txt')
    problem.init()

    greedy = GreedyHeuristic(problem)
    greedy.deploy_components()
    greedy.deploy_routes()
    print('Cost: {0}'.format(problem.fitness()))

    problem.constraint_service.check_all()
    problem.constraint_service.print_al_constraints()


if __name__ == '__main__':
    main()
