class IdolGraph():
    def __init__(self, input_file_name: str):
        self.n_deg_dict = {}
        self.m_edges = 0
        self.graph = {}
        self.input_file_name = input_file_name

    def load_graph(self) -> bool:
        try:
            with open(self.input_file_name) as def_file:
                self.m_edges = int(def_file.readline().rstrip())
                for it in range(self.m_edges):
                    buffor_line = def_file.readline().rstrip().split(", ")
                    p, q = int(buffor_line[0]), int(buffor_line[1])
                    if p not in self.graph:
                        self.graph[p] = []
                    self.graph[p].append(q)
                    if p not in self.n_deg_dict:
                        self.n_deg_dict[p] = 0
                    if q not in self.n_deg_dict:
                        self.n_deg_dict[q] = 1
                    else:
                        self.n_deg_dict[q] += 1
        except FileNotFoundError or IOError:
            print("Error while loading graph from file. Script will now terminate.")
            exit(-1)
        return True

    def save_result(self, output_file_name: str, does_idol_exist: bool) -> bool:
        try:
            with open(output_file_name, "w") as out_file:
                if does_idol_exist:
                    out_file.write("TAK")
                else:
                    out_file.write("NIE")
        except IOError:
            print("Result was acquired successful but there was IOError while file saving!")
            return False
        return True

    def look_for_idol(self) -> bool:
        for it in self.n_deg_dict:
            if self.n_deg_dict[it] == 0 and len(self.graph[it]) == (len(self.n_deg_dict)-1):
                return True
        return False


# Zadanie 3: Odpowiedz na pytanie, czy w tej grupie n osób istnieje idol? [W czasie liniowym]
#
# W tym zadaniu wynikiem jest wypisanie na standardowym wyjciu 'TAK' gdy jest idol lub 'NIE' gdy nie ma.
# W celui rozwiazania zadania w czasie liniowym, należało zauważyć pewną własność grafu
# skierowanego acyklicznego w zadaniu nr 2 z Sortowaniem Topologicznym.
# Posiadając zapisany graf w formie słownik listy sąsiaów oraz słownika występujących wierzchołków z licznikiem,
# Jesteśmy w stanie najpozniej w czasie O(n/2) znaleźć wierzchołek (potencjalnego idola) z liczbą zależności
# 'do niego' równą 0. Następnie sprawdzamy w czasie stałym:
#  O(n/2) - wybranie elementu ze słownika :: self.graph[p]
#  O(n/2) - zliczenie liczby indeksów     :: len(self.graph[p])
#  O(n/2) - zliczenie wszystkich indeksów :: len(self.n_deg_dict)-1)
# Dla powyższych rozważań teoretycznych możemy założyć, że wyszukanie idola w tak konsturowanym grafie
# Powinno mieć złożoność liniową w granicach ~O(2*n)
if __name__ == "__main__":
    idol = False
    graf = IdolGraph("idol.txt")
    if graf.load_graph():
        idol = graf.look_for_idol()
    if idol:
        print("TAK")
    else:
        print("NIE")
    exit(0)
