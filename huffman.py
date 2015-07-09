import codecs, sys, getopt

from gardener import Harvest
from frequency import GetMap
import bit
from tree import Node

# Metodo para escrever a arvore recursivamente
# Python possui um bitwriter pronto, que será usado aqui,
# Para a nossa implementacao de bitwriter, recorra ao codigo em Go
def writeNode(node, writer):
    if node.isLeaf(): # Folha
        writer.write(1)
        writer.writebyte(node.Value)
    else:
        writer.write(0)
        writeNode(node.Left, writer)
        writeNode(node.Right, writer)

# Metodo para criar um dicionario para o caracter e seu codigo gerado
# e seu codigo gerado pelo algoritmo de Huffman
def createDict(node, dict, code = ""):
    if node.isLeaf():
        dict[node.Value] = code
    else:
        createDict(node.Left, dict, code + '0')
        createDict(node.Right, dict, code + '1')

# Metodo para escrever o arquivo na forma codificada
def writeCodified(file, dict, writer):
    # Loop para ler um caracter e escreve-lo na saida em forma codificada
    while True:
        r = file.read(1)
        if r == '':
            break
        # Transformar o caracter lido no codigo feito pelo dicionario
        codeb = dict[r]

        # Temos que escrever bit a bit
        for i in range(len(codeb)):
            writer.write(codeb[i])
    writer.close()

# Recebe um arquivo de texto e cria um arquivo comprimido
def Compress(filename, outputName):
    with codecs.open(filename, 'r', 'utf-8') as file:
        # gerar a arvore a partit da frequencia dos caracteres no texto
        root = Harvest(GetMap(file))

        # gerar o dicionario
        dict = {}

        # Caso só tenha uma letra
        if(root.isLeaf()):
            dict[root.Value] = 0
        else:
            createDict(root, dict)

        # Resetar cursor
        file.seek(0, 0)

        # Escrever arvora
        with codecs.open(outputName, 'w', 'utf-8') as outputFile:
            writer = bit.Writer(outputFile)
            writeNode(root, writer)

            # Codificar
            writeCodified(file, dict, writer)

# Helper
def reverseBits(b):
    b = ord(b)
    d = 0
    for i in range(8):
        d <<= 1
        d |= b & 1
        b >>= 1
    return d

# Metodo para ler a arvore recursivamente
def readTree(reader):
    read = reader.read()
    if read == 1: # folha
        char = chr(reader.readbyte())
        # print('char: ' + str(char))
        # if char:
        #     char = reverseBits(char)

        return Node(char, None, None)
    elif read == 0: # Tem dois filhos
        leftChild = readTree(reader)
        rightChild = readTree(reader)
        return Node("", leftChild, rightChild)

def decodeFile(reader, outputname, root):
    with codecs.open(outputname, 'w', 'utf-8') as output:
        node = root
        while True:
            bit = reader.read()
            if bit == '':
                break

            # Anda na arvore, se bit = 0 vai para o filho esquerdo
            node = node.Right if bit == 1 else node.Left

            # Checar se chegarmos a uma folha
            if node.isLeaf():
                output.write(str(node.Value))
                node = root

# Recebe um arquivo comprimido (objeto) e retorna o arquivo original (objeto)
def Decompress(filename, outputName):
    with codecs.open(filename, 'r', 'utf-8') as file:
        # Ler arvore (reconstruir)
        reader = bit.Reader(file)
        root = readTree(reader)
        if root == None:
            raise ErroNaArvore("Nula!")

        # Decodificar percorrendo a arvore
        if root.isLeaf():
            nodeHelper = Node()
            nodeHelper.Left = root
            root = nodeHelper

        decodeFile(reader, outputName, root)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hc:d:", ["help"])
    except Exception as e:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == "-c":
            Compress(arg, arg[:len(arg) - arg.find('.')] + '.ch')
        elif opt == "-d":
            Decompress(arg, arg[:len(arg) - arg.find('.') + 1] + '_d.txt')

usageString = """usage: huffman [--help] [-h] [-c <path>] [-d <path>]

The commands are:
-c \t\t Compress the file at path
-d \t\t Decompress the file at path
-h, --help \t Show available commands
"""


def usage():
    print(usageString)

if __name__ == '__main__':
    main(sys.argv[1:])
