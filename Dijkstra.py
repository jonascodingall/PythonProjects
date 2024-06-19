class Node:
    def __init__(self, walkable, x, y):
        self.parent = None
        self.costs = float('inf')
        self.walkable = walkable
        self.x = x
        self.y = y

    def edge(self, kant_node):
        return abs(self.x - kant_node.x) + abs(self.y - kant_node.y)


def create_node_matrix(field):
    matrix = []
    for i in range(len(field)):
        row = []
        for j in range(len(field[i])):
            walkable = field[i][j] != 1
            row.append(Node(walkable, i, j))
        matrix.append(row)
    return matrix


def revert_nodes(nodes):
    new_nodes = []
    for node in nodes:
        new_nodes.append((node.x, node.y))
    return new_nodes


def get_neighbors(matrix, node):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        x, y = node.x + dx, node.y + dy
        if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]) and matrix[x][y].walkable:
            neighbors.append(matrix[x][y])
    return neighbors


def construct_path(end_node):
    path = []
    current = end_node
    while current is not None:
        path.append((current.x, current.y))
        current = current.parent
    path.reverse()
    return path


def dijkstra(array, start_cord, end_cord):
    nodes = create_node_matrix(array)
    start = nodes[start_cord[1]][start_cord[0]]
    end = nodes[end_cord[1]][end_cord[0]]

    start.costs = 0
    queue = [start]
    finished = []

    while queue:
        current = min(queue, key=lambda o: o.costs)
        queue.remove(current)
        finished.append(current)

        if current == end:
            break

        for neighbor in get_neighbors(nodes, current):
            if neighbor in finished:
                continue

            new_cost = current.costs + current.edge(neighbor)
            if new_cost < neighbor.costs:
                neighbor.costs = new_cost
                neighbor.parent = current
                if neighbor not in queue:
                    queue.append(neighbor)

    return construct_path(end), revert_nodes(finished)


def dijkstra_generator(field, start_cord, end_cord):
    path, search = dijkstra(field, start_cord, end_cord)

    def path_generator():
        for step in path:
            yield step

    def search_generator():
        for step in search:
            yield step

    return path_generator(), search_generator()


if __name__ == '__main__':
    matrix_map = [
        [0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 1, 1, 0, 0],
    ]
    path, search = dijkstra(matrix_map, (0, 0), (4, 4))
    print("Der kürzeste Pfad ist:", path)
    print("Die besuchten Knoten sind:", list(search))
