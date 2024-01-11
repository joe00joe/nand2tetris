def advance(fobj):
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
               return command.strip()


def commandType(command) -> str:
    ariths = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
    if command in ariths:
        return "C_ARITHMETIC"
    if command.startswith("push"):
        return "C_PUSH"
    if command.startswith("pop"):
        return "C_POP"



def arg1(command, type) -> str:
    if type == "C_RETURN":
        return ""
    if type == "C_ARITHMETIC":
        return command
    else:
        #print("Command: ", command)
        parts = command.split(" ")
        return parts[1].strip()


def arg2(command, type) -> str:
    if type in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
        parts = command.split(" ")
        return parts[2].strip()
    else:
        return ""



