import SymbolTable
import VMwriter

class compile:
   
    ops = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'div', '&': 'and', '|': 'or', '>': 'gt', '<': 'lt', '=': 'eq'}
    naryOps = {'~': 'not', '-': 'neg'}
     
    def __init__(self, wfile, tokens) -> None:
        self.wfile = wfile
        self.tokens = tokens
        self.table = None
        self.Writer  = VMwriter.VMwriter(self.wfile)
        self.flag1 = 0
        self.flag2 = 0
    
    def readToken(self):
        print("idx: ", self.tokens[1])
        token = self.tokens[0][self.tokens[1]]
        token = self.extractToken(token)
        self.tokens[1] += 1
        print("token: ", token)
        
        return token

    def rollToken(self):
        #token = tokens[0][tokens[1]]
        self.tokens[1] -= 1
        #return token
    

    

    def compileClass(self):
        self.readToken()            #class
        clsname =self.readToken()  #classname
        self.readToken()            #{
        self.table = SymbolTable.SymbolTable("class", clsname)
        token = self.readToken()
        while "field" in token or "static" in token: 
            self.rollToken()   
            self.compileClassVarDec()
            token = self.readToken()
        while "constructor" in token or "function" in token or "method" in token:
            self.rollToken()  
            self.complieSubroutine(clsname)
            token = self.readToken() 

        #wfile.write(space + token + '\n')  #}


    def compileClassVarDec(self):
        kind = self.readToken()
        type = self.readToken()
        name = self.readToken()
        self.table.define(name, type, kind)
        token = self.readToken()
        while ";" not in token:
            if "," not in token:
               self.table.define(token, type, kind)
            #wfile.write(space + token + '\n')  
            token = self.readToken()
        #wfile.write(space +  token + '\n') 


    def complieSubroutine(self, clsname):
        functionType = self.readToken()   #fucnction
        self.readToken()   #returnType
        functionName = self.readToken()  #fuucntionName
        self.table.startSubroutine(functionType,functionName)
        nLocals = 0
        self.readToken()   #(
        token  = self.readToken()
        if ")" not in token:
            self.rollToken()
            nArgs = self.compileParameterList()
            token = self.readToken()
        #wfile.write(space + token + '\n')  #)
        
        self.readToken()   #{
        token = self.readToken()
        while "var" in token:
            self.rollToken()
            nLocals +=  self.compileVarDec()
            token = self.readToken()
        self.rollToken()

        if  "method" in functionType:
           self.Writer.writeFunction( clsname+ "." + functionName, nLocals)
           self.Writer.writePush("argument", 0)
           self.Writer.writePop("pointer",0)  
        elif "constructor" in functionType:
           self.Writer.writeFunction( clsname+ "." + functionName, nLocals) 
           fieldVarCnt = self.table.varCount("field")
           self.Writer.writePush("constant", fieldVarCnt)
           self.Writer.writeCall("Memory.alloc", 1)
           self.Writer.writePop("pointer", 0)
        else:
           self.Writer.writeFunction( clsname+ "." + functionName, nLocals)
        self.compileSubroutineBody()
        


    def compileParameterList(self):
        
        token  = self.readToken()
        ParaList = [] 
        while ")"  not in token:
            if "," not in token:
                ParaList.append(token)
            #wfile.write(space + token + '\n')  
            token = self.readToken()
        for i in range(0, len(ParaList), 2):
            type, name = ParaList[i], ParaList[i + 1]
            self.table.define(name, type, "argument")
        self.rollToken()
        return len(ParaList) / 2


    def compileSubroutineBody(self):
        '''
        self.readToken()   #{
        token = self.readToken()
        while "var" in token:
            self.rollToken()
            self.compileVarDec()
            token = self.readToken()
        self.rollToken()
        '''
        self.compileStatememts()
        self.readToken()   #}



    def compileVarDec(self):
        varNum = 1
        var  = self.readToken()
        type = self.readToken()
        name = self.readToken()
        self.table.define(name, type, var)
        
        token = self.readToken()
        while ";" not in token:
            if "," not in token:
               self.table.define(token, type, var)
               varNum += 1
            #wfile.write(space + token + '\n')  
            token = self.readToken()
        #wfile.write(space +  token + '\n') 
        return varNum

    def compileStatememts(self):
        token = self.readToken()
        while "}" not in token:
            self.rollToken()
            self.compileStatement()
            token = self.readToken()
        self.rollToken()
            


    def compileStatement(self):
        token = self.readToken()
        if "do" in token:
            self.rollToken()
            self.compileDo()
        elif "let" in token:
            self.rollToken()
            self.compileLet()
        elif "if" in token:
            self.rollToken()
            self.compileIf()
        elif "while" in token:
            self.rollToken()
            self.compileWhile()
        elif "return" in token:
            self.rollToken()
            self.compileReturn()




    def compileLet(self):
        self.readToken()  #let
        varName = self.readToken()  #varName
        kind = self.table.kindOf(varName)
        segment = self.toSegment(kind)
        idx = self.table.indexOf(varName)
        token = self.readToken()
        if "[" in token:
            #wfile.write(space + token + '\n')  #[
            #wfile.write(space + " <expression>"  + "\n")
            self.compileExpression()
            self.Writer.writePush(segment, idx)
            self.Writer.writeArithmetic("add")
            segment = "that"
            #wfile.write(space + " </expression>"  + "\n")
            self.readToken()  #]
            token = self.readToken()
        
        #wfile.write(space + token + '\n')  #=
        #wfile.write(space + " <expression>"  + "\n")
        self.compileExpression()
        #wfile.write(space + " </expression>"  + "\n")
        if segment == "that":
            self.Writer.writePop("temp", 0)
            self.Writer.writePop("pointer", 1) # set that pointer
            self.Writer.writePush("temp",0)
            self.Writer.writePop("that", 0)
        else:
            self.Writer.writePop(segment, idx)
        self.readToken()   #;
        
    

    def compileIf(self):
        label1 = "IF_LABEL_1_" + str(self.flag1)
        self.flag1 += 1
        label2 = "IF_LABEL_2_" + str(self.flag2)
        self.flag2 += 1

        self.readToken()  #if
        self.readToken()  #(
        self.compileExpression()
        self.Writer.writeArithmetic("not")                 #~cond
        self.Writer.writeIf(label1)                        #if-goto label1
        
        self.readToken()  #)
        self.readToken()  #{
        self.compileStatememts()                           #s1
        self.readToken()  #}
        self.Writer.writeGoto(label2)                      #goto label2
        self.Writer.writeLabel(label1)                     #labe1
        token = self.readToken()
        if "else" in token:
            #wfile.write(space + token + '\n')  #else
            self.readToken()   #{ 
            self.compileStatememts()                       #s2
            self.readToken()   #}
            token = self.readToken()
        self.Writer.writeLabel(label2)                     #label2
        self.rollToken()
        
        


    def compileWhile(self):
        label1 = "WHILE_LABEL_1_" + str(self.flag1)
        self.flag1 += 1
        label2 = "WHILE_LABEL_2_" + str(self.flag2)
        self.flag2 += 1 

        
        self.readToken()  #while
        self.readToken()  #(
        self.Writer.writeLabel(label1)
        self.compileExpression()
        self.Writer.writeArithmetic("not")                 #~cond
        self.Writer.writeIf(label2)                        #if-goto label2 
        
        self.readToken()   #)
        self.readToken()   #{
        self.compileStatememts()       #s1
        self.readToken()  #}
        self.Writer.writeGoto(label1)
        self.Writer.writeLabel(label2) 
        

    def compileDo(self):
        
        self.readToken() #do
        self.subroutineCall()
        self.Writer.writePop("temp", 0)
        self.readToken()  #;


    def subroutineCall(self):
        fullName = []
        token = self.readToken()
        isStaticFun = False
        while "(" not in token:
            if "." not in token:
                fullName.append(token) 
            token = self.readToken()
        #wfile.write(space + token + '\n')  #(
        if len(fullName) == 1:
            clsname = self.table.className
            fullName.insert(0, clsname)
            self.Writer.writePush("pointer", 0)
        elif len(fullName) == 2:
            if self.table.kindOf(fullName[0]) != "None":
                clsname = self.table.typeof(fullName[0])
                varName = fullName[0]
                fullName[0] = clsname 
                self.readValue(varName)
            else:
                isStaticFun = True
    
            
        nArgs = 0
        token  = self.readToken()
        if ")" not in token:
            self.rollToken()
            nArgs = self.compileExpressList()
            token  = self.readToken()
        if isStaticFun:
            self.Writer.writeCall('.'.join(fullName), nArgs)
        else:
            self.Writer.writeCall('.'.join(fullName), nArgs + 1)
        #wfile.write(space + token + '\n')  #）
    


    def compileReturn(self):
        self.readToken()  #return
        token = self.readToken()
        if ";" not in token:
            #wfile.write(space + " <expression>"  + "\n")
            self.rollToken()
            self.compileExpression()
            #wfile.write(space + " </expression>"  + "\n")
            token  = self.readToken()
        else:
            self.Writer.writePush("constant", 0)    
        # wfile.write(space + token + '\n')  #;
        self.Writer.writeReturn()

    def compileExpression(self):
        self.compileTerm()
        token  = self.readToken()
        while self.isOP(token):
            #wfile.write(space + token + "\n") #op
            self.compileTerm()
            self.writeOperator(token, False)
            token = self.readToken()
        self.rollToken()
        





    def compileTerm(self):
        #wfile.write(space + " <term>"  + "\n")
        #space = space + " "
        token = self.readToken()
        if self.isUnaryOP(token):
            #wfile.write(space + token  + "\n") #unarryOp
            self.compileTerm()
            self.writeOperator(token, True)
        elif  "("  in token:
            #wfile.write(space + token  + "\n") #(
            self.compileExpression()
            self.readToken() #)
        else:
            nextToken = self.readToken()
            if "[" in nextToken:
                #wfile.write(space + token  + "\n") #varName
                #wfile.write(space + nextToken  + "\n") #[
                self.compileExpression()
                self.readValue(token) #base
                self.Writer.writeArithmetic("add")    #base + i
                self.Writer.writePop("pointer", 1)
                self.Writer.writePush("that", 0)      #*(base + i)
                self.readToken() #]
            elif "(" in nextToken or "." in nextToken:
                self.rollToken()
                self.rollToken()
                self.subroutineCall()
            else:
                self.rollToken()
                #IntergerConstant or stringConstant or keyword or varName
                self.readValue(token)
                #wfile.write(space + token  + "\n")     
        #wfile.write(space + self.readToken() + '\n')  #varName
        #wfile.write(space + " </term>"  + "\n")
        
 




    def compileExpressList(self):
        expressNum = 1
        self.compileExpression()
        token = self.readToken()
        while "," in  token:
            #wfile.write(space + token + '\n')  #,
            self.compileExpression()
            expressNum += 1
            token = self.readToken()
        self.rollToken()
        return expressNum



    def isOP(self, token):
        #token =self.extractToken(token)
        for op in self.ops.keys():
            if op in token:
                return True
        return False

    def isUnaryOP(self, token):
        #token =self.extractToken(token)
        for op in self.naryOps.keys():
            if op in token:
                return True
        return False
    

    def  extractToken(self,line):
        token = line.split(">")[1].split("<")[0].strip()
        if token == "&gt;":
            token = ">"
        elif token == "&lt;":
            token = "<"
        elif token == "&amp;":
            token = "&"
        return token
        
    

    def writeOperator(self, op, isSingle):
        if op == '*':
            self.Writer.writeCall("Math.multiply", 2)
        elif op == '/':
            self.Writer.writeCall("Math.divide", 2)
        elif not isSingle:
            self.Writer.writeArithmetic(self.ops[op])
        elif isSingle:
            self.Writer.writeArithmetic(self.naryOps[op])

    def readValue(self, Identifer):
        if Identifer == "null" or Identifer  == "false":
           self.Writer.writePush("constant", 0)
        elif Identifer  == "true":
           self.Writer.writePush("constant", 1)
           self.Writer.writeArithmetic("neg")
        elif Identifer == "this":
           self.Writer.writePush("pointer", 0)
        elif Identifer.isdigit():
           self.Writer.writePush("constant", Identifer)
        elif Identifer.startswith('"'):
            Identifer = Identifer[1:-1]
            string_length=len(Identifer)
            self.Writer.writePush('constant',string_length)
            self.Writer.writeCall('String.new',1)
            for i in range(0,string_length):
                self.Writer.writePush('constant',ord(Identifer[i]))
                self.Writer.writeCall('String.appendChar',2)
        else:
            kind = self.table.kindOf(Identifer) 
            idx = self.table.indexOf(Identifer)
            if kind != "None":
                self.Writer.writePush(self.toSegment(kind), idx)
            else:
                print("identifer isn't exist")



    def writeValue(self, identifer):
            kind = self.table.kindOf(identifer) 
            idx = self.table.indexOf(identifer)
            if kind != "None":
                 self.Writer.writePop(self.toSegment(kind), idx)
            else:
                print("identifer isn't exist")

    
    
    def toSegment(self, kind):
          if kind == "argument":
                return "argument"
          elif kind == "var":
                return "local"
          elif kind == "static":
                return "static"
          elif kind == "field":
                return "this"
            
        




        
    


    


