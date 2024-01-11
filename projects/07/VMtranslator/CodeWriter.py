import os

CODEFLAG1=0
CODEFLAG2=0
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
    segment, index, wfile = args[0], args[1], args[2]
    codes = None
    if segment == "constant":
        codes = ["@" + index, "D=A"]  + pushCodes()
    if segment in ["local", "argument", "this", "that"]:
        codes = pushPopSegment(cmdType, segment, index)
    if segment in ["temp", "pointer"]:
        codes = pushPopTmpPoint(cmdType,segment, index)
    if segment == "static":
        codes = pushPopStatic(wfile, cmdType, index)
    return '\n'.join(codes) + '\n'

    

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
    
    

def pushPopStatic(wfile, cmdType, index):
    codes = None
    curfile = os.path.basename(wfile.name).split(".")[0]
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












