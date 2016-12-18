import requests
import json
import time
import datetime
from datetime import timedelta
import sys
import dateutil.parser as dp
import os

import requests, json, time
global url,uuids,sensor_names,sensor_values,actuator_identity,actuator_type,actuator_values
url="https://bd-exp.andrew.cmu.edu"

sensor_names=[]
sensor_values=[]
actuator_type=[]
actuator_identity=[]
actuator_values=[]



def getOauthToken():
    url="https://bd-exp.andrew.cmu.edu:81/oauth/access_token/client_id=9V9CgOEgypeBr8LlSeaC5NbEtqjIQZ8f7bBpWz0H/client_secret=2RhqVwdqIjEJyEWly9GN3ZC1pmlhZVLqTcl0y0soAdrHNFA0uP"
    response = requests.get(url).json()
    access_token = response["access_token"]
    print response
    return access_token

def get_sensor_data(sensor,mins):
  headers = {'content-type':'application/json',
        'charset' : 'utf-8',
        'Authorization' : 'Bearer '+ getOauthToken()}
  end_time = int(time.time()-86400*6.5)
  start_time = int(end_time-(mins*60))
  get_url = url + ":82/api/sensor/"+sensor+"/timeseries?start_time="+`start_time` + "&end_time="+`end_time`
  try:
    response=requests.get(get_url, headers = headers).json()
    return response
  except Exception as e:
    print sensor+" didn't find data for the past 150 seconds . Please check the sensor"
    return str(e)

def sensorlist():
  access_token=getOauthToken()
  #print access_token
  header = {"Authorization": "Bearer " + access_token, 'content-type':'application/json'}
  url_sensor_list = url+":81/api/search"
  data={"data":{"Tags":["room:DemoRoom"]}}
  #print url_sensor_list,data,type(data)
  response = requests.post(url_sensor_list,data=json.dumps(data),headers = header).json()
  return response

def return_latest_values(uuid):
  temp=get_sensor_data(uuid)
  #print uuid
  #print temp
  for t in temp['data']['series']:
    for sens in t['values']:
      if(sens==t['values'][-1]):
        return (sens[2])
        #print i

def actuate_devices():
  for d in range(0,len(actuator_identity)):
    url_post=url+':69/api'
    #print url_post
    data={"type":actuator_type[d],"identity":actuator_identity[d],"new_state":actuator_values[d]}
    #print data
    response=requests.post(url_post,data=json.dumps(data))
    return response

def get_timeseries_data(sensor,mins):
  url="https://bd-exp.andrew.cmu.edu:82/"
  sensorUUID = sensor
  OauthToken = getOauthToken()
  header = {"Authorization": "bearer " + OauthToken, 'content-type':'application/json'}
  end_time = int(time.time())
  start_time = int(end_time-(60)*mins) 
  url1 = url+"api/sensor/%s/timeseries?start_time=%s&end_time=%s" % (sensorUUID, start_time,end_time)
  #print url1
  response = requests.get(url1, headers = header)
  print response.text
  return response.json()

def print2file():
    bashCommand = "rm ./Files/*.csv"
    os.system(bashCommand)
    allow=0
    arr=[]
    Sens=sensorlist()
    print Sens
    print sensor_names
    print sensor_values
    print actuator_type
    print actuator_identity
    print actuator_values
    for sensor in Sens['result']:	
	lul=sensor['tags']
	for ta in lul:
	 arr.append(ta['name']);
        print arr
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
	    print sensor['source_name']
            data=get_timeseries_data(sensor['name'],2)
            handle=open('./Files/'+filename+","+region+".csv",'w')
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
    bashCommand = "matlab -nodisplay -r \"cd ./DataProcess; Suggest_Rules\""
    os.system(bashCommand)
    
onlytrain()
