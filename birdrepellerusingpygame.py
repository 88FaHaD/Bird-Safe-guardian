import cv2
import pygame
import threading
import time
import win32api

# Initialize pygame mixer
pygame.mixer.init()

thres = 0.3 # Threshold to detect object

classNames = []
classFile = "coco.names"
with open(classFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# Load the sound file
try:
    bird_sound = pygame.mixer.Sound("high-frequency-birdscarer.mp3")
except pygame.error as e:
    print(f"Error loading sound file: {e}")
    bird_sound = None

# Global flags
playing_sound = False
detection_paused = False

def play_sound_sequence():
    global playing_sound
    if bird_sound:
        for _ in range(2):  # Play 2 times
            if not playing_sound:
                break
            try:
                bird_sound.play()
                time.sleep(bird_sound.get_length())  # Wait for the sound to finish before playing again
            except Exception as e:
                print(f"Error playing sound: {e}")
                break
    playing_sound = False

def start_sound_sequence():
    global playing_sound
    if not playing_sound:
        playing_sound = True
        threading.Thread(target=play_sound_sequence, daemon=True).start()

def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)
    if len(objects) == 0:
        objects = classNames
    objectInfo = []
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box, className])
                if draw:
                    cv2.rectangle(img, box, color=(0, 0, 255), thickness=2)
                    cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    return img, objectInfo

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)  # 0 is usually the default webcam

    if not cap.isOpened():
        print("Error: Could not open the webcam.")
    else:
        # Get the screen resolution
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)

        # Set the window to full screen
        cv2.namedWindow("Output", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Output", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while True:
            success, img = cap.read()

            if not success:
                print("Error: Failed to capture a frame.")
                break

            img = cv2.resize(img, (screen_width, screen_height))

            if not detection_paused:
                result, objectInfo = getObjects(img, 0.45, 0.2, objects=['bird'])

                if 'bird' in [obj[1] for obj in objectInfo]:
                    if not playing_sound:
                        print("Bird detected! Playing sound sequence...")
                        start_sound_sequence()
                        detection_paused = True
                        pause_start_time = time.time()

            else:
                # Check if pause time (10 seconds) has elapsed
                if time.time() - pause_start_time > 10:
                    detection_paused = False
                    print("Resuming detection...")

            cv2.imshow("Output", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()