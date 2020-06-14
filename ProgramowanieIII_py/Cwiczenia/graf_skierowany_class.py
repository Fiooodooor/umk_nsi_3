class DirectedGraph:
    def __init__(self):
        self.vertex_lst = {}
        self.edges_lst = {}

    def add_vertex(self, vertex: str) -> bool:
        if vertex not in self.vertex_lst:
            self.vertex_lst[vertex] = 0
            self.edges_lst[vertex] = []
            return True
        print("add_vertex: Vertex already exist")
        return False

    def add_edge(self, start_vertex: str, end_vertex: str) -> bool:
        if start_vertex == end_vertex:
            print("add_edge: start_vertex == end_vertex. No loops allowed.")
            return False
        if start_vertex not in self.vertex_lst:
            print("add_edge: start_vertex does not exist")
            return False
        if end_vertex not in self.vertex_lst:
            print("add_edge: end_vertex does not exist")
            return False
        if end_vertex not in self.edges_lst[start_vertex]:
            self.edges_lst[start_vertex].append(end_vertex)
            return True
        print("add_edge: Edge already exist")
        return False

    def show_vertex_degree(self, vertex: str) -> int:
        if vertex not in self.vertex_lst:
            print("show_vertex_degree: vertex does not exist")
            return -1
        degree = 0
        for it in self.vertex_lst:
            for it_j in self.edges_lst[it]:
                if it_j == vertex:
                    degree += 1
        degree += len(self.edges_lst[vertex])
        return degree

    def clear_graph(self):
        self.vertex_lst.clear()
        self.edges_lst.clear()

    def search_graph_dfs(self, start_vertex: str):
        if start_vertex not in self.vertex_lst:
            print("search_graph_dfs: start_vertex does not exist")
            return
        visited = [start_vertex]
        to_visit = self.edges_lst[start_vertex].copy()
        while len(to_visit) > 0:
            act = to_visit.pop()
            if act not in visited:
                visited.append(act)
                for it in self.edges_lst[act]:
                    if it not in visited and it not in to_visit:
                        to_visit.append(it)
        print("Visited vertexes: ")
        print(visited)


class UndirectedGraph(DirectedGraph):
    def __init__(self):
        super().__init__()

    def init_with_directed(self, dGraph : DirectedGraph):
        self.vertex_lst = dGraph.vertex_lst.copy()
        self.edges_lst = dGraph.edges_lst.copy()
        for it in dGraph.vertex_lst:
            for it_j in dGraph.edges_lst[it]:
                if it_j not in self.edges_lst[it]:
                    self.edges_lst[it].append(it_j)
                if it not in self.edges_lst[it_j]:
                    self.edges_lst[it_j].append(it)

    def add_edge(self, start_vertex: str, end_vertex: str) -> bool:
        if super().add_edge(start_vertex, end_vertex) == False:
            return False
        if super().add_edge(end_vertex, start_vertex) == False:
            return False
        return True

if __name__ == "__main__":
    graf = DirectedGraph()
    graf.add_vertex("a")
    graf.add_vertex("b")
    graf.add_vertex("c")
    graf.add_vertex("d")
    graf.add_vertex("e")
    graf.add_vertex("f")
    graf.add_vertex("g")
    graf.add_vertex("h")
    graf.add_edge("a", "b")
    graf.add_edge("a", "f")
    graf.add_edge("c", "b")
    graf.add_edge("c", "d")
    graf.add_edge("d", "e")
    graf.add_edge("e", "b")
    graf.add_edge("e", "f")
    graf.add_edge("f", "b")
    graf.add_edge("f", "c")
    graf.add_edge("g", "b") # not in path for directed graph; in for undirected
    graf.add_edge("h", "g") # not in path for directed graph; in for undirected
    graf.search_graph_dfs("a")

    graf1 = UndirectedGraph()
    graf1.init_with_directed(graf)
    graf1.search_graph_dfs("a")

    exit(0)