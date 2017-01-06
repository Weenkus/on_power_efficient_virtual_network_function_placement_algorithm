from algorithm.grid import GridFactory
from algorithm.parser import Parser


def main():
    grid = init_grid()


def init_grid():
    parser = Parser('data/instance.txt')
    parser.parse()

    grid_factory = GridFactory(parser.get_parsed_data())
    grid_factory.create_grid()
    return grid_factory.get_grid()

if __name__ == '__main__':
    main()
