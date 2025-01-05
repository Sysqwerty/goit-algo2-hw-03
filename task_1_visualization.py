import networkx as nx
import matplotlib.pyplot as plt

# Створюємо граф
G = nx.DiGraph()

# Додаємо ребра з пропускною здатністю
edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),
    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

# Додаємо всі ребра до графа
G.add_weighted_edges_from(edges)

# Позиції для малювання графа
pos = {
    "Термінал 1": (2, 4),
    "Термінал 2": (10, 4),
    "Склад 1": (4, 6),
    "Склад 2": (8, 6),
    "Склад 3": (4, 2),
    "Склад 4": (8, 2),
    "Магазин 1": (0, 8),
    "Магазин 2": (2, 8),
    "Магазин 3": (4, 8),
    "Магазин 4": (6, 8),
    "Магазин 5": (8, 8),
    "Магазин 6": (10, 8),
    "Магазин 7": (0, 0),
    "Магазин 8": (2, 0),
    "Магазин 9": (4, 0),
    "Магазин 10": (6, 0),
    "Магазин 11": (8, 0),
    "Магазин 12": (10, 0),
    "Магазин 13": (12, 0),
    "Магазин 14": (14, 0),
}

# Малюємо граф
plt.figure(figsize=(16, 10))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=2000,
    node_color="skyblue",
    font_size=10,
    font_weight="bold",
    arrows=True,
)
labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Відображаємо граф
plt.show()
