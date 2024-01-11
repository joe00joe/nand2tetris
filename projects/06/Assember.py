import Parse
import Code
import sys
import SymbolTable


def firstPass(srcFilePath):
    with open(srcFilePath, 'r') as fobj:
         pc = 0
         while True:
             line = fobj.readline()
             if not line:
                 return
             line = line.strip()
             if line == "" or line.startswith("//"):
                 continue
             elif line.startswith("("):     #L_COMMAND
                 symbol = line.replace('(', '').replace(')', '')
                 if SymbolTable.contains(symbol) == False:
                     SymbolTable.addEntry(symbol, pc )
             else:                          #A_COMMAND or C_COMMAND
                 pc = pc + 1
                     
        


def secondPass(srcFilePath, dstFilePath):
    with open(dstFilePath, 'w') as dstfobj:
        with open(srcFilePath, 'r') as srcfobj:
            command = None
            varCnt = 0
            while True:
                command = Parse.Advance(srcfobj)
                if not command:
                    return
                Type  = Parse.commandType(command)
                if Type == "A_COMMAND":
                     symbol =  Parse.symbol(command)
                     if symbol.isdigit():
                         digit = encode(symbol)
                         dstfobj.write(digit + "\n")
                     else:
                         address = -1
                         if SymbolTable.contains(symbol):
                             address = SymbolTable.getAddress(symbol)
                         else:
                             address = 16 + varCnt
                             SymbolTable.addEntry(symbol, address)
                             varCnt = varCnt + 1
                         dstfobj.write(encode(str(address)) + '\n')
                             
                if Type == "C_COMMAND":
                    dstToken, compToken, jumpToken = \
                        Parse.dest(command), Parse.comp(command), Parse.jump(command)
                    dstField, compField, jumpField = \
                        Code.dest(dstToken), Code.comp(compToken), Code.jump(jumpToken)
                    dstfobj.write("111" + compField + dstField + jumpField + "\n")
                if Type == "L_COMMAND":
                    pass

                    
        


def encode(decimalStr):
    binStr = bin(int(decimalStr, 10))[2:]
    binStr = binStr.zfill(16)
    return binStr


def main(src, dst):
    firstPass(src)
    secondPass(src, dst)
    print("parse done!")
    


if __name__ == '__main__':
     src = sys.argv[1]
     dst = sys.argv[2]
     #src = ".\\max\\Max.asm"
     #dst = ".\\max\\Max.hack"
     main(src, dst)
    
    

    