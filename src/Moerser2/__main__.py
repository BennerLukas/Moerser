import cv2
from matplotlib import pyplot as plt
from Moerser.utils import set_logger
from periphery import Camera

camera_p = Camera()
frame_count = 0
frame = 1 # Frame per second
brightness_threshold = 0
tolerance = 0.05
bright_counter = 0
darkness_counter = 0
sequence = ""
total_sequence = ""

while True:
    frame = cv2.imshow("webcam", camera_p.get_frame())
    frame_brightness = Camera.calc_mean_brightness(camera_p.get_frame())
    
    # If first frame -> set avg brightness 2 threshold
    if frame_count == 0:
        print(f"Threshold initiated  at {frame_brightness}")
        brightness_threshold = frame_brightness
    
    # Track brightness
    if frame_brightness > brightness_threshold * (1 + tolerance):
        bright_counter += 1
        darkness_counter = 0
    else:
        # Decoding light to morse code
        darkness_counter += 1
        print(f"Current Brightness Counter: {bright_counter}")
        print(f"Current Darkness Counter: {darkness_counter}") 
        
        # Brightness
        if bright_counter in range(1, 3):
            sequence += "."
            #print(".")
            #bright_counter = 0 
        elif bright_counter >= 3 :
            sequence += "-"
            #print("-")
            #bright_counter = 0
        
        # Darkness
        if darkness_counter in range(1, 3):
            # next character in word
            total_sequence += sequence
            sequence = ""
            bright_counter = 0
            
        elif darkness_counter > 7 :
            # next word
            #total_sequence += sequence # not needed because a darkness_counter of 1 will push sequence already 
            #sequence = ""
            total_sequence += " "
            bright_counter = 0
        

        
        
        print(f"Current sequence: {total_sequence}")
       

    frame_count += 1
    
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    cv2.waitKey(1000)# one frame per second
