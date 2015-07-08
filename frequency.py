def GetMap(file):
    # Dicionario que relaciona cada string com sua frequencia
    freqMap = {}
    # Em Go nao existe while, for {} é equivalente a while True:
    while True:
        # Em python ler arquivos só retorna uma variavel
        r = file.read(1)
        # Nao temos que lidar com um possivel erro
        # Se chegar ao fim do arquivo saimos do loop
        if r == '':
            break

        # Nao precisamos mudar o tipo de r por python possui tipos dinamicos
        # Go nao possui tipos dinamicos

        # Aumenta a frequencia do elemento com o valor da string
        # ou adiciona um novo key ao Dicionario
        ## O debug ainda nao é necessario pois nao encontramos o problema das runas
        # Nesse caso o python nao é tao bom quanto o Go
        freqMap[r] = 1 if r not in freqMap else freqMap[r] + 1

    return freqMap
