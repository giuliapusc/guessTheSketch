#!/bin/bash
#######################################################################################
# FLATWOKEN ICON THEME CONFIGURATION SCRIPT
# Copyright: (C) 2014 FlatWoken icons7 Robotics Brain and Cognitive Sciences
# Author:  Giulia Pusceddu
# email:  giulia.pusceddu@iit.it
# Permission is granted to copy, distribute, and/or modify this program
# under the terms of the GNU General Public License, version 2 or any
# later version published by the Free Software Foundation.
#  *
# A copy of the license can be found at
# http://www.robotcub.org/icub/license/gpl.txt
#  *
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details
#######################################################################################

#######################################################################################
# ICUB SPEECH AND MOVEMENTS FOR PUBLIC GOOD GAME EXPERIMENT:                                                        #
#######################################################################################


# include icub_basics
source /usr/local/src/robot/cognitiveInteraction/icub-interaction-demos/app/icubDemos/conf/icub_basics.sh #check if the path is correct or not

#######################################################################################
# MAIN FUNCTIONS:                                                                    #
#######################################################################################

close_eyes(){
	echo "S65" | yarp write ... /icub/face/eyelids/raw/in
}

open_eyes(){
	echo "S08" | yarp write ... /icub/face/eyelids/raw/in
}

greet_right_arm(){

  echo "ctpq time 2.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0 -11.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/right_arm/rpc
  echo "ctpq time 0.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0  25.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/right_arm/rpc
  echo "ctpq time 0.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0 -11.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/right_arm/rpc
  echo "ctpq time 0.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0  25.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/right_arm/rpc
  echo "ctpq time 0.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0 -11.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/right_arm/rpc
   	
}

start_pos(){
	echo "ctpq time 2.5 off 0 pos (-6.0 23.0 25.0 29.0 -24.0 -3.0 -3.0 19.0 29.0 8.0 30.0 32.0 42.0 50.0 50.0 114.0)" | yarp rpc /ctpservice/left_arm/rpc
  echo "ctpq time 2.5 off 0 pos (-6.0 23.0 25.0 29.0 -24.0 -3.0 -3.0 19.0 29.0 8.0 30.0 32.0 42.0 50.0 50.0 114.0)" | yarp rpc /ctpservice/right_arm/rpc
  look_down
  sleep 3.0
}
#######################################################################################
# "MAIN" DEMOS:                                                                    #
#######################################################################################
intro() {
  look_p2
	speak "Ciao!"
  sleep 2.0
 
  greet_right_arm
  smile && speak "Io sono aicab!"
    	
  sleep 2.0
  start_pos
  smile
}

rules() {
	speak "Tutto chiaro. Sono pronto per iniziare anch'io."
  sleep 2.0
  start_pos
  smile
}

goodbye() {
	smile
  	echo "ctpq time 2.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0 -11.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/left_arm/rpc
   	sleep 2.0 && speak "Ciao amici, grazie per aver giocato con me !"
   	echo "ctpq time 0.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0  25.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/left_arm/rpc
    	echo "ctpq time 0.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0 -11.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/left_arm/rpc
    	echo "ctpq time 0.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0  25.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/left_arm/rpc
   	echo "ctpq time 0.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0 -11.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/left_arm/rpc
    	smile
    	sleep 4.0 && speak "Ci vediamo!"
   	echo "ctpq time 2.5 off 0 pos (-6.0 23.0 25.0 29.0 -24.0 -3.0 -3.0 19.0 29.0 8.0 30.0 32.0 42.0 50.0 50.0 114.0)" | yarp rpc /ctpservice/right_arm/rpc
    	echo "ctpq time 2.5 off 0 pos (-6.0 23.0 25.0 29.0 -24.0 -3.0 -3.0 19.0 29.0 8.0 30.0 32.0 42.0 50.0 50.0 114.0)" | yarp rpc /ctpservice/left_arm/rpc
    	smile
}

press_key(){
  echo "ctpq time 2 off 0 pos (-17.989011 60.142857 48.281978 118.043956 24.212504 -16.285714 -1.978022 13.510583 58.4198 22.535264 51.734322 0.0 1.165385 57.962563 153.660138 155.057471)" | yarp rpc /ctpservice/left_arm/rpc
}

#######################################################################################
# FUNCTIONS EYES:                                                               #
#######################################################################################

look_at_participant(){
  echo "abs 15 0 0" | yarp write ... /iKinGazeCtrl/angles:i
}

look_at_cat(){
  echo "abs 0 0 0" | yarp write ... /iKinGazeCtrl/angles:i
}

# Look left
look_at_dog(){
  echo "abs -15 0 0" | yarp write ... /iKinGazeCtrl/angles:i
}

look_at_apple(){
  echo "abs 0 -15 0" | yarp write ... /iKinGazeCtrl/angles:i
}

look_at_orange(){
  echo "abs 0 -15 0" | yarp write ... /iKinGazeCtrl/angles:i
}

look_at_house(){
  echo "abs 0 -15 0" | yarp write ... /iKinGazeCtrl/angles:i
}

look_at_park(){
  echo "abs 0 -15 0" | yarp write ... /iKinGazeCtrl/angles:i
}

look_at_giovanna(){
  echo "abs 0 -15 0" | yarp write ... /iKinGazeCtrl/angles:i
}

look_at_navel(){
  echo "abs 0 -15 0" | yarp write ... /iKinGazeCtrl/angles:i
}

pet_the_cat(){
  look_at_cat
	echo "ctpq time 2.5 off 0 pos (-6.0 23.0 25.0 29.0 -24.0 -3.0 -3.0 19.0 29.0 8.0 30.0 32.0 42.0 50.0 50.0 114.0)" | yarp rpc /ctpservice/left_arm/rpc
  echo "ctpq time 2.5 off 0 pos (-6.0 23.0 25.0 29.0 -24.0 -3.0 -3.0 19.0 29.0 8.0 30.0 32.0 42.0 50.0 50.0 114.0)" | yarp rpc /ctpservice/right_arm/rpc
}

pet_the_dog(){
  look_at_dog
	echo "ctpq time 2.5 off 0 pos (-6.0 23.0 25.0 29.0 -24.0 -3.0 -3.0 19.0 29.0 8.0 30.0 32.0 42.0 50.0 50.0 114.0)" | yarp rpc /ctpservice/left_arm/rpc
  echo "ctpq time 2.5 off 0 pos (-6.0 23.0 25.0 29.0 -24.0 -3.0 -3.0 19.0 29.0 8.0 30.0 32.0 42.0 50.0 50.0 114.0)" | yarp rpc /ctpservice/right_arm/rpc
}

point_to_park(){
  look_at_park
	echo "ctpq time 2.5 off 0 pos (-6.0 23.0 25.0 29.0 -24.0 -3.0 -3.0 19.0 29.0 8.0 30.0 32.0 42.0 50.0 50.0 114.0)" | yarp rpc /ctpservice/left_arm/rpc
  echo "ctpq time 2.5 off 0 pos (-6.0 23.0 25.0 29.0 -24.0 -3.0 -3.0 19.0 29.0 8.0 30.0 32.0 42.0 50.0 50.0 114.0)" | yarp rpc /ctpservice/right_arm/rpc
}

point_to_house(){
  look_at_house
	echo "ctpq time 2.5 off 0 pos (-6.0 23.0 25.0 29.0 -24.0 -3.0 -3.0 19.0 29.0 8.0 30.0 32.0 42.0 50.0 50.0 114.0)" | yarp rpc /ctpservice/left_arm/rpc
  echo "ctpq time 2.5 off 0 pos (-6.0 23.0 25.0 29.0 -24.0 -3.0 -3.0 19.0 29.0 8.0 30.0 32.0 42.0 50.0 50.0 114.0)" | yarp rpc /ctpservice/right_arm/rpc
}


#######################################################################################
# "MAIN" FUNCTION:                                                                    #
#######################################################################################
list() {
	compgen -A function
}

echo "********************************************************************************"
echo ""

$1 "$2"

if [[ $# -eq 0 ]] ; then 
    echo "No options were passed!"
    echo ""
    usage
    exit 1
fi


