import RPi.GPIO as GPIO
import time
from threading import Thread, Event

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

		self.timeout = 2.0 #two second watchdog timer for motor safety
		self.running = False #motor state
		self.last_input_time = time.time()
		self.stop_event = Event()

		#watchdog thread
		self.watchdog_thread = Thread(target=self._watchdog_timer, daemon=True)
		self.watchdog_thread.start()

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

	def _step_cont(self, delay=0.001):
		#makes the motor step continuously
		while self.running and not self.stop_event.is_set():
			GPIO.output(STEP, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(STEP, GPIO.LOW)
			time.sleep(delay)


	def step(self, steps, delay=0.001):
		#moves the motor a specific # of steps

		self.last_input_time = time.time() #reset watchdog

		if not self.running:
			self.running = True
			self.stop_event.clear()
			self.thread = Thread(target=self._step_cont, args=(delay,))
			self.thread.start()


	def stop_step(self):
		#stops motor
		self.running = False
		self.stop_event.set()
		if hasattr(self, "thread"):
			self.thread.join()

	def _watchdog_timer(self):
		#monitors to see if no input is given
		while True:
			if time.time() - self.last_input_time > self.timeout:
				if self.running:
					print("no motor input, ensuring no movement")
					self.stop_step()
			time.sleep(0.1) #check every 100ms




	def cleanup(self):
		self.stop_stepping()
		GPIO.cleanup()


