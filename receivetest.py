from SetPin import SetPin

if __name__ == '__main__':
	with SetPin(16, "GPIO_23", direction="RX") as RXpin:
		while(True):
			if(RXpin.read_pin()):
				print(1)
			else:
				print(0)
				