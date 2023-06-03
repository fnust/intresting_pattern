from transactions import generate_dataset
from graph import Node
from algorithms import generate_interesting_patterns
from typing import Callable
import numpy as np
import matplotlib.pyplot as plt


def counting_metrics(replications_count: int, root: Node, count_transactions: int, true_set: set, count_items: int,
                     threshold: float, parameter: Callable[[int, int, list], float]) -> [list, list, list]:
    loss_avg = []
    precision_avg = []
    recall_avg = []

    for _ in range(replications_count):
        dataset = generate_dataset(root, count_transactions)
        sets_with_value, sets = generate_interesting_patterns(dataset, count_items, threshold, parameter)

        recall = len(sets.intersection(true_set)) / (len(true_set) + 0.00001)
        recall_avg.append(recall)

        precision = len(sets.intersection(true_set)) / (len(sets) + 0.00001)
        precision_avg.append(precision)

        loss = len(sets.symmetric_difference(true_set))
        loss_avg.append(loss)

    return loss_avg, precision_avg, recall_avg


def make_experiment(max_count: int, step: int, replications_count: int, root: Node, true_set: set, count_items: int,
                    threshold: float, parameter: Callable[[int, int, list], float]) -> None:
    numbers_of_transactions = [i for i in range(0, max_count + 1, step)]
    y = []
    precision_lst = []
    recall_lst = []

    for number in numbers_of_transactions:
        loss, precision, recall = counting_metrics(replications_count, root, number, true_set, count_items,
                                                               threshold, parameter)
        print(f'#{number} transactions')

        y.append(np.median(loss))
        precision_lst.append(np.median(precision))
        recall_lst.append(np.median(recall))

    print("Max precision:", max(precision_lst))
    print("Max recall:", max(recall_lst))
    show_metric_graphs(numbers_of_transactions, recall_lst, precision_lst)


def show_metric_graphs(numbers_of_transactions: list, recall_lst: list, precision_lst: list) -> None:
    fig = plt.plot(numbers_of_transactions, recall_lst, label='linear', marker='o', color="green")  # graphs
    plt.ylabel('Recall')
    plt.title('T/Recall')
    plt.show()
    plt.plot(numbers_of_transactions, precision_lst, label='linear', marker='o', color="red")
    plt.title('T/Precision')
    plt.ylabel('Precision')
    plt.show()
    plt.plot(precision_lst, recall_lst, marker='o')
    plt.title('Precision/Recall')
    plt.ylabel('Recall')
    plt.show()
