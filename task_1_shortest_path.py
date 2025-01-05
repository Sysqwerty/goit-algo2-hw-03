from collections import deque
from pprint import pprint


# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()

        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if (
                    not visited[neighbor]
                    and capacity_matrix[current_node][neighbor]
                    - flow_matrix[current_node][neighbor]
                    > 0
            ):
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)

    return False


# Основна функція для обчислення максимального потоку
def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [
        [0] * num_nodes for _ in range(num_nodes)
    ]  # Ініціалізуємо матрицю потоку нулем
    parent = [-1] * num_nodes
    max_flow = 0

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float("Inf")
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(
                path_flow,
                capacity_matrix[previous_node][current_node]
                - flow_matrix[previous_node][current_node],
            )
            current_node = previous_node

        # Оновлюємо потік уздовж шляху, враховуючи зворотний потік
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        # Збільшуємо максимальний потік
        max_flow += path_flow

    return max_flow


def build_flow_report(capacity_matrix, source_nodes, target_nodes):
    report = []
    for source in source_nodes:
        for target in target_nodes:
            flow = edmonds_karp(capacity_matrix, source, target)
            if flow > 0:  # Додаємо тільки реальні потоки
                report.append((f"Термінал {source + 1}", f"Магазин {target - 5}", flow))
    return report


def print_flow_report(report):
    print("Термінал\tМагазин\tФактичний Потік (одиниць)")
    for terminal, shop, flow in report:
        print(f"{terminal}\t{shop}\t{flow}")


def find_bottlenecks(capacity_matrix, flow_matrix):
    bottlenecks = []
    for i in range(len(capacity_matrix)):
        for j in range(len(capacity_matrix[i])):
            if capacity_matrix[i][j] > 0:
                residual_capacity = capacity_matrix[i][j] - flow_matrix[i][j]
                if residual_capacity > 0:  # Якщо залишкова здатність існує
                    bottlenecks.append((i, j, residual_capacity))
    bottlenecks.sort(key=lambda x: x[2])  # Сортуємо за залишковою здатністю
    return bottlenecks


def find_min_supply_shops(capacity_matrix, target_nodes):
    shop_flows = {f"Магазин {node - 5}": sum(capacity_matrix[i][node] for i in range(len(capacity_matrix))) for node in
                  target_nodes}
    min_supply_shop = min(shop_flows, key=shop_flows.get)
    return shop_flows, min_supply_shop


if __name__ == "__main__":
    # Матриця пропускної здатності для каналів у мережі (capacity_matrix)
    capacity_matrix = [
        [0, 0, 25, 20, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Термінал 1
        [0, 0, 0, 10, 15, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Термінал 2
        [0, 0, 0, 0, 0, 0, 15, 10, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Склад 1
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 10, 25, 0, 0, 0, 0, 0, 0, 0, 0],  # Склад 2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 15, 10, 0, 0, 0, 0, 0],  # Склад 3
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 10, 15, 5, 10],  # Склад 4
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 1
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 3
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 4
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 5
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 6
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 7
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 8
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 9
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 10
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 11
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 12
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 13
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 14
    ]

    source = 0  # Термінал 1
    sink = 14  # Магазин 9
    max_flow = edmonds_karp(capacity_matrix, source, sink)
    print(f"Максимальний потік для обраного термінала '{source + 1}' та магазина '{sink - 5}': {max_flow}")

    # Визначення вузлів
    source_nodes = [0, 1]  # Термінали (0 і 1)
    target_nodes = list(range(6, 20))  # Магазини (6 до 19)

    # Побудова звіту
    flow_report = build_flow_report(capacity_matrix, source_nodes, target_nodes)
    print_flow_report(flow_report)

    # Які термінали забезпечують найбільший потік товарів до магазинів?
    terminal_flows = {f"Термінал {i + 1}": sum(capacity_matrix[i]) for i in source_nodes}
    max_terminal = max(terminal_flows, key=terminal_flows.get)
    print(f"\nЗагальна сума потоків кожного термінала: {terminal_flows}")
    print(f"Термінал з найбільшим потоком: {max_terminal}")

    # Які маршрути мають найменшу пропускну здатність і як це впливає на загальний потік?

    # Мінімальна пропускна здатність визначає "вузьке місце" в потоці, тобто обмеження, через яке загальний потік не
    # може збільшитися. Це особливо важливо на маршрутах, які входять до знайдених збільшуючих шляхів. Якщо "вузьке
    # місце" усунути (збільшити пропускну здатність цього маршруту), то максимальний потік може зрости.
    flow_matrix = [
        [0] * len(capacity_matrix) for _ in range(len(capacity_matrix))
    ]
    bottlenecks = find_bottlenecks(capacity_matrix, flow_matrix)
    print("\nМаршрути з мінімальною залишковою пропускною здатністю:")
    for route in bottlenecks[:5]:  # Виведемо топ-5 "вузьких місць"
        print(f"Маршрут {route[0]} → {route[1]}: залишкова здатність = {route[2]}")

    # Які магазини отримали найменше товарів і чи можна збільшити їх постачання, збільшивши пропускну здатність
    # певних маршрутів?

    # Чи можна збільшити постачання? Якщо магазин отримав мало товарів, це може бути пов'язано з
    # вузькими місцями на маршрутах, які ведуть до нього. Для збільшення постачання: Визначте всі маршрути,
    # які ведуть до цього магазину. Перевірте залишкову пропускну здатність цих маршрутів. Якщо пропускна здатність
    # недостатня, спробуйте її збільшити.

    shop_flows, min_supply_shop = find_min_supply_shops(capacity_matrix, target_nodes)
    print("Постачання кожного магазину")
    pprint(shop_flows)
    print(f"Магазин з найменшим постачанням: {min_supply_shop} (отримав {shop_flows[min_supply_shop]} одиниць)")
    print("В нашому випадку магазин 13 отримав 5 одиниць товару через вузьке місце 'Склад 4 - Магазин 13'")

    # Чи є вузькі місця, які можна усунути для покращення ефективності логістичної мережі?

    # Так, є вузькі місця, які ми розглянули у попередніх питаннях. Наприклад, якщо ми хочемо збільшити пропускну
    # здатність маршруту, який веде від "Склад 4" до "Магазин 13" до 30, то ми можемо збільшити пропускну здатність
    # цього маршруту без втрати ефективності.
