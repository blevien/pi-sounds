import RPi.GPIO as GPIO 
import time 
import pygame.mixer 
from sys import exit
import argparse

    

#configure Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(18, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.IN)

#Initialize variables
x=0
GPIO.output(17, False)
GPIO.output(22, False)

#initialize pygame mixer and sounds
pygame.mixer.init(48000, -16, 1, 1024)
sndA = pygame.mixer.Sound("sounds/siren2.wav")
sndB = pygame.mixer.Sound("sounds/cddyshack.wav")
sndC = pygame.mixer.Sound("sounds/train.wav")
soundChannelA = pygame.mixer.Channel(1)
soundChannelB = pygame.mixer.Channel(2)
soundChannelC = pygame.mixer.Channel(3)

#parse optional parameters fro Command Line
parser = argparse.ArgumentParser()
parser.add_argument("-c", help="Enter -c to use command line", action="store_true")
args = parser.parse_args() 
    
#Loop through the program to continually test if buttons are high or low
try:
    while True:
 
        if args.c:
            button = raw_input("Which Button would you like to simulate (1  |  2  |  3 )")
            print (button)

	print ("Are you making it here?")
            
        # This code is for a button 1 that plays a sound and turns on a light
        # then turns the light off after it's done playing
        input_value = GPIO.input(18)
        if input_value == False:
            GPIO.output(17, True)
            while input_value == False:
                input_value = GPIO.input(18)
            print('The light should be on, here comes the sound.')
            soundChannelB.play(sndB)
            while pygame.mixer.get_busy():
		GPIO.output(17,True)
            print('Sound is done, turn out the lights')
            GPIO.output(17,False)
            
        if button == "1":
            GPIO.output(17, True)
            print('The light should be on, here comes the sound.')
            soundChannelB.play(sndB)
            time.sleep(sndB.get_length())
            print('Sound is done, turn out the lights')
            GPIO.output(17,False)
    
            
        #This code is just for blinky lights while button 2 is pressed
        #Now with two alternating LEDs (Police Siren)
        input_value = GPIO.input(25)
        if input_value == False:
            print('The light should blink, and sound should play until you release the button')
            soundChannelA.play(sndA)
            while input_value == False:
                input_value = GPIO.input(25)
                GPIO.output(17, True)
                GPIO.output(22, False)
                time.sleep(.1)
                GPIO.output(17, False)
                GPIO.output(22, True)
                time.sleep(.1)
            soundChannelA.stop()
            GPIO.output(17, False)
            GPIO.output(22, False)
            print('Button released, lights and sound off')

        if button == "2":
            print('The light should blink, and sound should play until the sound is done')
            soundChannelA.play(sndA)
            while pygame.mixer.get_busy():
                input_value = GPIO.input(25)
                GPIO.output(17, True)
                GPIO.output(22, False)
                time.sleep(.1)
                GPIO.output(17, False)
                GPIO.output(22, True)
                time.sleep(.1)
            GPIO.output(17, False)
            GPIO.output(22, False)
            print('Sounds done, lights and sound off')
            
            

                        
        # This code is for a button 3 that has 4 states: all off, light1, light 2, both
        input_value = GPIO.input(24)
        # state is  for telling me how long the button was pressed for debug, but can be removed for clarity
        state = 0
        if input_value == False and state == 0:
            GPIO.output(17, True)
            while input_value == False:
                input_value = GPIO.input(24)
            print('Light 1 should be on.')
            state = 1 # go to next state on next loop
               
        elif input_value == False and state == 1:
            GPIO.output(17, False)
            GPIO.output(22, True)
            while input_value == False:
                input_value = GPIO.input(24)
            print('Light 2 should be on')
            state=2 #go to next state on next loop

                   
        elif input_value == False and state == 2:
            GPIO.output(17, True)
            GPIO.output(22, True)
            while input_value == False:
                input_value = GPIO.input(24)
            print('Both lights should be on')
            state=3 #go to next state on next loop

                               
        elif input_value == False and state == 3:
            GPIO.output(17, False)
            GPIO.output(22, False)
            while input_value == False:
                input_value = GPIO.input(24)
            print('All lights should be off')
            print('Play Train Sound')
            soundChannelC.play(sndC)
            state=0

        if button == "3":
            GPIO.output(17, True)
            print('Light 1 should be on.')
            pattern = raw_input("Press n to go to the next pattern of this button")
            if pattern == "n":
                GPIO.output(17, False)
                GPIO.output(22, True)
                print('Light 2 should be on')
                pattern = 0
                pattern = raw_input("Press n to go to the next pattern of this button")
                if pattern == "n":
                        GPIO.output(17, True)
                        GPIO.output(22, True)
                        print('Both lights should be on')
                        pattern = 0
                        pattern = raw_input("Press n to go to the next pattern of this button")
                        if pattern == "n":
                             GPIO.output(17, False)
                             GPIO.output(22, False)
                             print('All lights should be off')
                             print('Play Train Sound')
                             soundChannelC.play(sndC)


except: 
        KeyboardInterrupt
        GPIO.output(17, True)
        time.sleep(.3)
        GPIO.output(17, False)
        time.sleep(.1)
        GPIO.output(17, True)
        time.sleep(.1)
        GPIO.output(17, False)
        time.sleep(.3)

    
