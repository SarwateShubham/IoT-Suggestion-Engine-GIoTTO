import sys,json
import os
with open('/home/shubham/.node-red/flows_shubham-Lenovo-G580.json', 'r') as myfile:
    data=myfile.read()

os.remove("/home/shubham/.node-red/flows_shubham-Lenovo-G580.json")
data=data[:-1]
print data
str1=',{"id":"A","type":"inject","z":"Suggestion","name":"","topic":"","payload":"","payloadType":"date","repeat":"2","crontab":"","once":false,"x":88,"y":145,"wires":[["B"]]},{"id":"B","type":"GioTTo-Sensor","z":"Suggestion","name":"GioTTo-Sensor","location":"'
before_value=str1+sys.argv[1] +'","sensor": "'+sys.argv[2]+','+sys.argv[1]+'","region": "'+sys.argv[3]+'","uuid": "'+sys.argv[4]
after_value='","x":155,"y":228,"wires":[["C"]]},{"id":"C","type":"GioTTo-Condition","z":"Suggestion","name":"","role":">","x":240,"y":163,"wires":[["D"]]},{"id":"D","type":"GioTTo-Value","z":"Suggestion","name":"","compare_value":"'+sys.argv[5]
actu='","satisfy": "on","notsatisfy": "off","x":360,"y":252,"wires":[["E"]]},{"id":"E","type":"GioTTo-Actuate","z":"Suggestion","name":"GioTTo_Actuate","location":"'
after_actu=actu+sys.argv[6] +'","sensor": "'+sys.argv[7]+','+sys.argv[6]+'","region": "'+sys.argv[8]+'","type1": "'+sys.argv[9]+'","identity":"'+sys.argv[10]+'","newstate":"1","x":493,"y":173,"wires":[["F"]]},{"id":"F","type":"debug","z":"Suggestion","name":"","active":true,"console":"false","complete":"false","x":638,"y":280,"wires":[]}]'
final=data+before_value+after_value+after_actu
print final

fi = open("/home/shubham/.node-red/flows_shubham-Lenovo-G580.json", "w")
fi.write(final)
fi.close()

