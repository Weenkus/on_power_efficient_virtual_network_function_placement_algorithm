from core.problem import Problem


def main():
    problem = Problem(file_path='data/instance.txt')
    problem.init()
    print(problem.fitness())

if __name__ == '__main__':
    main()
