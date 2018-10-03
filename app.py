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

CLIENT_MQTT_TOPIC_ET7044 = "ET7044/DOstatus"

CLIENT_MQTT_TOPIC_POWER_METER = "current"

CLIENT_MQTT_TOPIC_UPS_MONITOR = "UPS_Monitor"

SERVER_MQTT_SERVER = "tcp://iot.cht.com.tw"
SERVER_MQTT_TOPIC_HEAD = "/v1/device/"
SERVER_MQTT_TOPIC_END = "/rawdata"
SERVER_MQTT_PORT = 1883
SERVER_USER_NAME = ""
SERVER_USER_PWD = ""

SERVER_MQTT_TOPIC_DL303 = "DL303"
SERVER_DEVICE_ID_DL303 = "7839288845"
SERVER_DEVICE_KEY_DL303 = "DK1CSFECPSXST91BKE"

SERVER_MQTT_TOPIC_ET7044 = "ET7044"
SERVER_DEVICE_ID_ET7044 = "7839306572"
SERVER_DEVICE_KEY_ET7044 = "DKST1SRZ3CRBSZUKBF"

SERVER_MQTT_TOPIC_POWER_METER = "PowerMeter"
SERVER_DEVICE_ID_POWER_METER = "7839467604"
SERVER_DEVICE_KEY_POWER_METER = "DK4PA7GA7X55R7PKCB"

SERVER_MQTT_TOPIC_UPS_A = "UPS_A"
SERVER_DEVICE_ID_UPS_A = "7839547792"
SERVER_DEVICE_KEY_UPS_A = "DKF2SHXUGUU7942KZ3"

SERVER_MQTT_TOPIC_UPS_B = "UPS_B"
SERVER_DEVICE_ID_UPS_B = "7839666288"
SERVER_DEVICE_KEY_UPS_B = "DKTGWYSE0GCMG2ZFYC"


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

    print('------------------------------------------------------')
    print("message received " ,message.payload.decode('utf-8'))
    print("message topic=",message.topic)

    if (message.topic == CLIENT_MQTT_TOPIC_POWER_METER):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_POWER_METER + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_POWER_METER
        SERVER_USER_PWD = SERVER_DEVICE_KEY_POWER_METER
        print(SERVER_TOPIC)
        data = json.loads(message.payload)
        temp = str(data['Temperature'])
        humi = str(data['Humidity'])
        current = str(data['currents'])
        SERVER_PUB_COMMAND = '[{"id":"Current", "value":["' + temp + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"Humi", "value":["' + humi + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"Temp", "value":["' + temp + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}]'
        print(SERVER_PUB_COMMAND)

    if (message.topic == CLIENT_MQTT_TOPIC_UPS_MONITOR):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_UPS_A + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_UPS_A
        SERVER_USER_PWD = SERVER_DEVICE_KEY_UPS_A
        print(SERVER_TOPIC)
        data = json.loads(message.payload)
        inputStatus = data['input_A']
        inputLine = inputStatus['inputLine_A']
        inputFreq = inputStatus['inputFreq_A']
        inputVolt = inputStatus['inputVolt_A']
        outputStatus = data['output_A']
        outputLine = outputStatus['outputLine_A']
        outputFreq = outputStatus['outputFreq_A']
        outputVolt = outputStatus['outputVolt_A']
        outputAmp = outputStatus['outputAmp_A']
        outputWatt = outputStatus['outputWatt_A']
        outputPercent = outputStatus['outputPercent_A']
        battery_status = data['battery_A']['status']
        batteryHealth = battery_status['batteryHealth_A']
        batteryTemp = battery_status['batteryTemp_A']
        batteryVolt = battery_status['batteryVolt_A']
        batteryRemain_Percent = battery_status['batteryRemain_Percent_A']

        SERVER_PUB_COMMAND = '[{"id":"batteryRemain_Percent_A", "value":["' + batteryRemain_Percent + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"batteryTemp_A", "value":["' + batteryTemp + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"batteryVolt_A", "value":["' + batteryVolt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"inputFreq_A", "value":["' + inputFreq + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"inputLine_A", "value":["' + inputLine + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"inputVolt_A", "value":["' + inputVolt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"outputAmp_A", "value":["' + outputAmp + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"outputFreq_A", "value":["' + outputFreq + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"outputLine_A", "value":["' + outputLine + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"outputPercent_A", "value":["' + outputPercent + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"outputVolt_A", "value":["' + outputVolt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"outputWatt_A", "value":["' + outputWatt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}]'
        print(SERVER_PUB_COMMAND)

        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_UPS_B + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_UPS_B
        SERVER_USER_PWD = SERVER_DEVICE_KEY_UPS_B
        print(SERVER_TOPIC)
        inputStatus = data['input_B']
        inputLine = inputStatus['inputLine_B']
        inputFreq = inputStatus['inputFreq_B']
        inputVolt = inputStatus['inputVolt_B']
        outputStatus = data['output_B']
        outputLine = outputStatus['outputLine_B']
        outputFreq = outputStatus['outputFreq_B']
        outputVolt = outputStatus['outputVolt_B']
        outputAmp = outputStatus['outputAmp_B']
        outputWatt = outputStatus['outputWatt_B']
        outputPersent = outputStatus['outputPercent_B']
        battery_status = data['battery_B']['status']
        batteryHealth = battery_status['batteryHealth_B']
        batteryTemp = battery_status['batteryTemp_B']
        batteryVolt = battery_status['batteryVolt_B']
        batteryRemain_Percent = battery_status['batteryRemain_Percent_B']

        SERVER_PUB_COMMAND = '[{"id":"batteryRemain_Percent_B", "value":["' + batteryRemain_Percent + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"batteryTemp_B", "value":["' + batteryTemp + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"batteryVolt_B", "value":["' + batteryVolt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"inputFreq_B", "value":["' + inputFreq + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"inputLine_B", "value":["' + inputLine + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"inputVolt_B", "value":["' + inputVolt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"outputAmp_B", "value":["' + outputAmp + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"outputFreq_B", "value":["' + outputFreq + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"outputLine_B", "value":["' + outputLine + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"outputPercent_B", "value":["' + outputPercent + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"outputVolt_B", "value":["' + outputVolt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"outputWatt_B", "value":["' + outputWatt + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}]'
        print(SERVER_PUB_COMMAND)

    if (message.topic == CLIENT_MQTT_TOPIC_DL303_CO2):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_DL303 + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_DL303
        SERVER_USER_PWD = SERVER_DEVICE_KEY_DL303
        print(SERVER_TOPIC)
#        mqtt_pub = mqtt.Client("CHT-IOT")
#        mqtt_pub.username_pw_set(SERVER_USER_NAME, password=SERVER_USER_PWD)
#        mqtt_pub.connect(SERVER_MQTT_SERVER, SERVER_MQTT_PORT)
        SERVER_PUB_COMMAND = '{"id":"co2", "value":["' + str(message.payload.decode('utf-8')) + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}'
        print(SERVER_PUB_COMMAND)
#        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)

    if (message.topic == CLIENT_MQTT_TOPIC_DL303_DC):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_DL303 + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_DL303
        SERVER_USER_PWD = SERVER_DEVICE_KEY_DL303
        print(SERVER_TOPIC)
#        mqtt_pub = mqtt.Client("CHT-IOT")
#        mqtt_pub.username_pw_set(SERVER_USER_NAME, password=SERVER_USER_PWD)
#        mqtt_pub.connect(SERVER_MQTT_SERVER, SERVER_MQTT_PORT)
        SERVER_PUB_COMMAND = '{"id":"dewp", "value":["' + str(message.payload.decode('utf-8')) + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}'
        print(SERVER_PUB_COMMAND)
#        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
    if (message.topic == CLIENT_MQTT_TOPIC_DL303_RH):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_DL303 + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_DL303
        SERVER_USER_PWD = SERVER_DEVICE_KEY_DL303
        print(SERVER_TOPIC)
#        mqtt_pub = mqtt.Client("CHT-IOT")
#        mqtt_pub.username_pw_set(SERVER_USER_NAME, password=SERVER_USER_PWD)
#        mqtt_pub.connect(SERVER_MQTT_SERVER, SERVER_MQTT_PORT)
        SERVER_PUB_COMMAND = '{"id":"humi", "value":["' + str(message.payload.decode('utf-8')) + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}'
        print(SERVER_PUB_COMMAND)
#        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
    if (message.topic == CLIENT_MQTT_TOPIC_DL303_TC):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_DL303 + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_DL303
        SERVER_USER_PWD = SERVER_DEVICE_KEY_DL303
        print(SERVER_TOPIC)
#        mqtt_pub = mqtt.Client("CHT-IOT")
#        mqtt_pub.username_pw_set(SERVER_USER_NAME, password=SERVER_USER_PWD)
#        mqtt_pub.connect(SERVER_MQTT_SERVER, SERVER_MQTT_PORT)
        SERVER_PUB_COMMAND = '{"id":"temp", "value":["' + str(message.payload.decode('utf-8')) + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}'
        print(SERVER_PUB_COMMAND)
#        mqtt_pub.publish(SERVER_TOPIC, SERVER_PUB_COMMAND)
    if (message.topic == CLIENT_MQTT_TOPIC_ET7044):
        SERVER_TOPIC = SERVER_MQTT_TOPIC_HEAD + SERVER_DEVICE_ID_ET7044 + SERVER_MQTT_TOPIC_END
        SERVER_USER_NAME = SERVER_DEVICE_KEY_ET7044
        SERVER_USER_PWD = SERVER_DEVICE_KEY_ET7044
        print(SERVER_TOPIC)
        sw = ["0", "0", "0", "0", "0", "0", "0", "0"]
        message = message.payload.decode('utf8').split("[")[1].split("]")[0]
        for x in range(0, 8):
            status = message.split(",")[x]
#            print(status)
            if (status == "false"): sw[x] = "0"
            else: sw[x] = "1"
#            print(sw[x])
        SERVER_PUB_COMMAND = '[{"id":"sw1", "value":["' + sw[0] + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"sw2", "value":["' + sw[1] + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"sw3", "value":["' + sw[2] + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"sw4", "value":["' + sw[3] + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"sw5", "value":["' + sw[4] + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"sw6", "value":["' + sw[5] + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"sw7", "value":["' + sw[6] + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}, \
                            {"id":"sw8", "value":["' + sw[7] + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + '"}]'
        print(SERVER_PUB_COMMAND)

    print('MQTT To Server OK ! -->' , now)
    print('------------------------------------------------------')

# MQTT connection
mqtt_sub = mqtt.Client("NUTC-IMAC")
mqtt_sub.on_message = on_message
mqtt_sub.connect(CLIENT_MQTT_SERVER, CLIENT_MQTT_PORT)
mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_DL303_CO2)
mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_DL303_DC)
mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_DL303_RH)
mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_DL303_TC)
mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_ET7044)
mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_POWER_METER)
mqtt_sub.subscribe(CLIENT_MQTT_TOPIC_UPS_MONITOR)
mqtt_sub.loop_forever()