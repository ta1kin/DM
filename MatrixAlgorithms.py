import numpy as np
import collections as col
import sys


class Algorithms:

    def __init__(self, matrix: (list, np.array), start=0, end=None) -> object:
        self.adj_matrix = np.array(matrix.copy())
        self.start = int(start)
        if isinstance(end, int):
            self.end = int(end)
        else:
            self.end = None

    def __warshall(self):
        for i in range(self.adj_matrix.shape[0]):
            for j in range(self.adj_matrix.shape[1]):
                if self.adj_matrix[i, j] == 1:
                    self.adj_matrix[i] = self.adj_matrix[i] + self.adj_matrix[j]

        self.adj_matrix[self.adj_matrix > 0] = 1

        text = np.array2string(self.adj_matrix).replace('[', '').replace(']', '')
        text = '  ' + text.replace('', ' ')

        return text

    def __traversing_the_graph_in_width(self, vert=0):
        n = self.adj_matrix.shape[0]  # Количество вершин в графе
        if vert not in range(n):
            vert = 0
        visited = np.zeros(n, dtype=bool)  # Инициализируем массив для отслеживания посещенных вершин
        traversal = []  # Инициализируем список для сохранения порядка обхода BFS
        a = list(range(n))
        a.remove(vert)
        a[0] = vert

        # Выполним BFS, начиная с заданной вершины
        def bfs_start(vertex):
            queue = col.deque()
            queue.append(vertex)
            visited[vertex] = True

            while queue:
                current_vertex = queue.popleft()
                traversal.append(current_vertex)

                # Найдем индексы соседних вершин, используя матрицу смежности
                neighbors = np.where(self.adj_matrix[current_vertex] == 1)[0]

                # Поставим в очередь непрошеных соседей
                for neighbor in neighbors:
                    if not visited[neighbor]:
                        queue.append(neighbor)
                        visited[neighbor] = True

        # Выполним BFS для каждой непосещенной вершины
        for vertex in a:
            if not visited[vertex]:
                bfs_start(vertex)
        text = str(traversal)
        text += f'\nДлина путии: {len(traversal)}'

        return text

    def __traversing_the_graph_in_deep(self, vert=0):
        n = self.adj_matrix.shape[0]  # Количество вершин в графе
        if vert not in range(n):
            vert = 0
        visited = np.zeros(n, dtype=bool)  # Инициализируем массив для отслеживания посещенных вершин
        traversal = []  # Инициализируем список для сохранения порядка обхода DFS
        a = list(range(n))
        a.remove(vert)
        a[0] = vert

        # Выполним DFS, начиная с заданной вершины
        def dfs_recursive(vertex):
            visited[vertex] = True
            traversal.append(vertex)

            # Найдем индексы соседних вершин, используя матрицу смежности
            neighbors = np.where(self.adj_matrix[vertex] == 1)[0]
            neighbors = neighbors[::-1]
            # Рекурсивно посетим все соседние
            for neighbor in neighbors:
                if not visited[neighbor]:
                    dfs_recursive(neighbor)

        # Выполните DFS для каждой непосещенной вершины
        for vertex in a:
            if not visited[vertex]:
                dfs_recursive(vertex)

        text = str(traversal)
        text += f'\nДлина путии: {len(traversal)}'

        return text

    def __floyd_algorithm(self):
        n = len(self.adj_matrix)
        dist = self.adj_matrix

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        text = ''
        for row in dist:
            for i in row:
                text += str(i) + ' '
            text += '\n'
            # print(text)

        return text

    def __the_danzig_algorithm(self):
        n = len(self.adj_matrix)
        dist = self.adj_matrix
        all_text = ''

        for k in range(n):
            new_dist = [[float('inf') for _ in range(n)] for _ in range(n)]

            for i in range(n):
                for j in range(n):
                    new_dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

            dist = new_dist
            all_text += f"Шаг {k + 1}:"+'\n'
            print(f"Шаг {k + 1}:")
            for row in dist:
                all_text += str(row) + '\n'
                print(row)
            all_text += '\n\n'
            print()

        all_text = all_text.replace('[', '').replace(']', '').replace(',', '')
        return all_text

    def __the_ford_fulkerson_algorithm(self, source=0, sink=None):
        if sink is None:
            sink = self.adj_matrix.shape[0] - 1
        n = len(self.adj_matrix)
        residual = [[self.adj_matrix[i][j] for j in range(n)] for i in range(n)]
        flow = [[0 for _ in range(n)] for _ in range(n)]
        parents = [-1] * n  # Список для отслеживания родителей вершин в найденных путях

        def bfs():
            queue = [source]
            visited = [False] * n
            visited[source] = True

            while queue:
                u = queue.pop(0)
                for v in range(n):
                    if not visited[v] and residual[u][v] > 0:
                        queue.append(v)
                        visited[v] = True
                        parents[v] = u
                        if v == sink:
                            return True  # Путь до стока найден
            return False

        max_flow = 0

        while bfs():
            path_flow = float('inf')
            v = sink
            while v != source:
                u = parents[v]
                path_flow = min(path_flow, residual[u][v])
                v = u

            v = sink
            while v != source:
                u = parents[v]
                residual[u][v] -= path_flow
                residual[v][u] += path_flow
                flow[u][v] += path_flow
                v = u

            max_flow += path_flow

        text = '['
        for row in flow:
            text += str(row) +',\n'
        text = text[:-2] + ']\n'
        text += f'Максимальный путь: {str(max_flow)}'

        return text

    def __dijkstra_algorithm(self, start_node=0, end_node=None):
        if end_node is None:
            end_node = self.adj_matrix.shape[0] - 1
        nodes = list(range(len(self.adj_matrix)))
        graph = {}
        for i in range(len(self.adj_matrix)):
            g = {j: self.adj_matrix[i][j] for j in range(len(self.adj_matrix[i])) if self.adj_matrix[i][j] != 0}
            graph[i] = g

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value

        def get_outgoing_edges(node):
            """Возвращает соседей узла"""
            connections = []
            for out_node in nodes:
                if graph[node].get(out_node, False) != False:
                    connections.append(out_node)
            return connections

        unvisited_nodes = nodes

        # Мы будем использовать этот словарь, чтобы сэкономить на посещении каждого узла и обновлять его по мере продвижения по графику
        shortest_path = {}

        # Мы будем использовать этот dict, чтобы сохранить кратчайший известный путь к найденному узлу
        previous_nodes = {}

        # Мы будем использовать max_value для инициализации значения "бесконечности" непосещенных узлов
        max_value = sys.maxsize
        for node in unvisited_nodes:
            shortest_path[node] = max_value
        # Однако мы инициализируем значение начального узла 0
        shortest_path[start_node] = 0

        # Алгоритм выполняется до тех пор, пока мы не посетим все узлы
        while unvisited_nodes:
            # Приведенный ниже блок кода находит узел с наименьшей оценкой
            current_min_node = None
            for node in unvisited_nodes:  # Iterate over the nodes
                if current_min_node == None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node

            # Приведенный ниже блок кода извлекает соседей текущего узла и обновляет их расстояния
            neighbors = get_outgoing_edges(current_min_node)
            for neighbor in neighbors:
                tentative_value = shortest_path[current_min_node] + graph[current_min_node][neighbor]
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    # We also update the best path to the current node
                    previous_nodes[neighbor] = current_min_node

            # После посещения его соседей мы отмечаем узел как "посещенный"
            unvisited_nodes.remove(current_min_node)
        path = []
        node = end_node
        while node != start_node:
            path.append(node)
            node = previous_nodes[node]

        # Добавить начальный узел вручную
        path.append(start_node)

        text = str(list(reversed(path)))
        text += f'\nКротчайший путь: {shortest_path[end_node]}'

        return text

    def choice(self, name_algorithms, *args, **kwargs):
        if name_algorithms == 'Алгоритм Уоршалла':
            return self.__warshall()
        elif name_algorithms == 'Обход графа в ширину':
            return self.__traversing_the_graph_in_width(self.start)
        elif name_algorithms == 'Обход графа в глубину':
            return self.__traversing_the_graph_in_deep(self.start)
        elif name_algorithms == 'Алгоритм Флойда':
            return self.__floyd_algorithm()
        elif name_algorithms == 'Алгоритм Данцига':
            return self.__the_danzig_algorithm()
        elif name_algorithms == 'Алгоритм Форда-Фалкерсона':
            return self.__the_ford_fulkerson_algorithm(self.start, self.end)
        elif name_algorithms == 'Алгоритм Дейкстры':
            return self.__dijkstra_algorithm(self.start, self.end)

