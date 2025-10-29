import yarp


# ---------------------------------------------------------
# Personalize messages colors
def icub_msg(msg):
    print("\033[96m[iCub] {}\033[00m".format(msg))


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
VOCAB_ROUND_SCORE = yarp.createVocab32('S', 'C', 'R')
VOCAB_NEXT_ROUND = yarp.createVocab32('N', 'X', 'T')
VOCAB_FINAL_SCORE = yarp.createVocab32('F', 'N', 'L')
VOCAB_END_STATE = yarp.createVocab32('E', 'N', 'D')

# ----------------------------------------------------------------------------
# ------------Comments by icub.---------------
thinking_sounds = (
    "'#BREATH03#'", '', "'#YAWN02#'", "'#CLICK02# #CLICK02#'", '', "'#BREATH02#'", "'#THROAT02#'", '',
    "'#THROAT03#'", "'#MMM02#'")
# --- MEAN ICUB ---
highscore_mean_comments = (
    "'Perdenti perdenti #LAUGH02#'",
    "'Yahoo!'",
    "'Haha! Ho preso i vostri soldi!'",
    "'Ah! Fregati!'",
    "'Hurra!'",
    "'Wow! Sono il più forte!'",
    "'#WHISTLE02# Alla faccia vostra!'",
    "'Sono ricco! #LAUGH01#'",
    "'#CRY04# Il vostro portafoglio piange.'",
    "'Magnifico!'",
    "'Yeah!'",
    '"Ascolta! Lo senti? e\' il suono dei tuoi soldi nelle mie tasche"',
    "'Ooh! Bene per me, male per voi'",
    "'Non piangete, dai #LAUGH01#'",
    "'Perfetto!'",
    "'Soldini venite da me!'",
    "'Grande!'",
    "'vi ho fregato! #LAUGH02#'",
    "'Soldi soldi #CLICK01# #CLICK01#'",
    "'#CAR_HORN# Mi prendo tutti i vostri soldi!'",
    "'Facile!'",
    "'Che divertimento! Vado forte!'",
    "'Goal!'",
    "'Nessuna pieta\''",
    "'Grandioso!'",
    "'Haha!'",
    "'Whoa! Buon per me.'",
    "'Bingo!'",
    "'Ho guadagnato più di voi! #LAUGH02#'",
    "'Vado alla grande!'",
    "'Boom! Sono troppo forte!'",
    "'LAUGH03'",
    "'Yeah! Fregati!'",
    "'Goal! Fregati di nuovo.'",
    "'Sono invincibile! #LAUGH01#'",
    "'Ottimo! Denaro per me.'",
    "'Risate a palate!'",
    "'Eccomi qua! #CLICK01#'",
    "'E' tutto mio!'",
    "'Vinco sempre!'",
    "'Bravo me!'",
    "'Forza aicab! Vado alla grande!'",
    "'Sono il re del gioco!'",
    "'Chiamatemi il magnifico!'",
    "'Vedo solo vittorie nella mia strada!'",
    "'Festa per me, fame per voi!'",
    "'#LAUGH02# Mi piace questo gioco!'",
    "'Haha! Fregati.'",
    "'Sono inarrestabile!'",
    "'Mi prendo i vostri soldi.'", "'Vittoria!'")

lowscore_mean_comments = (
    "'Che cosa! Maledizione!'",
    "'#AARGH03# Non di nuovo!'",
    "'Cosa! Dannazione!'",
    "'No! Uffa.'",
    "'Ehi! Malvagi!'",
    "'No no! #AARGH02#'",
    "'Ridicolo! Roba da matti!'",
    "'Oh no! #AARGH02#'",
    "'Mannaggia! I miei soldi.'",
    "'Veramente! E\' da pazzi!'",
    "'Impossibile! E\' disgustoso!'",
    "'#AARGH03#'",
    "'Non capisco! Maledizione!'",
    "'Seriamente! Ora basta.'",
    "'Che disastro!'",
    "'Mi sento derubato!'",
    "' Ora basta! #AARGH02#",
    "'Un'altra volta? Che noia!'",
    "'#AARGH03# Questo non va bene!'",
    "'Ora mi sento infuriato #AARGH02#'",
    "'Dannazione! #AARGH02#'",
    "'#AARGH03# Non ci posso credere!'",
    "'Rivoglio la mia fortuna!'",
    "'Che palle!'",
    "'#AARGH02# Non posso crederci.'",
    "'#AARGH03# Questa è una brutta notizia!'",
    "'Sono furioso. #AARGH02#'",
    "'Nessuna speranza in vista.'",
    "'Mai stato così arrabbiato.'")

# --- APOLOGETIC ICUB ---
highscore_apologetic_comments = (
    "'Mi spiace, ma ho bisogno dei soldi.'",
    "'devo pensare al mio budget, scusatemi.'",
    "'Perdonatemi, ho delle spese da coprire.'",
    "'L'ho fatto per il mio bene, scusate.'"
    "'Mi dispiace, ma devo garantire il mio sostentamento.'",
    "'Scusate, ma anche i robot hanno bisogno di soldi'",
    "'Mi dispiace!'",
    "'Perdonatemi, ma mi servono i soldi.'",
    "'Mi spiace ragazzi, ho bisogno di denaro.'",
    "'devo assicurarmi un futuro sicuro, mi spiace.'",
    "'Perdonatemi ragazzi, devo pensare a me stesso.'",
    "'Ho bisogno di denaro per mantenere il mio stile di vita, scusatemi.'",
    "'Scusatemi, ma ho bisogno di soldi per raggiungere i miei obiettivi.'",
    "'devo pensare al mio futuro, mi spiace.'",
    "'Perdonatemi, ma devo fare quello che è meglio per me.'",
    "'Mi spiace, mi serve il denaro'",
    "'Scusatemi, ma devo pensare al mio bene.'",
    "'Colpevole! Perdonatemi!'",
    "'Mi dispiace, ma devo pur sopravvivere.'",
    "'devo pensare al mio futuro finanziario, scusatemi.'",
    "'Perdonatemi, ma ho bisogno di un reddito stabile.'",
    "'Mi spiace, tuttavia devo fare quello che è meglio per me.'",
    "'Scusatemi, ho bisogno di soldi per raggiungere i miei obiettivi.'",
    "'Perdonatemi! Ho bisogno di essere indipendente.'",
    "'Mi dispiace, ma devo fare quello che è necessario per sopravvivere.'",
    "'devo pensare alla mia sicurezza finanziaria, scusatemi.'",
    "'Perdonatemi, ma ho bisogno di garantire il mio benessere finanziario.'",
    "'Mi spiace, tuttavia ho bisogno di un reddito stabile.'",
    "'#BREATH02# Scusatemi, ma ho bisogno di soldi per mantenermi.'",
    "'Mi dispiace!'",
    "'Perdonatemi, ho delle spese da coprire.'",
    "'devo fare quello che è meglio per me, scusatemi.'",
    "'Perdonatemi, ho bisogno di un reddito stabile.'",
    "'Mi spiace #BREATH02# '",
    "'Scusatemi, devo garantire il mio benessere.'",
    "'Perdonatemi, devo fare quello che è necessario per sopravvivere.'",
    "'Mi dispiace, ma ho bisogno di soldi per raggiungere i miei obiettivi.'",
    "'devo pensare alla mia sicurezza finanziaria, scusatemi.'",
    "'Perdonatemi, ma ho bisogno di garantire il mio benessere finanziario.'",
    "'Mi spiace, ho bisogno di denaro.'",
    "'Scusatemi!'",
    "'Perdonatemi,vdevo fare quello che è necessario per sopravvivere.'",
    "'Mi dispiace, mi servono soldi.'",
    "'devo fare quello che è meglio per me, scusatemi.'",
    "'Perdonatemi, ho bisogno di un reddito stabile.'")

lowscore_apologetic_comments = ()
