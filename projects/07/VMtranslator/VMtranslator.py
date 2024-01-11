import sys
import Parser
import CodeWriter


transProcess= {
    "C_ARITHMETIC": CodeWriter.writeArithmetic,
    "C_PUSH":CodeWriter.writePushPop,
    "C_POP":CodeWriter.writePushPop
}

def translate(srcFilePath, dstFilePath):
    with open(dstFilePath, 'w') as dstfobj:
        with open(srcFilePath, 'r') as srcfobj:
            command = None
            #CodeWriter.curFile = srcfobj.name.split(".")[0]
            #print(CodeWriter.curFile)
            while True:
                command = Parser.advance(srcfobj)
                if not command:
                    return
                Type  = Parser.commandType(command)
                arg1, arg2 = Parser.arg1(command, Type), Parser.arg2(command, Type)
                codes = transProcess[Type](Type, arg1, arg2, dstfobj)
                dstfobj.write(codes)
                '''
                if Type == "C_ARITHMETIC":
                    codes = CodeWriter.writeArithmetic(type, arg1)
                    dstfobj.write(codes)
                             
                if Type == "C_PUSH" or Type == "C_POP":
                   codes = CodeWriter.writePushPop(type, arg1, arg2)
                   dstfobj.write(codes)
                if Type == "C_LABEL":
                    pass
                if Type == "C_GOTO":
                    pass 
                if Type == "C_IF":
                    pass
                if Type == "C_FUNCTION":
                    pass
                if Type ==
                '''
                

                    
        


def encode(decimalStr):
    binStr = bin(int(decimalStr, 10))[2:]
    binStr = binStr.zfill(16)
    return binStr


def main(src, dst):
   
    translate(src, dst)
    print("parse done!")
    


if __name__ == '__main__':
     src = sys.argv[1]
     dst = sys.argv[2]
     #src = ".\\max\\Max.asm"
     #dst = ".\\max\\Max.hack"
     main(src, dst)
    