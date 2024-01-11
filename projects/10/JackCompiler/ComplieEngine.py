ops = ['+', '-', '*', '/', '&', '|', '>', '<', '=']
unaryOps = ['~', '-']

def readToken(tokens):
    print("idx: ", tokens[1])
    token = tokens[0][tokens[1]]
    tokens[1] += 1
    print("token: ", token)
    
    return token

def rollToken(tokens):
    #token = tokens[0][tokens[1]]
    tokens[1] -= 1
    #return token


def compileClass(wfile, tokens, space):
    wfile.write(space + readToken(tokens) + '\n')  #class
    wfile.write(space + readToken(tokens) + '\n')  #classname
    wfile.write(space + readToken(tokens) + '\n')  #{
    token = readToken(tokens)
    while "field" in extractToken(token) or "static" in extractToken(token):
          wfile.write(space + "<classVarDec>"  + "\n")  
          rollToken(tokens)   
          compileClassVarDec(wfile, tokens, space + " ")
          wfile.write(space + "</classVarDec>"  + "\n")
          token = readToken(tokens)
    while "constructor" in extractToken(token) or "function" in extractToken(token) or "method" in extractToken(token):
          wfile.write(space + "<subroutineDec>"  + "\n")  
          rollToken(tokens)  
          complieSubroutine(wfile, tokens, space + " ")
          wfile.write(space + "</subroutineDec>"  + "\n")
          token = readToken(tokens) 

    wfile.write(space + token + '\n')  #}


def compileClassVarDec(wfile, tokens, space):
    wfile.write(space + readToken(tokens) + '\n')  #static or field
    wfile.write(space + readToken(tokens) + '\n')  #type
    wfile.write(space + readToken(tokens) + '\n')  #varName
    token = readToken(tokens)
    while ";" not in token:
        wfile.write(space + token + '\n')  
        token = readToken(tokens)
    wfile.write(space +  token + '\n') 


def complieSubroutine(wfile, tokens, space):
    wfile.write(space + readToken(tokens) + '\n')  #fucnction
    wfile.write(space + readToken(tokens) + '\n')  #returnType
    wfile.write(space + readToken(tokens) + '\n')  #fuucntionName
    wfile.write(space + readToken(tokens) + '\n')  #(
    wfile.write(space + "<parameterList>"  + "\n")
    token  = readToken(tokens)
    if ")" not in extractToken(token):
        rollToken(tokens)
        compileParameterList(wfile, tokens, space + " ")
        token = readToken(tokens)
    wfile.write(space + "</parameterList>"  + "\n")
    wfile.write(space + token + '\n')  #)
    
    wfile.write(space + " <subroutineBody>"  + "\n")
    compileSubroutineBody(wfile, tokens, space + " ")
    wfile.write(space + " </subroutineBody>"  + "\n")
 


def compileParameterList(wfile, tokens, space):
    token  = readToken(tokens)
    while ")"  not in extractToken(token):
        wfile.write(space + token + '\n')  
        token = readToken(tokens)
    rollToken(tokens)


def compileSubroutineBody(wfile, tokens, space):
    wfile.write(space + readToken(tokens) + '\n')  #{
    token = readToken(tokens)
    while "var" in extractToken(token):
         wfile.write(space + " <varDec>"  + "\n")
         rollToken(tokens)
         compileVarDec(wfile, tokens, space + " ")
         wfile.write(space + " </varDec>"  + "\n")
         token = readToken(tokens)
    wfile.write(space + " <statements>"  + "\n")
    rollToken(tokens)
    compileStatememts(wfile, tokens, space)
    wfile.write(space + " </statements>"  + "\n")
    wfile.write(space + readToken(tokens) + '\n')  #}



def compileVarDec(wfile, tokens, space):
    wfile.write(space + readToken(tokens) + '\n')  #var
    wfile.write(space + readToken(tokens) + '\n')  #type
    wfile.write(space + readToken(tokens) + '\n')  #varName
    token = readToken(tokens)
    while ";" not in extractToken(token):
        wfile.write(space + token + '\n')  
        token = readToken(tokens)
    wfile.write(space +  token + '\n') 

def compileStatememts(wfile, tokens, space):
    token = readToken(tokens)
    while "}" not in extractToken(token):
        rollToken(tokens)
        compileStatement(wfile, tokens, space + " ")
        token = readToken(tokens)
    rollToken(tokens)
        


def compileStatement(wfile, tokens, space):
    token = readToken(tokens)
    if "do" in extractToken(token):
        wfile.write(space + " <doStatement>"  + "\n")
        rollToken(tokens)
        compileDo(wfile, tokens, space + " ")
        wfile.write(space + " </doStatement>"  + "\n")
    elif "let" in extractToken(token):
        wfile.write(space + " <letStatement>"  + "\n")
        rollToken(tokens)
        compileLet(wfile, tokens, space + " ")
        wfile.write(space + " </letStatement>"  + "\n")
    elif "if" in extractToken(token):
        wfile.write(space + " <ifStatement>"  + "\n")
        rollToken(tokens)
        compileIf(wfile, tokens, space + " ")
        wfile.write(space + " </ifStatement>"  + "\n")
    elif "while" in extractToken(token):
        wfile.write(space + " <whileStatement>"  + "\n")
        rollToken(tokens)
        compileWhile(wfile, tokens, space + " ")
        wfile.write(space + " </whileStatement>"  + "\n")
    elif "return" in extractToken(token):
        wfile.write(space + " <returnStatement>"  + "\n")
        rollToken(tokens)
        compileReturn(wfile, tokens, space + " ")
        wfile.write(space + " </returnStatement>"  + "\n")




def compileLet(wfile, tokens, space):
    wfile.write(space + readToken(tokens) + '\n')  #let
    wfile.write(space + readToken(tokens) + '\n')  #varName
    token = readToken(tokens)
    if "[" in extractToken(token):
        wfile.write(space + token + '\n')  #[
        #wfile.write(space + " <expression>"  + "\n")
        compileExpression(wfile,tokens, space)
        #wfile.write(space + " </expression>"  + "\n")
        wfile.write(space + readToken(tokens) + '\n')  #]
        token = readToken(tokens)
    wfile.write(space + token + '\n')  #=
    #wfile.write(space + " <expression>"  + "\n")
    compileExpression(wfile,tokens, space)
    #wfile.write(space + " </expression>"  + "\n")
    wfile.write(space + readToken(tokens) + '\n')  #;
    
  

def compileIf(wfile, tokens, space):
    wfile.write(space + readToken(tokens) + '\n')  #if
    wfile.write(space + readToken(tokens) + '\n')  #(
    compileExpression(wfile, tokens, space)
    wfile.write(space + readToken(tokens) + '\n')  #)
    wfile.write(space + readToken(tokens) + '\n')  #{
    wfile.write(space + " <statements>"  + "\n")
    compileStatememts(wfile, tokens, space)
    wfile.write(space + " </statements>"  + "\n")
    wfile.write(space + readToken(tokens) + '\n')  #}
    token = readToken(tokens)
    if "else" in extractToken(token):
        wfile.write(space + token + '\n')  #else
        wfile.write(space + readToken(tokens) + '\n')  #{
        wfile.write(space + " <statements>"  + "\n")
        compileStatememts(wfile, tokens, space)
        wfile.write(space + " </statements>"  + "\n")
        wfile.write(space + readToken(tokens) + '\n')  #}
        token = readToken(tokens)
    rollToken(tokens)
    


def compileWhile(wfile, tokens, space):
    wfile.write(space + readToken(tokens) + '\n')  #while
    wfile.write(space + readToken(tokens) + '\n')  #(
    compileExpression(wfile, tokens, space + " ")
    wfile.write(space + readToken(tokens) + '\n')  #)
    wfile.write(space + readToken(tokens) + '\n')  #{
    wfile.write(space + " <statements>"  + "\n")
    compileStatememts(wfile, tokens, space)
    wfile.write(space + " </statements>"  + "\n")
    wfile.write(space + readToken(tokens) + '\n')  #}
    

def compileDo(wfile, tokens, space):
    
    wfile.write(space + readToken(tokens) + '\n')  #do
    subroutineCall(wfile, tokens, space)
    '''
    token = readToken(tokens)
    while "(" not in extractToken(token):
        wfile.write(space + token + '\n')  
        token = readToken(tokens)
    wfile.write(space + token + '\n')  #(
    wfile.write(space + " <expressionList>"  + "\n")
    token  = readToken(tokens)
    if ")" not in extractToken(token):
        rollToken(tokens)
        compileExpressList(wfile, tokens, space + " ")
        token  = readToken(tokens)
    wfile.write(space + " </expressionList>"  + "\n")
    wfile.write(space + token + '\n')  #）
    '''
    wfile.write(space + readToken(tokens) + '\n')  #;


def subroutineCall(wfile, tokens, space):
    token = readToken(tokens)
    while "(" not in extractToken(token):
        wfile.write(space + token + '\n')  
        token = readToken(tokens)
    wfile.write(space + token + '\n')  #(
    wfile.write(space + " <expressionList>"  + "\n")
    token  = readToken(tokens)
    if ")" not in extractToken(token):
        rollToken(tokens)
        compileExpressList(wfile, tokens, space + " ")
        token  = readToken(tokens)
    wfile.write(space + " </expressionList>"  + "\n")
    wfile.write(space + token + '\n')  #）
   


def compileReturn(wfile, tokens, space):
    wfile.write(space + readToken(tokens) + '\n')  #return
    token = readToken(tokens)
    if ";" not in extractToken(token):
        #wfile.write(space + " <expression>"  + "\n")
        rollToken(tokens)
        compileExpression(wfile,tokens, space)
        #wfile.write(space + " </expression>"  + "\n")
        token  = readToken(tokens)    
    wfile.write(space + token + '\n')  #;

def compileExpression(wfile, tokens, space):
    wfile.write(space + " <expression>"  + "\n")
    compileTerm(wfile, tokens, space + " ")
    token  = readToken(tokens)
    while isOP(token):
        wfile.write(space + token + "\n") #op
        compileTerm(wfile, tokens, space + " ")
        token = readToken(tokens)
    wfile.write(space + " </expression>"  + "\n")
    rollToken(tokens)
    




def compileTerm(wfile, tokens, space):
    wfile.write(space + " <term>"  + "\n")
    #space = space + " "
    token = readToken(tokens)
    if isUnaryOP(token):
         wfile.write(space + token  + "\n") #unarryOp
         compileTerm(wfile,tokens, space + " ")
    elif  "("  in extractToken(token):
         wfile.write(space + token  + "\n") #(
         compileExpression(wfile, tokens, space )
         wfile.write(space + readToken(tokens)  + "\n") #)
    else:
        nextToken = readToken(tokens)
        if "[" in extractToken(nextToken):
           wfile.write(space + token  + "\n") #varName
           wfile.write(space + nextToken  + "\n") #[
           compileExpression(wfile, tokens, space)
           wfile.write(space + readToken(tokens)  + "\n") #]
        elif "(" in extractToken(nextToken) or "." in extractToken(nextToken):
            rollToken(tokens)
            rollToken(tokens)
            subroutineCall(wfile, tokens, space)
        else:
            rollToken(tokens)
            #IntergerConstant or stringConstant or keyword or varName
            wfile.write(space + token  + "\n")     
    #wfile.write(space + readToken(tokens) + '\n')  #varName
    wfile.write(space + " </term>"  + "\n")
    





def compileExpressList(wfile, tokens, space):
    compileExpression(wfile, tokens, space)
    token = readToken(tokens)
    while "," in  extractToken(token):
        wfile.write(space + token + '\n')  #,
        compileExpression(wfile, tokens, space)
        token = readToken(tokens)
    rollToken(tokens)



def isOP(token):
    token =extractToken(token)
    for op in ops:
        if op in token:
            return True
    return False

def isUnaryOP(token):
    token =extractToken(token)
    for op in unaryOps:
        if op in token:
            return True
    return False


     
def  extractToken(line):
    token = line.split(">")[1].split("<")[0]
    return token


    


