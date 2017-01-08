from core.problem import Problem
from algorithms.greedy import GreedyHeuristic


def main():
    problem = Problem(file_path='data/instance.txt')
    problem.init()

    greedy = GreedyHeuristic(problem)
    greedy.deploy_components()

    problem.constraint_service.print_al_constraints()
    print(problem.fitness())

if __name__ == '__main__':
    main()
