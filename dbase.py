'''
Created on Aug 21, 2014

@author: Rasel
'''

#dataType
class SliceDB ():
    INT = "int"
    STRING = "str"
    DOUBLE = "float"

#slicefield 
class SliceField():
    element = ""
    category = ""
    def __init__(self,elem = None, cat=None):
        self.element = elem
        self.category = cat

class SliceOP():
    EQ = "equal"
    GREATER = ">"
    LESS = "<"
    
    
#does everything        
class SliceEnv():
    nameDB = ""
    scheme = []
    index = ""
    row = 0
    column = 0
    records = []
    
    def __init__(self,name=None, elements = [], index = None):
        self.nameDB = name
        self.scheme = elements
        self.index = index
    
    def setDb(self,name):
        self.nameDB = name
        
    def setElem(self,elem):
        self.scheme = elem
    
    def setIndex(self,indi):
        self.index = indi
    
    def getIndex(self):
        return self.index
    
    def setRecord(self,record):
        self.records.append([])
        for x in range(0, self.getSchemaLength()):
            temp = record[x].rstrip().lstrip()
            self.records[len(self.records)-1].append(temp) 
    
    def getSchemaLength(self):
        return len(self.scheme)
    
    def getScheme(self):
        return self.scheme
    
    def clearDB(self):
        self.records.clear()
        
    def getRecordLength(self):
        return len(self.records)
    
    def createDB (self):
        file = open(self.nameDB+'.scheme','w')
        sch = ""
        for l in self.scheme:
            sch +=(l.element +" " + l.category+"|")
        sch += self.index
        file.write(sch)
        file.close()
        file2 = open(self.nameDB+'.slc','w')
        file2.close()
 
 #adds a record into the database   
    def addRecord(self):
        string = []
        flag = 0
        for x in range(0, self.getSchemaLength()):
            flag = 0
            print("Enter", self.getScheme()[x].element,"of type",self.getScheme()[x].category)
            temp = input().lstrip().rstrip()
            if (self.checkInput(temp, self.getScheme()[x].category)):
                string.append(temp)
                flag = 1
            else:
                break
        if flag == 1:
            self.setRecord(string)
        else:
            return
  
  #checks input type
    def checkInput(self,value,category):
        if value == "":
            return True
        if category == "int":
            try:
                val = int(value)
                return True
            except ValueError:
                print("input is not int!")
        elif category == "float":
            try:
                val = float(value)
                return True
            except ValueError:
                print("input is not an double!")
        elif category == "str":
            try:
                val = str(value)
                return True
            except ValueError:
                print("input is not a string!")  
        else:
            return False
  
  #gets the position of the value  
    def getNumber(self,elem):
        for x in range(0,self.getSchemaLength()):
            if (elem == self.getScheme()[x].element):
                return x
    
    #deletes a record
    def deleteRecord(self,num,value):
        flag =0
        print(num , " ", value)
        for x in range(0,len(self.records)):
            if(self.records[x][num] == value):
                self.records.pop(x)
                flag = 1
                break    
        if flag != 1:
            print("record Not found")

#bulkLoad
    def bulkLoad(self,fileName):
        self.clearDB()
        file2 = open(fileName,'r')
        for f in iter(file2.readline,''):   #reads record
            temp = f.split('|')
            self.setRecord(temp)
        file2.close()                     
#reads schema and records into list   
    def openDb (self,dbName):
        sliceElement = []
        file = open(dbName+'.scheme','r') #opens file
        str = file.readline()
        indi = str.rsplit('|', 1)[-1] #gets index
        str= str.rsplit('|', 1)[0] #removes index
        schemaList = str.split('|')
        count = len(schemaList)
        for l in schemaList:
            wordSplit = l.split()
            sliceElement.append(SliceField(wordSplit[0],wordSplit[1]))
        self.setDb(dbName)
        self.setElem(sliceElement)
        self.setIndex(indi)
        file.close()
        file2 = open(dbName+'.slc','r')
        for f in iter(file2.readline,''):   #reads record
            temp = f.split('|')
            self.setRecord(temp)
        file2.close()
 
    def closeDB(self):
        file = open(self.nameDB+'.slc','w')
        for x in range(0,self.getRecordLength()):
            string = ""
            for y in range (0,self.getSchemaLength()):
                string += self.records[x][y] +'|'
            string = string.rsplit('|', 1)[0]
            file.write(string+"\n")
        self.records.clear()
        file.close()
    
    def appendElem(self,x,y,value):
        self.records[x].pop(y)
        self.records[x].insert(y,value)
    
    def append(self):
        val = input("Enter "+self.getIndex()+":")
        if(self.getIndex() != ''):
            flag = 0
            position = self.getNumber(self.getIndex())
            for x in range(0,self.getRecordLength()):
                if val == self.records[x][position]:
                    pos = x
                    flag =1
                    break
            if flag ==1:
                for y in range(0,self.getSchemaLength()):
                    tou = input("previous value of "+self.getScheme()[y].element+" of type "+ self.getScheme()[y].category+" is "+self.records[pos][y]+"\ninsert new value:")
                    if (tou != ''):
                        if self.checkInput(tou,self.getScheme()[y].category):
                            self.appendElem(pos,y,tou)
                        else:
                            break 
            else:
                print("record not found")
                
        else:
            print("NO index")
        
    def queary(self,litpos,Op,value):
        tempList = []
        if (Op == 'greater'):
            for x in range(0,self.getRecordLength()):
                if int(self.records[x][litpos]) > int(value) :
                    tempList.append(self.records[x])
        elif (Op == 'less'):
            for x in range(0,self.getRecordLength()):
                if int(self.records[x][litpos]) < int(value) :
                    self.append(self.records[x])
        elif (Op == 'equal'):
            for x in range(0,self.getRecordLength()):
                if self.records[x][litpos] == value :
                    tempList.append(self.records[x])    
        return tempList    
   
    def displaySchema (self):
        print(self.nameDB)
        for l in self.scheme:
            print(l.element , l.category,end=' ')
        print(" ")
        print(self.index)
        print(self.getRecordLength())
        print(self.records)