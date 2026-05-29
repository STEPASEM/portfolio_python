edges = [
    (0, 3, 3),
    (3, 5, 6),
    (5, 2, 4),
    (2, 4, 7),
    (1, 2, 2),
    (1, 0, 5),
    (1, 6, 1),
    (6, 4, 8)
]

n = 7
start = 0
INF = float('inf')

d = [INF] * n
p = [-1] * n
d[start] = 0

for _ in range(n - 1):
    for u, v, w in edges:
        if d[u] + w < d[v]:
            d[v] = d[u] + w
            p[v] = u

print("Вершина | Расстояние | Путь")
print("-" * 35)

for v in range(n):
    path = []
    x = v
    while x != -1:
        path.append(x)
        x = p[x]
    path.reverse()

    dist_str = str(d[v]) if d[v] != INF else "нет пути"
    path_str = " -> ".join(map(str, path)) if d[v] != INF else "нет пути"
    print(f"{v}       | {dist_str:<10} | {path_str}")