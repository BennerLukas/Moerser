import cv2
from matplotlib import pyplot as plt
from Moerser.utils import set_logger
from periphery import Camera

camera_p = Camera()
frame_count = 0
frames = 1 # Frame per second
brightness_threshold = 0
tolerance = 0.05
bright_counter = 0
darkness_counter = 0
sequence = ""
total_sequence = ""

while True:
    current_frame = camera_p.get_frame()
    frame_brightness = Camera.calc_mean_brightness(current_frame)
    
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
        if bright_counter in range(1, (3*frames)):
            sequence = "."
            #print(".")
            #bright_counter = 0 
        elif bright_counter >= (3*frames) :
            sequence = "-"
            #print("-")
            #bright_counter = 0
        
        # Darkness
        if darkness_counter in range(1, (3*frames)):
            # next character in word
            total_sequence += sequence
            sequence = ""
            bright_counter = 0
            
        elif darkness_counter > (7*frames) :
            # next word
            #total_sequence += sequence # not needed because a darkness_counter of 1 will push sequence already 
            #sequence = ""
            total_sequence += " "
            bright_counter = 0
        

        
        
        print(f"Current sequence: {total_sequence}")
       

    frame_count += 1
    
    cv2.putText(current_frame, f"Morse_Code: {total_sequence}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    cv2.imshow("webcam", current_frame)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    cv2.waitKey(500)# one frame per second
