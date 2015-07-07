import unittest

import frequency

# Como nao temos o interessante formato de packacges que o Go determina
# Faremos cada teste em sua propria classe



testString = "abbcccddddé"

class TestFrequencyMethods(unittest.TestCase):
     def test_frequency(self):
         # Python nao oferece a facilidade das implementacoes de interfaces como o Go faz
         # Assim, teremos que criar um arquivo de teste

         # Boas praticas de python
         with open('testFile', 'w') as testFile:
             testFile.write(testString)

         with open('testFile', 'r') as testFile:
             self.fail(testFile.read())


if __name__ == '__main__':
    unittest.main
