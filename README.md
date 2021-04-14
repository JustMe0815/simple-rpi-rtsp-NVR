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
