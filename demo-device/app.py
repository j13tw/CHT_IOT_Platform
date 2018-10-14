#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

import serial, time
import json
import datetime
import paho.mqtt.client as mqtt

# MQTT setup data
MQTT_SERVER = "iot.cht.com.tw"
MQTT_PORT = 1883
MQTT_SERVER_HEAD = "/v1/device/"
MQTT_DATA_COMMAND_END = "/rawdata"
MQTT_CONTROL_DEVICE_ID = "Relay"
MQTT_CONTROL_COMMAND_END = "/sensor/" + MQTT_CONTROL_DEVICE_ID + "/rawdata"
MQTT_DEVICE_TOPIC = "7864192663"
MQTT_SERVER_KEY= "DKB93XG0K3G7BGTB00"

MQTT_TOPIC = MQTT_SERVER_HEAD + MQTT_DEVICE_TOPIC
print(MQTT_SERVER)
demo = serial.Serial()
response_send = ["", "", "", "", ""]
pre_status = "0"
new_status = 0
topic_count = 0

def on_message(client, userdata, message):
	global demo, pre_status, control, new_status, topic_count
	print("on message new_status ==> ", new_status)
	print('------------------------------------------------------')
	print("message received -->" ,message.payload.decode('utf-8'))
	print("message topic =",message.topic)
	if(message.topic == "/v1/device/7864192663/sensor/Relay/rawdata" and topic_count == 0):
		control = json.loads(message.payload.decode("utf-8"))["value"][0]
	#	print(type(str(control)), control)
		topic_count = topic_count + 1
		if (str(control) == "1" and str(control) != pre_status): 
			demo.write(b"A")
			pre_status = str(control)
			new_status = 1
			print("ON")
		if (str(control) == "0" and str(control) != pre_status): 
			demo.write(b"Y")
			pre_status = str(control)
			new_status = 1
			print("OFF")

		print("control ON/OFF ==> ", control)

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	mqtt_sub.subscribe(MQTT_TOPIC + MQTT_CONTROL_COMMAND_END)


while(1):
	error = 0
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
	if(demo.is_open):
		response = demo.readline()
#		print(response)
		response = response.decode('utf-8')
#		print(response)
		if (response != ""):
			response = response.split("{")[1].split("}")[0]
			response = "{" + response + "}"
		else:
			error = 1
		print(response)
		if(error == 0):
			response_json = json.loads(response)
			Humi = str(response_json["Humidity"])
			Temp = str(response_json["Temperature"])
			Current = str(response_json["currents"])
			Relay = str(response_json["control_A"])
			Light = str(response_json["control_B"])
			response_send[0] = '[{"id":"Humi", "value":["' + Humi + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
			response_send[1] = '[{"id":"Temp", "value":["' + Temp + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
			response_send[2] = '[{"id":"Current", "value":["' + Current + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
			response_send[3] = '[{"id":"Light", "value":["' + Light + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
			response_send[4] = '[{"id":"Relay", "value":["' + pre_status + '"], "time":"' + year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "." + micro_second + 'Z"}]'
			print(response_send[4])
		if (error == 0):
			print('------------------------------------------------------')
			try:
				# MQTT connection
				mqtt_pub = mqtt.Client("CHT-IOT")
				mqtt_pub.username_pw_set(MQTT_SERVER_KEY, MQTT_SERVER_KEY)
				mqtt_pub.connect(MQTT_SERVER, MQTT_PORT)
				mqtt_pub.publish(MQTT_TOPIC +  MQTT_DATA_COMMAND_END, response_send[0])
				print('------------------------------------------------------1')
				time.sleep(0.1)
				mqtt_pub.publish(MQTT_TOPIC + MQTT_DATA_COMMAND_END, response_send[1])
				print('------------------------------------------------------2')
				time.sleep(0.1)
				mqtt_pub.publish(MQTT_TOPIC + MQTT_DATA_COMMAND_END, response_send[2])
				print('------------------------------------------------------3')
				time.sleep(0.1)
				mqtt_pub.publish(MQTT_TOPIC + MQTT_DATA_COMMAND_END, response_send[3])
				print('------------------------------------------------------4')
				time.sleep(0.1)
				print("new_status ==> ", new_status)
				if(new_status == 1):
					mqtt_pub.publish(MQTT_TOPIC + MQTT_DATA_COMMAND_END, response_send[4])
					print('------------------------------------------------------4')
					time.sleep(0.1)
					new_status = 0
				now = datetime.datetime.now()
				print('MQTT To Server OK ! -->' , now)
			except:
				print('MQTT To Server Error !')
			print('------------------------------------------------------')
	else:
		try:
			demo = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
		except:
			demo = serial.Serial()
			time.sleep(1)
	print(MQTT_TOPIC, MQTT_CONTROL_COMMAND_END)

	# MQTT connection
	mqtt_sub = mqtt.Client("NUTC-IMAC")
	mqtt_sub.on_connect = on_connect
	mqtt_sub.on_message = on_message
	mqtt_sub.username_pw_set(MQTT_SERVER_KEY, MQTT_SERVER_KEY)
	mqtt_sub.connect(MQTT_SERVER, MQTT_PORT)
	mqtt_sub.loop_start()
	time.sleep(1)
	mqtt_sub.loop_stop()
	topic_count = 0
