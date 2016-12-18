import requests
import time
import json
import time
import calendar
from json_setting import JsonSetting

class GiottoHelper:
    def __init__(self, settingFilePath="./config.json"):
        setting = JsonSetting(settingFilePath)
        self.giotto_rest_api = setting.get('giotto_rest_api')
        self.oauth = setting.get('oauth')
        self.tag=setting.get('tag')

    def getOauthToken(self):
        headers = {'content-type': 'application/json'}
        url = self.giotto_rest_api['server']
        url += ':' + self.giotto_rest_api['oauth_port'] 
        url += '/oauth/access_token/client_id='
        url += self.oauth['id']
        url += '/client_secret='
        url += self.oauth['key']
        result = requests.get(url, headers=headers)
        if result.status_code == 200:
            dic = result.json()
            return dic['access_token']
        else:
            return ''

    def sensorlist(self):
      url = self.giotto_rest_api['server']
      access_token=self.getOauthToken()
      header = {"Authorization": "Bearer " + access_token, 'content-type':'application/json'}
      url_sensor_list = url+":"+self.giotto_rest_api['oauth_port']+"/api/search"
      data={"data":{"Tags":[self.tag]}}
      response = requests.post(url_sensor_list,data=json.dumps(data),headers = header).json()
      return response

    def get_timeseries_data(self,sensor,mins):
      url = self.giotto_rest_api['server']
      sensorUUID = sensor
      OauthToken = self.getOauthToken()
      header = {"Authorization": "bearer " + OauthToken, 'content-type':'application/json'}
      end_time = int(time.time()-86400*35.5)
      #print end_time
      start_time = int(end_time-(60)*mins) 
      url1 = url+":"+self.giotto_rest_api['port']+"/api/sensor/%s/timeseries?start_time=%s&end_time=%s" % (sensorUUID, start_time,end_time)
      #print url1
      response = requests.get(url1, headers = header)
      #print response.text
      if response.status_code == 200:
            return response.json()
      else:
            return 'in get_timeseries_data in giotto_helper.py:: \\\
            Please check the error corresponding to '+response.status_code

if __name__ == "__main__":
    giotto_helper = GiottoHelper()
    
