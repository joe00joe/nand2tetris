import sys
import JackTokenizer
import ComplieEngine
import os






def tokenizer(srcFile, dstFile):
   copyFile = "copyfile"
   deleteNote(srcFile, copyFile)
   with open(dstFile, 'w') as wfile:
        with open(copyFile, 'rb') as rfile:
            wfile.write("<tokens>\n")
            while True:
                token  = JackTokenizer.advance(rfile)
                if token == "":
                   break
                type  = JackTokenizer.tokenType(token)
                if type == "SYMBOL":
                    token = JackTokenizer.symbol(token)
                    wfile.write("<symbol> " + token + " </symbol>" + "\n")
                elif type == "KEYWORD":
                    token = JackTokenizer.keyword(token)
                    wfile.write("<keyword> " + token + " </keyword>" + "\n")
                elif type == "INT_CONST":
                    token = JackTokenizer.intVal(token)
                    wfile.write("<integerConstant> " + token + " </integerConstant>" + "\n")
                elif type == "STRING_CONST":
                    token = JackTokenizer.stringVal(token)
                    wfile.write("<stringConstant> " + token + " </stringConstant>" + "\n")
                elif type == "IDENTIFER":
                    token = JackTokenizer.identifer(token)
                    wfile.write("<identifier> " + token + " </identifier>" + "\n")
            wfile.write("</tokens>\n")




def parse(tokenFile, dstFile):
    tokens = []
    with open(tokenFile, 'r') as rfile:
        
        lines = [line.rstrip('\n') for line in rfile]
        #lines = rfile.readlines()
        if len(lines) > 2 :
            lines  = lines[1:-1]
            tokens = [lines, 0]   # tokens = [lines, index]
            #print("tokens: ", tokens)
            #print("the len of tokens: ", len(tokens[0]))
        else:
            print("token list  is Empty!")
            return
    with open (dstFile, 'w') as wfile:
        engine = ComplieEngine.compile(wfile, tokens)
        engine.compileClass()
        
           
            
   
   
             









def deleteNote(srcFile, copyFile):
     with open(copyFile, 'w') as cfile:
        with open(srcFile, 'r') as sfile:
             line = sfile.readline()
             while line:
                line = line.strip()
                if line == "" or line.startswith("//"):
                    line = sfile.readline()
                elif line.startswith("/*"):
                    while line.endswith("*/") == False:
                        line = sfile.readline().strip()
                    line  = sfile.readline()
                else:
                    line  = line.split("//")[0]
                    cfile.write(line + "\n")
                    line = sfile.readline()
        cfile.flush()            
                 

def findJackFilesHelper(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.jack'):
                fullname = os.path.join(root, f)
                yield fullname
                

    
              

def main(src):
    #tokenizer(src,dst)
    if os.path.isdir(src):
        for file in findJackFilesHelper(src):
            print("//" + file +"\n")
            tokenFile = file + ".xml"
            tokenizer(file, tokenFile)
            vmFile = file + ".vm"
            parse(tokenFile, vmFile) 
    elif os.path.isfile(src):
           tokenFile = src + ".xml"
           tokenizer(src, tokenFile)
           vmFile = src + ".vm"
           parse(tokenFile, vmFile)
    
    
    print("done!")


if __name__ == "__main__":
    #src , dst = sys.argv[1], sys.argv[2]
    src= "..\\Pong\\"
    #dst = "..\\ConvertToBin\\Main.jack"  
    main(src)
    

