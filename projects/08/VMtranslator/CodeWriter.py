import os

CODEFLAG1=0
CODEFLAG2=0
CODEFLAG3=0


#curFile = ""

def Arith(cmd):
    global CODEFLAG1, CODEFLAG2
    CODEFLAG1  = CODEFLAG1 + 1
    CODEFLAG2 = CODEFLAG2 + 1
    codes = [
        'D=D-A',
        '@RET_TRUE'+str(CODEFLAG1),
        'D;J' + cmd.upper(),
        'D=0',
        '@CONTINUE'+str(CODEFLAG2),
        '0;JMP',
        '(RET_TRUE'+str(CODEFLAG1)+')',
        'D=-1',
        '(CONTINUE'+str(CODEFLAG2)+')',
            
    ]


    return '\n'.join(codes)



compMap = {
    "add": "D=D+A", 
    "sub": "D=D-A",
    "neg": "D=-A", 
    "eq": Arith,
    "gt": Arith,
    "lt": Arith, 
    "and": "D=D&A",
    "or": "D=D|A", 
    "not": "D=!A"
}

def writeArithmetic(cmdType, *args) -> str:
     cmd = args[0]
     codes = None
     if cmd == "neg" or cmd == 'not':
         codes = popCodes() + D2M("R15") + compCodes(cmd) + M2D("R13") + pushCodes()
     else:
         codes = popCodes() + D2M("R15") + popCodes() + D2M("R14") + compCodes(cmd) + M2D("R13") + pushCodes()
     return '\n'.join(codes) + "\n"
    

def writePushPop(cmdType, *args) -> str:
    #print(args)
    segment, index, rfile = args[0], args[1], args[2]
    codes = None
    if segment == "constant":
        codes = ["@" + index, "D=A"]  + pushCodes()
    if segment in ["local", "argument", "this", "that"]:
        codes = pushPopSegment(cmdType, segment, index)
    if segment in ["temp", "pointer"]:
        codes = pushPopTmpPoint(cmdType,segment, index)
    if segment == "static":
        codes = pushPopStatic(rfile, cmdType, index)
    return '\n'.join(codes) + '\n'



def writeInit() :
    setSP = ["@256", "D=A", "@SP", "M=D" ]
    setSP = '\n'.join(setSP) + '\n'
    callSysInit = writeCall("C_CALL", "Sys.init", "0")
    deadLoop = ["(init$END)", "@init$END", "0;JMP" ]
    deadLoop = '\n'.join(deadLoop) + '\n'
    codes = setSP + callSysInit + deadLoop
    return codes


def writeLabel(cmdType, *args):
    label =getFileName(args[2]) + "$" + args[0]
    return "(" +  label  + ")" + "\n"


def writeGoto(cmdType, *args):
    label =getFileName(args[2]) + "$" + args[0]
    codes = drictAddress(label) + ["0;JMP"]
    return '\n'.join(codes) + '\n'
 

def writeIf(cmdType, *args):
    label = getFileName(args[2]) + "$" + args[0]
    codes = popCodes() + drictAddress(label) + ["D;JNE"]
    return '\n'.join(codes) + '\n'

def writeCall(cmdType, *args):
    functionName = args[0]
    nArgs = args[1]
    global CODEFLAG3
    CODEFLAG3 = CODEFLAG3 + 1
    returnAddress = "RETURN_" +functionName.upper() + "_" + str(CODEFLAG3)
    pushRetAddr  = ["@" + returnAddress, "D=A"] + pushCodes()
    pushLCL =  M2D("LCL")  + pushCodes()
    pushARG =  M2D("ARG")  + pushCodes() 
    pushTHIS =  M2D("THIS")  + pushCodes()
    pushTHAT =  M2D("THAT")  + pushCodes()
    setARG = M2D("SP") + ["@"+ str(nArgs), "D=D-A", "@5", "D=D-A"] + D2M("ARG")    #ARG = SP-n-5
    setLCL = M2D("SP") + D2M("LCL")   #LCL = SP
    gotoF = drictAddress(functionName)  + ["0;JMP"]
    setRetAddr = ["(" + returnAddress + ")"]
    
    codes = pushRetAddr + pushLCL + pushARG + pushTHIS + pushTHAT + setARG + setLCL + gotoF + setRetAddr
    return '\n'.join(codes) + '\n'



def writeFunction(cmdType, *args):
    #functionName = getFileName(args[2]) + "." + args[0]
    functionName = args[0]
    nLocals = args[1]
    codes = [ "(" + functionName + ")"]
    for  i in range(0, int(nLocals)):
        codes.append("D=0")
        codes = codes + pushCodes()
    return '\n'.join(codes) + '\n'


def writeReturn(cmdType, *args):
    savaFP =  M2D("LCL") + D2M("R14")                               #FRAME = LCL   
    savaRET = M2D(address=["R14", -5]) + D2M("R13")                 #RET = *(FRAME - 5)
    setRetValue = popCodes() + D2M(address=["ARG", 0])\
                  + M2D("ARG") + ["D=D+1"] + D2M("SP")             #*ARG = pop()  SP = ARG+1 
    setTHIS = M2D(["R14", -1]) + ["@THAT", "M=D"]                   #THAT = *(FRAME - 1)
    setTHAT = M2D(["R14", -2]) + ["@THIS", "M=D"]                   #THIS = *(FRAME - 2)
    setARG = M2D(["R14", -3]) + ["@ARG", "M=D"]                     #ARG = *(FRAME - 3)
    setLCL = M2D(["R14", -4]) + ["@LCL", "M=D"]                     #LCL = *(FRAME - 4)
    returnF = ["@R13", "A=M", "0;JMP"]                             #goto RET
    
    codes = savaFP + savaRET + setRetValue + setTHAT + setTHIS + setARG + setLCL + returnF
    return '\n'.join(codes) + '\n'

    

def getFileName(readfile):
    filename = os.path.basename(readfile.name).split(".")[0]
    return filename

     


def  pushPopSegment(cmdType, segment, index):
    if segment == "local":
        segment = "LCL"
    if segment == "argument":
        segment = "ARG"
    if segment == "this":
        segment = "THIS"
    if segment == "that":
        segment = "THAT"
    codes = None
    if cmdType == "C_PUSH":
        codes = M2D(address=[segment, index]) + pushCodes()
    elif cmdType == "C_POP":
        codes = popCodes() + D2M(address=[segment, index])
    return codes

def pushPopTmpPoint(cmdType, segment, index):
    if segment == "pointer":
        segment = 3
    if segment == "temp":
        segment = 5
    setAddr=["@" + str(segment)]
    for i in range (0,int(index)):
        setAddr.append("A=A+1")
    codes = None
    if cmdType == "C_PUSH":
        codes = setAddr + ["D=M"] + pushCodes()
    elif cmdType == "C_POP":
        codes = popCodes() + setAddr + ["M=D"]
    return codes
    
    

def pushPopStatic(rfile, cmdType, index):
    codes = None
    curfile = os.path.basename(rfile.name).split(".")[0]
    print("Code: ",curfile)
    if cmdType == "C_PUSH":
        codes = ["@"+str(curfile) + "." + str(index), "D=M"] + pushCodes()
    elif cmdType == "C_POP":
        codes = popCodes() + ["@"+str(curfile) + "." + str(index), "M=D"]
    return codes


def popCodes():
    return [
        "@SP",
        "M=M-1",
        "@SP",
        "A=M",
        "D=M"
    ]



def pushCodes():
    return [
        "@SP", 
        "A=M",
        "M=D",
        "@SP",
        "M=M+1"
    ]


def compCodes(comType):
    compResult = compMap[comType]
    if isinstance(compResult, str) == False:
        compResult = compMap[comType](comType)
    
    return  [
        "@R14",
        "D=M",
        "@R15",
        "A=M",
        compResult,
        "@R13",
         "M=D"
         
        ]

   


def drictAddress(address):
    return ["@" + str(address)]


def indrictAddress(base, offset=0):
    codes = ["@" + str(base), "A=M"]
    offset = int(offset)
    if offset < 0 :
       for i in range (0,int(-offset)):
          codes.append("A=A-1") 
    else:
       for i in range (0,int(offset)):
          codes.append("A=A+1")
   
    return codes   
    '''
    return [
        "@" + str(base),
        "D=A",
        "@" + str(offset), 
        "A=D+A"
    ]
    '''

def M2D(address):
    setAddressCode = None
    if(isinstance(address, list)):
       setAddressCode = indrictAddress(base=address[0], offset=address[1])
    else:
       setAddressCode = drictAddress(address)
    return setAddressCode  + ["D=M"]
    



def D2M(address):
    setAddressCode = None
    if(isinstance(address, list)):
       setAddressCode = indrictAddress(base=address[0], offset=address[1])
    else:
       setAddressCode = drictAddress(address)
    return setAddressCode  + ["M=D"]










