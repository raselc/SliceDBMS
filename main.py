import dbase
import os
import subprocess
'''
Created on Aug 13, 2014

@author: Rasel
'''

def createDatabase():
    env = dbase.SliceEnv()
    sliceElement = []
    tableName = input("Enter Table Name: ")
    count = int(input("Enter scheme count: "))
    for x in range(0,count):
        elem = input("enter element:")
        temp = elem.split('|')
        if (len(temp)) >1 :
            if temp[1] == "INT":
                sliceElement.append(dbase.SliceField(temp[0],dbase.SliceDB.INT))
            elif temp[1] == "STRING":
                sliceElement.append(dbase.SliceField(temp[0],dbase.SliceDB.STRING))
            elif temp[1] == "DOUBLE":
                sliceElement.append(dbase.SliceField(temp[0],dbase.SliceDB.DOUBLE))
            else:
                print("Wrong Input")
                return
        else:
            print("Wrong Input")
            return    
    index = input("Enter Index:") 
    for x in range(0,len(sliceElement)):
        if (sliceElement[x].element == index):
            flag = 1
            break
        else:
            flag = 0
    if (flag == 1  or index ==''):
        env.__init__(tableName,sliceElement,index) 
        env.createDB()
        print ("DATABASE CREATED")
    else :
        print("Index Doesn't match")
    #env.displaySchema() 
    env.closeDB()
    return

def updateRecord():
    env =dbase.SliceEnv()
    dbname = input ("enter database Name :")
    env.openDb(dbname)
    env.append()
    #env.displaySchema()
    env.closeDB()
    return

def addRecord():
    env = dbase.SliceEnv()
    dbname = input ("enter database Name :")
    env.openDb(dbname)
    env.addRecord()
    #env.displaySchema()
    env.closeDB()
    return

def deleteRecord():
    env = dbase.SliceEnv()
    dbname = input ("enter database Name :")
    env.openDb(dbname)
    if (env.getIndex() != ''):
        value = input ("enter "+ env.getIndex()+":")
        number = env.getNumber(env.getIndex())
        env.deleteRecord(number,value)
        env.displaySchema()
        env.closeDB()
    else:
        print("no index")
      
    return

def bulkLoad():
    env = dbase.SliceEnv()
    dbName = input ("enter database Name :")
    env.openDb(dbName)
    fileName = input ("enter File Name: ")
    env.bulkLoad(fileName)
    #env.displaySchema()
    env.closeDB()
    
    return

def joinRecord(list1,list2,pos1,pos2):
    result = []
    for x in range (0,len(list1)-1):
        for y in range (0,len(list2)):
            if list1[x][pos1] == list2[y][pos2]:
                list2[y].pop(pos2)
                result.append(list1[x]+list2[y])
    return result


def displayJoin():
    schema = []
    schema2 = []
    newSchema = []
    join = []
    posList = []
    env = dbase.SliceEnv()
    dbName1 = input ("enter database Name :")
    env2 = dbase.SliceEnv()
    dbName2 = input ("enter database Name :")
    env.openDb(dbName1)
    env2.openDb(dbName2)
    column = input("Enter column name for joining")
    pos1 = env.getNumber(column)
    pos2 = env2.getNumber(column)
    for x in range (0,env.getSchemaLength()):
        schema.append(env.getScheme()[x].element)
    for x in range(0,env2.getSchemaLength()):
        schema2.append(env2.getScheme()[x].element)
    schema2.pop(pos2)
    newSchema = schema + schema2
    #print(len(newSchema))
    join = joinRecord(env.records,env2.records,pos1,pos2)
    print("How many columns to join (max",len(newSchema),")")
    num = input()
    print("please Select from:",newSchema)
    for x in range(0,int(num)):
        temp = input("enter column name: ")
        flag = 0
        for y in range(0,len(newSchema)):
            if temp == newSchema[y]:
                posList.append(y)
                flag =1
        if flag == 0:
            print("Column doesn't exit")
            env.closeDB()
            return
    #print(posList)
    for x in range(0,len(join)-1):
        for y in range(0,len(posList)):
            print(join[x][int(posList[y])],end =' ')
        print("")
    env.closeDB()
    return

def runQuery():
    env = dbase.SliceEnv()
    dbName = input ("enter database Name :")
    env.openDb(dbName)
    column = []
    pos = []
    result = []
    for x in range(0,int(input("enter number of columns"))):
        column.append(input("Enter Field:"))
    for x in range(0,len(column)):
        pos.append(env.getNumber(column[x]))
    field = input ("Enter the name of the column you want to search: ")
    litpos = env.getNumber(field)
    value = input ("Enter the value of the column:")
    op = input("enter Operation (EQ,GREATER,LESS)")
    if op == "EQ":
        result = env.queary(litpos, "equal", value)
    elif op == "GREATER":
        result = env.queary(litpos, "greater", value)
    elif op == "LESS":
        result = env.queary(litpos, "less", value)
    else :
        print("Wrong input")
    if (len(result)>0):    
        for y in range(0,len(result)):
            for z in range (0,len(pos)):
                print(result[y][pos[z]],end =' ')
            print("")
    else:
        print("Queary returns null")
    env.closeDB()
    return

def reportOne():
    os.system("runhaskell report1")
    return

def reportTwo():
    os.system("runhaskell report2")
    return

while True:
    print ("\nPython DB Menu")
    print ("____________________")
    print ("1.  Create database")
    print ("2.  Update Record")
    print ("3.  Add record")
    print ("4.  Delete Record")
    print ("5.  Bulk load")
    print ("6.  Display Join")
    print ("7.  Run Query")
    print ("8.  Report 1")
    print ("9.  Report 2")
    print ("10. Exit \n")
    selection = input("Select: ")
    
    if selection == '1':
        createDatabase()
    elif selection == '2':
        updateRecord()
    elif selection == '3':
        addRecord()
    elif selection == '4':
        deleteRecord()
    elif selection == '5':
        bulkLoad()
    elif selection == '6':
        displayJoin()
    elif selection == '7':
        runQuery()
    elif selection == '8':
        reportOne()
    elif selection == '9':
        reportTwo()
    elif selection == '10':
        print ("Good Bye")
        break
    else:
        print ("wrong input")