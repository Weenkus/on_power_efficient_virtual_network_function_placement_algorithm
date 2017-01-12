from core.problem import Problem, WriterService
from algorithms.greedy import GreedyHeuristic


def main():
    problem = Problem(file_path='data/instance.txt')
    problem.init()

    greedy = GreedyHeuristic(problem)
    greedy.deploy_components()
    greedy.deploy_routes()
    print('Cost: {0}\n'.format(problem.fitness()))

    problem.constraint_service.check_all()
    problem.constraint_service.print_al_constraints()

    print()
    writer = WriterService(problem)
    writer.write(file_path='solution.txt')


if __name__ == '__main__':
    main()
