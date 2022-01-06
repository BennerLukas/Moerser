import cv2
from matplotlib import pyplot as plt
from Moerser.utils import set_logger
from periphery import Camera

def cam():       
    # Connect to webcam
    cap = cv2.VideoCapture(2)
    # Loop through every frame until we close our webcam
    while cap.isOpened(): 
        ret, frame = cap.read()
        
        # Show image 
        cv2.imshow('Webcam', frame)
        
        # Checks whether q has been hit and stops the loop
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    # Releases the webcam
    cap.release()
    # Closes the frame
    cv2.destroyAllWindows()

camera_p = Camera()
frame_count = 0
brightness_threshold = 0
tolerance = 0.25
bright_counter = 0
sequence = ""

while True:
    frame = cv2.imshow("webcam", camera_p.get_frame())
    frame_brightness = Camera.calc_mean_brightness(camera_p.get_frame())
    
    #if first frame -> set avg brightness 2 threshold
    if frame_count == 0:
        brightness_threshold = frame_brightness
        
    if frame_brightness >= brightness_threshold * (1 - tolerance):
        bright_counter += 1
    
    else:
        print(bright_counter)
        if bright_counter in range(0,3):
            sequence.append(".")
            bright_counter == 0
            
        elif bright_counter > 3:
            sequence.append("-")
            bright_counter == 0
        
    frame_count += 1
    
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    cv2.waitKey(1000)# one frame per second
