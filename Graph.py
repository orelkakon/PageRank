import csv
import operator


class Node:
    def __init__(self):
        self.list_neighbors = []
        self.list_reverse_neighbors = []
        self.r_tag_t = -1
        self.r_t_previous = -1
        self.r_t = -1


loaded_graph = {}


def load_graph(path):
    with open(path, newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='|')
        for row in reader:
            name = row[0]
            neighbor = row[1]
            if name not in loaded_graph:
                node_details = Node()
                loaded_graph[name] = node_details
            loaded_graph[name].list_neighbors.append(neighbor)
            if neighbor not in loaded_graph:
                node_details = Node()
                loaded_graph[neighbor] = node_details
            loaded_graph[neighbor].list_reverse_neighbors.append(name)


def sum_r_tag_t(reverse_neighbors_list, b):
    sum1 = 0
    for i in reverse_neighbors_list:
        i_r_t_previous = loaded_graph[i].r_t_previous
        di = len(loaded_graph[i].list_neighbors)
        sum1 = sum1 + b*(i_r_t_previous/di)
    return sum1


def calculate_page_rank(b, epsilon, max_iterations):
    counter = 0
    gap_sum = 100000.0
    s = 0
    for j in loaded_graph:
        loaded_graph[j].r_t = 1/len(loaded_graph)
        loaded_graph[j].r_t_previous = loaded_graph[j].r_t

    while counter < max_iterations or gap_sum > epsilon:
        gap_sum = 0
        s = 0
        for j in loaded_graph:
            if len(loaded_graph[j].list_reverse_neighbors)== 0:
                loaded_graph[j].r_tag_t = 0
            else:
                loaded_graph[j].r_tag_t = sum_r_tag_t(loaded_graph[j].list_reverse_neighbors, b)
            s = s + loaded_graph[j].r_tag_t

        for j in loaded_graph:
            loaded_graph[j].r_t_previous = loaded_graph[j].r_t
            loaded_graph[j].r_t = loaded_graph[j].r_tag_t + ((1 - s) / len(loaded_graph))
            gap_sum = gap_sum + abs(loaded_graph[j].r_t - loaded_graph[j].r_t_previous)
        counter = counter + 1


def get_page_rank(node_name):

    if node_name in loaded_graph:
        return loaded_graph[node_name].r_t
    return -1


def get_top_nodes(n):
    list_of_nodes = {}
    for node in loaded_graph:
        list_of_nodes[node] = loaded_graph[node].r_t
    sorted_list_by_value = sorted(list_of_nodes.items(), key = operator.itemgetter(1), reverse = True)
    return sorted_list_by_value[:n]


def get_all_page_rank():
    result = []
    for node in loaded_graph:
        result.append([node, loaded_graph[node].r_t])
    return result


notYet = True
Cont = True
while Cont:
    print("Insert [1] to load_graph\n"
          "Insert [2] to calculate_page_rank\n"
          "Insert [3] to get_PageRank\n"
          "Insert [4] to get_top_nodes\n"
          "Insert [5] to get_all_PageRank\n"
          "Insert [6] to Exit")
    ans = input()
    if ans == "1":
        notYet = True
        pathVal = input("Insert path of graph to load\n")
        load_graph(pathVal)
    elif ans == "2":
        notYet = False
        calculate_page_rank(0.85, 0.001, 20)
    elif ans == "3":
        nodeName = input("Insert the name of node\n")
        print(get_page_rank(nodeName))
    elif ans == "4":
        if notYet:
            print([])
        else:
            numTop = input("Insert number of top n\n")
            print(get_top_nodes(int(numTop)))
    elif ans == "5":
        if notYet:
            print([])
        else:
            print(get_all_page_rank())
    else:
        Cont = False


