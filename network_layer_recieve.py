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

def processMessagePart(msgPart, msgMax):
	# nums1 = msgPart.split('***')
	nums1 = splitAsterisks(msgPart)
	rec1 = ''
	for n in nums1:
		rec1 += Inverted[n.replace('...', '-').replace('*', '')]
	nums2 = splitAsterisks(msgMax)
	rec2 = ''
	for n in nums2:
		rec2 += Inverted[n.replace('...', '-').replace('*', '')]
	print('Message is part {} of {}'.format(rec1, rec2))
	return int(rec1), int(rec2)


def processToAddress(header, curAddress):
	# Process header
	# letters = header.split('***')
	letters = splitAsterisks(header)
	rec = ''
	for l in letters:
		rec += Inverted[l.replace('...', '-').replace('*', '')]
	print('Message intended for {}'.format(rec))
	if rec == curAddress:
		print('This is the correct recipient')
	else:
		print('This is the incorrect recipient')

def processFromAddress(header):
	# letters = header.split('***')
	letters = splitAsterisks(header)
	rec = ''
	for l in letters:
		rec += Inverted[l.replace('...', '-').replace('*', '')]
	print('Message received from {}'.format(rec))

def nwOperations(msgList, thisAddress):
	processToAddress(msgList[0], thisAddress)
	processFromAddress(msgList[1])
	x, y = processMessagePart(msgList[2], msgList[3])
	return msgList[4:], x, y
	