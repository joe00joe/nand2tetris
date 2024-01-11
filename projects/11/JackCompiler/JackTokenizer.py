STable=('{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~')
KWtable=('class','constructor','function','method','field','static','var','int','char','boolean',\
	'void','true','false','null','this','let','do','if','else','while','return')

'''
def hasMoreToken(rfile) -> bool:
    ch = rfile.read(1)
    while ch and str(ch) in " \t\n":
        ch = rfile.read(1)
    if not ch :
        return False
    else:
        rfile.seek(-1, 1)
        return True
'''



def advance (rfile) -> str:
   token = ""
   ch = readCh(rfile)
   while ch and ch in ' \t\n\r':
        ch = readCh(rfile)
   if not ch :
        return token
   
   if ch in STable:
       token = ch
   elif ch == '"':
       ch = readCh(rfile)
       while ch != '"':
           token  = token + ch
           ch = readCh(rfile)
       token = '"' + token + '"'
   elif ch.isdigit()  or ch.isalpha() or ch == '_':
        token, ch  = token + ch , readCh(rfile)
        while  ch not in STable and  ch not in ' \t\n\r':
            token = token + ch
            ch = readCh(rfile)
        if ch in STable:
            rfile.seek(-1, 1)
   else:
       pass
   return token



def readCh(rfile):
    ch = rfile.read(1)
    return  ch.decode('utf-8')
         
          

def tokenType(token) -> str:
    if token in STable:
        return "SYMBOL"
    elif token in KWtable:
        return "KEYWORD"
    elif token.isdigit():
        return "INT_CONST"
    elif token.startswith('"'):
        return "STRING_CONST"
    else:
        return "IDENTIFER"
       

def keyword(token) -> str:
    return token

def symbol(token) -> str:
    if token == "<":
        token = "&lt;"
    elif token == ">":
        token = "&gt;"
    elif token == "&":
        token = "&amp;"
    return token


def identifer(token) -> str:
    return token

def intVal(token) -> str:
    return token


def stringVal(token) -> str:
    #print(token)
    return token


