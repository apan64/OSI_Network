from SetPin import SetPin
import time
def pot(pinIn, pinOut):
	while True:
		if pinIn.read_pin():
			pinOut.turn_high()
		else:
			pinOut.turn_low()

if __name__ == '__main__':
	pinIn = SetPin(16, "GPIO_23", direction="RX")
	pinOut = SetPin(15, "GPIO_22", direction="TX")
	pot(pinIn, pinOut)