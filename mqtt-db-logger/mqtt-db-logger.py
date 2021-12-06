#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import sys
import datetime
import json
import paho.mqtt.client as mqtt
from mqtt_db_logger_conf import *
import time

print ("Brocker address : " + mqtt_brocker) 


def debugprint (string):
	print  (string)
	
def db_connection (db_srvname,db_name,db_username,db_user_pwd):
	try:
		con = mdb.connect(db_srvname, db_username, db_user_pwd, db_name)
	except con.Error as err:
		print("Something went wrong: {}".format(err))
		sys.exit(1)
	return con


def pressure_compensed (pressure,altitude):
	new_pressure =float (pressure) + (float (altitude) * 0.12)
	debugprint ("Calculating altitude correction for pressure : " + str(new_pressure))
	return new_pressure

def db_create_table (json_dic,db_connection_obj):
#create  table
	db_table_name=json_dic["deviceid"]
	debugprint ("Creating table : %s" %(db_table_name))
	cursor = db_connection_obj.cursor ()
	cursor.execute("""CREATE TABLE IF NOT EXISTS %s  (
	id int NOT NULL AUTO_INCREMENT,
	deviceid VARCHAR (40) DEFAULT Null,
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	brocker_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id))""" %(db_table_name)) 
	db_connection_obj.commit()
	cursor.close ()

def db_create_settings_table (json_dic,db_connection_obj):
#create  table
	db_table_name=json_dic["deviceid"] + "_settings"
	debugprint ("Creating table : %s" %(db_table_name))
	cursor = db_connection_obj.cursor ()
	cursor.execute("""CREATE TABLE IF NOT EXISTS %s  (
	latitude VARCHAR (40) DEFAULT 0,
	longitude VARCHAR (40) DEFAULT 0,
	battery_offset VARCHAR (40) DEFAULT 0,
	altitude VARCHAR (40) DEFAULT 0)""" %(db_table_name)) 
	db_connection_obj.commit()
	cursor.close ()
	
def db_create_cumulative_table (json_dic,db_connection_obj):
#create  table
	db_table_name=json_dic["deviceid"] + "_cumul"
	debugprint ("Creating table : %s" %(db_table_name))
	cursor = db_connection_obj.cursor ()
	cursor.execute("""CREATE TABLE IF NOT EXISTS %s (
	deviceid VARCHAR (40) DEFAULT Null,
	timestamp2 DATETIME DEFAULT CURRENT_TIMESTAMP,
	record_type VARCHAR (40) DEFAULT 'daily',
	energy FLOAT DEFAULT 0,
	energy2 FLOAT DEFAULT 0,
	PRIMARY KEY (timestamp2,record_type))""" %(db_table_name))
	db_connection_obj.commit()
	cursor.close ()

def db_get_setting (db_connection_obj,db_table,setting):
	
	try:
		query="""SELECT %s FROM %s LIMIT 1""" %(setting, db_table)
		cursor = db_connection_obj.cursor ()
		cursor.execute(query)
		row=cursor.fetchone()
		debugprint ("Read setting:%s Value:%s" %  (setting, row[0]))
		return row[0]
	except Exception as exep: 
		print(exep)
		debugprint ("-----> Error reading setting %s" %(setting))
		return 0
		pass
	
	
def db_create_columns (json_dic,db_connection_obj):
	db_table_name=json_dic["deviceid"]
	cursor = db_connection_obj.cursor ()
	for  column in json_dic:
		print ("Create column : " + column)
		try:
			query="""ALTER TABLE %s ADD  %s  FLOAT DEFAULT Null;""" %(db_table_name,column)
			cursor.execute(query)
			db_connection_obj.commit()
		except:
			pass
	cursor.close ()

def db_read_last_value (db_connection_obj,db_table,column):
	cursor = db_connection_obj.cursor ()
	debugprint ("Read last value : " + column)
	try:
		query="""SELECT brocker_timestamp ,%s  FROM %s ORDER BY id DESC LIMIT 1""" %(column, db_table)
		cursor.execute(query)
		row=cursor.fetchone()
		debugprint ("Read last row : " + str (row))
		return row
	except Exception as exep:
		print (exep)
		return [datetime.datetime.now(),0]
		pass
	cursor.close ()





def add_quotes (mystring):
	return "'"+str(mystring)+"'"

	
def db_insert_json (json_dic,db_connection_obj):
	db_table=json_dic["deviceid"]
	cols=",".join(json_dic.keys ())
	vals_with_quotes = map (add_quotes,json_dic.values ()) 
	vals_str=','.join(vals_with_quotes)
	query = """INSERT INTO %s  (%s) VALUES (%s) """ %(db_table, cols,vals_str)
	cursor = db_connection_obj.cursor ()
	cursor.execute(query)
	db_connection_obj.commit()

def db_insert_cumulative (json_dic,db_connection_obj,cumulative_field):
	db_table=json_dic["deviceid"] + "_cumul"
	try:
		query = """INSERT INTO %s (timestamp2,record_type,%s) VALUES ("%s","%s",%s) """ %(db_table,cumulative_field,date_to_day(datetime.datetime.now()),"daily",json_dic[cumulative_field])
		cursor = db_connection_obj.cursor ()
		cursor.execute(query)
		db_connection_obj.commit()
	except:
		query = """UPDATE %s SET %s=%s + %s WHERE timestamp2="%s" and record_type= "%s" """ %(db_table,cumulative_field,cumulative_field,json_dic[cumulative_field],date_to_day(datetime.datetime.now()),"daily")
		print (query)
		cursor = db_connection_obj.cursor ()
		cursor.execute(query)
		db_connection_obj.commit()
		pass

def date_to_day (date_obj):
	return date_obj.strftime ('%Y-%m-%d')

def db_log_msg (json_dic,db_srvname,db_name,db_username,db_user_pwd):
# logging msg to db
	db_table=json_dic["deviceid"]
	db_table_settings=db_table + "_settings"
	try:
		db_connection_obj=db_connection (db_srvname,db_name,db_username,db_user_pwd)
#create settings table
		db_create_settings_table (json_dic,db_connection_obj)
		db_create_cumulative_table (json_dic,db_connection_obj)
		if "power" in json_dic:
			column="power"
			lastrow=db_read_last_value (db_connection_obj,db_table,column)
			energy=calc_integral (lastrow[0],lastrow[1],datetime.datetime.now(),json_dic[column])
			debugprint ("Energy :" + str (energy))
			json_dic['energy']= energy
			db_create_cumulative_table (json_dic,db_connection_obj)
			db_insert_cumulative (json_dic,db_connection_obj,"energy")

		if "pressure" in json_dic:
			src_pressure=json_dic["pressure"]
			altitude=db_get_setting (db_connection_obj,db_table_settings,"altitude")
			tgt_pressure=pressure_compensed (src_pressure, altitude)
			json_dic.update({'pressure': tgt_pressure})
			#json_dic["pressure"]=pressure_compensed (json_dic["pressure"], db_get_setting (db_connection_obj,db_table_settings,"altitude"))

# insert data mesures
		db_create_table(json_dic,db_connection_obj)
		db_create_columns(json_dic,db_connection_obj)
		db_insert_json(json_dic,db_connection_obj)
		db_connection_obj.close()
	except Exception as exep:
		print (exep)
		pass


# calculate surface (power)
def calc_integral (time1,value1,time2,value2):
	debugprint ("Calculating power : %s --- %s --- %s ---  %s" %(time1,value1,time2,value2))
	deltatime = (time2 - time1).total_seconds()
	result = ((value1 + value2) / 2) * (deltatime)
	debugprint ("Calculating power deltatime: %s, energy :%s" %(deltatime, result))
	return result

# main

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("xavfan/data")

def on_message(client, userdata, msg):
	global db_srvname,db_name,db_username,db_user_pwd
	mqtt_msg_str=msg.payload.decode()
	print ("Message received : " + mqtt_msg_str)
	json_msg=json.loads (mqtt_msg_str)
	db_log_msg (json_msg,db_srvname,db_name,db_username,db_user_pwd)
	#client.disconnect()
    
client = mqtt.Client()

connected = False
while not connected :
	try:
		client.connect(mqtt_brocker,1883,60)
		client.on_connect = on_connect
		client.on_message = on_message
		client.loop_forever()
		connected = True
	except:
		print ("Connection error")
		time.sleep (5)







