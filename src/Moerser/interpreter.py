import cv2
from matplotlib import pyplot as plt
from Moerser.utils import set_logger
from Moerser.periphery import Camera
from Moerser.morse2text import Morse2Text

class Interpreter:
    def __init__(self, frames = 1, tolerance = 0.05):
        self.frames = 1  # Frame per second
        self.frame_count = 0
        self.brightness_threshold = 0
        self.tolerance = 0.05
        self.bright_counter = 0
        self.darkness_counter = 0
        self.sequence = ""
        self.total_sequence = " "
        self.decoder = Morse2Text()
        #self.capture = Camera(2)
        self.current_frame = None
        
    def set_baseline(self, current_frame):
        '''
        sets the current frame as the base brightness
        '''
        #current_frame = self.capture.get_frame()
        self.brightness_threshold = Camera.calc_mean_brightness(current_frame)
        print(f"Threshold initiated  at: {self.brightness_threshold}")

        return None
    
    def check_brightness(self, frame_brightness, tolerance = 0.05):
        if frame_brightness > self.brightness_threshold * (1 + tolerance):
    
            if self.darkness_counter != 0:
                self.sequence = self.interpret_darkness(self.darkness_counter)
                
                self.total_sequence += self.sequence
                
                #if self.total_sequence[-1] != "/":
                    
                    #if self.darkness_counter >= 7:
                    #    total_sequence = self.total_sequence[:-1] #not needed since only once written
                                                    
                    #self.total_sequence += self.sequence
                    
                
                self.darkness_counter = 0

            self.bright_counter += 1
            
            current_sequence = self.interpret_brightness(self.bright_counter) #current sequence

        else:

            if self.bright_counter != 0:
                self.sequence = self.interpret_brightness(self.bright_counter)
                
                if self.sequence != "DEL":
                    self.total_sequence += self.sequence
                    
                else:
                    
                    if len(self.total_sequence) > 1:
                        self.total_sequence = self.total_sequence[:-1] #Correct last letter
                        
                    else:
                        pass #Avoids deleting already empty strings
                    
                self.bright_counter = 0
            
            self.darkness_counter += 1
            
            current_sequence = self.interpret_darkness(self.darkness_counter)
        
        
        print(f"Current Darkness Counter: {self.darkness_counter}")
        print(f"Current Brightness Counter: {self.bright_counter}")
            
        return current_sequence
            
    
    def interpret_brightness(self, counter, frames = 1):
        if counter in range(1, (5 * frames)): #Dit
            sequence = "."
                
        elif counter in range ((5 * frames), (8 * frames)): #Dah
            sequence = "-"
                
        elif counter >= (8 * frames): #Delete Seq
            sequence = "DEL"

        return sequence
    
    
    def interpret_darkness(self, counter, frames = 1):
        if counter in range(1, (4 * frames)): #Next sequence in Letter
            sequence = ""
            
        elif counter in range((4 * frames), (7 * frames)): #Next letter in word
            sequence = "/"

        elif counter >= (7 * frames): #Next word
            sequence = " "
                
        return sequence