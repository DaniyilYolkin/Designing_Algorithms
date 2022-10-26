import pygame
import pygame.display
import random
import time
from queue import PriorityQueue

DIMENSION = 8
WIDTH = HEIGHT = 512
MAX_FPS = 120
BOARD_GREY = (122, 131, 148)
BOARD_WHITE = (235, 236, 240)
CELL_SIZE = HEIGHT // DIMENSION
pygame.display.set_caption("8-Queens Problem")
QUEEN_IMAGE = pygame.image.load("Queen3.png")
QUEEN_IMAGE = pygame.transform.scale(QUEEN_IMAGE, (CELL_SIZE, CELL_SIZE))


class QueensProblem:
    def __init__(self):
        self.board = [[0 for _ in range(0, 8)] for _ in range(0, 8)]


def BFS_all_permutations():
    levels = [-1, -1, -1, -1, -1, -1, -1, -1]
    current_i = 0
    list_of_levels = []
    while current_i != 8:
        j = 0
        while j <= 7:
            levels[current_i] = j
            j += 1
            print(levels)
            list_of_levels.append(levels.copy())
        levels[current_i] = 0
        i = current_i - 1
        if current_i == 0:
            current_i += 1
        if i >= 0:
            levels[i] += 1
            while i >= 0 and levels[i] > 7:
                if i == 0:
                    current_i += 1
                levels[i] = 0
                i -= 1
                if i >= 0:
                    levels[i] += 1
    return list_of_levels


def BFS_all_solutions():
    levels = [-1, -1, -1, -1, -1, -1, -1, -1]
    current_i = 0
    list_of_solutions = []
    while current_i != 8:
        j = 0
        while j <= 7:
            levels[current_i] = j
            j += 1
            print(levels)
            if current_i == 7:
                board = [[0 for _ in range(0, 8)] for _ in range(0, 8)]
                for m in range(0, 8):
                    board[m][levels[m]] = 1
                counter = 0
                for m in range(0, 8):
                    if available(board, m, levels[m]):
                        counter += 1
                    else:
                        break
                if counter == 8:
                    print("Solution was found!")
                    list_of_solutions.append(levels.copy())
        levels[current_i] = 0
        i = current_i - 1
        if current_i == 0:
            current_i += 1
        if i >= 0:
            levels[i] += 1
            while i >= 0 and levels[i] > 7:
                if i == 0:
                    current_i += 1
                levels[i] = 0
                i -= 1
                if i >= 0:
                    levels[i] += 1
    return list_of_solutions


def func_2(levels: list[int]):
    length = len(levels)
    board = [[0 for _ in range(0, length)] for _ in range(0, length)]
    for m in range(0, length):
        if levels[m] != -1:
            board[m][levels[m]] = 1
    x = 0
    count = 0
    for level in levels:
        current_x = x
        current_y = level

        starting_x = current_x
        starting_y = current_y

        # Left side
        starting_y -= 1
        while starting_y >= 0:
            if not board[starting_x][starting_y]:
                starting_y -= 1
            else:
                starting_y -= 1
                count += 1
        # Refresh
        starting_y = current_y

        # Right side
        starting_y += 1
        while starting_y < length:
            if not board[starting_x][starting_y]:
                starting_y += 1
            else:
                starting_y += 1
                count += 1

        # Refresh
        starting_y = current_y

        # Upper side
        starting_x += 1
        while starting_x < length:
            if not board[starting_x][starting_y]:
                starting_x += 1
            else:
                starting_x += 1
                count += 1

        # Refresh
        starting_x = current_x

        # Lower side
        starting_x -= 1
        while starting_x >= length:
            if not board[starting_x][starting_y]:
                starting_x -= 1
            else:
                starting_x -= 1
                count += 1

        # Refresh
        starting_x = current_x
        starting_y = current_y

        # Up-Right diagonal
        starting_x -= 1
        starting_y += 1
        while starting_x >= 0 and starting_y < length:
            if not board[starting_x][starting_y]:
                starting_x -= 1
                starting_y += 1
            else:
                starting_x -= 1
                starting_y += 1
                count += 1

        # Refresh
        starting_x = current_x
        starting_y = current_y

        # Up-Left diagonal
        starting_x -= 1
        starting_y -= 1
        while starting_x >= 0 and starting_y >= 0:
            if not board[starting_x][starting_y]:
                starting_x -= 1
                starting_y -= 1
            else:
                starting_x -= 1
                starting_y -= 1
                count += 1

        # Refresh
        starting_x = current_x
        starting_y = current_y

        # Down-Right diagonal
        starting_x += 1
        starting_y += 1
        while starting_x <= length-1 and starting_y <= length-1:
            if not board[starting_x][starting_y]:
                starting_x += 1
                starting_y += 1
            else:
                starting_x += 1
                starting_y += 1
                count += 1

        # Refresh
        starting_x = current_x
        starting_y = current_y

        # Down-Left diagonal
        starting_x += 1
        starting_y -= 1
        while starting_x <= length-1 and starting_y >= 0:
            if not board[starting_x][starting_y]:
                starting_x += 1
                starting_y -= 1
            else:
                starting_x += 1
                starting_y -= 1
                count += 1
        x += 1
    return count



def A_star_solve(initial_level):
    q = PriorityQueue()
    q.put((func_2(initial_level), initial_level))
    solution = []
    while q.qsize() > 0:
        value, current_level = q.get()
        print(current_level, value)
        if current_level not in solution:
            solution.append(current_level)
            for i in range(0, len(current_level)):
                new_level = list(current_level)
                new_level[i] += 1
                if new_level[i] < len(current_level):
                    func_result = func_2(new_level)
                    print("Depth: " + str(sum(new_level)))
                    if func_result == 0:
                        solution.append(new_level)
                        return solution
                    else:
                        q.put((sum(new_level) + func_result, new_level))
    return solution


def available(board: list[list[int]], current_x: int, current_y: int):
    starting_x = current_x
    starting_y = current_y

    # Left side
    starting_y -= 1
    while starting_y >= 0:
        if not board[starting_x][starting_y]:
            starting_y -= 1
        else:
            return False
    # Refresh
    starting_y = current_y

    # Right side
    starting_y += 1
    while starting_y < 8:
        if not board[starting_x][starting_y]:
            starting_y += 1
        else:
            return False

    # Refresh
    starting_y = current_y

    # Upper side
    starting_x += 1
    while starting_x < 8:
        if not board[starting_x][starting_y]:
            starting_x += 1
        else:
            return False

    # Refresh
    starting_x = current_x

    # Lower side
    starting_x -= 1
    while starting_x >= 0:
        if not board[starting_x][starting_y]:
            starting_x -= 1
        else:
            return False

    # Refresh
    starting_x = current_x
    starting_y = current_y

    # Up-Right diagonal
    starting_x -= 1
    starting_y += 1
    while starting_x >= 0 and starting_y < 8:
        if not board[starting_x][starting_y]:
            starting_x -= 1
            starting_y += 1
        else:
            return False

    # Refresh
    starting_x = current_x
    starting_y = current_y

    # Up-Left diagonal
    starting_x -= 1
    starting_y -= 1
    while starting_x >= 0 and starting_y >= 0:
        if not board[starting_x][starting_y]:
            starting_x -= 1
            starting_y -= 1
        else:
            return False

    # Refresh
    starting_x = current_x
    starting_y = current_y

    # Down-Right diagonal
    starting_x += 1
    starting_y += 1
    while starting_x <= 7 and starting_y <= 7:
        if not board[starting_x][starting_y]:
            starting_x += 1
            starting_y += 1
        else:
            return False

    # Refresh
    starting_x = current_x
    starting_y = current_y

    # Down-Left diagonal
    starting_x += 1
    starting_y -= 1
    while starting_x <= 7 and starting_y >= 0:
        if not board[starting_x][starting_y]:
            starting_x += 1
            starting_y -= 1
        else:
            return False

    return True


def main():
    pygame.init()
    screen = pygame.display.set_mode((HEIGHT, WIDTH))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    problem = QueensProblem()
    problem.board[0][0] = 1
    problem.board[2][1] = 1
    # list_of_levels = BFS_all_solutions()
    list_of_levels = A_star_solve([0 for i in range(0, 7)])
    # list_of_levels = BFS_all_permutations()
    running = True
    count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if count < len(list_of_levels):
            problem.board = [[0 for _ in range(0, 8)] for _ in range(0, 8)]
            level = list_of_levels[count]
            for k in range(0, len(list_of_levels[count])):
                if level[k] != -1:
                    problem.board[k][level[k]] = 1
            count += 1
        draw(screen, problem)
        # time.sleep(0.1)
        # clock.tick(MAX_FPS)
        pygame.display.flip()

'''
def main():
    print(A_star_solve())
'''

def draw(screen, game):
    drawCells(screen)
    drawPieces(screen, game.board)


def drawCells(screen):
    colors = [BOARD_WHITE, BOARD_GREY]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if board[r][c]:
                screen.blit(QUEEN_IMAGE, pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))


if __name__ == "__main__":
    main()
