class Node:
    def __init__(self, walkable, x, y):
        self.g_cost = float('inf')
        self.h_cost = 0
        self.f_cost = float('inf')
        self.walkable = walkable
        self.x = x
        self.y = y
        self.parent = None

    def update_costs(self, g_cost, h_cost):
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = self.g_cost + self.h_cost


def get_distance(node_a, node_b):
    return abs(node_a.x - node_b.x) + abs(node_a.y - node_b.y)
    # return math.sqrt((node_a.x - node_b.x) ** 2 + (node_a.y - node_b.y) ** 2)


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


def revert_nodes(nodes):
    new_nodes = []
    for node in nodes:
        new_nodes.append((node.x, node.y))
    return new_nodes


def create_node_matrix(field):
    matrix = []
    for i in range(len(field)):
        row = []
        for j in range(len(field[i])):
            walkable = True
            if field[i][j] == 1:
                walkable = False
            row.append(Node(walkable, i, j))
        matrix.append(row)
    return matrix


def astar(field, start_cord, end_cord):
    # change field to a* Node matrix
    matrix = create_node_matrix(field)
    start = matrix[start_cord[1]][start_cord[0]]
    end = matrix[end_cord[1]][end_cord[0]]

    # start algorythm
    open_set = [start]
    closed_set = []

    start.update_costs(0, get_distance(start, end))

    while open_set:
        current = min(open_set, key=lambda o: o.f_cost)
        if current == end:
            return construct_path(current), revert_nodes(closed_set)

        open_set.remove(current)
        closed_set.append(current)

        for neighbor in get_neighbors(matrix, current):
            if neighbor not in closed_set and neighbor.walkable:
                tentative_g_cost = current.g_cost + get_distance(current, neighbor)

                if tentative_g_cost < neighbor.g_cost:
                    neighbor.parent = current
                    neighbor.update_costs(tentative_g_cost, get_distance(neighbor, end))

                    if neighbor not in open_set:
                        open_set.append(neighbor)

    return [], revert_nodes(closed_set)


def astar_generator(field, start_cord, end_cord):
    path, search = astar(field, start_cord, end_cord)

    def path_generator():
        for step in path:
            yield step

    def search_generator():
        for step in search:
            yield step

    return path_generator(), search_generator()
