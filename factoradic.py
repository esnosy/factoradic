def permutation_to_factoradic(permutation):
    tree = [] #TODO: replace with binary tree
    factoradic = []
    for e in reversed(permutation):
        num_less_than = 0
        for v in tree:
            if v < e:
                num_less_than += 1
        factoradic.insert(0, num_less_than)
        tree.append(e)
    return factoradic


perm = (2, 0, 1)
factoradic = permutation_to_factoradic(perm)
print(factoradic)
