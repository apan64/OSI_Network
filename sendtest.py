from SetPin import SetPin
import time
if __name__ == '__main__':
	with SetPin(15,"GPIO_22",direction="TX") as blink:
		state = True
		while(True):
			blink.turn_high() if state else blink.turn_low()
			state = False if state else True
			time.sleep(.5)