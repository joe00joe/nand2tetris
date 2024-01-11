class Node:
     def __init__(self, type, name, next) -> None:
         self.type = type
         self.name = name 
         self.table = {}
         self.nextScope = next
         self.kindCnt = {}



class SymbolTable:


    def __init__(self, type, name) -> None:
        self.className = name
        self.head = Node(type, name, None)
        
        
    def startSubroutine(self,type, name):
         if self.head.nextScope :
              self.head = self.head.nextScope
         newNode = Node(type, name, self.head)
         self.head = newNode
        
        
    def define(self, name, type, kind):
        #print(kind, kind in self.head.kindCnt.keys())
        if kind in self.head.kindCnt.keys():
           self.head.kindCnt[kind] += 1
        else:
           self.head.kindCnt[kind] = 1
        
        self.head.table[name] = {"name": name, 
                            "type": type, 
                            "kind": kind, 
                            "index": self.head.kindCnt[kind] - 1}

    
    def varCount(self, kind):
        curTable  = self.head
        while curTable:
            if  kind in curTable.kindCnt.keys():
                return curTable.kindCnt[kind] 
            curTable = curTable.nextScope
        return 0
    
    def kindOf(self, name):
        curTable  = self.head
        while curTable:
            if  name  in curTable.table.keys():
                return curTable.table[name]["kind"]
            curTable = curTable.nextScope
        return "None"
    
    def typeof(self, name):
        curTable  = self.head
        while curTable:
            if name  in curTable.table.keys():
                return curTable.table[name]["type"]
            curTable = curTable.nextScope
        return "None"
    
    def indexOf(self, name):
        idx = -1
        curTable  = self.head
        while curTable:
            if name in curTable.table.keys():
                idx =  curTable.table[name]["index"]
                break
            curTable = curTable.nextScope
        if self.kindOf(name) == "argument"  and  self.head.type == "method":
            idx += 1
        return idx
    






        






