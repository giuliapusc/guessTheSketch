# Authors: Giulia Pusceddu 
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
import tkinter as tk
from tkinter import messagebox


class guessTheSketch(yarp.RFModule):
    """
    Description:
        Class to run the Guess The Sketch experiment
    """

    def __init__(self):
        yarp.RFModule.__init__(self)

        yarpinfo(ICUB_ACTIONS)
        yarpinfo(expanded_rounds)

        #TODO use expanded trials from utils for actions 

        # --- Module parameters ---
        self.module_name = None
        self.process = False # True = starts automatically, False = write "start" on rpc port
        
        # --- Game parameters ---
        self.current_state = 'intro'
        self.current_round = 0

        # --- Ports ---
        # rpc port
        self.handle_port = yarp.Port()
        self.attach(self.handle_port)
        # Ports to/from whiteboardApp 
        self.in_port = yarp.BufferedPortBottle()
        self.out_port = yarp.BufferedPortBottle()
        # Port to external speaker
        self.speaker_port = yarp.BufferedPortBottle()
        # Port for data saving
        self.data_port = yarp.BufferedPortBottle()
        # Port to send command to interaction interface
        self.cmd_port = yarp.BufferedPortBottle()

        self.init_save_data()

    def configure(self, rf):
        self.module_name = rf.check("name",
                                    yarp.Value("guessTheSketch"),
                                    "module name (string)").asString()
        
        # Open ports
        self.handle_port.open(f"/{self.module_name}")
        # Ports to/from whiteboardApp
        self.in_port.open(f"/{self.module_name}/whiteboard:i")
        self.out_port.open(f"/{self.module_name}/whiteboard:o")
        # Port to external speaker 
        self.speaker_port.open(f"/{self.module_name}/speaker:o")

        self.data_port.open(f"/{self.module_name}/data")
        self.cmd_port.open(f"/{self.module_name}/cmd:o")

        yarpinfo("Initialization complete")

        # while not (self.out_port.getOutputCount() == 1 and
        #            self.in_port.getInputCount()
        #         ):
        #     yarpinfo("Waiting for port connection...")
        #     time.sleep(1)
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
            help_msg = "guessTheSketch module commands are: "
            help_msg += "start; "
            help_msg += "stop; "
            print(help_msg)
            reply.addString(help_msg)
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
        self.in_port.interrupt()
        self.out_port.interrupt()
        self.data_port.interrupt()
        self.cmd_port.interrupt()
        return True

    def close(self):
        yarpinfo("Closing ports.")
        self.handle_port.close()
        self.in_port.close()
        self.out_port.close()
        self.data_port.close()
        self.cmd_port.close()
        return True

    def updateModule(self):
        if self.process:
            # --- DATA SAVING ---
            self.save_data()

            # ------ STATE MACHINE ------
            if self.current_state == 'intro':
                yarpinfo("State is: INTRO\n")

                # icub in starting position
                self.icub_do("start_pos")
                time.sleep(10)

                # sentence = f"""speak "Ciao!" """
                # self.icub_do("sentence")
                # time.sleep(2)
                # self.external_voice("Benvenuti!")
                # time.sleep(2)

                self.current_state = 'rules'

            elif self.current_state == 'rules':
                yarpinfo("State is: RULES\n")
                # Send RULES to GUI
                self.send_to_GUI()

                # speaker_msg("Rules")
                # self.external_voice("Queste sono le regole!")
                # time.sleep(5)

                self.current_state = 'startRound'

            elif self.current_state == 'startRound':
                yarpinfo("State is: START ROUND")
                yarpinfo(f"Current round: {self.current_round} out of {MAX_ROUNDS}")
                if self.current_round >= MAX_ROUNDS:
                    self.current_state = 'endState'
                else: 
                    self.send_to_GUI()
                    time.sleep(2)
                    self.current_round += 1
                    self.current_state = 'sketch'

            elif self.current_state == 'sketch':
                yarpinfo("State is: SKETCH")
                msg_from_whiteboard = self.read_vocab(buffered_port=self.in_port)

                if msg_from_whiteboard ==  VOCAB_END_SKETCH:
                    self.current_state = 'action'

            elif self.current_state == 'action':
                yarpinfo("State is: ACTION")

                actions = ICUB_ACTIONS[self.current_round - 1]
                yarpinfo(actions)
                for action in actions:
                    self.icub_do(action)
                    time.sleep(4)

                self.icub_do("start_pos")
                
                self.current_state = 'understood'

            elif self.current_state == 'understood':
                yarpinfo("State is: UNDERSTOOD")
                self.send_to_GUI() 

                msg_from_whiteboard = self.read_vocab(buffered_port=self.in_port)

                if msg_from_whiteboard ==  VOCAB_END_SKETCH:
                    self.current_state = 'startRound'

            elif self.current_state == 'endState':
                yarpinfo("State is: END STATE.\n The experiment ends.")
                # self.external_voice("Grazie per aver partecipato!")
                # time.sleep(2)
                # sentence = f"""speak "Arrivederci!" """
                # self.icub_do(sentence)
                
                self.close()
                self.interruptModule()

        return True

    # --------- Custom Functions ---------

    def init_save_data(self):
        bottle = self.data_port.prepare()
        bottle.clear()
        row = (f"current_round current_state\n") 
        bottle.addString(row)
        self.data_port.write()

    def save_data(self):
        bottle = self.data_port.prepare()
        bottle.clear()
        row = (f"{self.current_round} {self.current_state}")
        bottle.addString(row)
        self.data_port.write()

    def save_exp_config(self):
        variables_to_save = ['exp_id', 'player1_username', 'player2_username',
                             'tot_round', 'bonus', 'strategy_percentage', 'icub_profile', 'icub_mood']

        # Create dictionary to hold selected variables
        variables = {}
        for name, value in zip(guessthesketch.__dict__.keys(), guessthesketch.__dict__.values()):
            if name in variables_to_save:
                variables[name] = value
        variables["date_time"] = datetime.now()

        # Define the folder path
        folder_path = "data"
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
    def read_vocab(buffered_port):
        msg = int()
        if buffered_port.getInputCount():
            msg_bottle = buffered_port.read(shouldWait=True)
            if msg_bottle is not None:
                msg = msg_bottle.get(0).asVocab32()
            
            # cmd = data.get(0).asVocab32()
            # debug(f"reading vocab32: {msg}")
        return msg

    def send_to_GUI(self):
        bottle = self.out_port.prepare()
        bottle.clear()

        if self.current_state == 'intro':
            # if self.gui_out_port.getOutputCount() == 3:
            bottle.addVocab32(VOCAB_INTRO)
            yarpinfo(f"Sent INTRO to GUI: {VOCAB_INTRO}")

        elif self.current_state == 'rules':
            bottle.addInt32(VOCAB_RULES)
            yarpinfo(f"Sent RULES to GUI: {VOCAB_RULES}")

        elif self.current_state == 'startRound':
            bottle.addInt32(VOCAB_NEXT_SKETCH)
            yarpinfo(f"Sent NEXT ROUND to GUI: {VOCAB_NEXT_SKETCH}")
        
        elif self.current_state == 'understood':
            bottle.addInt32(VOCAB_UNDERSTOOD)
            yarpinfo(f"Sent UNDERSTOOD to GUI: {VOCAB_UNDERSTOOD}")

        elif self.current_state == 'endState':
            bottle.addInt32(VOCAB_FINISH)
            yarpinfo(f"Sent FINISH to GUI: {VOCAB_FINISH}")

        self.out_port.write()

    @staticmethod
    def clear_bottle(buffered_port):
        bottle = buffered_port.prepare()
        bottle.clear()

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
        icub_msg(action)
    
    def external_voice(self, speech):
        # send text to acapelaSpeak
        if self.speaker_port.getOutputCount():
            speaker_bottle = self.speaker_port.prepare()
            speaker_bottle.clear()
            speaker_bottle.addString(speech)
            self.speaker_port.write()
            speaker_msg(speech)



if __name__ == '__main__':

    # Initialise YARP
    if not yarp.Network.checkNetwork():
        print("Unable to find a yarp server. Exiting ...")
        sys.exit(1)

    yarp.Network.init()
    guessthesketch = guessTheSketch()

    rf = yarp.ResourceFinder()
    rf.setVerbose(True)
    rf.setDefaultContext('guessTheSketch')
    rf.setDefaultConfigFile("guessTheSketch.ini")

    if rf.configure(sys.argv):
        guessthesketch.runModule(rf)

    sys.exit()
