import huffmanHeap, tree

def Harvest(freqMap):
    # Primeiro a gente cria a nossa priorityqueue a partir do dicionario de frequencias
    hh = huffmanHeap.HuffmanHeap(freqMap)

    while True:
        # Caso a heap contenha um unico elemento retornamos ela
        if hh.Len() == 1:
            return hh.Pop().Node

        # Caso contrario pegamos os dois elementos do topo
        r = hh.Pop()
        l = hh.Pop()

        # E criamos uma "arvore" intermediaria com eles
        newItem = huffmanHeap.Item(
                    Node = tree.Node(l = l.Node, r = r.Node),
                    Frequency = l.Frequency + r.Frequency
        )

        hh.Push(newItem)
