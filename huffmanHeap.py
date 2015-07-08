# Como nao temos packages esse arquivo estara na mesma pasta
import tree
from queue import PriorityQueue

class Item():
    Node = tree.Node() # Cada elemento da arvore
    Frequency = 0
    # Nao estamos usado go portanto nao precisamos de indice

    def __init__(self, Node, Frequency):
        self.Node = Node
        self.Frequency = Frequency

    def __lt__(self, other):
        return self.Frequency < other.Frequency



# Em Go para satisfazer a interface heap e usarmos os metodos do package heap,
# tivemos que criar os metodos Len, Push, Pop, Less e Swap. Aqui aproveitaremos
# a implementacao pronta de uma fila de prioridade, criando metodos para manter a traducao
class HuffmanHeap(PriorityQueue):
    hh = PriorityQueue()
    # O construtor recebe um mapa de frequencias
    def __init__(self, freqMap):
        for value, frequency in freqMap.items():
            item = Item(
                    Node = tree.Node(value),
                    Frequency = frequency
            )
            self.hh.put(item)

    # Para termos metodos com os mesmos nomes que em Go
    def Push(self, item):
        self.hh.put(item)

    # Retorna o elemento com a menor frequencia
    def Pop(self):
        item = self.hh.get()
        return item

    def Len(self):
        return len(self.hh.queue)
