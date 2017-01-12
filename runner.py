from core.problem import Problem, WriterService
from algorithms.greedy import GreedyHeuristic


def main():
    problem = Problem(file_path='data/instance.txt')

    for i in range(1000000):
        problem.init()

        greedy = GreedyHeuristic(problem)
        greedy.deploy_components()
        greedy.deploy_routes()
        cost = problem.fitness()
        print('Cost: {0}\n'.format(cost))

        if cost < 4085:
            problem.constraint_service.check_all()
            problem.constraint_service.print_al_constraints()

            print()
            writer = WriterService(problem)
            writer.write(file_path='solutions/solution.txt')
            break


if __name__ == '__main__':
    main()
