# from SetPin import SetPin
import time, string
import datalink_layer_receive as dl
import network_layer_recieve as nw
delimiters = ['**', '***', '****']
address = 'A'

from MorseCode import MorseCode
Inverted = {MorseCode[letter]: letter for letter in MorseCode}
Numbers = {1: '.----', 2: '..---', 3: '...--', 4: '....-', 5: '.....', 6: '-....', 7: '--...', 8: '---..', 9: '----.', 10: '-----'}
InvertNumbers = {Numbers[n]: n for n in Numbers}

def splitAsterisks(incoming):
	out = []
	second = []
	first = incoming.split('**')
	for i in first:
		second += i.split('***')
	for j in second:
		out += j.split('****')
	return out

def splitMessages(incoming):
	out = []
	second = []
	first = incoming.split('******')
	for i in first:
		second += i.split('*******')
	for j in second:
		out += j.split('********')
	return out

def process(input_message):
	input_message = splitMessages(input_message.split('*' * 15)[0])
	
	curMsg, msgPart, totalMsgs = nw.nwOperations(dl.dlOperations(input_message, address), address)

	# incoming = curMsg[0] # check to see what is in curMsg (only one word or more)
	# something is up here, dropping the last incomplete word in fragmented messages
	newwords = []
	if(curMsg[len(curMsg) - 1] == '*' + '.'*8):
		curMsg = curMsg[:len(curMsg) - 1]
	else:
		curMsg[len(curMsg) - 1] = curMsg[len(curMsg) - 1][:len(curMsg) - 10]
	for w in curMsg:
		letters = splitAsterisks(w)
		for i in range(len(letters)):
			letter = letters[i]
			letters[i] = Inverted[letter.replace('...', '-').replace('*','')]
		newwords.append(''.join(letters))
	return ' '.join(newwords)
