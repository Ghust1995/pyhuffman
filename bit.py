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

    def read(self):
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
        return rv

    def readbits(self, n):
        v = 0
        while n > 0:
            v = (v << 1) | self.read()
            n -= 1
        return v

    def readbyte(self):
        self.readbits(8)

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
    	if self.bcount > 0:
    		self.bcount = 8 - self.bcount
    		for i in range(self.bcount):
    			self.write('0')
    		self.writebyte(chr(self.bcount))

    def flush(self):
        # print("Flushed: " + chr(self.accumulator))
        self.out.write(chr(self.accumulator))
        self.accumulator = 0
        self.bcount = 0
