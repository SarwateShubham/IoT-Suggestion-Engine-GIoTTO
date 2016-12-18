
import requests
import json
import time
import datetime
from datetime import timedelta
import sys
import dateutil.parser as dp
import os
from sys import platform

import requests, json, time
global url,uuids,sensor_names,sensor_values,actuator_identity,actuator_type,actuator_values
sensor_names=[]
sensor_values=[]
actuator_type=[]
actuator_identity=[]
actuator_values=[]


from giotto_helper import GiottoHelper
from json_setting import JsonSetting


def print2file():
    if platform == "linux" or platform == "linux2":
        bashCommand = "rm ./Sensor_data/*.csv"
    elif platform == "win32":
        bashCommand = "del .\Sensor_data\*.csv"
    
    os.system(bashCommand)
    print "filescleaned"
    allow=0
    arr=[]
    Sens=giotto_helper.sensorlist()
    #print Sens
    '''
    print sensor_names
    print sensor_values
    print actuator_type
    print actuator_identity
    print actuator_values
    '''
    for sensor in Sens['result']:	
        lul=sensor['tags']
        for ta in lul:
         arr.append(ta['name']);
        #print arr
        if('identity' not in arr):
          allow=1
          filename=sensor['source_name'] + ","+sensor['source_identifier']+ ","+sensor['name']
        arr=[]        
        try:
          for tag in sensor['tags']:
           if(sensor['source_name']=='status' or tag['name']=='status'):
              allow=1
              filename=sensor['source_name'] + ","+sensor['source_identifier']+ ","+sensor['name']
           if(tag['name']=='region'):
              region=tag['value']
        except:
          print "No actuator present in the region!"

        if(allow==1):
            #print sensor['source_name']
            data=giotto_helper.get_timeseries_data(sensor['name'],2)
            handle=open('./Sensor_data/'+filename+","+region+".csv",'w')
            series=(data['data']['series'][0])
            for col in series['columns']:
                handle.write(str(str(col)+","))
            handle.write("\r\n")
            for val in series['values']:
                st_time=time.mktime(dp.parse(str(val[0])).timetuple())
                en_time=time.mktime(dp.parse(str(val[1])).timetuple())
                if(val[2]=='on'):
                   val[2]=1
                elif(val[2]=='off'):
                   val[2]=0
                handle.write(str(str((st_time))+","+str((en_time))+","+str(val[2])+"\r\n"))
            handle.close()
            allow=0

    onlytrain()


def onlytrain():
    if platform == "linux" or platform == "linux2":
        bashCommand = bashCommand = "matlab -nodisplay -r \"cd ./DataProcess; Suggest_Rules\""
    elif platform == "win32":
        bashCommand = bashCommand = "matlab -nodesktop -r \"cd ./DataProcess; Suggest_Rules\""
    os.system(bashCommand)
    
if __name__ == "__main__":
	giotto_setting = JsonSetting('./config.json')
	giotto_helper = GiottoHelper()
	if(sys.argv[1]=='only_train'):
            onlytrain()
        elif(sys.argv[1]=='download_train'):
            print2file()
        else :
            print('Please provide valid arguments : only_train & download_train')
