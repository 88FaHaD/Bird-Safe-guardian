Bird SafeGuardian
A computer vision-based, humane bird repellent system. This project runs on a Raspberry Pi with a Camera Module and triggers an ultrasonic deterrent when a bird is detected.

Hardware
Raspberry Pi 4 Model B

Raspberry Pi Camera Module 2

Speaker

Software
Python 3

OpenCV

pygame

DNN Files:

ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt

frozen_inference_graph.pb

coco.names

Audio:

high-frequency-birdscarer.mp3

Setup
Clone Repository
git clone https://github.com/88FaHaD/Bird-SafeGuardian.git
cd Bird-SafeGuardian

Install Dependencies
(Optional) Create a virtual environment and install: pip install opencv-python pygame

Place Files
Ensure that all the DNN model files and the audio file are in the project directory.

Run the Project
python bird_safe_guardian.py
Press q to exit the application.

Image And Demo Video

![Image](https://github.com/user-attachments/assets/315f64e0-1213-4823-8c1c-caaed616b2bf)

https://github.com/user-attachments/assets/8127c4f9-d3d0-485e-9073-6c6779f3c500

https://github.com/user-attachments/assets/85505606-838f-47e9-89a3-e1d870109604


