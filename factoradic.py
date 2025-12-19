from typing import Optional


class Node:
    def __init__(self) -> None:
        self.right: Optional[Node] = None
        self.left: Optional[Node] = None
        self.left_size = 0
        self.value: Optional[int] = None
        self.height = 1  # Height for AVL balancing


class Tree:
    def __init__(self) -> None:
        self.root = None

    def query_less_than(self, value):
        count = 0
        current = self.root
        while current:
            if value > current.value:
                # Add left subtree size + the node itself
                count += (current.left_size + 1)
                current = current.right
            else:
                # Move left; do not add to count
                current = current.left
        return count

    def _get_height(self, node):
        return node.height if node else 0

    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _update_height(self, node):
        if node:
            node.height = 1 + max(self._get_height(node.left),
                                  self._get_height(node.right))

    def _rotate_right(self, y):
        r"""
        Right rotation:
            y              x
           / \            / \
          x   C    ->    A   y
         / \                / \
        A   B              B   C
        """
        x = y.left
        B = x.right

        # Perform rotation
        x.right = y
        y.left = B

        # Update left_size
        # y's left subtree is now B, so y.left_size = size of B
        y.left_size = self._get_size(B)
        # x's left subtree is still A, so x.left_size unchanged
        # (it was already correct)

        # Update heights
        self._update_height(y)
        self._update_height(x)

        return x

    def _rotate_left(self, x):
        r"""
        Left rotation:
          x                y
         / \              / \
        A   y      ->    x   C
           / \          / \
          B   C        A   B
        """
        y = x.right
        B = y.left

        # Perform rotation
        y.left = x
        x.right = B

        # Update left_size
        # x's right subtree is now B, so x.right doesn't affect left_size
        # y's left subtree is now x (with all its left subtree), so:
        y.left_size = self._get_size(x.left) + 1 + self._get_size(B)
        # Actually simpler: y.left_size = size of entire left subtree of y
        # which is now x's left + x itself + B
        # But we can compute it as: x.left_size + 1 + size(x.right)
        y.left_size = x.left_size + 1 + self._get_size(B)

        # Update heights
        self._update_height(x)
        self._update_height(y)

        return y

    def _get_size(self, node):
        """Get the total size of a subtree."""
        if node is None:
            return 0
        return node.left_size + 1 + self._get_size(node.right)

    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        # Standard BST insertion
        if node is None:
            new_node = Node()
            new_node.value = value
            return new_node

        if value < node.value:
            node.left_size += 1
            node.left = self._insert_recursive(node.left, value)
        else:
            node.right = self._insert_recursive(node.right, value)

        # Update height
        self._update_height(node)

        # Get balance factor
        balance = self._get_balance(node)

        # Left-Left Case
        if balance > 1 and value < node.left.value:
            return self._rotate_right(node)

        # Right-Right Case
        if balance < -1 and value >= node.right.value:
            return self._rotate_left(node)

        # Left-Right Case
        if balance > 1 and value >= node.left.value:
            node.left = self._rotate_left(node.left)
            # After rotating left on left child, need to recalculate node.left_size
            node.left_size = self._get_size(node.left)
            return self._rotate_right(node)

        # Right-Left Case
        if balance < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node


def permutation_to_factoradic(permutation):
    """
    >>> permutation_to_factoradic((0,1,2))
    [0, 0, 0]
    >>> permutation_to_factoradic((0,2,1))
    [0, 1, 0]
    >>> permutation_to_factoradic((1,0,2))
    [1, 0, 0]
    >>> permutation_to_factoradic((1,2,0))
    [1, 1, 0]
    >>> permutation_to_factoradic((2,0,1))
    [2, 0, 0]
    >>> permutation_to_factoradic((2,1,0))
    [2, 1, 0]
    >>> permutation_to_factoradic((4,0,6,2,1,3,5))
    [4, 0, 4, 1, 0, 0, 0]
    """
    tree = Tree()
    factoradic = []
    for e in reversed(permutation):
        num_less_than = tree.query_less_than(e)
        factoradic.insert(0, num_less_than)
        tree.insert(e)
    return factoradic


perm = (2, 0, 1)
factoradic = permutation_to_factoradic(perm)
print(factoradic)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
