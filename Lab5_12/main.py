# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import random

NUMBER_OF_NODES = 100
NUMBER_OF_WORKING_BEES = 55
NUMBER_OF_RECONNAISSANCE_BEES = 5

class Solution:

    def __init__(self):
        self.path_length = 0
        self.solution = []

    def generate_rnd_solution(self, number_of_nodes: int):
        for i in range(0, number_of_nodes):
            self.solution.append(i)
        for i in range(0, len(self.solution)):
            j = random.randint(i, len(self.solution)-1)
            k = self.solution[i]
            self.solution[i] = self.solution[j]
            self.solution[j] = k

    def generate_neighboring_solution(self):
        neighbor_solution = Solution()
        neighbor_solution.solution = self.solution
        changed_index = random.randint(0, len(self.solution)-1)
        if changed_index == len(self.solution)-1:
            neighbor_index = 0
        else:
            neighbor_index = changed_index + 1
        k = neighbor_solution.solution[changed_index]
        neighbor_solution.solution[changed_index] = neighbor_solution.solution[neighbor_index]
        neighbor_solution.solution[neighbor_index] = k
        return neighbor_solution

    @staticmethod
    def calculate_weight(slt, mtrx):
        weight = 0
        for i in range(0, len(slt.solution)-1):
            weight += mtrx[slt.solution[i]][slt.solution[i+1]]
        weight += mtrx[slt.solution[len(slt.solution)-1]][slt.solution[0]]
        slt.path_length = weight
        return weight

    def greedy_algorithm(self, mtrx, number_of_nodes):
        visited = []
        start = random.randint(0, number_of_nodes-1)
        self.solution.append(start)
        visited.append(start)
        for i in range(0, number_of_nodes-1):
            current_node = self.solution[len(self.solution)-1]
            local_best = 200000000
            local_best_index = 200000000
            for j in range(0, number_of_nodes):
                if mtrx[current_node][j] == 0:
                    continue
                if mtrx[current_node][j] < local_best and mtrx[current_node][j] not in visited:
                    local_best = mtrx[current_node][j]
                    local_best_index = j
            self.solution.append(local_best_index)
            visited.append(local_best_index)
        Solution.calculate_weight(self, mtrx)


class Algorithm:
    def __init__(self, bee_number, scout_number, forager_number, solutions_number, iterations_number, mtrx, is_greedy):
        self.bee_number = bee_number
        self.scout_number = scout_number
        self.forager_number = forager_number
        self.solutions_number = solutions_number
        self.iterations_number = iterations_number
        self.nodes_number = len(mtrx[0])
        self.mtrx = mtrx
        self.is_greedy = is_greedy
        self.best_solution = None
        self.solutions = []
        self.generate_solutions()
        self.sort_solutions()

    def generate_solutions(self):
        if self.is_greedy:
            for i in range(0, self.solutions_number):
                self.solutions.append(Solution())
                self.solutions[i].greedy_algorithm(self.mtrx, self.nodes_number)
                Solution.calculate_weight(self.solutions[i], self.mtrx)
        else:
            for i in range(0, self.solutions_number):
                self.solutions.append(Solution())
                self.solutions[i].generate_rnd_solution(self.nodes_number)
                Solution.calculate_weight(self.solutions[i], self.mtrx)

    def sort_solutions(self):
        for i in range(0, len(self.solutions)):
            for j in range(0, len(self.solutions)):
                if self.solutions[i].path_length > self.solutions[j].path_length:
                    self.solutions[i], self.solutions[j] = self.solutions[j], self.solutions[i]

    def send_scout(self, current_best_index, visited_solutions):
        random_indicator = random.randint(0, 1)
        if not random_indicator:
            random_index = random.randint(0, len(self.solutions)-1)
            if self.solutions[random_index] in visited_solutions:
                return False
            visited_solutions.append(self.solutions[random_index])
            self.send_foragers(random_index)
        else:
            if current_best_index in visited_solutions:
                current_best_index += 1
                return False
            visited_solutions.append(current_best_index)
            self.send_foragers(current_best_index)
            current_best_index += 1
        return True

    def send_foragers(self, index):
        best_neighbor = Solution()
        best_neighbor_path_length = 2000000
        for i in range(0, self.forager_number):
            current_neighbor = self.solutions[index].generate_neighboring_solution()
            Solution.calculate_weight(current_neighbor, self.mtrx)
            if current_neighbor.path_length < best_neighbor_path_length:
                best_neighbor = current_neighbor
                best_neighbor_path_length = current_neighbor.path_length
        if best_neighbor.path_length < self.solutions[index].path_length:
            self.solutions[index] = best_neighbor

    def launch_algorithm(self):
        for i in range(0, self.iterations_number):
            visited_solutions = []
            current_best_index = 0
            number_of_scouts_sent = 0
            while number_of_scouts_sent != self.scout_number and number_of_scouts_sent != self.solutions_number:
                if self.send_scout(current_best_index, visited_solutions):
                    number_of_scouts_sent += 1
            self.sort_solutions()
            if (i+1) % 10 == 0 or i == self.iterations_number:
                print(f'Best solution found on iteration # {i+1} with path length {self.solutions[0].path_length}')
        return self.solutions[0]


def generate_graph():
    graph = [[0 for _ in range(0, NUMBER_OF_NODES)] for _ in range(0, NUMBER_OF_NODES)]
    for i in range(0, NUMBER_OF_NODES):
        for j in range(0, NUMBER_OF_NODES):
            distance = random.randint(5, 150)
            if i != j:
                graph[i][j] = distance
                graph[j][i] = distance
            else:
                graph[i][j] = 0
    return graph


def print_matrix(matrix):
    for i in range(0, NUMBER_OF_NODES):
        string = ""
        for j in range(0, NUMBER_OF_NODES):
            string += str(matrix[i][j]) + " "
        print(string)
    return 0


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    matrix = generate_graph()
    print_matrix(matrix)
    bee_colony_algorithm = Algorithm(NUMBER_OF_WORKING_BEES + NUMBER_OF_RECONNAISSANCE_BEES, NUMBER_OF_RECONNAISSANCE_BEES, NUMBER_OF_WORKING_BEES, 50, 10000, matrix, False)
    best_solution = bee_colony_algorithm.launch_algorithm()
    print(best_solution.solution)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
