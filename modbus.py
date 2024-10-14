import sys
import urllib.request
import json
import configparser
import time
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# =======================
# Functions
# =======================

def readChannels():
    # voltage phase 1 to neutral
    print("New measurement readings: ", int(time.time()))
    listValues = []
    for c in listChannels:
        handle = client.read_holding_registers(c['register'], c['words'], unit=c['unit'])
        if c['words'] > 1:
            decoder = BinaryPayloadDecoder.fromRegisters(handle.registers, endian=Endian.Big)
            value = decoder.decode_32bit_int() / float(c['factor'])
        else:
            value = handle.registers[0] / float(c['factor'])
        listValues.append(value)    

    for i, channel in enumerate(listChannels):
        addValue(channel['uuid'], int(time.time() * 1000), listValues[i])

# Add measurement value
def addValue(uuid, timestamp, value):
    url = f"{strURL}/data/{uuid}.json?operation=add&ts={timestamp}&value={value}"
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    jsonVZ = response.read().decode('utf-8')
    return 1

# Create group in VZ
def createGroup(title, public=1):
    url = f"{strURL}/group.json?operation=add&title={title}&public={public}"
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    jsonVZ = response.read().decode('utf-8')
    data = json.loads(jsonVZ)
    _uuid = data["entity"]["uuid"]
    return _uuid

# Add group or channel to a parent group
def addToGroup(uuidParent, uuidChild):
    url = f"{strURL}/group/{uuidParent}.json?operation=add&uuid={uuidChild}"
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    jsonVZ = response.read().decode('utf-8')
    return 1

# Get group
def getGroup(uuid):
    url = f"{strURL}/group/{uuid}.json"
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    jsonVZ = response.read().decode('utf-8')
    return jsonVZ

# Get children of group
def getChildren(uuid):
    data = json.loads(getGroup(uuid))
    listChildren = []
    if 'entity' in data and 'children' in data['entity']:
        for child in data['entity']['children']:
            listChildren.append(child['uuid'])
    return listChildren

# Get title of group
def getGroupTitle(uuid):
    data = json.loads(getGroup(uuid))
    return data['entity']['title']

# Create Channel
def createChannel(type, title):
    url = f"{strURL}/channel.json?operation=add&type={type}&title={title}"
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    jsonVZ = response.read().decode('utf-8')
    data = json.loads(jsonVZ)
    _uuid = data["entity"]["uuid"]
    return _uuid

# Test VZ installation
def testVZ():
    req = urllib.request.Request(strURL)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        return False
    jsonVZ = response.read().decode('utf-8')
    try:
        data = json.loads(jsonVZ)
    except ValueError as e:
        return False
    return data.get('version')

# =======================
# Definitions
# =======================

print("Used Python version: ")
print(sys.version)

# Add channels
listChannels = [
    {'description': "V1_ph2n", 'register': 51284, 'words': 1, 'unit': 0xFF, 'measurement': "voltage", 'factor': 100},
    {'description': "V2_ph2n", 'register': 51285, 'words': 1, 'unit': 0xFF, 'measurement': "voltage", 'factor': 100},
    {'description': "V3_ph2n", 'register': 51286, 'words': 1, 'unit': 0xFF, 'measurement': "voltage", 'factor': 100},
    {'description': "frequency", 'register': 51287, 'words': 1, 'unit': 0xFF, 'measurement': "frequency", 'factor': 100},
    {'description': "P", 'register': 50536, 'words': 2, 'unit': 0xFF, 'measurement': "activepower", 'factor': 0.1},
    {'description': "P1", 'register': 50544, 'words': 2, 'unit': 0xFF, 'measurement': "activepower", 'factor': 0.1},
    {'description': "P2", 'register': 50546, 'words': 2, 'unit': 0xFF, 'measurement': "activepower", 'factor': 0.1},
    {'description': "P3", 'register': 50548, 'words': 2, 'unit': 0xFF, 'measurement': "activepower", 'factor': 0.1},
    {'description': "Q", 'register': 50538, 'words': 2, 'unit': 0xFF, 'measurement': "reactivepower", 'factor': 0.1},
    {'description': "Q1", 'register': 50550, 'words': 2, 'unit': 0xFF, 'measurement': "reactivepower", 'factor': 0.1},
    {'description': "Q2", 'register': 50552, 'words': 2, 'unit': 0xFF, 'measurement': "reactivepower", 'factor': 0.1},
    {'description': "Q3", 'register': 50554, 'words': 2, 'unit': 0xFF, 'measurement': "reactivepower", 'factor': 0.1}
]

# =======================
# Initialization
# =======================

# Load data from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
mainGrpUUID = config.get('Status', 'uuid')
strURL = config.get('General', 'url')

_testVZ = testVZ()

if not _testVZ:
    print("Something is wrong with VZ server or URL.")
    exit()

print("Version of VZ middleware:", _testVZ)

intervalTime = config.get('General', 'intervalTime')
strName = config.get('General', 'name')
strIP = config.get('General', 'IPsocomec')

# Initialize Modbus client
client = ModbusTcpClient(strIP)
ret = client.connect()
if ret:
    print("Connected to Socomec.")
else:
    print("Connection to Socomec failed.")
    exit()

# Start the scheduler
sched = BlockingScheduler()

# Check if main group already exists. If not, create one
if not mainGrpUUID:
    print("No main group exists. Going to create one ...")
    mainGrpUUID = createGroup(strName, 1)
    print(mainGrpUUID)
    config.set('Status', 'uuid', mainGrpUUID)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
else:
    print("Main group UUID: ", mainGrpUUID)

# Check for existing subgroups
subGroups = {}
listGroups = getChildren(mainGrpUUID)

for x in listGroups:
    key = getGroupTitle(x)
    if key not in subGroups:
        subGroups[key] = x
    else:
        print("Subgroup exists twice. That shouldn't happen.")
        exit(500)

# Check measurement channels and assign to group
for c in listChannels:
    strMeasurement = c['measurement']
    _uuid = 0

    # Check if subgroup already exists
    if strMeasurement not in subGroups:
        _uuid = createGroup(strMeasurement, 0)
        subGroups[strMeasurement] = _uuid
        print("Group created:", strMeasurement, addToGroup(mainGrpUUID, _uuid))

    # Create channel and add to group
    if c['measurement'] == "voltage":
        _uuid = createChannel("voltage", c['description'])
    elif c['measurement'] == "frequency":
        _uuid = createChannel("frequency", c['description'])
    elif c['measurement'] in ["activepower", "reactivepower"]:
        _uuid = createChannel("powersensor", c['description'])
    else:
        print("Measurement type not known.")
        exit()

    # Add channel to subgroup
    print("Added to group successfully:", addToGroup(subGroups[c['measurement']], _uuid))
    c['uuid'] = _uuid

# =======================
# Main
# =======================

sched.add_job(readChannels, 'interval', seconds=int(intervalTime))
sched.start()

client.close()
