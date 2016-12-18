from numpy import loadtxt
from io import StringIO


class Parser(object):
    integer_variables = ('numServers', 'numVms', 'numRes', 'numNodes', 'numServiceChains')
    list_variables = ('lat', 'P_max', 'P_min', 'P')
    matrix_variables = ('req', 'av', 'al', 'sc')
    list_vector_variables = ('Edges', 'VmDemands')

    def __init__(self, file_path):
        assert isinstance(file_path, str), 'File path must be string'

        self.file_path = file_path
        self.data = dict()

        self.parser_factory = {
            self.integer_variables: self.__parse_integers,
            self.list_variables: self.__parse_lists,
            self.matrix_variables: self.__parse_matrices,
            self.list_vector_variables: self.__parse_list_vectors
        }

    def read(self):
        lines = open(self.file_path).read().replace('\n', '').split(';')
        return filter(None, lines)

    def parse(self):
        lines = self.read()

        for i, line in enumerate(lines):
            var_name, var_content = line.split(' = ')

            for variables, extractor in self.parser_factory.items():
                if var_name in variables:
                    self.data[var_name] = extractor(var_content)

    def __parse_integers(self, var_content):
        return int(var_content)

    def __parse_lists(self, var_content):
        return loadtxt(StringIO(var_content[1:-1]), delimiter=',')

    def __parse_matrices(self, var_content):
        content = var_content[1:-1].replace('][', '\n')[1:-1]
        return loadtxt(StringIO(content), delimiter=',')

    def __parse_list_vectors(self, var_content):
        content = var_content[1:-1].replace('>,', '\n').replace('<', '')
        return loadtxt(StringIO(content), delimiter=',')

    def __getitem__(self, item):
        return self.data.get(item)

    def __str__(self):
        return self.data.__str__()


def main():
    parser = Parser('../data/instance.txt')
    parser.parse()
    print(parser)

if __name__ == '__main__':
    main()
