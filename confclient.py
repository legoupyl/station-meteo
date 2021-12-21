mqtt_brocker="m.legoupyl.com"
topic="xavfan/data"


#Managed probe type
measureList=('TEMP','HUM','PRESSURE')

#Initialisation des sondes et interrupeurs
node = dict ()

node0 = dict ()
node0["ID"]="0000"
node0["CATEGORY"]="PROBE"
node0["DEVICETYPE"]="PCDUINO"
node0["LOCATION"]="Salon"
node0["TEMP"]= None
node0["PRESSURE"]= None
node0["TIMESTAMP"]= None
node0["deviceid"]= "station_oullins_1"
node[0]=node0

node1 = dict ()
node1["ID"]="9210"
node1["CATEGORY"]="PROBE"
node1["DEVICETYPE"]="Oregon TempHygro"
node1["LOCATION"]="Balcon"
node1["TEMP"]= None
node1["TEMPFormat"]= "oregon"
node1["TIMESTAMP"]= None
node1["deviceid"]= "station_oullins_2"
node[1]=node1

node2 = dict ()
node2["ID"]="XX"
node2["CATEGORY"]="PLUG"
node2["DEVICETYPE"]="PLUG"
node2["CMDON"]=b'10;TriState;08808a;2;ON;\n\r'
node2["CMDOFF"]=b'10;TriState;08808a;2;ON;\n\r'
node2["deviceid"]= "PLUG_1"
node[2]=node2

node3 = dict ()
node3["ID"]="XX"
node3["CATEGORY"]="PLUG"
node3["DEVICETYPE"]="PLUG"
node3["CMDON"]=b'10;TriState;08802a;2;ON;\n\r'
node3["CMDOFF"]=b'10;TriState;08802a;2;ON;\n\r'
node[3]=node3

# boutton 1 - ON de la telecommande
node4 = dict ()
node4["ID"]="5b"
node4["SWITCH"]="28"
node4["CATEGORY"]="RC"
node4["DEVICETYPE"]="RC"
node4["CMDON"]=""
node4["CMD"]="ON"
node4["CMDON"]=""
node4["CMDOFF"]=""
node[4]=node4


node5 = dict ()
node5["ID"]="0A01"
node5["CATEGORY"]="PROBE"
node5["DEVICETYPE"]="Xiron"
node5["LOCATION"]="Inconnu"
node5["TEMP"]= None
node5["TEMPFormat"]= "oregon"
node5["HUM"]= None 
node5["TIMESTAMP"]= None
node5["deviceid"]= "station_oullins_3"
node[5]=node5

node6 = dict ()
node6["ID"]="000a"
node6["CATEGORY"]="PROBE"
node6["DEVICETYPE"]="Renkforce E_TA"
node6["LOCATION"]="Inconnu"
node6["TEMP"]= None
node6["TEMPFormat"]= "oregon"
#node["HUM"]= None 
node6["TIMESTAMP"]= None
node6["deviceid"]= "station_oullins_5"
node[6]=node6
