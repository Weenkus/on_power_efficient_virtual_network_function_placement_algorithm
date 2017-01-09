from core.problem import Problem
from algorithms.greedy import GreedyHeuristic


def main():

    run = True
    while run:
        problem = Problem(file_path='data/instance.txt')
        problem.init()
        greedy = GreedyHeuristic(problem)
        greedy.deploy_components()
        greedy.deploy_routes()
        print(problem.fitness())

        run = not problem.constraint_service.check_all()


if __name__ == '__main__':
    main()
