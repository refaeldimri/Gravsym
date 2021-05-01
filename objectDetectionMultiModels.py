#!/usr/local/bin/python3

import cgi
import cgitb
cgitb.enable()

# Print necessary headers.
print("Content-Type: text/html")
print()

from datetime import datetime
from imageai.Detection.Custom import CustomObjectDetection
import pathlib
import os
import sys 
from dataBase import fetchData, addEvent
import dataBase
import mysql.connector
import json
import urllib.request

def answer_from_client(ans):
 db = mysql.connector.connect(host="172.16.4.57", user="test", passwd="password", db="gravsym_db")       
 cur = db.cursor()
 ans = bool(ans)
 addEvent("Identification error", "system could not detect symbol", 2, cur, db)
 db.close() 
    
###
def detectObject(url):
 db = mysql.connector.connect(host="172.16.4.57", user="test", passwd="password", db="gravsym_db")       
 cur = db.cursor()
 photoName = ""
 JSONStringList = []
 modelAndConf = {"StarOfDavidModel.h5":"StarOfDavid.json",
		"IDFSymbolModel.h5":"IDFSymbol.json",
		"CandelabrumModel.h5":"Candelabrum.json",
		"HandsModel.h5":"Hands.json",
		"crossModel.h5":"cross.json"
		}

 photoName = downloadPhoto(url)
 detector = CustomObjectDetection()
 detector.setModelTypeAsYOLOv3()
 for model in modelAndConf:  
  detector.setModelPath(model) 
  detector.setJsonPath(modelAndConf[model])
  detector.loadModel()
  detections = detector.detectObjectsFromImage(input_image=photoName, output_image_path=photoName, minimum_percentage_probability=60)
  for detection in detections:
   JSONStringList.append(json.dumps(fetchData(detection["name"] + ":" + str(detection["box_points"]), cur)))

 if len(JSONStringList) == 0:
  print("No identification")
  addEvent("No identification", "not detect symbol", 2, cur, db)
 else:     
  print(JSONStringList)
 os.remove(photoName)
 db.close()
  

def downloadPhoto(url):  
 arrTemp = url.split(".")
 photoName = str(datetime.utcnow().strftime("%Y %m %d %H:%M:%S.%f")[:-3]) + "photoName." + arrTemp[-1]
 urllib.request.urlretrieve(url, photoName)    
 return photoName

if __name__ == "__main__":
 value = ""
 form = cgi.FieldStorage()
 if "url" in form:
  value = str(cgi.FieldStorage().getvalue("url"))
  detectObject(value)
 if "ans" in form:
  value = str(cgi.FieldStorage().getvalue("ans"))
  answer_from_client(value)

