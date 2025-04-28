class Node:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.next = None  


class BPlusTree:
    def __init__(self, degree):
        self.root = Node(is_leaf=True)
        self.degree = degree
        self.comparisons = 0

    def _find_leaf(self, key):
        current = self.root
        while not current.is_leaf:
            for i, item in enumerate(current.keys):
                self.comparisons += 1
                if key < item:
                    current = current.children[i]
                    break
            else:
                current = current.children[-1]
        return current

    def add_player(self, key, player):
        leaf = self._find_leaf(key)
        self.comparisons += len(leaf.keys)

        if key in leaf.keys:
            index = leaf.keys.index(key)
            leaf.children[index].append(player)
        else:
            index = next((i for i, item in enumerate(leaf.keys) if key < item), len(leaf.keys))
            leaf.keys.insert(index, key)
            leaf.children.insert(index, [player])

            if len(leaf.keys) == self.degree:
                self._split_node(leaf)

    def _split_node(self, node):
        mid_index = len(node.keys) // 2
        mid_key = node.keys[mid_index]

        new_node = Node(is_leaf=node.is_leaf)
        new_node.keys = node.keys[mid_index + 1:]
        new_node.children = node.children[mid_index + 1:]
        node.keys = node.keys[:mid_index]
        node.children = node.children[:mid_index + 1]

        if node.is_leaf:
            new_node.next = node.next
            node.next = new_node

        if node == self.root:
            new_root = Node()
            new_root.keys = [mid_key]
            new_root.children = [node, new_node]
            self.root = new_root
        else:
            parent = self._find_parent(self.root, node)
            insert_pos = next((i for i, item in enumerate(parent.keys) if mid_key < item), len(parent.keys))
            parent.keys.insert(insert_pos, mid_key)
            parent.children.insert(insert_pos + 1, new_node)

            if len(parent.keys) == self.degree:
                self._split_node(parent)

    def _find_parent(self, current, child):
        if current.is_leaf:
            return None
        for i, node in enumerate(current.children):
            if node == child:
                return current
            elif not node.is_leaf:
                result = self._find_parent(node, child)
                if result:
                    return result

    def find_players_in_range(self, start, end):
        leaf = self._find_leaf(start)
        results = []
        self.comparisons += len(leaf.keys)

        while leaf:
            for i, key in enumerate(leaf.keys):
                self.comparisons += 1
                if start <= key <= end:
                    results.extend(leaf.children[i])
                elif key > end:
                    return results
            leaf = leaf.next
        return results

    def find_best_player(self):
        leaf = self.root
        while not leaf.is_leaf:
            leaf = leaf.children[-1]
        return leaf.keys[-1], leaf.children[-1]

    def find_worst_player(self):
        leaf = self.root
        while not leaf.is_leaf:
            leaf = leaf.children[0]
        return leaf.keys[0], leaf.children[0]

    def get_score(self, player):
        current = self.root
        while not current.is_leaf:
            for i, item in enumerate(current.keys):
                self.comparisons += 1
                if player < item:
                    current = current.children[i]
                    break
            else:
                current = current.children[-1]

        for i, players in enumerate(current.children):
            self.comparisons += 1
            if player in players:
                return current.keys[i]
        return None

    def remove_player(self, player):
        leaf = self._find_leaf(player)
        for i, players in enumerate(leaf.children):
            self.comparisons += 1
            if player in players:
                leaf.children[i].remove(player)
                if not leaf.children[i]:
                    leaf.keys.pop(i)
                    leaf.children.pop(i)
                return
