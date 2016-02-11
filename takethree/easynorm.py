def lazy_rep(node):
    stack = [node]
    while stack:
        node = stack.pop()
        yield (node[0], str(node[1]))
        stack.extend(reversed(node[2]))

def gt(node1, node2):
    for x, y in zip(lazy_rep(node1), lazy_rep(node2)):
        if x == y:
            continue
        elif x[0] == "un" or y[0] == "un":
            return False
        elif x > y:
            return True
    return False

class EasyNormalizer(object):
    def __init__(self, tags):
        select = lambda tag, xs: set([n for t, n in xs if t == tag])
        self._comm = select("comm", tags)
        self._idem = select("idem", tags)
        self._assoc = select("assoc", tags)
        self._ac = select("ac", tags)
    def __call__(self, node):
        return all(self.check(node.at_position(p)) for p in node.positions)
    def check(self, node):
        # step 1: look up rep for node
        # short circuit if we aren't even a func
        if node[0] != "func":
            return True
        n = node[1]
        # step 2: apply check associated with the tag
        if n in self._comm:
            left, right = node[2]
            # left <= right -> good
            if gt(left, right):
                return False
        elif n in self._idem:
            # better be unary
            child = node[2][0]
            # don't stack 
            if child[1] == n:
                return False
        elif n in self._assoc:
            left = node[2][0]
            if left[1] == n:
                return False
        elif n in self._ac:
            left, right = node[2]
            # force align left
            if right[1] == n:
                print(str(right) + " has ac")
                return False
            elif left[1] == n:
                a, b = left[2]
                c = right
                if gt(a, b):
                    print(str(a) + " greater than " + str(b))
                    return False
                if gt(b, c):
                    print(str(b) + " greater than " + str(c))
            else:
                if gt(left, right):
                    print("comm check, " + str(left) + " greater than " + str(right))
                    return False
            
            '''
            if left[1] != n:
                if right[1] == n:
                    b, c = right[2]
                    if gt(left, b) or gt(b, c):
                        return False
                else:
                    if gt(left, right):
                        return False
            '''
        # if none of the checks for non-normalness pass, we're normal
        return True
