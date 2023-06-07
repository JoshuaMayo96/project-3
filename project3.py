
import requests
import json
import pandas as pd
# from pandas_geojson import read_geojson_url #pip install pandas_geojson, decided to get it with requests. 
import eel 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import sqlite3
import csv
import os
import traceback
import io
import time

class Publish():
    def __init__(self):
        # self.obesity_end_point = 'https://chronicdata.cdc.gov/resource/hn4x-zwk7.json'
        self.obesity_end_point = 'https://chronicdata.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD'
        self.obesit_end_point_geojson = 'https://chronicdata.cdc.gov/resource/hn4x-zwk7.geojson'
        eel.init('web', allowed_extensions=['.html'])
        self.eel = eel
        
class NoSelf():
    def __init__(self):
        global publish
        self.obesity_end_point = publish.obesity_end_point
        self.obesit_end_point_geojson = publish.obesit_end_point_geojson

    def startPage():
        try:
            eel.start('project3.html', port=0)
        except Exception as e:
            print(f"ERROR {e} KEEP IN MIND THAT THIS SCRIPT REQUIRES YOU TO pip install eel")
  
    @eel.expose
    def updateDatabase():
        conn = sqlite3.connect('./Resources/obesity.db')
        try:
            conn.execute('''CREATE TABLE obesity_data (YearEnd,LocationDesc,Question,Data_Value,Age_years,GeoLocation)''') 
        except Exception as e: 
            print(e)
            eel.updateMessage("Database already exist reading it")
            NoSelf.readDataBase()
            return

        try:
            # Import data from CSV file
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
        eel.updateMessage(" COMPLETED READING DATABASE")
        # y11 = [x for x in tempList if x['YearEnd'] == '2011']
        # y12 = [x for x in tempList if x['YearEnd'] == '2012']
        # y13 = [x for x in tempList if x['YearEnd'] == '2013']
        # y14 = [x for x in tempList if x['YearEnd'] == '2014']
        # y15 = [x for x in tempList if x['YearEnd'] == '2015']
        # y16 = [x for x in tempList if x['YearEnd'] == '2016']
        # y17 = [x for x in tempList if x['YearEnd'] == '2017']
        # y18 = [x for x in tempList if x['YearEnd'] == '2018']
        # y19 = [x for x in tempList if x['YearEnd'] == '2019']
        # y20 = [x for x in tempList if x['YearEnd'] == '2020']
        # y21 = [x for x in tempList if x['YearEnd'] == '2021']


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
            # df = df.dropna()
            df.columns = df.columns.str.replace('[:,@]', '', regex=True)
            df.columns = df.columns.str.replace('[.]', '_', regex=True)
            df = df[['YearEnd', 'LocationDesc', 'Question', 'Data_Value', 'Age(years)', 'GeoLocation']]
            df = df.rename(columns={'Age(years)': 'Age_years'}) #changed this name becuase caused issues with DB. 
            # print (df.isnull().sum())
            df_clean = df.dropna() #Do not seem to be nas are maybe blank row. 
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
            # Import data from CSV file
            c = conn.cursor()
            with open('./Resources/obesity_data.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == 'YearEnd': continue
                    clause = 'INSERT INTO obesity_data (YearEnd,LocationDesc,Question,Data_Value,Age_years,GeoLocation)\
                            VALUES(?,?,?,?,?,?)' 
                    c.execute(clause,row)
            # Query data from table
            # cursor = conn.execute("SELECT * from obesity_data")
            # for row in cursor:
            #     eel.updateMessage(row)
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
 
