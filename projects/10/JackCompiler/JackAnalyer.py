import sys
import JackTokenizer
import ComplieEngine







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
            print("tokens: ", tokens)
            print("the len of tokens: ", len(tokens[0]))
        else:
            print("token list  is Empty!")
            return
    with open (dstFile, 'w') as wfile:
        wfile.write("<class>" + "\n")
        ComplieEngine.compileClass(wfile, tokens, " ")
        wfile.write("</class>" + "\n")
        
           
            
   
   
             









def deleteNote(srcFile, copyFile):
     with open(copyFile, 'w') as cfile:
        with open(srcFile, 'r') as sfile:
             line = sfile.readline()
             while line:
                line = line.strip()
                if line == "\n" or line.startswith("//"):
                    line = sfile.readline()
                elif line.startswith("/*"):
                    while line.endswith("*/") == False:
                        line = sfile.readline()
                    if line:
                        line = sfile.readline()
                else:
                    line  = line.split("//")[0]
                    cfile.write(line + "\n")
                    line = sfile.readline()
        cfile.flush()            
                 
                
            
              

def main(src, dst):
    #tokenizer(src,dst)
    parse(src, dst)
    print("done!")



if __name__ == "__main__":
    #src , dst = sys.argv[1], sys.argv[2]
    src= "..\\Square\\SquareGameT.xml"
    dst = "..\\Square\\SquareGameT.xml.xml"
    
    main(src, dst)
    