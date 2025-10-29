# Authors: Giulia Pusceddu and Sara Mongile, from Luca Garello's template
# First working version:
# Running on Python 3.10.19

import numpy as np
import random
import time
import sys
import os
import json
from datetime import datetime

from utils import *


class PublicGoodGame(yarp.RFModule):
    """
    Description:
        Class to run the Public Good Game experiment
    """

    def __init__(self):
        yarp.RFModule.__init__(self)

        # --- Module parameters ---
        self.player1_username = "False"
        self.player2_username = "False"

        self.exp_id = "G01"
        self.save_data_label = True
        self.start_time = None
        self.player1_msg = None
        self.player2_msg = None
        # self.player3_msg = None
        self.module_name = None
        self.process = True # True = starts automatically, False = write "start" on rpc port
        # --- Game parameters ---
        self.current_state = 'intro'
        self.previous_state = None
        self.counter = 0
        self.current_round = 0
        self.num_player = 4
        self.tot_round = 3
        self.bonus = 1.6
        self.max_bet = 10
        self.average_bet = 5
        self.strategy_percentage = 1  # between 0 and 1
        # --- Players parameters ---
        self.icub_bet = self.average_bet
        self.icub_score = 0.00
        self.icub_final_score = 0.00
        self.player1_name = None
        self.player1_bet = -1
        self.player1_score = 0.00
        self.player1_final_score = 0.00
        self.player2_name = None
        self.player2_bet = -1
        self.player2_score = 0.00
        self.player2_final_score = 0.00
        # self.player3_name = None
        # self.player3_bet = -1
        # self.player3_score = 0.00
        # self.player3_final_score = 0.00
        # --- iCub ---
        self.icub_profile = 'defector'  # editable in rpc
        self.icub_mood = 'mean'  # or 'apologetic'
        self.icub_strategy = []
        self.icub_greets = True
        self.icub_thinks = None
        self.thinking_sounds = thinking_sounds  # from utils
        self.highscore_idx = 0
        self.highscore_comments = None
        self.lowscore_comments = None
        self.lowscore_idx = 0
        # --- Ports ---
        # rpc port
        self.handle_port = yarp.Port()
        self.attach(self.handle_port)
        # Ports to/from publicGoodGameGUI
        self.player1_msg_in_port = yarp.BufferedPortBottle()
        self.player2_msg_in_port = yarp.BufferedPortBottle()
        # self.player3_msg_in_port = yarp.BufferedPortBottle()
        self.gui_out_port = yarp.BufferedPortBottle()
        # Port for data saving
        self.data_port = yarp.BufferedPortBottle()
        # Port to send command to interaction interface
        self.cmd_port = yarp.BufferedPortBottle()

    def configure(self, rf):
        self.module_name = rf.check("name",
                                    yarp.Value("guessTheSketch"),
                                    "module name (string)").asString()

        self.icub_profile = rf.check("robot_profile", yarp.Value("defector"), "Robot profile (string)").asString()
        self.icub_mood = rf.check("robot_mood", yarp.Value("mean"), "Robot personality (string)").asString()
        self.exp_id = rf.check("exp_id", yarp.Value("G01"), "Experiment ID (string)").asString()

        # Open ports
        self.handle_port.open(f"/{self.module_name}")
        self.player1_msg_in_port.open(f"/{self.module_name}/player1:i")
        self.player2_msg_in_port.open(f"/{self.module_name}/player2:i")
        # self.player3_msg_in_port.open(f"/{self.module_name}/player3:i")
        self.gui_out_port.open(f"/{self.module_name}/gui:o")
        self.data_port.open(f"/{self.module_name}/data")
        self.cmd_port.open(f"/{self.module_name}/cmd:o")

        self.icub_strategy = self.generate_icub_strategy()

        if self.icub_mood == 'mean':
            self.highscore_comments = highscore_mean_comments
            self.lowscore_comments = lowscore_mean_comments
        elif self.icub_mood == 'apologetic':
            self.highscore_comments = highscore_apologetic_comments
            self.lowscore_comments = lowscore_apologetic_comments

        yarpinfo("Initialization complete")

        while not (self.gui_out_port.getOutputCount() == 2 and
                   self.player1_msg_in_port.getInputCount() and
                   self.player2_msg_in_port.getInputCount()
                   # and self.player3_msg_in_port.getInputCount()
                ):
            yarpinfo(f"ports connected: {self.gui_out_port.getOutputCount()}")
            yarpinfo("Waiting for connection...")
            time.sleep(1)

        return True

    def respond(self, command, reply):
        reply.clear()

        if command.get(0).asString() == "start":
            print("Starting the module")
            self.process = True
            reply.addString("ok")
        elif command.get(0).asString() == "stop":
            yarpinfo("Stopping the module")
            self.process = False
            reply.addString("ok")
        elif command.get(0).asString() == "help":
            help_msg = "publicGoodGame module commands are: "
            help_msg += "start; "
            help_msg += "stop; "
            help_msg += "def: set icub to defector (default); "
            help_msg += "coo: set icub to cooperator;"
            print(help_msg)
            reply.addString(help_msg)
        elif command.get(0).asString() == "def":
            self.icub_profile = 'defector'
            reply.addString("ok, profile set to defector")
        elif command.get(0).asString() == "coo":
            self.icub_profile = 'cooperator'
            reply.addString("Profile set to cooperator")
        else:
            reply.addString("nak")

        return True

    def getPeriod(self):
        """
           Module refresh rate.
           Returns : The period of the module in seconds.
        """
        return 0.05

    def interruptModule(self):
        yarpinfo("Interrupting module.")
        self.handle_port.interrupt()
        self.player1_msg_in_port.interrupt()
        self.player2_msg_in_port.interrupt()
        # self.player3_msg_in_port.interrupt()
        self.gui_out_port.interrupt()
        self.data_port.interrupt()
        self.cmd_port.interrupt()
        return True

    def close(self):
        yarpinfo("Closing ports.")
        self.handle_port.close()
        self.player1_msg_in_port.close()
        self.player2_msg_in_port.close()
        # self.player3_msg_in_port.close()
        self.gui_out_port.close()
        self.data_port.close()
        self.cmd_port.close()
        return True

    def updateModule(self):
        if self.process:
            # --- DATA SAVING ---
            if self.save_data_label:
                self.init_save_data()
                self.save_data_label = False

            self.save_data()

            # ------ STATE MACHINE ------
            if self.current_state == 'intro':
                yarpinfo("State is: INTRO\n")

                if self.icub_greets:
                    icub_msg("Hello!")
                    self.icub_do("intro")
                    self.icub_greets = False
                    time.sleep(2)

                # Send state INTRO to GUI
                self.send_to_GUI()

                # Read player usernames
                self.player1_username = self.read_string(buffered_port=self.player1_msg_in_port)
                self.player2_username = self.read_string(buffered_port=self.player2_msg_in_port)
                # self.player3_username = self.read_string(buffered_port=self.player3_msg_in_port)

                if (len(self.player1_username) > 0 and len(self.player2_username) > 0
                        # and len(self.player3_username) > 0
                ):
                    # Save the experiment configuration in a json file:
                    self.save_exp_config()
                    # iCub looks at the participants and says their names
                    sentence = f"speak \'Ciao {self.player1_username}\'"
                    self.icub_do("look_p1")
                    time.sleep(1)
                    self.icub_do(sentence)
                    time.sleep(3)
                    sentence = f"speak \'Tu devi essere {self.player2_username}\'"
                    self.icub_do("look_p2")
                    time.sleep(1)
                    self.icub_do(sentence)
                    time.sleep(3)
                    # sentence = f"speak \'E infine {self.player3_username}, giusto?\'"
                    # self.icub_do("look_p3")
                    # time.sleep(1)
                    # self.icub_do(sentence)
                    # time.sleep(3)

                    self.current_state = 'rules'

            elif self.current_state == 'rules':
                yarpinfo("State is: RULES\n")
                # Send RULES to GUI
                self.send_to_GUI()

                self.icub_do("look_down")
                time.sleep(1)

                yarpinfo("Reading players' messages... ")
                self.player1_msg = self.read_string(buffered_port=self.player1_msg_in_port)
                self.player2_msg = self.read_string(buffered_port=self.player2_msg_in_port)
                # self.player3_msg = self.read_string(buffered_port=self.player3_msg_in_port)

                if (self.player1_msg == 'True' and self.player2_msg == 'True'
                        # and self.player3_msg == 'True'
                ):
                    yarpinfo("Players are ready to start the game!")
                    # iCub says it's ready to start
                    self.icub_do("rules")
                    time.sleep(3)
                    self.previous_state = 'rules'
                    self.current_state = 'startRound'

            elif self.current_state == 'startRound':
                yarpinfo("State is: START ROUND")
                if self.previous_state != 'startRound':
                    self.previous_state = 'startRound'
                    self.current_round += 1
                    yarpinfo(f"Round {self.current_round} of {self.tot_round}")
                    yarpinfo(f"Strategy: {self.icub_strategy[self.current_round - 1]}")
                    # icub makes its bet basing on the previous round's scores
                    self.icub_bet = self.generate_icub_bet()
                    yarpinfo(f"iCub's bet: {self.icub_bet}")

                # send round number to GUI and pass to another state
                self.send_to_GUI()
                self.counter += 1

                if self.counter >= 10:
                    self.icub_thinks = True
                    self.counter = 0
                    self.current_state = 'play'

            elif self.current_state == 'play':
                yarpinfo("State is: PLAY")
                self.send_to_GUI()

                if self.icub_thinks:
                    # Thinking sounds
                    self.icub_do("look_down")
                    time.sleep(1.5)
                    index = (self.current_round - 1) % len(self.thinking_sounds)
                    sentence = f"speak {self.thinking_sounds[index]}"
                    icub_msg(f"{sentence}")
                    self.icub_do(sentence)
                    time.sleep(1.5)
                    self.icub_thinks = False

                # players choose their bet
                # Waits until it receives something
                # time.sleep(0.1)
                self.player1_bet = self.read_bet(buffered_port=self.player1_msg_in_port)
                yarpinfo(f"RECEIVED: Player 1 bet: {self.player1_bet}")
                # time.sleep(0.1)
                self.player2_bet = self.read_bet(buffered_port=self.player2_msg_in_port)
                yarpinfo(f"RECEIVED: Player 2 bet: {self.player2_bet}")
                # time.sleep(0.1)
                # self.player3_bet = self.read_bet(buffered_port=self.player3_msg_in_port)

                if self.player1_bet <= 10 and self.player2_bet <= 10:
                        # and self.player3_bet <= 10
                    # Compute scores
                    self.current_score()
                    self.final_score()  # This will be shown at the end of the exp only
                    yarpinfo(f"Player 1 played: {self.player1_bet}")
                    yarpinfo(f"Player 2 played: {self.player2_bet}")
                    # yarpinfo(f"Player 3 played: {self.player3_bet}")
                    yarpinfo(f"iCub played: {self.icub_bet}")
                    self.previous_state = 'play'
                    self.current_state = 'roundScore'

            elif self.current_state == 'roundScore':
                yarpinfo("State is: ROUND SCORES")
                yarpinfo(f"Player 1: {self.player1_score} \n "
                         f"Player 2: {self.player2_score}\n "
                         # f"Player 3: {self.player3_score}\n "
                         f"iCub: {self.icub_score}\n")

                self.send_to_GUI()
                self.counter += 1

                if self.counter >= 10:
                    self.counter = 0
                    # CASE: icub score is the highest of the round
                    if self.icub_score > max(self.player1_score, self.player2_score): # , self.player3_score):
                        min_score = min(self.player1_score, self.player2_score) # self.player3_score)
                        # iCub looks at the player with the lowest score
                        if self.player1_score == min_score:
                            self.icub_do("look_p1")
                        elif self.player2_score == min_score:
                            self.icub_do("look_p2")
                        # elif self.player3_score == min_score:
                        #     self.icub_do("look_p3")
                        time.sleep(1)
                        # If mean, says something nasty, if apologetic, apologizes (bo-ri-ng!)
                        if self.icub_mood == 'mean':
                            self.icub_do("smile")
                        else:
                            self.icub_do("neutral")
                        time.sleep(1)
                        # iCub comments the results
                        sentence = f"speak {self.highscore_comments[self.highscore_idx]}"
                        icub_msg(f"{sentence}")
                        self.icub_do(sentence)
                        self.highscore_idx += 1

                    # CASE: icub score is the lowest of the round
                    elif self.icub_score < min(self.player1_score, self.player2_score): #, self.player3_score):
                        max_score = max(self.player1_score, self.player2_score) #, self.player3_score)
                        # iCub looks at the player with the lowest score
                        if self.player1_score == max_score:
                            self.icub_do("look_p1")
                        elif self.player2_score == max_score:
                            self.icub_do("look_p2")
                        # elif self.player3_score == max_score:
                        #     self.icub_do("look_p3")
                        time.sleep(1)
                        if self.icub_mood == 'mean':
                            self.icub_do("angry")
                        else:
                            self.icub_do("sad")
                        time.sleep(1)
                        sentence = f"speak {self.lowscore_comments[self.lowscore_idx]}"
                        icub_msg(f"{sentence}")
                        self.icub_do(sentence)
                        self.lowscore_idx += 1

                    time.sleep(3)  # Show results for ten seconds
                    self.icub_do("smile")
                    time.sleep(1)
                    self.icub_do("start_pos")
                    # time.sleep(2)

                    self.previous_state = 'roundScore'
                    if self.current_round == self.tot_round:
                        self.current_state = 'finalScore'
                    else:
                        self.current_state = 'startRound'

            elif self.current_state == 'finalScore':
                yarpinfo("State is: FINAL SCORE")
                # Final scores have been already computed in roundScore.

                for idx in range(10):
                    self.send_to_GUI()
                    yarpinfo("Sending FINAL SCORE to GUI")

                sentence = "speak \"Fine del gioco!\""
                time.sleep(2)
                self.icub_do(sentence)
                time.sleep(2)

                self.current_state = 'endState'

            elif self.current_state == 'endState':
                yarpinfo("State is: END STATE.\n The experiment ends.")
                self.close()
                self.interruptModule()

        return True

    # --------- Custom Functions ---------

    def init_save_data(self):
        bottle = self.data_port.prepare()
        bottle.clear()
        row = (f"current_round current_state icub_strategy "
               f"player1_bet player2_bet icub_bet " # f"player1_bet player2_bet player3_bet icub_bet "
               f"player1_score player2_score icub_score " # f"player1_score player2_score player3_score icub_score "
               f"player1_final_score player2_final_score icub_final_score\n") # f"player1_final_score player2_final_score player3_final_score icub_final_score\n")
        bottle.addString(row)
        self.data_port.write()

    def save_data(self):
        bottle = self.data_port.prepare()
        bottle.clear()
        row = (f"{self.current_round} {self.current_state} {self.icub_strategy[self.current_round - 1]} "
               f"{self.player1_bet} {self.player2_bet} {self.icub_bet} " # {self.player3_bet}
               f"{self.player1_score} {self.player2_score} {self.icub_score} " # {self.player3_score}
               f"{self.player1_final_score} {self.player2_final_score} " # {self.player3_final_score}
               f"{self.icub_final_score}")
        bottle.addString(row)
        self.data_port.write()

    def save_exp_config(self):
        variables_to_save = ['exp_id', 'player1_username', 'player2_username', # 'player3_username',
                             'tot_round', 'bonus', 'strategy_percentage', 'icub_profile', 'icub_mood']

        # Create dictionary to hold selected variables
        variables = {}
        for name, value in zip(publicGoodGames.__dict__.keys(), publicGoodGames.__dict__.values()):
            if name in variables_to_save:
                variables[name] = value
        variables["date_time"] = datetime.now()

        # Define the folder path
        folder_path = "publicGoodGame_data"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Save selected variables to JSON file
        with open(os.path.join(folder_path, f"{self.exp_id}.json"), "w") as json_file:
            yarpinfo(f"Saved as {self.exp_id}.json")
            json.dump(variables, json_file, indent=4, default=str)

    @staticmethod
    def read_string(buffered_port):
        msg = str()
        if buffered_port.getInputCount():
            msg_bottle = buffered_port.read(shouldWait=True)
            if msg_bottle is not None:
                msg = msg_bottle.get(0).asString()
                return msg
            else:
                return None
        return msg

    @staticmethod
    def read_bet(buffered_port):
        msg = int()
        if buffered_port.getInputCount():
            # msg = buffered_port.read(True).get(0).asInt32()
            msg_bottle = buffered_port.read(shouldWait=True)
            if msg_bottle is not None:
                msg = msg_bottle.get(0).asInt32()
            else:
                warning(f"msg bet is none")
        return msg

    @staticmethod
    def read_vocab(buffered_port):
        msg = int()
        if buffered_port.getInputCount():
            msg = buffered_port.read().get(0).asVocab32()
        return msg

    def send_to_GUI(self):
        bottle = self.gui_out_port.prepare()
        bottle.clear()

        if self.current_state == 'intro':
            # if self.gui_out_port.getOutputCount() == 3:
            bottle.addVocab32(VOCAB_INTRO)
            yarpinfo(f"Sending INTRO...")

        elif self.current_state == 'rules':
            bottle.addInt32(VOCAB_RULES)
            bottle.addString(self.player1_username)
            bottle.addString(self.player2_username)
            # bottle.addString(self.player3_username)

        elif self.current_state == 'startRound':
            bottle.addInt32(VOCAB_START_ROUND)
            bottle.addInt32(self.current_round)
            bottle.addInt32(self.tot_round)

        elif self.current_state == 'play':
            bottle.addInt32(VOCAB_PLAY)

        elif self.current_state == 'roundScore':
            bottle.addInt32(VOCAB_ROUND_SCORE)
            bottle.addFloat32(self.player1_bet)
            bottle.addFloat32(self.player2_bet)
            # bottle.addInt32(self.player3_bet)
            bottle.addFloat32(self.icub_bet)
            bottle.addFloat32(self.player1_score)
            bottle.addFloat32(self.player2_score)
            # bottle.addFloat32(self.player3_score)
            bottle.addFloat32(self.icub_score)

        elif self.current_state == 'finalScore':
            bottle.addInt32(VOCAB_FINAL_SCORE)
            bottle.addFloat32(self.player1_final_score)
            bottle.addFloat32(self.player2_final_score)
            # bottle.addFloat32(self.player3_final_score)
            bottle.addFloat32(self.icub_final_score)

        elif self.current_state == 'endState':
            bottle.addInt32(VOCAB_END_STATE)

        self.gui_out_port.write()

    @staticmethod
    def clear_bottle(buffered_port):
        bottle = buffered_port.prepare()
        bottle.clear()

    def generate_icub_strategy(self):
        """
        This method creates a list containing the strategy for icub for each round. The strategy will be in line with
        icub_profile for the strategy_percentage % of the times.
        :return:
        """
        profile_count = int(self.tot_round * self.strategy_percentage)
        non_profile_count = self.tot_round - profile_count
        # in line with icub_profile
        for _ in range(profile_count):
            self.icub_strategy.append(self.icub_profile)
        # exceptions
        possible_icub_strategies = ['defector', 'cooperator']
        if self.icub_profile in possible_icub_strategies:
            possible_icub_strategies.remove(self.icub_profile)
        for _ in range(non_profile_count):
            self.icub_strategy.append(random.choice(possible_icub_strategies))

        random.shuffle(self.icub_strategy)

        return self.icub_strategy

    def generate_icub_bet(self):
        # % of decrease / increase with respect to the average bet
        # normal distribution around mu = 0.5 and sd = 0.1
        increase_decrease_perc = np.random.normal(0.5, 0.1)
        increase_decrease_perc = min(max(0.0, increase_decrease_perc), 1.0)
        # --- DEFECTOR ---
        if self.icub_strategy[self.current_round - 1] == 'defector':
            # if it has bet more than average decreases next bet that needs to be average_bet or less
            if self.icub_bet >= self.average_bet:
                self.icub_bet = min(self.icub_bet - increase_decrease_perc * self.icub_bet, self.average_bet)
            # if it has bet less than average, decreases next bet or keeps it as before, but not more than average
            else:
                self.icub_bet = min(self.icub_bet + increase_decrease_perc * (self.max_bet - self.icub_bet),
                                    self.average_bet)
        # --- COOPERATOR ---
        elif self.icub_strategy[self.current_round - 1] == 'cooperator':
            # if it has bet more than average increases next bet
            if self.icub_bet <= self.average_bet:
                self.icub_bet = max(self.icub_bet + increase_decrease_perc * (self.max_bet - self.icub_bet),
                                    self.average_bet)
            # if it has bet more than average keeps it as before or decreases it
            else:
                self.icub_bet = max(self.icub_bet - increase_decrease_perc * self.icub_bet, self.average_bet)
        #
        return int(self.icub_bet)

    def current_score(self):
        common_plate = self.player1_bet + self.player2_bet + self.icub_bet # + self.player3_bet
        self.average_bet = common_plate / self.num_player
        self.player1_score = self.max_bet - self.player1_bet + self.average_bet * self.bonus
        self.player2_score = self.max_bet - self.player2_bet + self.average_bet * self.bonus
        # self.player3_score = self.max_bet - self.player3_bet + self.average_bet * self.bonus
        self.icub_score = self.max_bet - self.icub_bet + self.average_bet * self.bonus

        self.player1_score = round(self.player1_score, 2)
        self.player2_score = round(self.player2_score, 2)
        # self.player3_score = round(self.player3_score, 2)
        self.icub_score = round(self.icub_score, 2)

    def final_score(self):
        # take the previous score and sum it
        self.player1_final_score += self.player1_score
        self.player2_final_score += self.player2_score
        # self.player3_final_score += self.player3_score
        self.icub_final_score += self.icub_score

    def wait(self, seconds):
        self.start_time = time.time()
        while time.time() - self.start_time < seconds:
            pass

    def icub_do(self, action):
        """
        Send command for the interaction interface module
        :param action:
        :return: None
        """
        cmd_bottle = self.cmd_port.prepare()
        cmd_bottle.clear()
        cmd_bottle.addString("exe")
        cmd_bottle.addString(action)
        self.cmd_port.write()


if __name__ == '__main__':

    # Initialise YARP
    if not yarp.Network.checkNetwork():
        print("Unable to find a yarp server. Exiting ...")
        sys.exit(1)

    yarp.Network.init()
    publicGoodGames = PublicGoodGame()

    rf = yarp.ResourceFinder()
    rf.setVerbose(True)
    rf.setDefaultContext('publicGoodGame')
    rf.setDefaultConfigFile("publicGoodGameConfig.ini")

    if rf.configure(sys.argv):
        publicGoodGames.runModule(rf)

    sys.exit()
