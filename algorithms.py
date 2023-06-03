import math
import numpy as np
from typing import Callable


def correlation_coefficient(x: int, y: int, dataset: list) -> float:
    try:
        sup_x = support([x], dataset)
        sup_y = support([y], dataset)
        sup_xy = support([x, y], dataset)
        return (sup_xy - sup_x * sup_y) / math.sqrt(sup_x * sup_y * (1 - sup_x) * (1 - sup_y))
    except ZeroDivisionError:
        return 0


def interest_ratio(x: int, y: int, dataset: list) -> float:
    try:
        sup_x = support([x], dataset)
        sup_y = support([y], dataset)
        sup_xy = support([x, y], dataset)
        return sup_xy / (sup_x * sup_y)
    except ZeroDivisionError:
        return 0


def support(x: list, dataset: list) -> float:
    return len([i for i in dataset if len(set(i).union(set(x))) == len(set(i))]) / len(dataset)


def brute_force_algorithms(dataset: list, count_items: int, threshold: float,
                           parameter: Callable[[int, int, list], float]) -> [list, set]:
    result = set()
    result_with_values = []
    for i in range(1, count_items):
        for j in range(i + 1, count_items + 1):
            value = parameter(i, j, dataset)
            if value >= threshold:
                result.add(tuple([i, j]))
                result_with_values.append([[i, j], value])
    return result_with_values, result


def get_violent_rate(items: list, dataset: list) -> float:
    violent = 0
    for transaction in dataset:
        union_len = len(set(transaction).union(set(items)))
        if union_len != len(set(transaction)) and union_len != len(set(transaction)) + len(set(items)):
            violent += 1
    try:
        return violent / len(dataset)
    except ZeroDivisionError:
        return 0


def get_expected_violation_rate(items: list, dataset: list) -> float:
    return 1 - np.prod([support([i], dataset) for i in items]) - np.prod([1 - support([i], dataset) for i in items])


def collective_strength(x: int, y: int, dataset: list) -> float:
    try:
        items = [x, y]
        violent_rate = get_violent_rate(items, dataset)
        expected_violation_rate = get_expected_violation_rate(items, dataset)

        if violent_rate == 0 or expected_violation_rate == 1:
            return 0
        return ((1 - violent_rate) * expected_violation_rate) / ((1 - expected_violation_rate) * violent_rate)
    except ZeroDivisionError:
        return 0


def generate_interesting_patterns(dataset: list, count_items: int, threshold: float,
                                  parameter: Callable[[int, int, list], float]) -> [list, set]:
    return brute_force_algorithms(dataset, count_items, threshold, parameter)
