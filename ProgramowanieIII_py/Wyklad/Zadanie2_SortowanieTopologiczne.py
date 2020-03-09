class GraphTopologicSort():
    def __init__(self, input_file_name: str, output_file_name: str):
        self.n_vertex = 0
        self.n_degrees = []
        self.m_edges = 0
        self.graph = {}
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name

    def load_graph(self, split_string: str) -> bool:
        try:
            with open(self.input_file_name) as def_file:
                buffor_line = def_file.readline().rstrip().split(" ")
                self.n_vertex, self.m_edges = int(buffor_line[0]), int(buffor_line[1])
                self.n_degrees = [0 for _ in range(self.n_vertex)]
                for it in range(self.m_edges):
                    buffor_line = def_file.readline().rstrip().split(split_string)
                    p, q = int(buffor_line[0]), int(buffor_line[1])
                    if p not in self.graph:
                        self.graph[p] = []
                    self.graph[p].append(q)
                    self.n_degrees[q] += 1
        except FileNotFoundError or IOError:
            print("Error while loading graph from file. Script will terminate.")
            exit(-1)
        return True

    def topologic_sort(self) -> []:
        resulting_order = []
        working_queue = []
        for it in range(self.n_vertex):
            if self.n_degrees[it] == 0:
                working_queue.append(it)
        while working_queue:
            if working_queue[0] in self.graph:
                for it in self.graph.pop(working_queue[0]):
                    self.n_degrees[it] -= 1
                    if self.n_degrees[it] == 0:
                        working_queue.append(it)
            resulting_order.append(working_queue[0])
            del(working_queue[0])
        return resulting_order

    def save_result_to_file(self, result_list: []) -> bool:
        try:
            with open(self.output_file_name, "w") as out_file:
                out_file.write(str(result_list))
        except IOError:
            print("Graph was sorted but not saved. IOError while saving file output.")
            return False
        return True

# Z powodu literówki oraz drobnej nieścisłości w treści zadania
# przyjęto, że plik z danymi posiada następującą postać:

# n m
# a1, b1
# a2, b2
# .., ..
# aM, bM

# gdzie n i m to pierwsza linia pliku i są to dwie liczby całkowite
# n - liczba wierzchołków, tj. a i b należą do zbioru {0, 1, 2, ... , n-1}
# m - liczba krawędzi, tj linie w pliku od 2 do m+1 zawierają kolejne łuki,
#     to znaczy pary liczb całkowitych oddzielonych znakiem spacji i przecinkiem
#     użyty do splitowania string można zmienić w parametrze metody .load_graph ponizej

if __name__ == "__main__":
    graf = GraphTopologicSort("digraf.txt", "topologiczne.txt")
    graf.load_graph(", ")
    the_line = graf.topologic_sort()
    print(the_line)
    graf.save_result_to_file(the_line)
    exit(0)