import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import matplotlib.pyplot as plt


def function_sort(dictik_value: dict):
    for key, value in dictik_value.items():
        dictik_value[key] = sorted(value, key=lambda x: x[0])
    return dictik_value


def top_function():
    with open('hackathon_sirius_data.csv', 'r') as file:
        dict_val_start = dict()
        dict_val_stop = dict()
        for el in file.readlines()[1:]:
            val = el.split(',')
            start, end, size = int(val[2]), int(val[3]), float(val[5])
            # print(f'{start}-({size})>{end}')
            if dict_val_start.get(start) is None:
                dict_val_start[start] = [[end, size]]
            else:
                dict_val_start[start].append([end, size])
            if dict_val_stop.get(end) is None:
                dict_val_stop[end] = [[start, size]]
            else:
                dict_val_stop[end].append([start, size])

    sorted_list_diff_start = sorted(function_sort(dict_val_start).items(), key=lambda x: x[0])
    sorted_list_diff_stop = sorted(function_sort(dict_val_stop).items(), key=lambda x: x[0])
    for i, el in enumerate(sorted_list_diff_stop):
        diff_summ = 0
        max_sum = 0
        min_sum = 0
        summ_diff = 0
        for el2 in sorted_list_diff_start[i]:
            if isinstance(el2, list):
                const_el_start = sorted_list_diff_start[i][1][0]
                el = el[1]
                for index in range(len(el)):
                    index2 = 0

                    if el[index] > el2[index]:
                        summ_diff = el[index][1] - el2[index][1]
                    if el[index] < el2[index]:
                        diff_summ += el2[index][1] - el[index][1]
                        min_sum += el[index][1]
                        max_sum += el2[index][1]
                        if summ_diff == 0 and diff_summ > 0:
                            sorted_list_diff_start[i][1][0][1] = min_sum
                        while summ_diff > 0 or diff_summ > 0 or index2 < len(el)-1:
                            # print(sorted_list_diff_start[index2][1][0][1] >= sorted_list_diff_stop[index2][1][0][1], sorted_list_diff_start[index2][1][0][1], sorted_list_diff_stop[index2][1][0][1])
                            while sorted_list_diff_start[index2][1][0][1] <= sorted_list_diff_stop[index2][1][0][1]:
                                sorted_list_diff_start[index2][1][0][1] += 1
                                # sorted_list_diff_stop[index2][1][0][1] += 1
                            index2 += 1
                            summ_diff -= 1
                            diff_summ -= 1
                    sorted_list_diff_start[index2][1][0][1] -= 1

                # print(diff_summ, max_sum, min_sum, summ_diff)


        # print(diff_summ)

    # sorted_list_diff_start = sorted(dict_val_start.items(), key=lambda x: x[0])
    # sorted_list_diff_stop = sorted(dict_val_stop.items(), key=lambda x: x[0])
    return f"{sorted_list_diff_start}\n {sorted_list_diff_stop}"


print(top_function())
# top_function()

# with open('hackathon_sirius_data.csv', 'r') as file:
#     edges = list()
#     nodes = list()
#     graphs = nx.DiGraph()
#
#     for el in file.readlines()[1:]:
#         val = el.split(',')
#         start, end = int(val[2]), int(val[3])
#         edges.append((start, end))
#         if start not in nodes:
#             nodes.append(start)
#
#
# pos = nx.circular_layout(graphs)
#
# graphs.add_edges_from(edges)
# graphs.add_nodes_from(nodes)
# nx.draw(graphs, with_labels=True, arrows=True)
# plt.show()
