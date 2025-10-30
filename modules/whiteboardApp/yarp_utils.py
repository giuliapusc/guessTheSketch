import yarp

# Vocabs to be passed in a yarp bottle from backend to distinguish between game phases
VOCAB_INTRO = yarp.createVocab32('I', 'N', 'T', 'R')  # 1381256777
VOCAB_RULES = yarp.createVocab32('R', 'U', 'L', 'E')  # 1162630482
VOCAB_START_ROUND = yarp.createVocab32('R', 'N', 'D')  # 4476498
VOCAB_DRAW = yarp.createVocab32('D', 'R', 'A', 'W')
VOCAB_END_SKETCH = yarp.createVocab32('E', 'N', 'D')
VOCAB_NEXT_ROUND = yarp.createVocab32('N','E', 'X', 'T') #1415071054
VOCAB_WAIT = yarp.createVocab32('W', 'A', 'I', 'T')

# Custom messages
def icub_msg(msg):
    print("\033[96m[iCub] {}\033[00m".format(msg))


def yarpinfo(msg):
    print("\033[92m[INFO] {}\033[00m".format(msg))

def guiinfo(msg):
    print("\033[95m[GUI] {}\033[00m".format(msg))


def debug(msg):
    print("\033[96m[DEBUG] {}\033[00m".format(msg))


def warning(msg):
    print("\033[93m[WARNING] {}\033[00m".format(msg))


def error(msg):
    print("\033[91m[ERROR] {}\033[00m".format(msg))


class YarpCallbackBinder(yarp.BottleCallback):

    def __init__(self, on_read):
        super().__init__()
        self.callback = on_read

    def onRead(self, *args):
        if self.callback is not None:
            self.callback(*args)