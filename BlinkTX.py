#
## Lab 2.2 - Physical Layer  - Send Tuples as blinks
#
from MorseTX import MorseTX
from SetPin import SetPin
from MorseCode import MorseCode
import time, random
Inverted = {MorseCode[letter]: letter for letter in MorseCode}
address = 'A'
morseNumbers = {1 : '.----', 2 : '..---', 3 : '...--', 4 : '....-', 5 : '.....', 6 : '-....', 7 : '--...', 8 : '---..', 9 : '----.', 0 :'-----'}
speed = .02

class BlinkTX(SetPin):
    def __init__(self,headerpin,BCM,direction="TX"):
        if direction != "TX":
            raise ValueError("direction must be 'TX'")
        super().__init__(headerpin,BCM,direction="TX")

    def __call__(self,tups):
        for state,direction in tups:
            self.blinkTX(state,direction)

    def blinkTX(self,state,duration):
        self.turn_high() if state else self.turn_low()
        time.sleep(duration * speed)    

    def blinkTuple(self,t):
        self.turn_high() if t[0] else self.turn_low()
        time.sleep(t[1] * speed)     
def getquote():
    x = makeMorseHappy(quotes[random.randint(0,len(quotes)-1)])
    return x

def splitAsterisks(incoming):
    out = []
    second = []
    first = incoming.split('**')
    for i in first:
        second += i.split('***')
    for j in second:
        out += j.split('****')
    return out

def blinkTargetAddress(addressTarget):
    ans = ''
    for c in addressTarget:
        for Dd in MorseCode[c]:
            ans += '.' if Dd == '.' else '...'
            ans += '*'
        ans += '**'
    ans += '****'
    return ans

def blinkOwnAddress():
    ans = ''
    for c in address:
        for Dd in MorseCode[c]:
            ans += '.' if Dd == '.' else '...'
            ans += '*'
        ans += '**'
    ans += '****'
    return ans

def splitMessages(morseMsg, msgSize): #splits messages, returns an array of split messages, split messages end in a character and won't send an incomplete character
    ans = []
    while len(morseMsg) > msgSize:
        cur = morseMsg[:msgSize]
        endPos = cur[::-1].find('***')
        if(morseMsg[msgSize:].find('.') != 0):
            endPos = -1 * (morseMsg[msgSize:].find('.'))
        ans.append(morseMsg[:msgSize - endPos])
        morseMsg = morseMsg[msgSize - endPos:]
    ans.append(morseMsg)
    return ans

def blinkMessagePart(num, maxNum):
    ans = ''
    for c in str(num)[::-1]:
        for dd in morseNumbers[int(c)]:
            ans += '.' if dd == '.' else '...'
            ans += '*'
        ans += '**'
    ans += '****'
    for c in str(maxNum)[::-1]:
        for dd in morseNumbers[int(c)]:
            ans += '.' if dd == '.' else '...'
            ans += '*'
        ans += '**'
    ans += '****'
    return ans

def blinkChecksum(morseMsg):
    ans = ''
    chk = 0
    words = []
    for w in morseMsg.split('*'*7):
        letters = splitAsterisks(w)
        for i in range(len(letters)):
            letter = letters[i]
            letters[i] = Inverted[letter.replace('...', '-').replace('*','')]
        words.append(''.join(letters))
    msgDecoded = ' '.join(words)
    while(msgDecoded[::-1][0] == ' '):
        msgDecoded = msgDecoded[:len(msgDecoded) - 1]
    print(msgDecoded)
    for l in msgDecoded:
        chk += ord(l.upper())
    parity = chr(65 + (chk % 26))
    for c in MorseCode[parity]:
        ans += '.' if c == '.' else '...'
        ans += '*'
    ans += '*'*6
    # print(parity)
    return ans



def makeMorseHappy(Q):
    return "".join([a if a in string.ascii_uppercase+" " else " "+"".join(unicodedata.name(a,"").split("-"))+" " for a in Q.upper() ])

def sendMessage():
    with BlinkTX(15,"GPIO_22",direction="TX") as blink:
        with SetPin(16, 'GPIO_23', direction='RX') as RXpin:
            while True:
                clear = True
                blink.blinkTX(0, 1)
                targetAddress = input('TARGET ADDRESS: ').upper()
                msg = input("MESSAGE TO SEND (EMPTY ENTRY YIELDS RANDOM QUOTE) :")
                print('Checking for clear connection...')
                for i in range(random.randint(5, 15)):
                    if(RXpin.read_pin()):
                        clear = False
                        break
                    time.sleep(.1)
                if(clear):
                    if not msg:
                        send = getquote()
                    else:
                        send = msg.upper()
                    morseMsg = ''
                    for W in send.split(" "):
                        for L in W:
                            for Dd in MorseCode[L]:
                                morseMsg += '.' if Dd == "." else '.'*3
                                morseMsg += '*'
                            morseMsg += '*'*2
                        morseMsg += '*'*4
                    morseArray = splitMessages(morseMsg, 300) # fragmentation for network
                    print('Sending message')
                    addressHeader = blinkTargetAddress(targetAddress) + blinkOwnAddress()
                    chksumArray = [blinkChecksum(q) for q in morseArray] # datalink
                    partArray = [blinkMessagePart(q + 1, len(morseArray)) for q in range(len(morseArray))] # network
                    messageArray = [addressHeader + chksumArray[q] + addressHeader + partArray[q] + morseArray[q] for q in range(len(morseArray))]
                    messageFinal = '........'.join(messageArray) + '........'
                    logicMessage = [1 if q == '.' else 0 for q in messageFinal]
                    logicTuples = []
                    count = 0
                    previous = 0
                    for m in logicMessage:
                        if m == previous:
                            count += 1
                        else:
                            logicTuples.append((previous, count))
                            count = 1
                            previous = m
                    logicTuples.append((1, 8))

                    for part in logicTuples:
                        # blink.blinkTX(1, 1) if(char == '.') else blink.blinkTX(0, 1)
                        blink.blinkTuple(part)
                    blink.blinkTX(0, 1)
                    print('Message sent!')
                else:
                    ranTime = random.random() * 5 + 10
                    print('Collision detected, timeout for {} seconds'.format(ranTime))
                    time.sleep(ranTime)
                    print('Ready for next message')

if __name__ == "__main__":
    import random
    import mobydickquotes
    import string
    import unicodedata
    quotes = mobydickquotes.quotes
    sendMessage()
    

    
