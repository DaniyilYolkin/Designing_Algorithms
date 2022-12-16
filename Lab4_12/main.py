import random

NUMBER_OF_NODES = 500
NUMBER_OF_ITERATIONS = 100000
NUMBER_OF_WORKING_BEES = 55
NUMBER_OF_RECONNAISSANCE_BEES = 5
MAX_NUMBER_OF_CONNECTIONS = 30
MIN_NUMBER_OF_CONNECTIONS = 1
NODES_CLEARED = []


def generate_graph():
    graph = [[0 for _ in range(0, NUMBER_OF_NODES)] for _ in range(0, NUMBER_OF_NODES)]
    for i in range(0, NUMBER_OF_NODES):
        for j in range(0, NUMBER_OF_NODES):
            value = random.randint(0, 1)
            if i != j and not graph[i][j] and value:
                count_x_1 = 0
                count_x_2 = 0
                count_y_1 = 0
                count_y_2 = 0
                for k in range(0, NUMBER_OF_NODES):
                    if graph[i][k]:
                        count_x_1 += 1
                    if graph[k][j]:
                        count_y_1 += 1
                    if graph[j][k]:
                        count_x_1 += 1
                    if graph[k][i]:
                        count_x_1 += 1
                if count_x_1 >= MAX_NUMBER_OF_CONNECTIONS or count_x_2 >= MAX_NUMBER_OF_CONNECTIONS \
                    or count_y_1 >= MAX_NUMBER_OF_CONNECTIONS or count_y_2 >= MAX_NUMBER_OF_CONNECTIONS:
                    continue
                else:
                    graph[i][j] = value
                    graph[j][i] = value
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


def ABC(graph):
    number_of_iterations = 0
    best_current_coloring = [0 for _ in range(0, NUMBER_OF_NODES)]
    flag = True
    while number_of_iterations != NUMBER_OF_ITERATIONS:

        # Copy the best found coloring
        current_coloring = list(best_current_coloring)

        # Randomly select nodes
        nodes_selected = selecting_nodes()

        # Calculate nectar values
        nectar_values = count_nectar(nodes_selected, graph)

        # Clear nectar from nodes that were already cleared
        for node in nodes_selected:
            if node in NODES_CLEARED:
                nectar_values[nodes_selected.index(node)] = 0

        # Rearrange nodes
        temp_node_storage = []
        nectar_values_copy = list(nectar_values)
        for i in range(0, len(nodes_selected)):
            max_value = max(nectar_values_copy)
            index = nectar_values.index(max_value)
            while nodes_selected[index] in temp_node_storage:
                index += 1
            temp_node_storage.append(nodes_selected[index])
            nectar_values_copy.pop(nectar_values_copy.index(max_value))
        nodes_selected = list(temp_node_storage)

        # Assign bees in proportion
        bees = []
        bees_used = 0
        nectar_values.sort()
        counter = 0
        for i in range(0, len(nectar_values)):
            if nectar_values[i] != 0:
                bees_count = int(NUMBER_OF_WORKING_BEES * nectar_values[i])
                bees_used += bees_count
                bees.append(bees_count)
            else:
                counter += 1
        end_counter = counter
        while counter:
            bees.append(int((NUMBER_OF_WORKING_BEES - bees_used) / end_counter))
            counter -= 1

        # print(sum(bees))
        # print(bees)

        # Check each node according to nectar value
        for node in nodes_selected:
            node_connections = []

            # Find all adjacent nodes to the node
            for i in range(0, NUMBER_OF_NODES):
                if graph[node][i]:
                    node_connections.append(i)

            # Crop the list of connection according to the number of allocated bees
            if bees[nodes_selected.index(node)] < len(node_connections):
                node_connections = node_connections[:bees[nodes_selected.index(node)]-1:]

            # Check each node adjacent to current node
            for sub_node in node_connections:
                sub_node_connections = []

                # Find all adjacent nodes to the node
                for j in range(0, NUMBER_OF_NODES):
                    if graph[sub_node][j] and j != node:
                        sub_node_connections.append(j)

                # Determine all colors used by adjacent nodes
                colors_used = []
                for sub_node_connection in sub_node_connections:
                    colors_used.append(current_coloring[sub_node_connection])

                # Paint adjacent node in color that wasn't used by adjacent nodes
                color_selected = 0
                for i in range(1, NUMBER_OF_NODES):
                    if i not in colors_used:
                        color_selected = i
                        break
                current_coloring[sub_node] = color_selected

            # Determine all colors used by adjacent nodes
            sub_node_colors = []
            for sub_node in node_connections:
                sub_node_colors.append(current_coloring[sub_node])

            # Paint node in color that wasn't used by adjacent nodes
            for i in range(1, NUMBER_OF_NODES):
                if i not in sub_node_colors:
                    current_coloring[node] = i
                    break

            # Check whether new solution is better than previously considered best
            if not best_current_coloring.__contains__(0):
                if max(current_coloring) <= max(best_current_coloring):
                    best_current_coloring = list(current_coloring)
            else:
                best_current_coloring = list(current_coloring)

            # Indicate that nectar should be cleared from the node
            NODES_CLEARED.append(node)

        # Check whether all nodes were painted
        if not best_current_coloring.__contains__(0) and flag:
            print("All nodes painted!")
            flag = False
        number_of_iterations += 1

        # Print the result of every 20th iteration
        if number_of_iterations % 20 == 0:
            print("Number of iteration: " + str(number_of_iterations))
            print("Number of colors: " + str(max(best_current_coloring)))

    # Print the result
    print(best_current_coloring)

    return best_current_coloring


def selecting_nodes():
    nodes_selected = []
    while len(nodes_selected) != NUMBER_OF_RECONNAISSANCE_BEES:
        node = random.randint(0, NUMBER_OF_NODES-1)
        if node not in nodes_selected:
            nodes_selected.append(node)
    return nodes_selected


def count_nectar(nodes: list[int], graph: list[list[int]]):
    nectar_values = []
    for node in nodes:
        current_nectar = 0
        for value in graph[node]:
            if value:
                current_nectar += 1
        nectar_values.append(current_nectar)
    nectar_sum = sum(nectar_values)
    for i in range(0, len(nectar_values)):
        nectar_values[i] = nectar_values[i]/nectar_sum
    return nectar_values


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    matrix = generate_graph()
    print_matrix(matrix)
    ABC(matrix)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
