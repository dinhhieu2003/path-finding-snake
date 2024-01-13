import utils
from Square import Square
from Point import Point

def is_valid_position(x, y, dangers_set):
    if x <= 0 or y <= 0 or x >= utils.WIDTH or y >= utils.HEIGHT or (x,y) in dangers_set:
        return False
    return True

def get_neighbors(curr_state):
    x, y = curr_state[0]
    neighbors = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    body_set_position = {(square.position.x, square.position.y) for square in curr_state[2]}
    for dx, dy in directions:
        head = (x + dx, y + dy)
        body = list(curr_state[2])
        if can_move(curr_state[1], dx, dy):
            curr_dir = ""
            if dx == 1:
                curr_dir = "right"
            if dx == -1:
                curr_dir = "left"
            if dy == 1:
                curr_dir = "down"
            if dy == -1:
                curr_dir = "up"
            head_position = Point(head[0], head[1])
            if (head[0], head[1]) not in body_set_position:
                body.append(Square('#000000', head_position))
                neighbors.append((head, curr_dir, tuple(body)))
    return neighbors

def get_neighbors_cost(curr_state,fn):
    x, y = curr_state[1][0]
    neighbors = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    body_set_position = {(square.position.x, square.position.y) for square in curr_state[1][2]}
    for dx, dy in directions:
        head = (x + dx, y + dy)
        if can_move(curr_state[1][1], dx, dy):
            body = list(curr_state[1][2])
            curr_dir = ""
            if dx == 1:
                curr_dir = "right"
            if dx == -1:
                curr_dir = "left"
            if dy == 1:
                curr_dir = "down"
            if dy == -1:
                curr_dir = "up"
            if (head[0], head[1]) not in body_set_position:
                g = curr_state[2] + 1
                cost = fn(curr_state, g)
                body.append(Square('#000000',Point(head[0], head[1])))
                snake = (head, curr_dir, tuple(body))
                neighbors.append((cost, snake, g))
    return neighbors

def can_move(curr_dir, dx, dy):
    if (curr_dir == "right" and dx != -1) or \
            (curr_dir == "left" and dx != 1) or \
            (curr_dir == "down" and dy != -1) or \
            (curr_dir == "up" and dy != 1):
        return True
    return False

def find_path(path, prev, curr_direction):
    way = ""
    if len(path) == 0:
        print("len path = 0")
        return curr_direction[0]
    for p in path:
        if p[1] == prev[1] - 1:
            way += "u"
        if p[0] == prev[0] + 1:
            way += "r"
        if p[1] == prev[1] + 1:
            way += "d"
        if p[0] == prev[0] - 1:
            way += "l"
        prev = p
    return way

def heu(head_x, head_y, food_x, food_y):
    return abs(head_x - food_x) + abs(head_y - food_y)