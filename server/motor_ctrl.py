import RPi.GPIO as GPIO
import time


#this file will control our stepper motor driver

#Pin def
STEP = 23
DIR = 27
ENABLE = 4
#need to later define ms1-3

#sets gpio mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)





#class for stepper motor
class StepperMotor:
	def __init__(self, microstep=None):

		'''
		to init the motor
		'''

		#setup
		#GPIO.setmode(GPIO.BCM)
		#GPIO.setup(STEP, GPIO.OUT)
		#GPIO.setup(DIR, GPIO.OUT)
		#GPIO.setup(ENABLE, GPIO.OUT)

	def set_dir(self, high=True): #may need to make this more robust
		#sets direction of the motor
		GPIO.output(DIR, GPIO.HIGH if high else GPIO.LOW)

	def set_microstep(self, ms1, ms2, ms3):
		pass #TODO


	def step(self, steps, delay=0.002):
		#moves the motor a specific # of steps
		for _ in range(steps):
			GPIO.output(STEP, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(STEP, GPIO.LOW)
			time.sleep(delay)

	def cleanup(self):
		GPIO.cleanup()


