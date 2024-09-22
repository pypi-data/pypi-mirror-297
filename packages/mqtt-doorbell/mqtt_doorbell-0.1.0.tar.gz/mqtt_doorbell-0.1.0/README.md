# Simple MQTT Door Bell 
A simple Linux-based doorbell, which plays the mp3 bell ringtone upon receiving 
a MQTT message.

The main idea is to create a system service, which can play an audio file
upon receiving the message from the MQTT message broker. This may be useful
for configuring sound notifications or alarms in the Home Assistant 
automations.

## Supported platforms
This solution has been tested on Ubuntu 22.04, but most likely will work on 
other Linux distros, with minor changes.

## Prerequisites

1. Mosquitto MQTT message broker installed and accessible from the deployment
   machine.
   
2. MP3 player utility, which can play mp3 files from the command line, installed
   on the host machine. I used mpg123 but other options should work as well.
   
3. Python verison >= 3.10 

## Installation


## Configuration



