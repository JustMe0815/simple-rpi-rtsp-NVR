# simple-rpi-rtsp-NVR is a Self-hosted NVR solution
This is a simple Python script to use a Raspberry Pi, any other Linux machine or even Windows machines as NVR (Network Video Recorder).
The Code will connect to your configured rtsp streams and saves the video files (chunks) to a storage location.
The code will also connect to a MQTT server and will publish to a assigned topic. For example: FilePath,FileSize,Status.

# Notable features
- Records RTSP streams
- Simultaneous Recordings
- Variable Chunk Size
- Sorted by Year/Month/Day/Hour
- Home Assistant/iobroker integration via MQTT
- MQTT publish status idle/recording/error
- MQTT publish FileSize/FilePath
- easy configuration via yaml config file.

# Configuration
Configuration of RTSP Streams, file location, chunk size, MQTT connection can be set within the config.yml file.

- For example:
   ```
   cameras:
     Camera1:
       Name: FrontDoor
       IP: 192.168.103.10
       Port: 554
       Path: /ch0_0.264
       User: USERNAME
       Password: PASSWORD
       Width: 1920
       Height: 1080
       Fps: 25
     Camera2:
       Name: Garage
       IP: 192.168.103.11
       Port: 554
       Path: /ch0_0.264
       User: USERNAME
       Password: PASSWORD
       Width: 1920
       Height: 1080
       Fps: 25
   Recorder:
     Path: /PATH/TO/surveillance/recordings
     Chunks: 300
   MQTT:
     Enabled: True
     ClientID: RTSP-Recoder
     IP: 192.168.100.99
     Port: 1886
     User: USERNAME
     Password: PASSWORD
     Topic: Surveillance/Recorder
     ```

# Start-up
 Once configured, you can then start the script by typing:

```
python3 recorder.py
```

# Prerequisites
On Debian/Ubuntu
```
sudo apt update && sudo apt install openRTSP pip3
```
```
pip3 install paho-mqtt pyyaml
```
