# Python nao oferece a facilidade das implementacoes de interfaces como o Go faz
# Assim, teremos que criar um arquivo de teste com classes para cada um
from unittest import TestCase, skip
import os, codecs
from tempfile import TemporaryDirectory

import frequency, gardener, huffman
from testconstants import testString, testMap, testTree
import bit

# Como nao temos o interessante formato de packacges que o Go determina
# Faremos cada teste em sua propria classe

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
            with codecs.open(tempFileName, 'r', 'utf-8') as testOutput:
                self.assertEqual(testOutput.read(), 'a')

    def test_writesinglebit(self):
        output = "testWrite"
        with TemporaryDirectory() as td:
            tempFileName = os.path.join(td, output)
            with codecs.open(tempFileName, 'w', 'utf-8') as testOutput:
                writer = bit.Writer(testOutput)
                writer.write(1)
            with codecs.open(tempFileName, 'r', 'utf-8') as testOutput:
                self.assertEqual(testOutput.read(), chr(0b10000000) + chr(0b00000111))


class TestHuffmanMethods(TestCase):
    def test_writeNode(self):
        output = "testNode"
        with TemporaryDirectory() as td:
            tempFileName = os.path.join(td, output)
            with codecs.open(tempFileName, 'w', 'utf-8') as testOutput:
                writer = bit.Writer(testOutput)
                huffman.writeNode(testTree, writer)
            with codecs.open(tempFileName, 'r', 'utf-8') as testOutput:
                reader = bit.Reader(testOutput)
                s = ''
                while True:
                    r = reader.read()
                    if r == '':
                        break
                    # print(str(r))




    @skip
    def test_compress_decompress(self):
        compressedOutput = 'testFile.ch'
        decompressedOutput = 'testFile.txt'
        with TemporaryDirectory() as td:
            tempFileName = os.path.join(td, 'testFile')
            with open(tempFileName, 'w') as testFile:
                testFile.write(testString)
            with open(tempFileName, 'r') as testFile:
                huffman.Compress(testFile, compressedOutput)
                co = codecs.open(compressedOutput, 'r', 'utf-8')
                huffman.Decompress(co, decompressedOutput)
                co.close()


if __name__ == '__main__':
    unittest.main()
