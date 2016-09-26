# Module MorseTX
from .MorseCode import MorseCode


def MorseTX(M):
    m_list = M.split(' ')
    for i in range(len(m_list)):
        for L in m_list[i]:
            for Dd in MorseCode[L]:
                yield (1,1) if Dd == "." else (1,3)
                yield (0,1)
            yield(0,2)
        #don't send an extra space at the end of messages
        if i + 1 == len(m_list):
            break
        #otherwise put a space between words
        yield (0,4)
    #high-bit EOM
    yield (1,8)

if __name__ == "__main__":
    print("AN ACE")
    for OOKtuple in MorseTX("AN ACE"):
        print(OOKtuple)
    print("OOK AT ME")
    for OOKtuple in MorseTX("OOK AT ME"):
        print(OOKtuple)
