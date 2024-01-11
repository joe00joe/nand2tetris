


compMap = { '0':'0101010',  '1':'0111111',  '-1':'0111010', 'D':'0001100', 
                    'A':'0110000',  '!D':'0001101', '!A':'0110001', '-D':'0001111', 
                    '-A':'0110011', 'D+1':'0011111','A+1':'0110111','D-1':'0001110', 
                    'A-1':'0110010','D+A':'0000010','D-A':'0010011','A-D':'0000111', 
                    'D&A':'0000000','D|A':'0010101',
                    '':'xxxxxxx',   '':'xxxxxxx',   '':'xxxxxxx',   '':'xxxxxxx', 
                    'M':'1110000',  '':'xxxxxxx',   '!M':'1110001', '':'xxxxxxx', 
                    '-M':'1110011', '':'xxxxxxx',   'M+1':'1110111','':'xxxxxxx', 
                    'M-1':'1110010','D+M':'1000010','D-M':'1010011','M-D':'1000111', 
                    'D&M':'1000000', 'D|M':'1010101' }


dstTokens = ['', 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']


jmpTokens = ['', 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']


def comp(compToken):
    return compMap[compToken]
    

def dest(destToken):
    return _bits(dstTokens.index(destToken)).zfill(3)


def jump(jumpToken):
   return _bits(jmpTokens.index(jumpToken)).zfill(3)


def _bits( n):
        return bin(int(n))[2:]

