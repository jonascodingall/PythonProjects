from collections import deque

class Node:
    def __init__(self, walkable, x, y):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.parent = None

def get_neighbors(matrix, node):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        x, y = node.x + dx, node.y + dy
        if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]) and matrix[x][y].walkable:
            neighbors.append(matrix[x][y])
    return neighbors

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
            walkable = field[i][j] != 1
            row.append(Node(walkable, i, j))
        matrix.append(row)
    return matrix

def construct_path(end_node):
    path = []
    current = end_node
    while current is not None:
        path.append((current.x, current.y))
        current = current.parent
    path.reverse()
    return path

def bfs(array, start_cord, end_cord):
    nodes = create_node_matrix(array)
    start = nodes[start_cord[1]][start_cord[0]]
    end = nodes[end_cord[1]][end_cord[0]]

    queue = deque([start])
    searched = []
    visited = set([start])

    while queue:
        current = queue.popleft()
        searched.append(current)

        if current is end:
            return construct_path(current), revert_nodes(searched)

        for neighbor in get_neighbors(nodes, current):
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = current
                queue.append(neighbor)

    return [], revert_nodes(searched)

def bfs_generator(field, start_cord, end_cord):
    path, search = bfs(field, start_cord, end_cord)

    def path_generator():
        for step in path:
            yield step

    def search_generator():
        for step in search:
            yield step

    return path_generator(), search_generator()
