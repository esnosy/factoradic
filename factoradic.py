from typing import Optional


class Node:
    def __init__(self) -> None:
        self.right: Optional[Node] = None
        self.left: Optional[Node] = None
        self.left_size = 0
        self.value: Optional[int] = None


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

    # TODO: make it self-balancing
    def insert(self, value):
        new_node = Node()
        new_node.value = value
        if self.root is None:
            self.root = new_node
            return

        current = self.root
        while True:
            if value < current.value:
                # We are moving into the left subtree,
                # so the left size of the current node increases.
                current.left_size += 1

                if current.left is None:
                    current.left = new_node
                    break
                current = current.left
            else:
                # Moving right does not change the left_size of the current node.
                if current.right is None:
                    current.right = new_node
                    break
                current = current.right


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
