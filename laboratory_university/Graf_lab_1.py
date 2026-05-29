def dijkstra(graph, start, end):
    vertices = list(graph.keys())

    distances = {vertex: float('inf') for vertex in vertices}
    distances[start] = 0
    visited = []
    previous = {vertex: None for vertex in vertices}

    while len(visited) < len(vertices):
        current = None
        min_distance = float('inf')
        for vertex in vertices:
            if vertex not in visited and distances[vertex] < min_distance:
                min_distance = distances[vertex]
                current = vertex

        if current is None:
            break

        visited.append(current)

        # Обновляем расстояния до соседей
        if current in graph:
            for neighbor, weight in graph[current].items():
                if neighbor not in visited:
                    new_distance = distances[current] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current

        #print(previous, distances, visited)

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    return path, distances[end]


graph = {
    'V1': {'V2': 7, 'V3': 9, 'V5': 11},
    'V2': {'V3': 6, 'V4': 6, 'V6': 13},
    'V3': {'V4': 5, 'V5': 6},
    'V4': {},
    'V5': {'V2': 4, 'V4': 6, 'V6': 8},
    'V6': {'V4': 6}
}

# 1) От вершины V1 до вершины V4
path1, distance1 = dijkstra(graph, 'V1', 'V4')
print("1) От V1 до V4:")
print(f"   Путь: {' -> '.join(path1)}")
print(f"   Длина пути: {distance1}")
print()

# 2) От вершины V3 до вершины V6
path2, distance2 = dijkstra(graph, 'V3', 'V6')
print("2) От V3 до V6:")
print(f"   Путь: {' -> '.join(path2)}")
print(f"   Длина пути: {distance2}")
print()

# 3) От вершины V1 до вершины V6
path3, distance3 = dijkstra(graph, 'V1', 'V6')
print("3) От V1 до V6:")
print(f"   Путь: {' -> '.join(path3)}")
print(f"   Длина пути: {distance3}")