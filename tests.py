# Python nao oferece a facilidade das implementacoes de interfaces como o Go faz
# Assim, teremos que criar um arquivo de teste com classes para cada um
from unittest import TestCase, skip
import os, codecs
from tempfile import TemporaryDirectory

import frequency, gardener, huffman
from testconstants import testString, testMap, testTree, testTreeBinary, \
 testCodeDict, testEncoded
import bit

# Como nao temos o interessante formato de packacges que o Go determina
# Faremos cada teste em sua propria classe

# Helper
def getFileBinary(f):
    reader = bit.Reader(f)
    s = ""
    while True:
        r = reader.read()
        if r == '':
            break
        s += str(r)
    return s


class TestFrequencyMethods(TestCase):
     def test_frequency(self):
         # Boas praticas de python
         with TemporaryDirectory() as td:
             tempFileName = os.path.join(td, 'testFile')
             with open(tempFileName, 'w') as testFile:
                 testFile.write(testString)
             with open(tempFileName, 'r') as testFile:
                 m = frequency.GetMap(testFile)
                 self.assertEqual(m, testMap)


class TestGardenerMethods(TestCase):
    def test_harvest(self):
        self.assertEqual(str(gardener.Harvest(testMap)), str(testTree))

class TestBitMethods(TestCase):
    def test_writebyte(self):
        output = "testWrite"
        with TemporaryDirectory() as td:
            tempFileName = os.path.join(td, output)
            with codecs.open(tempFileName, 'w', 'utf-8') as testOutput:
                writer = bit.Writer(testOutput)
                writer.writebyte('a')
                writer.close()
            with codecs.open(tempFileName, 'r', 'utf-8') as testOutput:
                self.assertEqual(testOutput.read(), 'a' + chr(0b00000000))

    def test_writesinglebit(self):
        output = "testWrite"
        with TemporaryDirectory() as td:
            tempFileName = os.path.join(td, output)
            with codecs.open(tempFileName, 'w', 'utf-8') as testOutput:
                writer = bit.Writer(testOutput)
                writer.write(1)
                writer.close()
            with codecs.open(tempFileName, 'r', 'utf-8') as testOutput:
                r = testOutput.read()
                self.assertEqual(r, chr(0b10000000) + chr(0b00000111))

    def test_readbyte(self):
        output = "testRead"
        with TemporaryDirectory() as td:
            tempFileName = os.path.join(td, output)
            with codecs.open(tempFileName, 'w', 'utf-8') as testOutput:
                testOutput.write('é' + chr(0b00000000))
            with codecs.open(tempFileName, 'r', 'utf-8') as testOutput:
                reader = bit.Reader(testOutput)
                r = reader.readbyte()
                self.assertEqual(chr(r), 'é')

    def test_readbits(self):
        output = "testRead"
        with TemporaryDirectory() as td:
            tempFileName = os.path.join(td, output)
            with codecs.open(tempFileName, 'w', 'utf-8') as testOutput:
                testOutput.write(chr(0b11000000) + chr(0b00000101))
            with codecs.open(tempFileName, 'r', 'utf-8') as testOutput:
                s = getFileBinary(testOutput)
                self.assertEqual(s, "110")

class TestHuffmanMethods(TestCase):
    def test_writeNode(self):
        output = "testNode"
        with TemporaryDirectory() as td:
            tempFileName = os.path.join(td, output)
            with codecs.open(tempFileName, 'w', 'utf-8') as testOutput:
                writer = bit.Writer(testOutput)
                huffman.writeNode(testTree, writer)
                writer.close()
            with codecs.open(tempFileName, 'r', 'utf-8') as testOutput:
                s = getFileBinary(testOutput)
                self.assertEqual(s, testTreeBinary)

    def test_createDict(self):
        dict = {}
        huffman.createDict(testTree, dict)
        self.assertEqual(dict, testCodeDict)

    def test_writeCodified(self):
        output = "testEncoded"
        with TemporaryDirectory() as td:
            tempFileName = os.path.join(td, 'testFile')
            with open(tempFileName, 'w') as testFile:
                 testFile.write(testString)
            with open(tempFileName, 'r') as testFile:
                tempFileName = os.path.join(td, output)
                with codecs.open(tempFileName, 'w', 'utf-8') as testOutput:
                    writer = bit.Writer(testOutput)
                    huffman.writeCodified(testFile, testCodeDict, writer)
            with codecs.open(tempFileName, 'r', 'utf-8') as testOutput:
                s = getFileBinary(testOutput)
                self.assertEqual(s, testEncoded)


    def test_readTree(self):
        output = "testNode"
        with TemporaryDirectory() as td:
            tempFileName = os.path.join(td, output)
            with codecs.open(tempFileName, 'w', 'utf-8') as testOutput:
                writer = bit.Writer(testOutput)
                for b in testTreeBinary:
                    writer.write(int(b))
                writer.close()
            with codecs.open(tempFileName, 'r', 'utf-8') as testOutput:
                reader = bit.Reader(testOutput)
                t = huffman.readTree(reader)
                self.assertEqual(str(t), str(testTree))


    def test_decodeFile(self):
        output = "testDecoded"
        input_ = "testEncoded"
        with TemporaryDirectory() as td:
            outputName = os.path.join(td, output)
            tempFileName = os.path.join(td, input_)
            with codecs.open(tempFileName, 'w', 'utf-8') as testInput:
                writer = bit.Writer(testInput)
                for b in testEncoded:
                    writer.write(int(b))
                writer.close()
            with codecs.open(tempFileName, 'r', 'utf-8') as testInput:
                reader = bit.Reader(testInput)
                huffman.decodeFile(reader, outputName, testTree)
            with codecs.open(outputName, 'r', 'utf-8') as testDecoded:
                r = testDecoded.read()
                self.assertEqual(r, testString)


    def test_compress_decompress(self):
        compressedOutput = 'testFile.ch'
        decompressedOutput = 'testFile.txt'
        with TemporaryDirectory() as td:
            tempFileName = os.path.join(td, 'testFile')
            with open(tempFileName, 'w') as testFile:
                testFile.write(testString)
            with open(tempFileName, 'r') as testFile:
                huffman.Compress(testFile, compressedOutput)
            with codecs.open(compressedOutput, 'r', 'utf-8') as co:
                huffman.Decompress(co, decompressedOutput)
            with codecs.open(decompressedOutput, 'r', 'utf-8') as do:
                self.assertEqual(do.read(), testString)


if __name__ == '__main__':
    unittest.main()
