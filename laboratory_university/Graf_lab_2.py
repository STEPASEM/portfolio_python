edges = [
    (0,1,10),(0,2,4),(1,4,8),
    (2,5,20),(3,1,5),(4,3,3),
    (2,3,4),(3,5,17),(4,6,7),(5,6,5)
]

n = 7
start = 0
end = 6
INF = float('inf')

d = [INF]*n
p = [-1]*n
d[start] = 0

for _ in range(n-1):
    for u,v,w in edges:
        if d[u] + w < d[v]:
            d[v] = d[u] + w
            p[v] = u


path = []
v = end
while v != -1:
    path.append(v)
    v = p[v]

path.reverse()

print("Длина:", d[end])
print("Путь:", " -> ".join(map(str, path)))