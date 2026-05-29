class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    # ВСТАВКА
    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

    # ПОИСК
    def search(self, value):
        current = self.root
        while current:
            if current.value == value:
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return False

    # УДАЛЕНИЕ
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.left is None and node.right is None:
                return None
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            min_node = self._find_min(node.right)
            node.value = min_node.value
            node.right = self._delete_recursive(node.right, min_node.value)

        return node

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node

    # ОБХОД В ГЛУБИНУ (DFS)
    def dfs_inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    # ОБХОД В ШИРИНУ (BFS)
    def bfs(self):
        if self.root is None:
            return []

        result = []
        queue = [self.root]

        while queue:
            node = queue.pop(0)
            result.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

    # ВИЗУАЛИЗАЦИЯ
    def print_pretty(self):
        if self.root is None:
            print("Дерево пусто")
            return

        self._print_pretty(self.root, "", True)

    def _print_pretty(self, node, prefix, is_left):
        if node is None:
            return

        self._print_pretty(node.right, prefix + ("│   " if is_left else "    "), False)

        if prefix:
            if is_left:
                print(prefix + "└── " + str(node.value))
            else:
                print(prefix + "┌── " + str(node.value))
        else:
            print(str(node.value))

        self._print_pretty(node.left, prefix + ("    " if is_left else "│   "), True)


# СОЗДАЕМ ДЕРЕВО
tree = BinaryTree()

# Вставляем элементы
elements = [50, 30, 70, 20, 40, 60, 80, 35, 45, 55, 65, 75, 85, 25, 33]
print("СОЗДАНИЕ ДЕРЕВА:")
print("Вставляем:", elements)
for elem in elements:
    tree.insert(elem)

print("\n" + "=" * 60)
print("КРАСИВОЕ ДЕРЕВО (как в учебниках):")
print("=" * 60)
tree.print_pretty()

print("\n" + "=" * 60)
print("ОБХОД В ГЛУБИНУ (DFS):")
dfs_result = tree.dfs_inorder()
print("Симметричный обход:", dfs_result)
print("(дает отсортированный порядок)")

print("\n" + "=" * 60)
print("ОБХОД В ШИРИНУ (BFS):")
bfs_result = tree.bfs()
print("Обход по уровням:", bfs_result)
print("(сначала корень, потом его дети, потом внуки)")

print("\n" + "=" * 60)
print("ПОИСК ЭЛЕМЕНТОВ:")
print(f"Поиск 33: {'✓ НАЙДЕН' if tree.search(33) else '✗ НЕ НАЙДЕН'}")
print(f"Поиск 40: {'✓ НАЙДЕН' if tree.search(40) else '✗ НЕ НАЙДЕН'}")
print(f"Поиск 100: {'✓ НАЙДЕН' if tree.search(100) else '✗ НЕ НАЙДЕН'}")
print(f"Поиск 25: {'✓ НАЙДЕН' if tree.search(25) else '✗ НЕ НАЙДЕН'}")

print("\n" + "=" * 60)
print("УДАЛЕНИЕ ЭЛЕМЕНТОВ:")
print("\n▶ Удаляем 20 (лист - нет детей):")
tree.delete(20)
tree.print_pretty()

print("\n▶ Удаляем 70 (узел с двумя детьми):")
tree.delete(70)
tree.print_pretty()

print("\n▶ Удаляем 30 (узел с одним ребенком):")
tree.delete(30)
tree.print_pretty()

print("\n" + "=" * 60)
print("ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
print(f"DFS (обход в глубину): {tree.dfs_inorder()}")
print(f"BFS (обход в ширину): {tree.bfs()}")
print("=" * 60)

# Показываем структуру дерева
print("\nСТРУКТУРА ДЕРЕВА:")
remaining = [50, 30, 70, 20, 40, 60, 80, 35, 45, 55, 65, 75, 85, 25, 33]
print("Оставшиеся элементы в дереве:", [x for x in remaining if tree.search(x)])
print("Удаленные элементы:", [x for x in remaining if not tree.search(x)])