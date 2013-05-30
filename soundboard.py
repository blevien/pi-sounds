import RPi.GPIO as GPIO 
import time 
import pygame.mixer 
from sys import exit

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

#Loop through the program to continually test if buttons are high or low
try:
    while True:
        
        # This code is for a button that plays a sound and turns on a light
        # then turns the light off after it's done playing
        input_value = GPIO.input(18)
        if input_value == False and x == 0:
            GPIO.output(17, True)
            while input_value == False:
                input_value = GPIO.input(18)
                # print('Button 1 is still pressed.')
                # print(x)
                x+=1
            print('The light should be on, here comes the sound.')
            soundChannelB.play(sndB)
            time.sleep(sndB.get_length())
            print('Sound is done, turn out the lights')
            GPIO.output(17,False)
            x = 0
            
        # This code is for a button that has 4 states: all off, light1, light 2, both
        input_value = GPIO.input(24)
        state = 0
        
        # variable state tells me the state of the light
        # x is for debouncing
        # x is also for telling me how long the button was pressed for debug, but can be removed for clarity
        
        if input_value == False and x == 0:
            GPIO.output(17, True)
            print('Light 1 should be on.')
            while input_value == False:
                input_value = GPIO.input(24)
                print('Button 3 is still pressed.')
                print(x) #show me how many times this was executed
                x +=1 #increment
            x = 1 # go to next state on next loop
            
            
        elif input_value == False and x == 1:
            x=0 #reset so I can see how long button was pressed
            GPIO.output(17, False)
            GPIO.output(22, True)
            print('Light 2 should be on')
            while input_value == False:
                input_value = GPIO.input(24)
                print('Button 3 is still pressed')
                print(x)
                x+=1
            x=2 #go to next state on next loop
            
        elif input_value == False and x == 2:
            x=0 #reset so I can see how long button was pressed
            GPIO.output(17, True)
            GPIO.output(22, True)
            print('Both lights should be on')
            while input_value == False:
                input_value = GPIO.input(24)
                print('Button 3 is still pressed')
                print(x)
                x+=1
            x=3 #go to next state on next loop
            
        elif input_value == False and x == 3:
            x=0 #reset so I can see how long button was pressed
            GPIO.output(17, False)
            GPIO.output(22, False)
            print('All lights should be off')
            while input_value == False:
                input_value = GPIO.input(24)
                print('Button 3 is still pressed')
                print(x)
                x+=1
            print('The light should be off')
            x=0 #reset so I know the lights are off


        #This code is just for blinky lights while button is pressed
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
                #print('Button 3 is still pressed.')
            soundChannelA.stop()
            GPIO.output(17, False)
            GPIO.output(22, False)
            print('Button released, lights and sound off')                



except KeyboardInterrupt:
        GPIO.output(17, True)
        time.sleep(.3)
        GPIO.output(17, False)
        time.sleep(.1)
        GPIO.output(17, True)
        time.sleep(.1)
        GPIO.output(17, False)
        time.sleep(.3)

    
