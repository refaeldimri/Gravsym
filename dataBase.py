import mysql.connector
import json
import datetime
from mysql.connector import errorcode


# function which gets symbol name and return all the his names in other languages
def fetchData(symbolNameAndLocation, cur):
 tmpArr = symbolNameAndLocation.split(":")
 dictOfSymbolAndLanguage = {}
 tmpArrLocationSplit = []

 tmpArr[1] = tmpArr[1].replace('[', '')
 tmpArr[1] = tmpArr[1].replace(']', '')
 tmpArr[1] = tmpArr[1].replace(',', '')
 tmpArrLocationSplit = tmpArr[1].split(" ")

 cur.execute("select id from symbol where main_name = " + "'" + tmpArr[0] + "'" + "")
 for row in cur.fetchall():
   symbolID = row[0]
 
 cur.execute("select name, language from symbol_alt_name where id = " + str(symbolID) + "")
 for row in cur.fetchall():
   dictOfSymbolAndLanguage[row[1]] = row[0]
 dictOfSymbolAndLanguage["X1"] = tmpArrLocationSplit[0]
 dictOfSymbolAndLanguage["Y1"] = tmpArrLocationSplit[1]
 dictOfSymbolAndLanguage["X2"] = tmpArrLocationSplit[2]
 dictOfSymbolAndLanguage["Y2"] = tmpArrLocationSplit[3]
 
 return dictOfSymbolAndLanguage
# end func fetchData



# function which add  symbols to database
def addSymbol(name, language, cur, db):
 symbolID = None
 cur.execute("select count(*) from symbol")
 for row in cur.fetchall():
  symbolID = row[0]
 symbolID = symbolID + 1;


 addToSymbolTableQuery = "insert into symbol (id, main_name) values (%s, %s)";
 value = (symbolID, name);
 cur.execute(addToSymbolTableQuery, value);
 db.commit();
 addAltName(name, name, language, cur, db);
# end function addSymbol


# function which add alt name to database
def addAltName(MainSymbolName, altName, language, cur, db): 
 symbolID = None
 cur.execute("select id from symbol where main_name = " + "'" + MainSymbolName + "'" + "")
 for row in cur.fetchall():
  symbolID = row[0]
 
 addAltNameQuery = "insert into symbol_alt_name (id, name, language) values (%s, %s, %s)";
 value = (symbolID, altName, language)
 cur.execute(addAltNameQuery, value);
 db.commit();
# end function addAltName();
  

# function which add event to database
def addEvent2(eventType, description, severity, cur, db):
 cur.execute("select count(*) from system_event")
 for row in cur.fetchall():
  eventID = row[0]
 eventID = eventID + 1;

 now = datetime.datetime.now()
 addEventQuery = "insert into system_event (id, type, date_time, description, severity ) values (%s, %s, %s, %s, %s)";
 value = (eventID, eventType, now, description, severity)
 cur.execute(addEventQuery, value);
 db.commit();
# end function addEvent

# function which add event to database
def addEvent(eventType, description, severity, cur, db):
 cur.execute("select count(*) from system_event")
 for row in cur.fetchall():
  eventID = row[0]
 eventID = eventID + 1;

 now = datetime.datetime.now()
 addEventQuery = "insert into system_event (type, date_time, description, severity ) values (%s, %s, %s, %s)";
 value = (eventType, now, description, severity)
 cur.execute(addEventQuery, value);
 db.commit();
# end function addEvent


# function which show messages to Maintainer
def showMsgMaintainer(cur):
 msg = []
 cur.execute("select * from system_event where severity = 2")
 for row in cur.fetchall():
  msg.append(row[1] + "_" + str(row[2]) + "_" + row [3]);
 return msg
# end function showMsgMaintainer
 

# function which delete events from database
def deleteEventAndMsg(cur, db):
 cur.execute("delete from system_event")
 db.commit();
# end function deleteEventAndMsg


# function which translate one symbol
def translateSymbol(MainSymbolName, translation, language, cur, db):
 symbolID = None
 cur.execute("select id from symbol where main_name = " + "'" + MainSymbolName + "'" + "")
 for row in cur.fetchall():
  symbolID = row[0]

 addNewLanguageQuery = "insert into symbol_alt_name(id, name, language) values (%s, %s, %s)";
 value = (symbolID, translation, language)
 cur.execute(addNewLanguageQuery, value);
 db.commit();
# end function translate symbol


# function which trans All Symbol
def transAllSystem(arrSym, arrTrans, language, cur, db):
 for (sym, trans) in zip (arrSym, arrTrans):
  translateSymbol(sym, trans, language, cur, db)    
# end function transAllSystem


# function which delete symbol alt name
def deleteAltName(symbolAltName, cur, db):
 cur.execute("delete from symbol_alt_name where name = " + "'" + symbolAltName + "'" + "")
 db.commit(); 
# end function deleteAltName


# function which delete symbol from the DB
def deleteMainSymbol(mainSymbol, cur, db):
 cur.execute("select id from symbol where main_name = " + "'" + mainSymbol + "'" + "")
 for row in cur.fetchall():
  symbolID = row[0]

 cur.execute("delete from symbol_alt_name where id = " + str(symbolID))
 db.commit();

 cur.execute("delete from symbol where id = " + str(symbolID))
 db.commit();
# end function deleteMainSymbol


#function which show all Main symbol in Db
def showAllsymbols(cur):
 symbolID = []
 cur.execute(" select * from symbol")
 for row in cur.fetchall():
  symbolID.append(row[1])
 return(symbolID)
#end function showAllsymbols


#function which show all alt symbol name in Db
def showAltSymbolsName(cur):
 symbolID = []
 cur.execute(" select * from symbol_alt_name")
 for row in cur.fetchall():
  symbolID.append(row[1] + " : " + row[2])
 return(symbolID)
#end function showAltSymbolsName


#function which show all events in system
def showAllEvents(cur):
 events = []
 cur.execute("select * from system_event")
 for row in cur.fetchall():
  events.append(row[1] + "_" + str(row[2]) + "_" + row[3] + "_" + str(row[4]));
 return events
#end function showEvents



