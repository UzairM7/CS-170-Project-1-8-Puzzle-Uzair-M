import queue
import copy

easy = [[1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]]

medium = [[1, 0, 2],
          [4, 5, 3],
          [7, 8, 6]]

hard = [[1, 6, 7],
        [5, 0, 3],
        [4, 8, 2]]

eight_goal_state = [[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 0]]

def main():
    puzzle_mode = input("Welcome to an 8-Puzzle Solver. Type '1' to use a default puzzle, or '2' to create your own." + '\n')
    if puzzle_mode == "1":
        select_and_init_algorithm(init_default_puzzle_mode())
    
    elif puzzle_mode == "2":
        print("Enter your puzzle, using a zero to represent the blank. " +
              "Please only enter valid 8-puzzles. Enter the puzzle demiliting " +
              "the numbers with a space. RET only when finished." + '\n')
        puzzle_row_one = input("Enter the first row: ")
        puzzle_row_two = input("Enter the second row: ")
        puzzle_row_three = input("Enter the third row: ")

        for i in range(0, 3):
            puzzle_row_one[i] = int(puzzle_row_one[i])
            puzzle_row_two[i] = int(puzzle_row_two[i])
            puzzle_row_three[i] = int(puzzle_row_three[i])

        user_puzzle = [puzzle_row_one, puzzle_row_two, puzzle_row_three]
        select_and_init_algorithm(user_puzzle)

    return

def init_default_puzzle_mode():
    selected_difficulty = input("You wish to use a default puzzle. Please enter a desired difficulty on a scale from 0 to 2." + '\n')
    if selected_difficulty == "0":
        print("Difficulty of 'Easy' selected.")
        return easy
    
    if selected_difficulty == "1":
        print("Difficulty of 'Medium' selected.")
        return medium

    if selected_difficulty == "2":
        print("Difficulty of 'Hard' selected.")
        return hard

def print_puzzle(puzzle):
    for i in range(0, 3):
        print(puzzle[i])
    print('\n')

def select_and_init_algorithm(puzzle):
    
    algorithm = input("Select algorithm. (1) for Uniform Cost Search, (2) for the Misplaced Tile Heuristic, or (3) the Manhattan Distance Heuristic." + '\n')
    
    if algorithm == "1":
        uniform_cost_search(puzzle, 0)
    
    if algorithm == "2":
        misplaced_tile_heuristic(puzzle, 1)

    if algorithm == "3":
        manhattan_distance_heuristic(puzzle, 2)



class Node:
    
    def __lt__(self, compare): return self.fn + self.gn < compare.get_fn() + compare.get_gn()

    def __init__(self, puzzle):
        self.puzzle = puzzle

    def set_fn(self, sfn):
        self.fn = sfn
    
    def set_gn(self, sgn):
        self.gn = sgn

    def set_hn(self, shn):
        self.hn = shn

    def get_fn(self):
        return self.fn

    def get_gn(self):
        return self.gn

    def get_hn(self):
        return self.hn

    def board_to_tuple(self):
        tuples = tuple(tuple(x) for x in self.puzzle)
        return tuples

    def solved(self):
        return self.puzzle == eight_goal_state

    def board(self):
        return self.puzzle
    
    def findzero(self):
        for i in range (3):
            for k in range(3):
                if self.puzzle [i][k] == 0:
                    self.zerox = k
                    self.zeroy = i
                    return [i,k]


    def expand(self, repeat_set):
        m = list()

        self.findzero()

        if self.zerox > 0:
            left_shift = copy.deepcopy(self.puzzle)
            left_shift[self.zeroy][self.zerox] = left_shift[self.zeroy][self.zerox - 1]
            left_shift[self.zeroy][self.zerox - 1] = 0
            
            N = Node(left_shift)
            N.set_gn(self.gn + 1)
            N.set_hn(0)
            N.set_fn(self.gn + 1)

            if N.board_to_tuple() not in repeat_set:
                m.append(N)

        if self.zerox < 2:
    
            right_shift = copy.deepcopy(self.puzzle)
            right_shift[self.zeroy][self.zerox] = right_shift[self.zeroy][self.zerox+1]
            right_shift[self.zeroy][self.zerox+1] = 0

            N = Node(right_shift)
            N.set_gn(self.gn + 1)
            N.set_hn(0)
            N.set_fn(self.gn + 1)
        
            if N.board_to_tuple() not in repeat_set:
                m.append(N)

    
        if self.zeroy > 0:
            
            up_shift = copy.deepcopy(self.puzzle)
            up_shift[self.zeroy][self.zerox] = up_shift[self.zeroy - 1][self.zerox]
            up_shift[self.zeroy - 1][self.zerox] = 0
            
            N = Node(up_shift)
            N.set_gn(self.gn + 1)
            N.set_hn(0)
            N.set_fn(self.gn + 1)
        
            if N.board_to_tuple() not in repeat_set:
                m.append(N)

        
        if self.zeroy < 2:
        
            down_shift = copy.deepcopy(self.puzzle)
            down_shift[self.zeroy][self.zerox] = down_shift[self.zeroy+1][self.zerox]
            down_shift[self.zeroy + 1][self.zerox] = 0
            N = Node(down_shift)
            N.set_gn(self.gn + 1)
            N.set_hn(0)
            N.set_fn(self.gn + 1)
            
            if N.board_to_tuple() not in repeat_set:
                m.append(N)

        return m

        
    

def uniform_cost_search(puzzle, heuristic):
    starting_node = Node(puzzle)
    starting_node.set_fn(0)
    starting_node.set_gn(0)
    starting_node.set_hn(0)
    pq = queue.PriorityQueue()
    pq.put(starting_node)
    num_nodes_expanded = 0
    max_queue_size = 0
    
    repeat_set = set()
    repeat_set.add(starting_node.board_to_tuple())

    stack_to_print = []

    i = 0

    while 1:
        max_queue_size = max(pq.qsize(), max_queue_size)
        if (pq.empty()): return 'failed'
        node_from_queue = pq.get()
        if node_from_queue.solved(): 
            while len(stack_to_print) > 0:
                print_puzzle(stack_to_print.pop())
            print("Number of nodes expanded:", num_nodes_expanded)
            print("Max queue size:", max_queue_size)
            print("Depth: " + str(node_from_queue.get_gn()))
            return node_from_queue
        print_puzzle(node_from_queue.board())
        stack_to_print.append(node_from_queue.board())
        expandedNodes = node_from_queue.expand(repeat_set)
        num_nodes_expanded+=1

        for node in expandedNodes:
            repeat_set.add(node.board_to_tuple())
            pq.put(node)

def misplaced_tile_heuristic(puzzle, heuristic):
    starting_node = Node(puzzle)
    starting_node.set_fn(0)
    starting_node.set_gn(0)
    starting_node.set_hn(0)
    pq = queue.PriorityQueue()
    pq.put(starting_node)
    num_nodes_expanded = 0
    max_queue_size = 0
    
    repeat_set = set()
    repeat_set.add(starting_node.board_to_tuple())

    stack_to_print = [] 

    i = 0

    while 1:
        max_queue_size = max(pq.qsize(), max_queue_size)
        if (pq.empty()): return 'failed'
        node_from_queue = pq.get()
        if node_from_queue.solved(): 
            while len(stack_to_print) > 0: 
                print_puzzle(stack_to_print.pop())
            print("Number of nodes expanded:", num_nodes_expanded)
            print("Max queue size:", max_queue_size)
            print("Depth: " + str(node_from_queue.get_gn()))
            return node_from_queue
        print_puzzle(node_from_queue.board())
        stack_to_print.append(node_from_queue.board())
        expandedNodes = node_from_queue.expand(repeat_set)
        num_nodes_expanded+=1

        for node in expandedNodes:
            repeat_set.add(node.board_to_tuple())
            cost = 0
            for i in range(3):
                for j in range(3):
                    if node.board()[i][j] != eight_goal_state[i][j]: 
                        cost += 1
            node.set_hn(cost)
            node.set_fn(node.get_gn() + cost)
            pq.put(node)

def manhattan_distance_heuristic(puzzle, heuristic):
    starting_node = Node(puzzle)
    starting_node.set_fn(0)
    starting_node.set_gn(0)
    starting_node.set_hn(0)
    pq = queue.PriorityQueue()
    pq.put(starting_node)
    num_nodes_expanded = 0
    max_queue_size = 0
    
    repeat_set = set()
    repeat_set.add(starting_node.board_to_tuple())

    stack_to_print = [] 

    i = 0

    while 1:
        max_queue_size = max(pq.qsize(), max_queue_size)
        if (pq.empty()): return 'failed'
        node_from_queue = pq.get()
        if node_from_queue.solved(): 
            while len(stack_to_print) > 0: 
                print_puzzle(stack_to_print.pop())
            print("Number of nodes expanded:", num_nodes_expanded)
            print("Max queue size:", max_queue_size)
            print("Depth: " + str(node_from_queue.get_gn()))
            return node_from_queue
        print_puzzle(node_from_queue.board())
        stack_to_print.append(node_from_queue.board())
        expandedNodes = node_from_queue.expand(repeat_set)
        num_nodes_expanded+=1

        x_coords = [0, 1, 2, 0, 1, 2, 0, 1, 2]

        y_coords = [0, 0, 0, 1, 1, 1, 2, 2, 2]
        for node in expandedNodes:
            repeat_set.add(node.board_to_tuple())
            cost = 0
            for i in range(3):
                for j in range(3):
                    if node.board()[i][j] == 0:
                        continue
                    elif node.board()[i][j] != eight_goal_state[i][j]:
                        cost += abs(i - x_coords[i]) + abs(j + y_coords[j])
                    
            node.set_hn(cost)
            node.set_fn(node.get_gn() + cost)
            pq.put(node)
main()