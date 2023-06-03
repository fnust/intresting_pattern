from random import random
from graph import Node


def generate_transaction(root: Node, result: list) -> list:
    if root.parent is None:
        root.value = 1 if random() < root.p11 else 0
    else:
        if root.parent.value == 1:
            root.value = 1 if random() < root.p11 else 0
        else:
            root.value = 1 if random() < root.p10 else 0

    result.append(root.value)

    for child in root.children:
        generate_transaction(child, result)

    return transform_transaction(result)


def transform_transaction(transaction: list) -> list:
    result = []
    for i in range(len(transaction)):
        if transaction[i] == 1:
            result.append(i + 1)
    return result


def generate_dataset(model: Node, count: int) -> list:
    dataset = []
    for _ in range(count):
        transaction = generate_transaction(model, [])
        dataset.append(transaction)

    return dataset
