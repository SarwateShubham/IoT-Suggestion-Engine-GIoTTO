import json

class JsonSetting:
    def __init__(self, settingFilePath="./config.json"):
        self.setting = json.loads(open(settingFilePath,'r').read())

    def get(self, settingName):
        return self.setting[settingName]

if __name__ == "__main__":
    settingStringPath = './connector_setting.json'
    self.setting = json.loads(open(settingFilePath,'r').read())
    print self.setting
