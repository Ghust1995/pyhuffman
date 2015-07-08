from collections import deque

class Node():
    Value = ""
    Left = None
    Right = None

    def __init__(self, v = "", l = None, r = None):
        self.Value = v
        self.Left = l
        self.Right = r

    # Método que informa se um nó é uma folha
    def isLeaf(self):
        return self.Left == None and self.Right == None

    def __repr__(self):
        return self.Value
    def __str__(self):
        s = ""
        # Aqui em vez de slices do Go usaremos a implementacao pronta de fila
        q = deque()
        q.append({'depth': 0, 'node': self})
        while len(q) > 0:
            # s += str(q.queue)
            # s += '\t'
            first = q.pop()
            if first is not None:
                for i in range(first['depth']):
                    s += "  "
                s += '"' + first['node'].Value + '"' + '\n'

                if not first['node'].isLeaf():
                    nxtDepth = first['depth'] + 1
                    if first['node'].Left is not None:
                        q.append({'depth': nxtDepth, 'node': first['node'].Left})
                    if first['node'].Left is not None:
                        q.append({'depth': nxtDepth, 'node': first['node'].Right})
        return s
