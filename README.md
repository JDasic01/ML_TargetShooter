# Target Shooter 
- [x] **Mouth Recognition**
  - [ ] sometimes eye is found instead of mouth, change to only register bottom half of face 
- [ ] **Distance Recognition**
  - [x] add a step to recognize persons hand
  - [x] after hand is recognized, call face_and_mouth function
  - [ ] pass distance and postition data to python script to controll servo
- [ ] **Stepper Motor Control**
  - [ ] basic test of stepper motors on rpi zero w
  - [ ] try dc
- [ ] **Laser aim**
- [ ] **Piezo aim and shooting**
- [ ] **3D shooter model**
- [ ] **change requirements to specific version**


**Docs**
This script is designed to be run on a Raspberry Pi Zero Wireless to perform real-time object tracking.
Upon startup, the LED connected to the Raspberry Pi should illuminate red to indicate that the system is initializing.
While the hand detection process is in progress, the LED will turn yellow.
Once a hand is detected, the script will start detecting the mouth. During this process, the LED will change to green.
The thumb-up sign detection feature has been removed from this version of the script.
