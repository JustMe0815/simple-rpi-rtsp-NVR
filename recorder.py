import yaml
import subprocess
import time
import os
import signal
import argparse
import datetime
from datetime import date
import paho.mqtt.client as mqtt
import threading
from os import fork
with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
#Recorder Info
Recorder_Path=str(cfg["Recorder"]["Path"])
Recorder_Chunks=cfg["Recorder"]["Chunks"]
Recorder={}
firstrun=True
# Change to correct directory
os.chdir(Recorder_Path)
#MQTT Info
MQTT_Enabled=cfg["MQTT"]["Enabled"]
MQTT_ClientID=str(cfg["MQTT"]["ClientID"])
MQTT_IP=str(cfg["MQTT"]["IP"])
MQTT_Port=cfg["MQTT"]["Port"]
MQTT_User=str(cfg["MQTT"]["User"])
MQTT_Password=str(cfg["MQTT"]["Password"])
MQTT_Topic=str(cfg["MQTT"]["Topic"])
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client = mqtt.Client(MQTT_ClientID)
client.connect(MQTT_IP, MQTT_Port, 60)
client.loop_start()
def run():
    global checkthis
    checkthis=False
    start_recording()

def return_filename():
    # Creates a filename with the start time
    # of recording in its name
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    fl = current_time.replace(' ', '_')
    fl = fl.replace(':', '-')
    return fl

def chunk_timer(camera,full_path,Camera_Name):
    global proc
    global checkthis
    global client
    print('Send termination signal')
    if MQTT_Enabled == True:
	  # MQTT Publish FileName
      filesize = str(round(os.path.getsize(full_path) / (1024 * 1024), 2))
      print('FILE SIZE IS '+filesize+'MB')
      client.publish(MQTT_Topic+'/'+Camera_Name+'/FileSize', filesize +'MB')
      client.publish(MQTT_Topic+'/'+Camera_Name+'/Status', 'idle')
    proc.send_signal(signal.SIGHUP)
    time.sleep(1)
    os.kill(proc.pid, signal.SIGTERM)
    print(camera+' Killed')
    Recorder[camera] = False
    start_recording()

def start_recording():
    global checkthis
    global proc
    global firstrun
    global Recorder
    global client
    if firstrun == True:
        for camera in cfg["cameras"]:
            Recorder[camera]=False
        firstrun = False
    if firstrun == False:
        for camera in cfg["cameras"]:
            if Recorder[camera] == False:
                Recorder[camera] = True
                #Camera Info
                Camera_Name=str(cfg["cameras"][camera]["Name"])
                Camera_IP=str(cfg["cameras"][camera]["IP"])
                Camera_Port=str(cfg["cameras"][camera]["Port"])
                Camera_Path=str(cfg["cameras"][camera]["Path"])
                Camera_User=str(cfg["cameras"][camera]["User"])
                Camera_Password=str(cfg["cameras"][camera]["Password"])
                Camera_Width=cfg["cameras"][camera]["Width"]
                Camera_Height=cfg["cameras"][camera]["Height"]
                Camera_Fps=cfg["cameras"][camera]["Fps"]
                rtsp_url='rtsp://'+Camera_User+':'+Camera_Password+'@'+Camera_IP+':'+Camera_Port+Camera_Path
                common =' -4 -B 10000000 -b 10000000 -f %d -w %d -h %d -t -V -d %d %s' % (Camera_Fps,Camera_Width,Camera_Height,Recorder_Chunks,rtsp_url)
                filename = return_filename()
                now = datetime.datetime.now()
                currentyear = datetime.datetime.today().year
                currentmonth = datetime.datetime.today().month
                currentday = datetime.datetime.today().day
                current_path = os.getcwd()
                outdir = './%s/%s/%s/%s/%s' % (Camera_Name, currentyear, currentmonth, currentday, now.hour)
                isdir =  os.path.isdir('./%s/%s/%s/%s/%s' % (Camera_Name, currentyear, currentmonth, currentday, now.hour))
                full_path = current_path + '/%s/%s/%s/%s/%s/%s.mp4' % (Camera_Name, currentyear, currentmonth, currentday, now.hour, filename)
                if isdir == False:
                    os.system('mkdir -p %s' % outdir)
                outfile = './%s/%s.mp4' % (outdir, filename)
                if MQTT_Enabled == True:
                  # MQTT Publish FileName
                 client.publish(MQTT_Topic+'/'+Camera_Name+'/Status', 'recording')
                 client.publish(MQTT_Topic+'/'+Camera_Name+'/FilePath', full_path)
                # Create the openRTSP command and its parameters
                cmd = 'openRTSP ' + common
                cmd = cmd.split(' ')
                cmd = [ix for ix in cmd if ix != '']
                st = time.time()
                with open(outfile,"wb") as outp:
                  proc = subprocess.Popen(cmd, shell=False,stdin=None, stdout=outp, stderr=None, close_fds=True)
                  print(Camera_Name+' Recording started!')
                  threading.Timer(Recorder_Chunks, chunk_timer,[camera,full_path,Camera_Name]).start()

run()
client.loop_forever()
