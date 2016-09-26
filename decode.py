from MorseCode import MorseCode
Inverted = {MorseCode[letter]: letter for letter in MorseCode}

def splitAsterisks(incoming):
	out = []
	second = []
	first = incoming.split('**')
	for i in first:
		second += i.split('***')
	for j in second:
		out += j.split('****')
	return out

if __name__ == '__main__':
	w = '.*.*...*.***.*..*.***.*...***'
	letters = splitAsterisks(w)
	for i in range(len(letters)):
		letter = letters[i]
		letters[i] = Inverted[letter.replace('...', '-').replace('*','')]
	print(''.join(letters))