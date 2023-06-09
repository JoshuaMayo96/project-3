import requests
import pandas as pd
import eel 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # This is to get rid of errors in the terminal, nothing else
import sqlite3
import csv
import os
import traceback
import io
# from pandas_geojson import read_geojson_url #pip install pandas_geojson, decided to get it with requests. 
# import json   # didn't need json 
# import time # did not have to use time. 

class Publish():
    def __init__(self):
        # self.obesity_end_point = 'https://chronicdata.cdc.gov/resource/hn4x-zwk7.json' # only 1K records
        # self.obesity_end_point_geojson = 'https://chronicdata.cdc.gov/resource/hn4x-zwk7.geojson' # only 1K records
        self.obesity_end_point = 'https://chronicdata.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD'
        eel.init('web', allowed_extensions=['.html'])
        self.eel = eel
        
class NoSelf():
    def __init__(self):
        global publish
        self.obesity_end_point = publish.obesity_end_point
        # self.obesity_end_point_geojson = publish.obesit_end_point_geojson # not used only 1K records and only points to the center of the state

    def startPage():
        try:
            eel.start('project3.html', port=0) #port 0 finds any available port. 
        except Exception as e:
            print(f"ERROR {e} KEEP IN MIND THAT THIS SCRIPT REQUIRES YOU TO pip install eel")
  
    @eel.expose
    def updateDatabase(): # The DB is updated from the CSV file cleaned when collecting the data. 
        conn = sqlite3.connect('./Resources/obesity.db')
        try:
            conn.execute('''CREATE TABLE obesity_data (YearEnd,LocationDesc,Question,Data_Value,Age_years,GeoLocation)''') 
        except Exception as e: 
            print(e)
            eel.updateMessage("Database already exist reading it")
            NoSelf.readDataBase()
            return
        try:
            c = conn.cursor()
            with open('./Resources/obesity_data.csv', 'r') as f: 
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == 'yearstart': continue
                    clause = 'INSERT INTO obesity_data (YearEnd,LocationDesc,Question,Data_Value,Age_years,GeoLocation)\
                            VALUES(?,?,?,?,?,?)' 
                    c.execute(clause,row)
            # Query data from table
            cursor = conn.execute("SELECT * from obesity_data")
            for row in cursor:
                print(row)

            conn.commit()
            conn.close()
        except Exception as e:
            traceback.print_exc()
            message = "THE DATABASE CODE HAS ISSUES IN PYTHON... FUNCTION 'updateDatabase'  " + str(e)
            # eel.popAlert(message)
            eel.updateMessage(message)
               

    @eel.expose
    def readDataBase():
        eel.updateMessage("READING DATA BASE ")   
        conn = sqlite3.connect('./Resources/obesity.db')
        cursor = conn.execute("SELECT * from obesity_data")
        tempList = []
        for row in cursor:
            listOfKeys = [
                "YearEnd",
                "LocationDesc",
                "Question",
                "Data_Value",
                "Age_years",
                "GeoLocation",
            ]
            d = dict()
            indx = 0
            for el in row:
                d.update({listOfKeys[indx] : str(el)})
                indx += 1
            tempList.append(d)
            eel.updateMessage(str(row))
            # print(row)
        eel.updateMessage(" FINISHED READING DATABASE. SELECT YEAR OR STATE")
        return(tempList)

    @eel.expose
    def collectData():
        global publish
        if os.path.exists('./Resources/obesity.db'):
            data = NoSelf.readDataBase()
            return(data)
        eel.updateMessage("Collecting Data, please wait")
        try:
            dataJson = requests.get(publish.obesity_end_point)
            dataJson.encoding = 'utf-8'
            csvio = io.StringIO(dataJson.text, newline="")
            data = []
            for row in csv.DictReader(csvio):
                data.append(row)
   
            df = pd.DataFrame.from_records(data)
            df.columns = df.columns.str.replace('[:,@]', '', regex=True)
            df.columns = df.columns.str.replace('[.]', '_', regex=True)
            df = df[['YearEnd', 'LocationDesc', 'Question', 'Data_Value', 'Age(years)', 'GeoLocation']]
            df = df.rename(columns={'Age(years)': 'Age_years'}) #changed this name becuase caused issues with DB. 
            df_clean = df.dropna() #Does not have NaNs are maybe blank rows only but does not hurt. 
            df_clean = df_clean[df_clean.YearEnd != ''] #Removed blanks them like this
            df_clean = df_clean[df_clean.LocationDesc != '']
            df_clean = df_clean[df_clean.Question != '']
            df_clean = df_clean[df_clean.Data_Value != '']
            df_clean = df_clean[df_clean.Age_years != '']
            df_clean = df_clean[df_clean.GeoLocation != '']
            df_clean.to_csv('./Resources/obesity_data.csv', index=False, encoding='utf-8')
            eel.updateMessage("")
            d = df_clean.to_json()
            NoSelf.createDataBase(d)
            return(d)
        except Exception as e:
            print(e)
            eel.updateMessage(e)

    def createDataBase(d):
        conn = sqlite3.connect('./Resources/obesity.db')
        try:
            conn.execute('''CREATE TABLE obesity_data (YearEnd,LocationDesc,Question,Data_Value,Age_years,GeoLocation)''')
        except Exception as e: 
            print(e)
            eel.updateMessage("Database already exist reading it")
            NoSelf.readDataBase()
            return

        try:
            c = conn.cursor()
            with open('./Resources/obesity_data.csv', 'r') as f: # Import data from CSV file created when colecting data to DB
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == 'YearEnd': continue
                    clause = 'INSERT INTO obesity_data (YearEnd,LocationDesc,Question,Data_Value,Age_years,GeoLocation)\
                            VALUES(?,?,?,?,?,?)' 
                    c.execute(clause,row)
            conn.commit()
            conn.close()
        except Exception as e:
            traceback.print_exc()
            message = "THE DATABASE CODE HAS ISSUES IN PYTHON... FUNCTION 'updateDatabase'  " + str(e)
            eel.updateMessage(message)

if __name__ == "__main__":
    if not os.path.exists("./Resources"):
        os.makedirs("./Resources")
    publish = Publish()
    startPage = NoSelf.startPage()
 
