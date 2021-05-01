from dataBase import addSymbol, showAltSymbolsName, showAllsymbols, deleteMainSymbol, deleteAltName
from dataBase import transAllSystem, translateSymbol, deleteEventAndMsg, showMsgMaintainer, addAltName, showAllEvents

import mysql.connector
import json
import datetime
import docker
from mysql.connector import errorcode

########################################################################################################
listOfOption = []
listOfOption.append(" Turn on system") # 1
listOfOption.append(" Show system mode") # 2
listOfOption.append(" Add main symbol name") # 3
listOfOption.append(" Delete main symbol name") # 4
listOfOption.append(" Add alternative name to symbol") # 5
listOfOption.append(" Delete alternative name to symbol") # 
listOfOption.append(" Show events log") # 7
listOfOption.append(" Show exception messages") # 8
listOfOption.append(" Clear events log") # 9
listOfOption.append("Add new language to the system") # 10
listOfOption.append("Show list of main symbols") # 11
listOfOption.append("Show list of alternative symbols name") # 12
listOfOption.append("Turn off system") # 13
listOfOption.append("Quit") # 14

container_name = "test2"
def container_is_running(container_name):
    return docker.from_env().containers.get(container_name).attrs.get("State")["Running"]


def stop_container(container_name):
    docker.from_env().containers.get(container_name).stop()


def start_container(container_name):
    docker.from_env().containers.get(container_name).start()


def maintainerMenu():
    try:
        inputOption = 0
        # connect to database
        db = mysql.connector.connect(host="172.16.4.57", user="test", passwd="password", db="gravsym_db")       
        cur = db.cursor()
     
        while inputOption != '14':
            numberOfOption = 1
            print("\nMAINTAINER MENU: \n===============\n")
            print("Choose option between 1-" + str(len(listOfOption)) + "\n")
     
            for option in listOfOption:
                print(str(numberOfOption) + ". " + option)
                numberOfOption = numberOfOption + 1

            inputOption = input("\nYour option: ")

            if(inputOption == '1'):
                start_container(container_name)
                print("Server connected")

###
            elif(inputOption == '2'):
                print("Running: " + str(container_is_running(container_name)))
        
     
###
            elif(inputOption == '3'):  
                name = input("Type Main symbol name: ")
                language = input("Type language of this symbol: ")
                addSymbol(name, language, cur, db)
                print("the symbol was inserted")

###
            elif(inputOption == '4'):
                print(" All the main symbols name in the system:")
                print(" ============================================")
                for sym in showAllsymbols(cur):
                    print(" " + sym)
                name = input(" \n Type Main symbol name to delete: ")
                deleteMainSymbol(name, cur, db)
                print(" the symbol was removed")
        
###
            elif(inputOption == '5'):
                print("All the main symbols name in the system:")
                print("============================================")
                for sym in showAllsymbols(cur):
                    print(sym)
                mainName = input("Which symbol do you want to add an alternative name to?: ")
                altName = input("Type your alternative name to " + mainName + ": ")
                language = input("what is the language of this alternative name: ")
                addAltName(mainName, altName, language, cur, db)
                print("Alternative name was inserted")

###
            elif(inputOption == '6'):
                print("All the alternative symbols name in the system:")
                print("==================================================")
                for sym in showAltSymbolsName(cur):
                    print(sym)
                altName = input("Type symbol name to delete: ")
                deleteAltName(altName, cur, db)
                print("The symbol was deleted")


### 
            elif(inputOption == '7'):
                print("Events log:")
                print("============")
                for events in showAllEvents(cur):
                    events2 = []
                    events2 = events.split("_")
                    print("Type event: "  + events2[0] + "\n" +
                            "Event time: "  + str(events2[1]) +"\n" +
                            "Description: " + events2[2] + "\n" +
                            "Severity: "    + str(events2[3]) + "\n" + "\n")


###
            elif(inputOption == '8'):
                print("Exception messages:")
                print("==========")
                for msg in showMsgMaintainer(cur):
                    msg2 = []
                    msg2 = msg.split("_")
                    print("Type message: "  + msg2[0] + "\n" +
                        "message time: "  + str(msg2[1]) +"\n" +
                        "Description: " + msg2[2] + "\n" + "\n")
               

###    
            elif(inputOption == '9'):
                deleteEventAndMsg(cur, db)
                print("Events log was clear")


###
            elif(inputOption == '10'):
                symTrans = []
                sym = []  
                language = input("Type new language: ")
                for sym in showAllsymbols(cur):
                    symTrans.append(input("translet symbol " + sym + " :"))
                sym = showAllsymbols(cur)
                transAllSystem (sym, symTrans, language, cur, db)
                print(language + "was inserted to system")
          

### 
            elif(inputOption == '11'):
                print("Main symbol list:")
                print("==================")
                for symbols in showAllsymbols(cur):
                    print(symbols)


###
            elif(inputOption == '12'):
                print("alternative symbols names list:")
                print("===================================")
                for symbols in showAltSymbolsName(cur):
                    print(symbols)

      

###
            elif(inputOption == '13'):
                stop_container(container_name)
                print("Server disconnected")

###
            elif(inputOption == '14'):
                print("GOOD BYE :)")
                break
###
            else:
                print("Invalid option")

               
    except:
        print("Invalid option")  
        maintainerMenu()
        

    db.close()   
##################################################################
   







 

maintainerMenu()
