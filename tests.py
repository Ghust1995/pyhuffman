import unittest, os
from tempfile import TemporaryDirectory

import frequency, gardener
from testconstants import testString, testMap, testTree

# Como nao temos o interessante formato de packacges que o Go determina
# Faremos cada teste em sua propria classe



class TestFrequencyMethods(unittest.TestCase):
     def test_frequency(self):
         # Python nao oferece a facilidade das implementacoes de interfaces como o Go faz
         # Assim, teremos que criar um arquivo de teste

         # Boas praticas de python
         with TemporaryDirectory() as td:
             tempFileName = os.path.join(td, 'testFile')
             with open(tempFileName, 'w') as testFile:
                 testFile.write(testString)
             with open(tempFileName, 'r') as testFile:
                 m = frequency.GetMap(testFile)
                 self.assertEqual(m, testMap)


class TestGardenerMethods(unittest.TestCase):
    def test_harvest(self):
        self.assertEqual(str(gardener.Harvest(testMap)), str(testTree))

if __name__ == '__main__':
    unittest.main
