 

def Advance(fobj):
   while True:
       line = fobj.readline()
       if not line:
           return None
       else:
           line=line.strip()
           if line.startswith("//") or line == "":
               continue
           else:
               command = line.split("//")[0]
               return command.replace(' ', '')


def commandType(command) -> str:
    if command.startswith("@"):
        return "A_COMMAND"
    elif command.startswith("("):
        return "L_COMMAND"
    else:
        return "C_COMMAND"
    

def symbol(command) -> str:
    return command[1:]   # delete '@'

def comp(command) -> str:
    first = command.split(";")[0]
    parts = first.split("=")
    if len(parts) < 2:
        return parts[0]
    else:
        return parts[1]

def dest(command) -> str:
    parts = command.split("=")
    if len(parts) < 2 :
        return ""
    else:
        return  parts[0]

def jump(command) -> str:
    parts = command.split(";")
    if len(parts) < 2:
        return ""
    else:
        return parts[1]
    


