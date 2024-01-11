import sys
import Parser
import CodeWriter
import os 


transProcess= {
    "C_ARITHMETIC": CodeWriter.writeArithmetic,
    "C_PUSH":CodeWriter.writePushPop,
    "C_POP":CodeWriter.writePushPop,
    "C_LABEL":CodeWriter.writeLabel,
    "C_GOTO":CodeWriter.writeGoto,
    "C_IF":CodeWriter.writeIf,
    "C_FUNCTION":CodeWriter.writeFunction,
    "C_CALL":CodeWriter.writeCall,
    "C_RETURN":CodeWriter.writeReturn,
}

def translateVMFile(srcFilePath, dstfobj):
    #with open(dstFilePath, 'w') as dstfobj:
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
                codes = transProcess[Type](Type, arg1, arg2, srcfobj)
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

def findVMFilesHelper(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.vm'):
                fullname = os.path.join(root, f)
                yield fullname
                



def main(src, dst):
    with open(dst, 'w') as dstfobj:
        if os.path.isdir(src):
             initCode = CodeWriter.writeInit()
             dstfobj.write(initCode)
             for file in findVMFilesHelper(src):
                 dstfobj.write("//" + file +"\n")
                 translateVMFile(file, dstfobj)
        elif os.path.isfile(src):
            translateVMFile(src,dstfobj)
        else:
            print("Please input current file or dir!")
        
    print("parse done!")
    




if __name__ == '__main__':
     src = sys.argv[1]
     dst = sys.argv[2]
     #src = ".\\max\\Max.asm"
     #dst = ".\\max\\Max.hack"
     main(src, dst)
    