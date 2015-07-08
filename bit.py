"""
Aumentado de:
http://rosettacode.org/wiki/Bitwise_IO#Python
"""

class Reader:
    def __init__(self, f):
        self.input = f
        self.accumulator = 0
        self.bcount = 0
        self.read = 0

    def read(self):
        if self.bcount == 0 :
            a = self.input.read(1)
            if ( len(a) > 0 ):
                self.accumulator = ord(a)
            self.bcount = 8
            self.read = len(a)
        rv = ( self.accumulator & ( 1 << (self.bcount-1) ) ) >> (self.bcount-1)
        self.bcount -= 1
        return rv

    def readbits(self, n):
        v = 0
        while n > 0:
            v = (v << 1) | self.readbit()
            n -= 1
        return v

    def readbyte(self, n):
        self.readbits(8)

class Writer:
    def __init__(self, f):
        self.accumulator = 0
        self.bcount = 0
        self.out = f

    def __del__(self):
        self.flush()

    def write(self, bit):
        if self.bcount == 8 :
            self.flush()
        if bit > 0:
            self.accumulator |= (1 << (7-self.bcount))
        self.bcount += 1

    def writebits(self, bits, n):
        while n > 0:
            self.write( bits & (1 << (n-1)) )
            n -= 1

    def writebyte(self, byte):
        self.writebits(byte, 8)

    # Para sabermos o lixo no fim do arquivo
    def close(self):
    	if self.bcount > 0:
    		bcount = 8 - bcount
    		for i in range(bcount):
    			self.write('0')
    		self.writebyte(bcount)

    def flush(self):
        self.out.write(chr(self.accumulator))
        self.accumulator = 0
        self.bcount = 0
