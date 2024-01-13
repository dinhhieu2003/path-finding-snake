import copy
import queue

import utils
from Square import Square
import pygame

from state import *

def bfs(start, target, curr_direction, body, dangers_set):
    bfs_queue = queue.Queue()
    visited = set()
    parent = {}
    found = False
    start_state = (start, curr_direction, body)
    bfs_queue.put(start_state)
    visited.add(start)
    while bfs_queue.qsize() != 0:
        current = bfs_queue.get()
        if current[0] == target:
            found = True
            break
        for neighbor in get_neighbors(current):
            if is_valid_position(neighbor[0][0], neighbor[0][1], dangers_set) and neighbor[0] not in visited:
                bfs_queue.put(neighbor)
                visited.add(neighbor[0])
                parent[neighbor[0]] = current
    path = []
    while current[0] != start:
        path.append(current[0])
        current = parent[current[0]]
    path.reverse()
    prev = start
    way = find_path(path, prev, curr_direction)
    while bfs_queue.qsize() != 0:
        remain = bfs_queue.get()
        visited.add(remain[0])
    return way, visited

def ucs(start, target, curr_direction, body, dangers_set):
    pq = queue.PriorityQueue()
    visited = set()
    parent = {}
    pq.put((0, (start, curr_direction, body)))
    visited.add(start)
    found = False
    while not pq.empty():
        current = pq.get()
        if current[1][0] == target:
            found = True
            break
        for neighbor in get_neighbors(current[1]):
            if is_valid_position(neighbor[0][0], neighbor[0][1], dangers_set) and neighbor[0] not in visited:
                pq.put((current[0] + 1 ,neighbor))
                visited.add(neighbor[0])
                parent[neighbor[0]] = current
    path = []
    while current[1][0] != start:
        path.append(current[1][0])
        current = parent[current[1][0]]
    path.reverse()
    prev = start
    way = find_path(path, prev, curr_direction)
    while pq.qsize() != 0:
        remain = pq.get()
        visited.add(remain[1][0])
    return way, visited

def search_cost(start, target, curr_direction, body, fn, dangers_set):
    pq = queue.PriorityQueue()
    visited = set()
    parent = {}
    pq.put((0, (start, curr_direction, body), 0))
    visited.add(start)
    found = False
    while not pq.empty():
        current = pq.get()
        if current[1][0] == target:
            found = True
            break
        for neighbor in get_neighbors_cost(current, fn):
            if is_valid_position(neighbor[1][0][0], neighbor[1][0][1], dangers_set) and neighbor[1][0] not in visited:
                pq.put(neighbor)
                visited.add(neighbor[1][0])
                parent[neighbor[1][0]] = current
    path = []
    while current[1][0] != start:
        path.append(current[1][0])
        current = parent[current[1][0]]
    path.reverse()
    prev = start
    way = find_path(path, prev, curr_direction)
    while pq.qsize() != 0:
        remain = pq.get()
        visited.add(remain[1][0])
    return way, visited

def dfs(start, target, curr_direction, body, dangers_set):
    stack = []
    visited = set()
    parent = {}
    stack.append((start, curr_direction, body, 0))
    visited.add(start)
    found = False
    while len(stack) != 0:
        current = stack.pop()
        if current[0] == target:
            found = True
            break
        for neighbor in get_neighbors(current):
            if is_valid_position(neighbor[0][0], neighbor[0][1], dangers_set) and neighbor[0] not in visited:
                stack.append((neighbor[0], neighbor[1], neighbor[2], current[3] + 1))
                visited.add(neighbor[0])
                parent[neighbor[0]] = current
    path = []
    while current[0] != start:
        path.append(current[0])
        current = parent[current[0]]
    path.reverse()
    prev = start
    way = find_path(path, prev, curr_direction)
    while len(stack) != 0:
        remain = stack.pop()
        visited.add(remain[0])
    return found, way, visited

def ids(start, target, curr_direction, body, dangers_set):
    qu = queue.Queue()
    visited = set()
    parent = {}
    qu.put((start, curr_direction, body, 0))
    visited.add(start)
    found = False
    while qu.qsize() != 0:
        if found:
            break
        current_start = qu.get()
        max_depth = current_start[3] + 10
        stack = []
        stack.append(current_start)
        while len(stack) != 0:
            current = stack.pop()
            if current[3] >= max_depth:
                continue
            if current[0] == target:
                found = True
                break
            for neighbor in get_neighbors(current):
                if is_valid_position(neighbor[0][0], neighbor[0][1], dangers_set) and neighbor[0] not in visited:
                    stack.append((neighbor[0], neighbor[1], neighbor[2], current[3] + 1))
                    visited.add(neighbor[0])
                    parent[neighbor[0]] = current
                    if current[3] + 1:
                        qu.put((neighbor[0], neighbor[1], neighbor[2], current[3] + 1))
    path = []
    while current[0] != start:
        path.append(current[0])
        current = parent[current[0]]
    path.reverse()
    prev = start
    way = find_path(path, prev, curr_direction)
    return way, visited

def AStar(start, target, curr_direction, body, dangers_set):
    def fn(curr_state, g):
        head_x = curr_state[1][0][0]
        head_y = curr_state[1][0][1]
        food_x = target[0]
        food_y = target[1]
        return g + heu(head_x, head_y, food_x, food_y)
    return search_cost(start, target, curr_direction, body, fn, dangers_set)

def Greedy(start, target, curr_direction, body, dangers_set):
    def fn(curr_state, g):
        head_x = curr_state[1][0][0]
        head_y = curr_state[1][0][1]
        food_x = target[0]
        food_y = target[1]
        return heu(head_x, head_y, food_x, food_y)
    return search_cost(start, target, curr_direction, body, fn, dangers_set)

def Hill_Climbing(start, target, curr_direction, body, danger_set):
    def fn(curr_state):
        head_x = curr_state[0][0]
        head_y = curr_state[0][1]
        food_x = target[0]
        food_y = target[1]
        return heu(head_x, head_y, food_x, food_y)
    pq = queue.PriorityQueue()
    pq_tmp = queue.PriorityQueue()
    visited = set()
    cannot_choose = set()
    parent = {}
    state = (start, curr_direction, body)
    start_state = (fn(state), state)
    pq.put(start_state)
    visited.add(start)
    while pq.qsize() != 0:
        current = pq.get()
        pq.queue.clear()
        if current[1][0] == target:
            break
        for neighbor in get_neighbors(current[1]):
            if is_valid_position(neighbor[0][0], neighbor[0][1], danger_set) and neighbor[0] not in visited:
                if fn(neighbor) <= current[0]:
                    pq.put((fn(neighbor), neighbor))
                    visited.add(neighbor[0])
                    parent[neighbor[0]] = current
                else:
                    cannot_choose.add(neighbor[0])
                #     pq_tmp.put((fn(neighbor), neighbor))
        # if pq.qsize() == 0:
        #     if pq_tmp.qsize() != 0:
        #         tmp = pq_tmp.get()
        #         pq.put(tmp)
        #         visited.add(tmp[1][0])
        #         parent[tmp[1][0]] = current
        # pq_tmp.queue.clear()
    path = []
    while current[1][0] != start:
        path.append(current[1][0])
        current = parent[current[1][0]]
    path.reverse()
    prev = start
    way = find_path(path, prev, curr_direction)
    return way, visited, cannot_choose