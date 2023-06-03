from random import randint, random
import matplotlib.pyplot as plt
from igraph import Graph, plot
import pickle


class Node:
    def __init__(self, parent, p10, p11, position=0):
        self.position = position
        self.parent = parent
        self.value = None
        self.children = []
        self.p10 = p10
        self.p11 = p11

    def add_children(self, count, vertices):
        for i in range(vertices, vertices + count):
            self.children.append(Node(self, random(), random(), i))

        return vertices + count


def generate_tree(n: int) -> Node:
    max_children = 4
    vertices = 1
    root = Node(None, random(), random())

    count = randint(1, min(n, max_children))
    count_children = count if count + vertices < n else n - vertices - 1

    vertices = root.add_children(count_children, vertices)
    nodes = root.children.copy()

    while vertices < n:
        while len(nodes):
            node = nodes.pop(0)
            count = randint(1, min(n - vertices + 1, max_children))
            count_children = count if count + vertices <= n else n - vertices

            vertices = node.add_children(count_children, vertices)

            if vertices == n:
                return root

            nodes.extend(node.children)
    return root


def draw_edges_nodes(node: Node, graph: Graph, parent_id: Graph.add_vertex) -> Graph:
    if node.parent is None:
        parent_id = graph.add_vertex(node.position, color="green")

    for child in node.children:
        color = "yellow" if len(child.children) != 0 else "red"
        child_id = graph.add_vertex(child.position, color=color)
        graph.add_edge(parent_id, child_id)
        draw_edges_nodes(child, graph, child_id)

    return graph


def draw_graph(node: Node) -> None:
    graph = draw_edges_nodes(node, Graph(), 0)
    pickle.dump(node, open("data/last_graph", 'wb'))
    layout = graph.layout_reingold_tilford(mode="in", root=[0])
    plot(graph, target="data/graph.png", layout=layout, vertex_label=graph.vs['name'])
    fig, ax = plt.subplots()
    plot(graph, target=ax, layout=layout)
