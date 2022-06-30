# HeleLora
Drone Aided Device-to-Device Networks for Communications and Health Connectivity


<p align="center"> 
<img src="https://github.com/gadm21/HeleLora/blob/main/assets/images/project_overview.png">
</p>


# Introduction
This project provides a proof-of-concept to a device-to-device network that can be deployed in rural areas with no internet coverage, or during temporary loss of internet coverage due to accidents or disasters. To connect the unconnected, we rely on drones and lora modules. Drones are not constrained by geogrphical barriers and LoRa modules can communicate over long distances (up to 20 km for Line Of Sight (LOS) communication). We use health monitoring as an example of how the proposed network can be useful in collecting data from wearable devices from the residents of a rural area that lacks internet infrastructure.

# Structure
In the src directory you will find two sub-directories: Data_collection and lora. The Data_collection directory contains python scripts that connects to a band 4, collects a supervised dataset for composed of the timeseries readings: heart rate and gyroscope, in addition to an activity label assigned by the user. The activities recognized are: exercising, sleeping, and studying, which are given the labels: 1, 2, 3, respectively. 
Data collection duration is pre-defined in a variable called activities_durations in the listen_to_buttons.py script.

The lora sub-directory has python scripts that send a txt file, line by line, from lora node A to lora node B, given the address of lora node B. 

# Usage

This repository is only tested on linux. 

## Data Collection
- Clone this repository: `git clone https://github.com/gadm21/HeleLora`
- Authentication key and MAC address of the Miband4 are needed to access it and retrieve sensor readings. Refer to [freemyband website] (https://www.freemyband.com) to acquire them. They should be put in the auth_key.txt and the mac.txt files in the Data_collection directory. 
- The listen_to_buttons.service file sets a background-running service in linux that listens for a button (since we are running this experiment on a rasspberry pi with a simple button and led circuit). To activate the service, run the following commands: 

  ```
  sudo cp /HeleLora/src/Data_collection/listen_to_buttons.service /lib/systemd/system/
  sudo systemctl daemon-reload # run this whenever you do changes to the service.
  sudo systemctl enable listen_to_buttons
  sudo systemctl start listen_to_buttons
  ```

To check the status of the service: 'sudo systemctl status listen_to_buttons' 
To disable the service: 'sudo systemctl disable listen_to_buttons'
If the status of the service is active/running, this means that the service starts running as the system boots. The service listens for a long press on the button to start taking instructions, also through that single button, to set the activity label before starting connecting to the band and collecting data. 
- The circuit scheme will be uploaded soon!
