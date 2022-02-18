import cv2
import time
from matplotlib import pyplot as plt
from Moerser.utils import set_logger
from Moerser.periphery import Camera
from Moerser.morse2text import Morse2Text
from Moerser.interpreter import Interpreter

camera_p = Camera(0)
frame_throttle = 0.5 # throttle limit
frame_count = 0
sequence = ""
total_sequence = " "
decoded_sequence = " "
decoder = Morse2Text()
interpreter = Interpreter()
startTime = time.time()


while True:
    nowTime = time.time()
    current_frame = camera_p.get_frame()
    frame_brightness = Camera.calc_mean_brightness(current_frame)

    # If first frame -> set avg brightness 2 threshold
    if frame_count == 0:
        interpreter.set_baseline(current_frame)

    if (nowTime - startTime) > frame_throttle:
        print(nowTime - startTime)
        sequence = interpreter.check_brightness(frame_brightness)
        total_sequence = interpreter.total_sequence
        decoded_sequence = decoder.decode(total_sequence)
        startTime = time.time() # reset time
       
    frame_count += 1

    cv2.putText(current_frame, f"Morse_Code: {total_sequence}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(current_frame, f"Decoded_Sequence: {decoded_sequence}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(current_frame, f"Current_sequence: {sequence}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("webcam", current_frame)

    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break
    cv2.waitKey(10)  # one frame per second
