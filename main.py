# This is a sample Python script.
import math

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import test
import random
import copy
import pygame
import sys
from pygame.color import THECOLORS

class Node:
    def __init__(self, adjacent_nodes, value, move, player_name, current_game):
        self.value = value
        self.adjacent_nodes = list(adjacent_nodes)
        self.move = move
        self.player_name = player_name
        self.current_game = current_game

class Algorithm:
    def __init__(self, game, mode):
        self.game = game
        self.mode = mode
        self.decision_tree = Node(list(), None, None, 'MAX', copy.deepcopy(game))
        self.build_decision_tree()

    # Function for making decision
    def make_decision(self):
        # For 'easy' mode computer makes fully random decisions
        if self.mode == 'easy':
            return self.random_decision()

        # For 'medium' mode computer makes either random or alpha beta pruning decision with equal chances
        elif self.mode == 'medium':
            random_choice = random.randint(0, 1)
            if random_choice:
                return self.alpha_beta_pruning_decision()
            else:
                return self.random_decision()

        # For 'difficult' mode computer makes fully alpha beta pruning decisions
        else:
            return self.alpha_beta_pruning_decision()

    # Function for taking random decision
    def random_decision(self):
        random_index = random.randint(0, len(self.game.available_computer_connections)-1)
        return self.game.available_computer_connections[random_index]

    # Function for alpha beta pruning
    def alpha_beta_pruning_decision(self):
        for node in self.decision_tree.adjacent_nodes:
            if node.value == self.decision_tree.value:
                return node.move

    def build_decision_tree(self):
        decision_tree_queue = list()
        decision_tree_queue.append(self.decision_tree)
        while decision_tree_queue:
            current_node = decision_tree_queue.pop(0)
            if current_node.player_name == 'MAX':
                for move in current_node.current_game.available_computer_connections:
                    possible_game = copy.deepcopy(current_node.current_game)
                    possible_game.move_order.append(move)
                    possible_game.delete_connection(move)
                    if move in possible_game.available_computer_connections:
                        possible_game.available_computer_connections.remove(move)
                    possible_game.refresh_connections()
                    possible_game.is_Players_turn = True
                    node = Node(list(), None, move, 'MIN', possible_game)
                    decision_tree_queue.append(node)
                    current_node.adjacent_nodes.append(node)
            else:
                for move in current_node.current_game.available_player_connections:
                    possible_game = copy.deepcopy(current_node.current_game)
                    possible_game.move_order.append(move)
                    possible_game.delete_connection(move)
                    if move in possible_game.available_player_connections:
                        possible_game.available_player_connections.remove(move)
                    possible_game.refresh_connections()
                    possible_game.is_Players_turn = False
                    node = Node(list(), None, move, 'MAX', possible_game)
                    decision_tree_queue.append(node)
                    current_node.adjacent_nodes.append(node)
            if current_node.current_game.is_game_ended():
                if current_node.current_game.is_Players_turn:
                    current_node.value = 1
                else:
                    current_node.value = -1
        self.refresh_values()

    def refresh_values(self):
        decision_tree_queue = list()
        decision_tree_queue.append(self.decision_tree)
        visited_nodes = []
        while decision_tree_queue:
            current_node = decision_tree_queue.pop(0)
            visited_nodes.append(current_node)
            for node in current_node.adjacent_nodes:
                decision_tree_queue.append(node)
        while visited_nodes:
            current_node = visited_nodes.pop(len(visited_nodes)-1)
            if not current_node.value:
                if current_node.player_name == 'MAX':
                    current_min_node_value = -2
                    for node in current_node.adjacent_nodes:
                        if node.value == 1:
                            current_min_node_value = 1
                            break
                        elif node.value is None:
                            current_min_node_value = None
                            break
                        elif node.value > current_min_node_value:
                            current_min_node_value = node.value
                    current_node.value = current_min_node_value
                else:
                    current_min_node_value = 2
                    for node in current_node.adjacent_nodes:
                        if node.value == -1:
                            current_min_node_value = -1
                            break
                        elif node.value is None:
                            current_min_node_value = None
                            break
                        elif node.value < current_min_node_value:
                            current_min_node_value = node.value
                    current_node.value = current_min_node_value


class Game:
    def __init__(self):
        self.connections_matrix = Game.generate_game_matrix()
        self.current_matrix = list(self.connections_matrix)
        self.move_order = []
        self.is_Players_turn = True
        self.is_Game_ended = False
        self.victory = None
        self.available_player_connections = ['0-2', '2-4', '3-5', '5-7', '3-6']
        self.available_computer_connections = ['1-2', '2-5', '2-3', '4-5', '5-8']
        self.cleared_nodes = [0, 1]
        self.current_lowest_node = -1

    # Function to generate game matrix
    @staticmethod
    def generate_game_matrix():
        # Default starting combination
        return [
            ['x',0,1,0,0,0,0,0,0],
            [0,'x',2,0,0,0,0,0,0],
            [1,2,'x',2,1,2,0,0,0],
            [0,0,2,'x',0,1,1,0,0],
            [0,0,1,0,'x',2,0,0,0],
            [0,0,2,1,2,'x',0,1,2],
            [0,0,0,1,0,0,'x',0,0],
            [0,0,0,0,0,1,0,'x',0],
            [0,0,0,0,0,2,0,0,'x']
        ]

    # Function to determine whether game ended
    def is_game_ended(self):
        # Check whether there are any connection for one of the players
        for i in range(0, len(self.current_matrix[0])):
            for j in range(0, len(self.current_matrix[0])):
                if self.is_Players_turn:
                    if self.current_matrix[i][j] == 1:
                        self.is_Game_ended = False
                        return False
                else:
                    if self.current_matrix[i][j] == 2:
                        self.is_Game_ended = False
                        return False

        # Check if bottom nodes are connected
        for i in range(0, len(self.current_matrix)):
            if(self.current_matrix[0][i] == 1
                or self.current_matrix[0][i] == 2
                or self.current_matrix[1][i] == 1
                    or self.current_matrix[1][i] == 2):
                self.is_Game_ended = False
                return False
        # Check if any available moves are
        if len(self.available_player_connections) and len(self.available_computer_connections):
            return False
        return True

    # Function to delete connection
    def delete_connection(self, connection: str):
        x, y = [int(value) for value in connection.split('-')]
        self.current_matrix[x][y] = 0
        self.current_matrix[y][x] = 0
        self.refresh_connections()

    # Function to refresh the list of cleared nodes
    def refresh_cleared_nodes(self):
        for i in range(2, len(self.current_matrix[0])):
            found = False
            for j in range(0, len(self.current_matrix[0])):
                if self.current_matrix[i][j] == 1 or self.current_matrix[i][j] == 2:
                    found = True
                    break
            if not found and i not in self.cleared_nodes:
                self.cleared_nodes.append(i)
                for connection in list(self.available_player_connections):
                    x, y = [int(value) for value in connection.split('-')]
                    if x in self.cleared_nodes and y in self.cleared_nodes:
                        self.available_player_connections.remove(connection)
                for connection in list(self.available_computer_connections):
                    x, y = [int(value) for value in connection.split('-')]
                    if x in self.cleared_nodes and y in self.cleared_nodes:
                        self.available_computer_connections.remove(connection)
                self.refresh_cleared_nodes()

    # Function to clear node
    def clear_node(self, node):
        for i in range(0, len(self.current_matrix[0])):
            if node == i:
                self.current_matrix[node][i] = 'x'
            else:
                self.current_matrix[node][i] = 0
                self.current_matrix[i][node] = 0
        self.cleared_nodes.append(node)

    # Function to refresh connections
    def refresh_connections(self):
        self.refresh_cleared_nodes()
        for i in range(2, len(self.current_matrix[0])):
            if i not in self.cleared_nodes:
                self.current_lowest_node = i
                self.update_lowest_connected_node(i, i, [])
                lowest_node = self.current_lowest_node
                # print("Lowest node for " + str(i) + " is " + str(lowest_node))
                if lowest_node == i:
                    self.clear_node(i)
                    self.refresh_connections()
                    break

    # Function to find the lowest connected node to the given node
    def update_lowest_connected_node(self, node, initial_node, checked_nodes: list):
        if node not in checked_nodes:
            checked_nodes.append(node)
            if self.current_lowest_node < initial_node:
                return
            node_connections = [i for i in range(0, len(self.current_matrix[0])) if (self.current_matrix[node][i] != 0 and self.current_matrix[node][i] != 'x')]
            if not len(node_connections) or node == 0 or node == 1:
                if node < self.current_lowest_node:
                    self.current_lowest_node = node
                return
            for adjacent_node in node_connections:
                self.update_lowest_connected_node(adjacent_node, initial_node, checked_nodes)
        else:
            return

    # Function to launch the game
    def launch_game(self):
        while not self.is_game_ended():
            move = None
            if self.is_Players_turn:
                print("Player's move: ")
                print(self.available_player_connections)
                while move not in self.available_player_connections:
                    move = input()
                self.move_order.append(move)
                self.delete_connection(move)
                if move in self.available_player_connections:
                    self.available_player_connections.remove(move)
                self.refresh_connections()
                print("Move is successful!")
                print(self.cleared_nodes)
                self.is_Players_turn = False
            else:
                print("Computer's move: ")
                print(self.available_computer_connections)
                computer = Algorithm(self, 'difficult')
                move = computer.make_decision()
                self.move_order.append(move)
                self.delete_connection(move)
                if move in self.available_computer_connections:
                    self.available_computer_connections.remove(move)
                self.refresh_connections()
                print("Move is successful!")
                print(move)
                print(self.cleared_nodes)
                self.is_Players_turn = True
        if self.is_Players_turn:
            print("Computer won!")
        else:
            print("Player won!")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Hackenbush', True, THECOLORS['black'])
    textRect = text.get_rect()
    textRect.center = (600, 25)
    print('Enter computer difficulty mode(easy, medium, difficult): ')
    computer_difficulty_mode = input()
    screen = pygame.display.set_mode((1200, 800))
    screen.fill(THECOLORS['white'])
    pygame.display.set_caption('Hackenbush')
    game = Game()
    bottom_line = pygame.draw.line(screen, THECOLORS['black'], [50, 750], [600, 750], 4)
    all_connections = [['5-7', [175, 100], [275, 250], pygame.draw.line(screen, THECOLORS['blue'], [175, 100], [275, 250], 4)],
                       ['5-8', [375, 100], [275, 250], pygame.draw.line(screen, THECOLORS['red'], [375, 100], [275, 250], 4)],
                       ['4-5', [275, 250], [175, 400], pygame.draw.line(screen, THECOLORS['red'], [275, 250], [175, 400], 4)],
                       ['3-5', [275, 250], [375, 400], pygame.draw.line(screen, THECOLORS['blue'], [275, 250], [375, 400], 4)],
                       ['2-4', [175, 400], [275, 600], pygame.draw.line(screen, THECOLORS['blue'], [175, 400], [275, 600], 4)],
                       ['2-5', [275, 600], [275, 250], pygame.draw.line(screen, THECOLORS['red'], [275, 600], [275, 250], 4)],
                       ['2-3', [275, 600], [375, 400], pygame.draw.line(screen, THECOLORS['red'], [275, 600], [375, 400], 4)],
                       ['3-6', [375, 400], [500, 250], pygame.draw.line(screen, THECOLORS['blue'], [375, 400], [500, 250], 4)],
                       ['0-2', [175, 750], [275, 600], pygame.draw.line(screen, THECOLORS['blue'], [175, 750], [275, 600], 4)],
                       ['1-2', [375, 750], [275, 600], pygame.draw.line(screen, THECOLORS['red'], [375, 750], [275, 600], 4)]]
    all_nodes = [[[175, 750], pygame.draw.circle(screen, THECOLORS['black'], [175, 750], radius=6, width=0)],
                 [[375, 750], pygame.draw.circle(screen, THECOLORS['black'], [375, 750], radius=6, width=0)],
                 [[275, 600], pygame.draw.circle(screen, THECOLORS['black'], [275, 600], radius=6, width=0)],
                 [[375, 400], pygame.draw.circle(screen, THECOLORS['black'], [375, 400], radius=6, width=0)],
                 [[175, 400], pygame.draw.circle(screen, THECOLORS['black'], [175, 400], radius=6, width=0)],
                 [[275, 250], pygame.draw.circle(screen, THECOLORS['black'], [275, 250], radius=6, width=0)],
                 [[500, 250], pygame.draw.circle(screen, THECOLORS['black'], [500, 250], radius=6, width=0)],
                 [[175, 100], pygame.draw.circle(screen, THECOLORS['black'], [175, 100], radius=6, width=0)],
                 [[375, 100], pygame.draw.circle(screen, THECOLORS['black'], [375, 100], radius=6, width=0)]]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            screen.blit(text, textRect)
            if pygame.mouse.get_pressed()[0] and game.is_Players_turn and not game.is_game_ended():
                position = pygame.mouse.get_pos()
                for connection in list(all_connections):
                    if connection[3].collidepoint(position) and connection[0] in game.available_player_connections:
                        game.move_order.append(connection[0])
                        game.delete_connection(connection[0])
                        game.refresh_connections()
                        game.is_Players_turn = False
                        print("Player's move: " + connection[0])
                        if connection[0] in game.available_player_connections:
                            game.available_player_connections.remove(connection[0])
                        for move in list(all_connections):
                            if move[0] not in game.available_player_connections and move[0] not in game.available_computer_connections:
                                pygame.draw.line(screen, THECOLORS['white'], move[1], move[2], 4)
                                all_connections.remove(move)
                if not game.is_Players_turn and len(game.available_computer_connections) > 0:
                    pygame.time.wait(500)
                    computer = Algorithm(game, computer_difficulty_mode)
                    move = computer.make_decision()
                    game.move_order.append(move)
                    game.delete_connection(move)
                    game.refresh_connections()
                    game.is_Players_turn = True
                    print("Computer's move: " + move)
                    if move in game.available_computer_connections:
                        game.available_computer_connections.remove(move)
                    for move in list(all_connections):
                        if move[0] not in game.available_player_connections and move[0] not in game.available_computer_connections:
                            pygame.draw.line(screen, THECOLORS['white'], move[1], move[2], 4)
                            all_connections.remove(move)
                    for node in list(all_nodes):
                        if all_nodes.index(node) in game.cleared_nodes and all_nodes.index(node) > 1:
                            pygame.draw.circle(screen, THECOLORS['white'], node[0], radius=6, width=0)
                        else:
                            pygame.draw.circle(screen, THECOLORS['black'], node[0], radius=6, width=0)
                if game.is_game_ended():
                    for node in list(all_nodes):
                        if all_nodes.index(node) in game.cleared_nodes:
                            pygame.draw.circle(screen, THECOLORS['white'], node[0], radius=6, width=0)
                        else:
                            pygame.draw.circle(screen, THECOLORS['black'], node[0], radius=6, width=0)
                    bottom_line = pygame.draw.line(screen, THECOLORS['black'], [50, 750], [600, 750], 4)
                    if game.is_Players_turn:
                        text_2 = font.render('Computer won!', True, THECOLORS['black'])
                        textRect_2 = text_2.get_rect()
                        textRect_2.center = (1000, 25)
                        print("Computer won!")
                    else:
                        text_2 = font.render('Player won!', True, THECOLORS['black'])
                        textRect_2 = text_2.get_rect()
                        textRect_2.center = (1000, 25)
                        print("Player won!")
                    screen.blit(text_2, textRect_2)
            elif game.is_game_ended():
                pygame.display.flip()
                pygame.display.update()
            pygame.display.flip()
            pygame.display.update()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
