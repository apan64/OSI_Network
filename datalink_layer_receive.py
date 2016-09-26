from MorseCode import MorseCode
Inverted = {MorseCode[letter]: letter for letter in MorseCode}
Numbers = {1: '.----', 2: '..---', 3: '...--', 4: '....-', 5: '.....', 6: '-....', 7: '--...', 8: '---..', 9: '----.', 10: '-----'}
InvertNumbers = {Numbers[n]: n for n in Numbers}

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

def splitAsterisks(incoming):
	out = []
	second = []
	first = incoming.split('**')
	for i in first:
		second += i.split('***')
	for j in second:
		out += j.split('****')
	return out

def processChecksum(parityMorse, msg):
	# Process parity
	parity = Inverted[parityMorse.replace('...', '-').replace('*', '')]
	words = []
	toProcess = []
	for part in msg:
		toAdd = part
		if(len(part) > 8):
			if(part[len(part) - 8:] == '........'):
				toAdd = part[:len(part) - 8]
		toProcess.append(toAdd)
	# if(msg[len(msg) - 1] == '.'*8):
	# 	msg = msg[:len(msg) - 1]
	# else:
	# 	msg[len(msg) - 1] = msg[len(msg) - 1][:len(msg) - 10] # fuck if i know what's going on here
	# 	print(msg)
	# print(toProcess)
	for w in toProcess:
		letters = splitAsterisks(w)
		for i in range(len(letters)):
			letter = letters[i]
			letters[i] = Inverted[letter.replace('...', '-').replace('*','')]
		words.append(''.join(letters))
	pSum = 0
	msgDecoded = ' '.join(words) # for some reason this is only keeping the word checking, whereas toProcess contains both segments................
	# print(msgDecoded)
	while(msgDecoded[::-1][0] == ' '):
		msgDecoded = msgDecoded[:len(msgDecoded) - 1]
	for c in msgDecoded:
		pSum += ord(c.upper())
	parityCalculated = chr(65 + (pSum % 26))
	if parity == parityCalculated:
		print('Checksums match')
	else:
		print('Checksums do not match')
		print('Received parity: {} \t Calculated parity: {}'.format(parity, parityCalculated))

def dlOperations(msgList, thisAddress):
	processToAddress(msgList[0], thisAddress)
	processFromAddress(msgList[1])
	processChecksum(msgList[2], msgList[7:len(msgList) - 1])
	# processChecksum(msgList[2:len(msgList) - 1])
	return msgList[3:]