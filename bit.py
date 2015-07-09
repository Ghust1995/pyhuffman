"""
Aumentado de:
http://rosettacode.org/wiki/Bitwise_IO#Python
"""

class Reader():
    def __init__(self, f):
        self.input = f
        self.accumulator = 0
        self.bcount = 0
        self.r = 0
        self.totalRead = 0;
        fileBits = (len(f.read()) - 1)* 8
        # Vendo o ultimo byte para saber quanto sobrou
        f.seek(-1,2)
        # Ultimo byte possui o numero de bits que sobram
        ult = f.read(1)
        sob = ord(ult)
        self.MAX = fileBits - sob
        # Voltamos o ponteiro ao inicio do arquivo
        f.seek(0)


    def read(self):
        if self.totalRead >= self.MAX:
            # Se chegarmos ao fim dos bits
            return ''

        if self.bcount == 0 :
            a = self.input.read(1)
            if a == "":
                return a
            if ( len(a) > 0 ):
                self.accumulator = ord(a)
            self.bcount = 8
            self.r = len(a)
        rv = ( self.accumulator & ( 1 << (self.bcount-1) ) ) >> (self.bcount-1)
        self.bcount -= 1
        self.totalRead += 1
        return rv

    def readbits(self, n):
        v = 0
        while n > 0:
            v = (v << 1) | self.read()
            n -= 1
        return v

    def readbyte(self):
        return self.readbits(8)

class Writer():
    def __init__(self, f):
        self.accumulator = 0
        self.bcount = 0
        self.out = f

    def write(self, bit):
        # print('   -Written:' + ('1' if int(bit) > 0 else '0'))
        if int(bit) > 0:
            self.accumulator |= (1 << (7-self.bcount))
        self.bcount += 1
        if self.bcount == 8 :
            self.flush()

    def writebits(self, bits, n):
        while n > 0:
            self.write( ord(bits) & (1 << (n-1)) )
            n -= 1

    def writebyte(self, byte):
        # print('Start writing byte:' + str(byte))
        self.writebits(byte, 8)
        # print('End of writing byte:' + str(byte))

    # Para sabermos o lixo no fim do arquivo
    def close(self):
        remain = (8 - self.bcount) % 8
        # print('Bytes left: ' + str(remain))
        for i in range(remain):
            self.write('0')
        self.writebyte(chr(remain))


    def flush(self):
        # print("Flushed: " + chr(self.accumulator))
        self.out.write(chr(self.accumulator))
        self.accumulator = 0
        self.bcount = 0
