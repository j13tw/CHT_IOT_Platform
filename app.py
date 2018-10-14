#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

import serial, time
import json
import datetime
import paho.mqtt.client as mqtt

# MQTT setup data
CLIENT_MQTT_SERVER = "10.20.0.19"
CLIENT_MQTT_PORT = 1883

CLIENT_MQTT_TOPIC_DL303_CO2 = "DL303/CO2"
CLIENT_MQTT_TOPIC_DL303_RH = "DL303/RH"
CLIENT_MQTT_TOPIC_DL303_TC = "DL303/TC"
CLIENT_MQTT_TOPIC_DL303_DC = "DL303/DC"

CLIENT_MQTT_TOPIC_ET7044 = "ET7044/write"

CLIENT_MQTT_TOPIC_POWER_METER = "current"

CLIENT_MQTT_TOPIC_UPS_MONITOR = "UPS_Monitor"

CLIENT_MQTT_TOPIC_AIR_CONDITION = "air-conditioner-vent"

CLIENT_MQTT_TOPIC_UPS_ROUTE_A = "cabinet_A"
CLIENT_MQTT_TOPIC_UPS_ROUTE_B = "cabinet_B"

SERVER_MQTT_SERVER = "iot.cht.com.tw"
SERVER_MQTT_TOPIC_HEAD = "/v1/device/"
SERVER_MQTT_TOPIC_END = "/rawdata"
SERVER_MQTT_PORT = 1883
SERVER_USER_NAME = ""
SERVER_USER_PWD = ""

SERVER_MQTT_TOPIC_UPS_ROUTE_A = "UPS_ROUTE_A"
SERVER_DEVICE_ID_UPS_ROUTE_A = "7842144586"
SERVER_DEVICE_KEY_UPS_ROUTE_A = "DKRWM147RKRFB09GCB"

SERVER_MQTT_TOPIC_UPS_ROUTE_B = "UPS_ROUTE_B"
SERVER_DEVICE_ID_UPS_ROUTE_B = "7847484162"
SERVER_DEVICE_KEY_UPS_ROUTE_B = "DK1F110RXGX921MEKM"

SERVER_MQTT_TOPIC_AIR_CONDITION = "AIR_CONDITION"
SERVER_DEVICE_ID_AIR_CONDITION = "7842084764"
SERVER_DEVICE_KEY_AIR_CONDITION = "DKW0TZ77U027FURXYK"

SERVER_MQTT_TOPIC_DL303 = "DL303"
SERVER_DEVICE_ID_DL303 = "7839288845"
SERVER_DEVICE_KEY_DL303 = "DK1CSFECPSXST91BKE"

SERVER_MQTT_TOPIC_ET7044 = "ET7044"
SERVER_DEVICE_ID_ET7044 = "7839306572"
SERVER_DEVICE_KEY_ET7044 = "DKST1SRZ3CRBSZUKBF"
ET7044_CONTROL = [False, False, False, False, False, False, False, False]

SERVER_MQTT_TOPIC_POWER_METER = "PowerMeter"
SERVER_DEVICE_ID_POWER_METER = "7839467604"
SERVER_DEVICE_KEY_POWER_METER = "DK4PA7GA7X55R7PKCB"

SERVER_MQTT_TOPIC_UPS_A = "UPS_A"
SERVER_DEVICE_ID_UPS_A = "7839547792"
SERVER_DEVICE_KEY_UPS_A = "DKF2SHXUGUU7942KZ3"

SERVER_MQTT_TOPIC_UPS_B = "UPS_B"
SERVER_DEVICE_ID_UPS_B = "7839666288"
SERVER_DEVICE_KEY_UPS_B = "DKTGWYSE0GCMG2ZFYC"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_DL303_CO2)
    mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_DL303_DC)
    mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_DL303_RH)
    mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_DL303_TC)
    mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_ET7044)
    mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_POWER_METER)
    mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_UPS_MONITOR)
    mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_AIR_CONDITION)
    mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_UPS_ROUTE_A)
    mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_UPS_ROUTE_B)

def on_message(client, userdata, message):
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month)
    if (int(month) < 10): month = "0" + str(month)
    day = str(now.day)
    if (int(day) < 10): day = "0" + str(day)
    hour = str(now.hour)
    if (int(hour) < 10): hour = "0" + str(hour)
    minute = str(now.minute)
    if (int(minute) < 10): minute = "0" + str(minute)
    second = str(now.second)
    if (int(second) < 10): second = "0" + str(second)
    micro_second = str(int(datetime.datetime.now().microsecond/100))
    print('------------------------------------------------------')
    print("message received -->" ,message.payload.decode('utf-8'))
    print("message topic =",message.topic)
    
    if (message.topic == CLIENT_MQTT_TOPIC_UPS_ROUTE_B):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_UPS_ROUTE_B + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_UPS_ROUTE_B
        SERVER_USER_PWD = SERVER_DEVICE_KEY_UPS_ROUTE_B
        print(SERVER_TOPIC)
        data = json.loads(message.payload)
        IN_V110_A = str(data['IN_V110_A']) + "A"
        IN_V110_B = str(data['IN_V110_B']) + "A"
        OUT_V110_A = str(data['OUT_V110_A']) + "A"
        OUT_V110_B = str(data['OUT_V110_B']) + "A"
        OUT_V110_C = str(data['OUT_V110_C']) + "A"
        OUT_V110_D = str(data['OUT_V110_D']) + "A"
        OUT_V110_E = str(data['OUT_V110_E']) + "A"
        mqtt_pub = mqtt.Client("CHT-IOT")
        mqtt_pub.username_pw_set(SERVER_USER_NAME, password=SERVER_USER_PWD)
        mqtt_pub.connect(SERVER_MQTT_SERVER, SERVER_MQTT_PORT)
        SERVER_PUB_COMMAND = '[{"id":"IN_V110_A", "value":["' + IN_V110_A + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"IN_V110_B", "value":["' + IN_V110_B + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"OUT_V110_A", "value":["' + OUT_V110_A + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"OUT_V110_B", "value":["' + OUT_V110_B + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"OUT_V110_C", "value":["' + OUT_V110_C + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"OUT_V110_D", "value":["' + OUT_V110_D + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"OUT_V110_E", "value":["' + OUT_V110_E + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        print('------------------------------------------------------')

    if (message.topic == CLIENT_MQTT_TOPIC_UPS_ROUTE_A):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_UPS_ROUTE_A + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_UPS_ROUTE_A
        SERVER_USER_PWD = SERVER_DEVICE_KEY_UPS_ROUTE_A
        print(SERVER_TOPIC)
        data = json.loads(message.payload)
        IN_V110_A = str(data['IN_V110_A']) + "A"
        IN_V110_B = str(data['IN_V110_B']) + "A"
        OUT_V110_A = str(data['OUT_V110_A']) + "A"
        OUT_V110_B = str(data['OUT_V110_B']) + "A"
        OUT_V110_C = str(data['OUT_V110_C']) + "A"
        OUT_V110_D = str(data['OUT_V110_D']) + "A"
        OUT_V110_E = str(data['OUT_V110_E']) + "A"
        mqtt_pub = mqtt.Client("CHT-IOT")
        mqtt_pub.username_pw_set(SERVER_USER_NAME, password=SERVER_USER_PWD)
        mqtt_pub.connect(SERVER_MQTT_SERVER, SERVER_MQTT_PORT)
        SERVER_PUB_COMMAND = '[{"id":"IN_V110_A", "value":["' + IN_V110_A + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"IN_V110_B", "value":["' + IN_V110_B + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"OUT_V110_A", "value":["' + OUT_V110_A + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"OUT_V110_B", "value":["' + OUT_V110_B + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"OUT_V110_C", "value":["' + OUT_V110_C + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"OUT_V110_D", "value":["' + OUT_V110_D + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"OUT_V110_E", "value":["' + OUT_V110_E + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        print('------------------------------------------------------')

    if (message.topic == CLIENT_MQTT_TOPIC_AIR_CONDITION):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_AIR_CONDITION + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_AIR_CONDITION
        SERVER_USER_PWD = SERVER_DEVICE_KEY_AIR_CONDITION
        print(SERVER_TOPIC)
        data = json.loads(message.payload)
        temp = str(data['Temperature']) + "℃"
        humi = str(data['Humidity']) + "%"
        mqtt_pub = mqtt.Client("CHT-IOT")
        mqtt_pub.username_pw_set(SERVER_USER_NAME, password=SERVER_USER_PWD)
        mqtt_pub.connect(SERVER_MQTT_SERVER, SERVER_MQTT_PORT)
        SERVER_PUB_COMMAND = '[{"id":"Humi", "value":["' + humi + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
#        print(SERVER_PUB_COMMAND)
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"Temp", "value":["' + temp + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "."+ micro_second + 'Z"}]'
#        print(SERVER_PUB_COMMAND)
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
#       print(SERVER_PUB_COMMAND)
        print('------------------------------------------------------')

    if (message.topic == CLIENT_MQTT_TOPIC_POWER_METER):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_POWER_METER + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_POWER_METER
        SERVER_USER_PWD = SERVER_DEVICE_KEY_POWER_METER
        print(SERVER_TOPIC)
        data = json.loads(message.payload)
        temp = str(data['Temperature'])
        humi = str(data['Humidity'])
        current = str(data['currents'])
        mqtt_pub = mqtt.Client("CHT-IOT")
        mqtt_pub.username_pw_set(SERVER_USER_NAME, password=SERVER_USER_PWD)
        mqtt_pub.connect(SERVER_MQTT_SERVER, SERVER_MQTT_PORT)
        SERVER_PUB_COMMAND = '[{"id":"Current", "value":["' + current + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "."+ micro_second + 'Z"}, \
        {"id":"Humi", "value":["' + humi + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"},\
         {"id":"Temp", "value":["' + temp + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "."+ micro_second + 'Z"}]'
#       print(SERVER_PUB_COMMAND)
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        print('------------------------------------------------------')
        

    if (message.topic == CLIENT_MQTT_TOPIC_UPS_MONITOR):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_UPS_A + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_UPS_A
        SERVER_USER_PWD = SERVER_DEVICE_KEY_UPS_A
        print(SERVER_TOPIC)
        data = json.loads(message.payload)
        inputStatus = data['input_A']
        inputLine = inputStatus['inputLine_A'] + "線路" 
        inputFreq = inputStatus['inputFreq_A'] + "HZ"
        inputVolt = inputStatus['inputVolt_A'] + "V"
        outputStatus = data['output_A']
        outputLine = outputStatus['outputLine_A'] + "線路"
        outputFreq = outputStatus['outputFreq_A'] + "HZ"
        outputVolt = outputStatus['outputVolt_A']+ "V"
        outputAmp = outputStatus['outputAmp_A']+ "A"
        outputWatt = outputStatus['outputWatt_A']
        outputPercent = outputStatus['outputPercent_A'] + "%"
        battery_status = data['battery_A']['status']
        batteryTemp = battery_status['batteryTemp_A']
        batteryVolt = battery_status['batteryVolt_A'] + "V"
        batteryRemain_Percent = battery_status['batteryRemain_Percent_A'] + "%"
        mqtt_pub = mqtt.Client("CHT-IOT")
        mqtt_pub.username_pw_set(SERVER_USER_NAME, password=SERVER_USER_PWD)
        mqtt_pub.connect(SERVER_MQTT_SERVER, SERVER_MQTT_PORT)
        SERVER_PUB_COMMAND = '[{"id":"batteryRemain_Percent_A", "value":["' + batteryRemain_Percent + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"batteryTemp_A", "value":["' + batteryTemp + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"batteryVolt_A", "value":["' + batteryVolt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"inputFreq_A", "value":["' + inputFreq + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"inputLine_A", "value":["' + inputLine + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"inputVolt_A", "value":["' + inputVolt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"outputAmp_A", "value":["' + outputAmp + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"outputFreq_A", "value":["' + outputFreq + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"outputLine_A", "value":["' + outputLine + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"outputPercent_A", "value":["' + outputPercent + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second+ "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"outputVolt_A", "value":["' + outputVolt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"outputWatt_A", "value":["' + outputWatt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        print('------------------------------------------------------')

        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_UPS_B + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_UPS_B
        SERVER_USER_PWD = SERVER_DEVICE_KEY_UPS_B
        print(SERVER_TOPIC)
        inputStatus = data['input_B']
        inputLine = inputStatus['inputLine_B'] + "線路"
        inputFreq = inputStatus['inputFreq_B'] + "HZ"
        inputVolt = inputStatus['inputVolt_B'] + "V"
        outputStatus = data['output_B']
        outputLine = outputStatus['outputLine_B'] + "線路"
        outputFreq = outputStatus['outputFreq_B'] + "HZ"
        outputVolt = outputStatus['outputVolt_B'] + "V"
        outputAmp = outputStatus['outputAmp_B'] + "A"
        outputWatt = outputStatus['outputWatt_B']
        outputPersent = outputStatus['outputPercent_B'] + "%"
        battery_status = data['battery_B']['status']
        batteryTemp = battery_status['batteryTemp_B']
        batteryVolt = battery_status['batteryVolt_B'] + "V"
        batteryRemain_Percent = battery_status['batteryRemain_Percent_B'] + "%"

        mqtt_pub = mqtt.Client("CHT-IOT")
        mqtt_pub.username_pw_set(SERVER_USER_NAME, password=SERVER_USER_PWD)
        mqtt_pub.connect(SERVER_MQTT_SERVER, SERVER_MQTT_PORT)
        SERVER_PUB_COMMAND = '[{"id":"batteryRemain_Percent_B", "value":["' + batteryRemain_Percent + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"batteryTemp_B", "value":["' + batteryTemp + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"batteryVolt_B", "value":["' + batteryVolt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"inputFreq_B", "value":["' + inputFreq + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"inputLine_B", "value":["' + inputLine + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"inputVolt_B", "value":["' + inputVolt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"outputAmp_B", "value":["' + outputAmp + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"outputFreq_B", "value":["' + outputFreq + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"outputLine_B", "value":["' + outputLine + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"outputPercent_B", "value":["' + outputPercent + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second+ "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"outputVolt_B", "value":["' + outputVolt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        time.sleep(0.1)
        SERVER_PUB_COMMAND = '[{"id":"outputWatt_B", "value":["' + outputWatt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        print('------------------------------------------------------')
    
    if (message.topic == CLIENT_MQTT_TOPIC_DL303_CO2):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_DL303 + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_DL303
        SERVER_USER_PWD = SERVER_DEVICE_KEY_DL303
        print(SERVER_TOPIC)
        mqtt_pub = mqtt.Client("CHT-IOT")
        mqtt_pub.username_pw_set(SERVER_USER_NAME, password=SERVER_USER_PWD)
        mqtt_pub.connect(SERVER_MQTT_SERVER, SERVER_MQTT_PORT)
        SERVER_PUB_COMMAND = '[{"id":"co2", "value":["' + str(message.payload.decode('utf-8')) + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
        print(SERVER_PUB_COMMAND)
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        print('------------------------------------------------------')

    if (message.topic == CLIENT_MQTT_TOPIC_DL303_DC):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_DL303 + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_DL303
        SERVER_USER_PWD = SERVER_DEVICE_KEY_DL303
        print(SERVER_TOPIC)
        mqtt_pub = mqtt.Client("CHT-IOT")
        mqtt_pub.username_pw_set(SERVER_USER_NAME, password=SERVER_USER_PWD)
        mqtt_pub.connect(SERVER_MQTT_SERVER, SERVER_MQTT_PORT)
        SERVER_PUB_COMMAND = '[{"id":"dewp", "value":["' + str(message.payload.decode('utf-8'))  + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
#       print(SERVER_PUB_COMMAND)
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        print('------------------------------------------------------')

    if (message.topic == CLIENT_MQTT_TOPIC_DL303_RH):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_DL303 + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_DL303
        SERVER_USER_PWD = SERVER_DEVICE_KEY_DL303
        print(SERVER_TOPIC)
        mqtt_pub = mqtt.Client("CHT-IOT")
        mqtt_pub.username_pw_set(SERVER_USER_NAME, password=SERVER_USER_PWD)
        mqtt_pub.connect(SERVER_MQTT_SERVER, SERVER_MQTT_PORT)
        SERVER_PUB_COMMAND = '[{"id":"humi", "value":["' + str(message.payload.decode('utf-8'))  + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
#       print(SERVER_PUB_COMMAND)
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        print('------------------------------------------------------')

    if (message.topic == CLIENT_MQTT_TOPIC_DL303_TC):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_DL303 + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_DL303
        SERVER_USER_PWD = SERVER_DEVICE_KEY_DL303
        print(SERVER_TOPIC)
        mqtt_pub = mqtt.Client("CHT-IOT")
        mqtt_pub.username_pw_set(SERVER_USER_NAME, password=SERVER_USER_PWD)
        mqtt_pub.connect(SERVER_MQTT_SERVER, SERVER_MQTT_PORT)
        SERVER_PUB_COMMAND = '[{"id":"temp", "value":["' + str(message.payload.decode('utf-8'))  + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
#       print(SERVER_PUB_COMMAND)
        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
        print('------------------------------------------------------')

    print('MQTT To Server OK ! -->' , now)
    print('------------------------------------------------------')
    time.sleep(2)


def on_connect_iot(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    SERVER_CONTROL_ET7044 = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_ET7044 + "/sensor"
    print(SERVER_CONTROL_ET7044 + "/sw1" + SERVER_MQTT_TOPIC_END)
    mqtt_sub_iot.subscribe(SERVER_CONTROL_ET7044 + "/sw1" + SERVER_MQTT_TOPIC_END)
    mqtt_sub_iot.subscribe(SERVER_CONTROL_ET7044 + "/sw2" + SERVER_MQTT_TOPIC_END)
    mqtt_sub_iot.subscribe(SERVER_CONTROL_ET7044 + "/sw3" + SERVER_MQTT_TOPIC_END)
    mqtt_sub_iot.subscribe(SERVER_CONTROL_ET7044 + "/sw4" + SERVER_MQTT_TOPIC_END)
    mqtt_sub_iot.subscribe(SERVER_CONTROL_ET7044 + "/sw5" + SERVER_MQTT_TOPIC_END)
    mqtt_sub_iot.subscribe(SERVER_CONTROL_ET7044 + "/sw6" + SERVER_MQTT_TOPIC_END)
    mqtt_sub_iot.subscribe(SERVER_CONTROL_ET7044 + "/sw7" + SERVER_MQTT_TOPIC_END)
    mqtt_sub_iot.subscribe(SERVER_CONTROL_ET7044 + "/sw8" + SERVER_MQTT_TOPIC_END)

def on_message_iot(client, userdata, message):
    print('------------------------------------------------------')
    print("message received -->" ,message.payload.decode('utf-8'))
    print("message topic =",message.topic)
    SERVER_CONTROL_ET7044 = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_ET7044 + "/sensor"
    print(SERVER_CONTROL_ET7044 + "/sw1" + SERVER_MQTT_TOPIC_END)
    if (message.topic == SERVER_CONTROL_ET7044 + "/sw1" + SERVER_MQTT_TOPIC_END):
        control = json.loads(message.payload.decode('utf-8'))["value"][0]
        if(str(control) == "1"): ET7044_CONTROL[0] = True
        if(str(control) == "0"): ET7044_CONTROL[0] = False
        print("sw1 ==>", ET7044_CONTROL[0])
    if (message.topic == SERVER_CONTROL_ET7044 + "/sw2" + SERVER_MQTT_TOPIC_END):
        control = json.loads(message.payload.decode('utf-8'))["value"][0]
        if(str(control) == "1"): ET7044_CONTROL[1] = True
        if(str(control) == "0"): ET7044_CONTROL[1] = False
        print("sw2 ==>", ET7044_CONTROL[1])
    if (message.topic == SERVER_CONTROL_ET7044 + "/sw3" + SERVER_MQTT_TOPIC_END):
        control = json.loads(message.payload.decode('utf-8'))["value"][0]
        if(str(control) == "1"): ET7044_CONTROL[2] = True
        if(str(control) == "0"): ET7044_CONTROL[2] = False
        print("sw3 ==>", ET7044_CONTROL[2])
    if (message.topic == SERVER_CONTROL_ET7044 + "/sw4" + SERVER_MQTT_TOPIC_END):
        control = json.loads(message.payload.decode('utf-8'))["value"][0]
        if(str(control) == "1"): ET7044_CONTROL[3] = True
        if(str(control) == "0"): ET7044_CONTROL[3] = False
        print("sw4 ==>", ET7044_CONTROL[3])
    if (message.topic == SERVER_CONTROL_ET7044 + "/sw5" + SERVER_MQTT_TOPIC_END):
        control = json.loads(message.payload.decode('utf-8'))["value"][0]
        if(str(control) == "1"): ET7044_CONTROL[4] = True
        if(str(control) == "0"): ET7044_CONTROL[4] = False
        print("sw5 ==>", ET7044_CONTROL[4])
    if (message.topic == SERVER_CONTROL_ET7044 + "/sw6" + SERVER_MQTT_TOPIC_END):
        control = json.loads(message.payload.decode('utf-8'))["value"][0]
        if(str(control) == "1"): ET7044_CONTROL[5] = True
        if(str(control) == "0"): ET7044_CONTROL[5] = False
        print("sw6 ==>", ET7044_CONTROL[5])
    if (message.topic == SERVER_CONTROL_ET7044 + "/sw7" + SERVER_MQTT_TOPIC_END):
        control = json.loads(message.payload.decode('utf-8'))["value"][0]
        if(str(control) == "1"): ET7044_CONTROL[6] = True
        if(str(control) == "0"): ET7044_CONTROL[6] = False
        print("sw7 ==>", ET7044_CONTROL[6])
    if (message.topic == SERVER_CONTROL_ET7044 + "/sw8" + SERVER_MQTT_TOPIC_END):
        control = json.loads(message.payload.decode('utf-8'))["value"][0]
        if(str(control) == "1"): ET7044_CONTROL[7] = True
        if(str(control) == "0"): ET7044_CONTROL[7] = False
        print("sw8 ==>", ET7044_CONTROL[7])
        print('------------------------------------------------------')
        SEND_ET7044_COMMAND = str(ET7044_CONTROL).lower()
        print(SEND_ET7044_COMMAND)
        mqtt_pub_ET7044 = mqtt.Client("NUTC-IMAC-ET7044")
        mqtt_pub_ET7044.connect(CLIENT_MQTT_SERVER, CLIENT_MQTT_PORT)
        mqtt_pub_ET7044.publish(CLIENT_MQTT_TOPIC_ET7044, SEND_ET7044_COMMAND)
        print('------------------------------------------------------')
    





while(1):
    # MQTT connection
    mqtt_sub = mqtt.Client("NUTC-IMAC")
    mqtt_sub.on_message = on_message
    mqtt_sub.on_connect = on_connect
    mqtt_sub.connect(CLIENT_MQTT_SERVER, CLIENT_MQTT_PORT)
    mqtt_sub.loop_start()
    time.sleep(1)
    mqtt_sub.loop_stop()
    mqtt_sub_iot = mqtt.Client("CHT-IOT-CONTROL")
    mqtt_sub_iot.on_message = on_message_iot
    mqtt_sub_iot.on_connect = on_connect_iot
    mqtt_sub_iot.username_pw_set(SERVER_DEVICE_KEY_ET7044, SERVER_DEVICE_KEY_ET7044)
    mqtt_sub_iot.connect(SERVER_MQTT_SERVER, CLIENT_MQTT_PORT)
    mqtt_sub_iot.loop_start()
    time.sleep(1)
    mqtt_sub_iot.loop_stop()
