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

greet_right_arm(){

  echo "ctpq time 2.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0 -11.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/right_arm/rpc
  echo "ctpq time 0.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0  25.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/right_arm/rpc
  echo "ctpq time 0.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0 -11.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/right_arm/rpc
  echo "ctpq time 0.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0  25.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/right_arm/rpc
  echo "ctpq time 0.5 off 0 pos (-60.0 44.0 -2.0 96.0 53.0 -17.0 -11.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" | yarp rpc /ctpservice/right_arm/rpc
   	
}

start_pos(){
  neutral
  echo "abs 0 -5 0" | yarp write ... /iKinGazeCtrl/angles:i
  echo "ctpq time 2 off 0 pos (0 0 0)" | yarp rpc /ctpservice/torso/rpc
  sleep 1.0
	echo "ctpq time 2.5 off 0 pos (-6.0 23.0 25.0 29.0 -24.0 -3.0 -3.0 19.0 29.0 8.0 30.0 32.0 42.0 50.0 50.0 114.0)" | yarp rpc /ctpservice/left_arm/rpc
  echo "ctpq time 2.5 off 0 pos (-6.0 23.0 25.0 29.0 -24.0 -3.0 -3.0 19.0 29.0 8.0 30.0 32.0 42.0 50.0 50.0 114.0)" | yarp rpc /ctpservice/right_arm/rpc
  sleep 3.0
}

#######################################################################################
# FUNCTIONS LOOK:                                                               #
#######################################################################################

look_at_participant(){
  echo "abs 0 -5 0" | yarp write ... /iKinGazeCtrl/angles:i
}

look_at_cat(){
  echo "abs 10 -40 0" | yarp write ... /iKinGazeCtrl/angles:i
}

look_at_dog(){
  echo "abs -19 -40 0" | yarp write ... /iKinGazeCtrl/angles:i
}

look_at_orange(){
  echo "abs 15 -30 0" | yarp write ... /iKinGazeCtrl/angles:i
}

look_at_apple(){
  echo "abs -15 -30 0" | yarp write ... /iKinGazeCtrl/angles:i
}

look_at_house(){
  echo "abs 28 -20 0" | yarp write ... /iKinGazeCtrl/angles:i
}

look_at_park(){
  echo "abs -28 -20 0" | yarp write ... /iKinGazeCtrl/angles:i
}

look_at_giovanna(){
  echo "abs 60 -5 0" | yarp write ... /iKinGazeCtrl/angles:i
  echo "ctpq time 2 off 0 pos (30 0 -8)" | yarp rpc /ctpservice/torso/rpc
}

look_at_navel(){
  echo "abs -60 -15 0" | yarp write ... /iKinGazeCtrl/angles:i
  echo "ctpq time 2 off 0 pos (-30 0 -8)" | yarp rpc /ctpservice/torso/rpc
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


