import yarp


# ---------------------------------------------------------
# Personalize messages colors
def icub_msg(msg):
    print("\033[96m[iCub] {}\033[00m".format(msg))

def speaker_msg(msg):
    print("\033[96m[Speaker] {}\033[00m".format(msg))

def yarpinfo(msg):
    print("\033[92m[INFO] {}\033[00m".format(msg))


def debug(msg):
    print("\033[96m[DEBUG] {}\033[00m".format(msg))


def warning(msg):
    print("\033[93m[WARNING] {}\033[00m".format(msg))


def error(msg):
    print("\033[91m[ERROR] {}\033[00m".format(msg))


# ----------------------------------------------------------------------------

# Vocabs to be passed in a yarp bottle from backend to distinguish between game phases
VOCAB_INTRO = yarp.createVocab32('I', 'N', 'T', 'R')
VOCAB_RULES = yarp.createVocab32('R', 'U', 'L', 'E')
VOCAB_START_ROUND = yarp.createVocab32('R', 'N', 'D')
VOCAB_PLAY = yarp.createVocab32('P', 'L', 'A', 'Y')
VOCAB_NEXT_SKETCH = yarp.createVocab32('N', 'X', 'T')
VOCAB_END_SKETCH = yarp.createVocab32('E', 'N', 'D')
VOCAB_FINISH = yarp.createVocab32('F', 'I', 'N', 'I')

# ----------------------------------------------------------------------------
# ------------Comments by icub.---------------
thinking_sounds = (
    "'#BREATH03#'", '', "'#YAWN02#'", "'#CLICK02# #CLICK02#'", '', "'#BREATH02#'", "'#THROAT02#'", '',
    "'#THROAT03#'", "'#MMM02#'")
# --------------------------------------------
# -----------Game Parameters----------------
TO_DRAW_LIST = ["arancia", "palla", 
                "Giovanna", "Navel", 
                'parco', 'casa', 
                'cane', 'gatto']
MAX_ROUNDS = len(TO_DRAW_LIST)
ERROR_ROUNDS = [2]
