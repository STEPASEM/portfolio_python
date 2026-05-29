INF = 999

d = [
    [0, 3, INF],
    [1, 2, 4],
    [1, INF, 0]
]

for k in range(3):
    for i in range(3):
        for j in range(3):
            if d[i][k] + d[k][j] < d[i][j]:
                d[i][j] = d[i][k] + d[k][j]

print("Матрица кратчайших расстояний:")
print("       V1   V2   V3")
print("-" * 20)

for i in range(3):
    if i == 0:
        print(f"V{i + 1} |", end=" ")
    elif i == 1:
        print(f"V{i + 1} |", end=" ")
    else:
        print(f"V{i + 1} |", end=" ")

    for j in range(3):
        if d[i][j] == INF:
            print(f"{'∞':>3}", end="  ")
        else:
            print(f"{d[i][j]:>3}", end="  ")
    print()