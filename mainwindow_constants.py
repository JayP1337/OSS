# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 16:38:07 2016

@author: ekk
"""

# define all constants that build the GUI
FULLSCREEN = 1
HOR_RES  = 1920
VERT_RES = 1080
TOPBAR_RES = 70
BOTTOMBAR_RES = 70
RIGHTBAR_RES = 320
LINEWIDTH = 3
BEAMISO_HOR = 1026/2.5
BEAMISO_VERT = 665/2.5
VESSEL_HOR = 317
VESSEL_VERT = 454
BUTTON_HOR = 90
BUTTON_VERT = 23
SAFEMODEBUTTON_HOR = 220
SAFEMODEBUTTON_VERT = 34
OPERATOR = "SIM OPERATOR"
LOCAL_MODE = 1    # set to 0 for whitepark simulator, to 1 for standalone testing, to 2 for test PC at whitepark with OPC, to 3 for test PC at whitepark without OPC

# Standard button styles
STYLEOSSWRITE     = "background:white; \n"    "color: black;\n"      "border: 5px solid #a6a6a6;\n"   # write enabled, set in LBC, not in OS
STYLEHMIWRITE     = "background:orange; \n"    "color: black;\n"      "border: 5px solid #a6a6a6;\n"# write enabled, set in OSS, not in LBC
STYLELBCWRITE     = "background:#a6a6a6; \n"    "color: black;\n"      "border: 5px solid white;\n"   # write enabled, set in LBC, noting set by OSS/HMI
STYLELBCOSSWRITE  = "background:white; \n"    "color: black;\n"     "border: 5px solid white;\n"   # write enabled, set in LBC and OSS
STYLELBCHMIWRITE  = "background:orange; \n"    "color: black;\n"      "border: 5px solid white;\n"   # write enabled, set in LBC and HMI


STYLEOSSNOWRITE     = "background:white; \n"    "color: #a6a6a6;\n"      "border: 5px solid #a6a6a6;\n"   # write enabled, set in LBC, not in OS
STYLEHMINOWRITE     = "background:orange; \n"    "color: #a6a6a6;\n"      "border: 5px solid #a6a6a6;\n"# write enabled, set in OSS, not in LBC
STYLELBCNOWRITE     = "background:#a6a6a6; \n"    "color: #a6a6a6;\n"      "border: 5px solid white;\n"   # write enabled, set in LBC, noting set by OSS/HMI
STYLELBCOSSNOWRITE  = "background:white; \n"    "color: #a6a6a6;\n"     "border: 5px solid white;\n"   # write enabled, set in LBC and OSS
STYLELBCHMINOWRITE  = "background:orange; \n"    "color: #a6a6a6;\n"      "border: 5px solid white;\n"   # write enabled, set in LBC and HMI

STYLEWRITE          = "background:#a6a6a6; \n"  "color: black;\n"       "border: 5px solid #a6a6a6;\n"
STYLENOWRITE        = "background:#a6a6a6; \n"  "color: white;\n"       " border: 5px solid #a6a6a6; \n"
STYLEWRITEDASHED    = "background:black;\n"     "color: white;\n"       "border: 1px dashed white;\n" 
STYLEWHITE          = "background-color: white"

STYLEFLU = ["color: white;\n" "border: 2px solid black;\n" "border-radius: 2px;\n" "background:black;\n",
             "color: black;\n" "border: 2px solid #0000ff;\n" "border-radius: 2px;\n" "background:#0000ff;\n",
             "color: black;\n" "border: 2px solid #8080ff;\n" "border-radius: 2px;\n" "background:#8080ff;\n",
             "color: black;\n" "border: 2px solid #ffccff;\n" "border-radius: 2px;\n" "background:#ffccff;\n",
             "color: black;\n" "border: 2px solid #ff9999;\n" "border-radius: 2px;\n" "background: #ff9999;\n",
             "color: black;\n" "border: 2px solid #ff80ff;\n" "border-radius: 2px;\n" "background: #ff80ff;\n",
             "color: black;\n" "border: 2px solid #999966;\n" "border-radius: 2px;\n" "background: #999966;\n"]

FLUCONFIG = [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8]  # HMI init versus OSS init, 0 = no FLU

ACTIVE_BEAMS = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

NO_BEAMS = 16
beamIDtext = ["S1","S2","S3","S4","S5","S6","S7","S8","P1","P2","P3","P4","P5","P6","P7","P8"]

NO_ACTIVEFLAGS = 19
labelTextActive = ["Cabin Right","Cabin Left","Beam Walkway Right","Beam Walkway Left","Other Beam","Y-manifold Right","Y-manifold Left","LCA Middle","LCA End","Lower Beam Entrance","Air Compressor Room","Walkway E-room","LOP 2597","E-room 1","E-room 2","Forward Beam","Exit Door Beam","Lower Beam Middle","OSS Communication Timeout"]

NO_IGNOREFLAGS = 13
labelTextIgnore = ["AFE XY","LHPU","Z drive","Y hydraulics","Air compr","Racklocks","Y brakes","Y motors","Pinlock","Z locking","X locking","X motors","Other beam" ]

labelTextEstopReaction = [["X-locking E-stop reaction \nduring unlock","STOP","BYPASS"],["Y hydraulic E-stop reaction","ISOLATED","ALLOW EXT"],["", "BYPASS","ALLOW RETR"],["AHC E-stop reaction during AHC","STOP", "BYPASS"],["Y-brakes E-stop delay","0.0", ""]]

NO_ESTOPOUTPUTS = 13
labelTextOutput = labelTextIgnore

NO_SAFETYINPUTS = 19+16 + 1
labelTextInput = ["Fore Bridge","Aft Bridge","Cabin Right","Cabin Left","Beam Walkway Right","Beam Walkway Left","Other Beam","Y-manifold Right","Y-manifold Left","LCA Middle","LCA End","Lower Beam Entrance","Air Compressor Room","Walkway E-room","LOP 2597","E-room 1","E-room 2","Forward Beam","Exit Door Beam","Lower Beam Middle","Safety input 0","Safety input 1","Safety input 2","Safety input 3","Safety input 4","Safety input 5","Safety input 6","Safety input 7","Safety input 8","Safety input 9","Safety input 10","Safety input 11","Safety input 12","Safety input 13","Safety input 14","Safety input 15"]

HOST = 'opc.tcp://10.10.0.1:49320'

NO_BEAMSAFEMODES = 9
labelTextBeamSafe = ["LOCK","AMC","CONNECTING","FREEWHEEL","FAST LIFT START","FAST LIFT X LOCK","FAST LIFT XY LOCK","HOLD","CUSTOM"]

NO_DRIVESAFEMODES = 8  # number of rows in matrix (columns is fixed at 3 (X,Y,Z))
labelTextDriveSafe =[["X-DRIVE:","BRAKE AND LOCK","FREEWHEEL", "","","","","MAINTAIN","CUSTOM"],
                     ["Y-DRIVE:","BRAKE AND LOCK","FREEWHEEL", "ALLOW BEAM EXTEND","ALLOW BEAM RETRACT","","","MAINTAIN","CUSTOM"],
                     ["Z-DRIVE:","AHC PASSIVE BLOCKED","AHC PASSIVE FREE","","","","","MAINTAIN","CUSTOM"]]


labelTextPeopleInBeam = ["MANNED","UNMANNED","CUSTOM"]


# MAPPING BETWEEN BEAM SAFE MODES AND DRIVE SAFE MODES         
XDRIVEMAPPING = [0, 6, 1, 1, 6, 0, 0, 0, 7]
YDRIVEMAPPING = [0, 6, 1, 1, 6, 6, 2, 0, 7] 
ZDRIVEMAPPING = [0, 1, 6, 0, 6, 6, 6, 1, 7] 


## MAPPING BETWEEN DRIVE SAFE MODES AND IGNORE FLAGS         
#       See mainwindow_functions.py


## MAPPING BETWEEN DRIVE SAFE MODES AND E-STOP REACTIONS 
#       See mainwindow_functions.py

## FLU PAGE CONSTANTS
STARTING_X = 35
STARTING_Y = 125
BOX_WIDTH = 220
BOX_HIGHT = 100
SPACER = 20
BEAMBOX_SIZE = 30
BEAMLABEL_SIZE = 25
STARTING_BEAMBOX_X = 215
STARTING_BEAMBOX_Y = 143
FLUCONFIG_2 = [True, False, True, False, True, False, True, False]
LINK_ESTOP_ALL_BEAMS = True

# FLU NAVIGATION BAR LINES CONSTANTS
LINE_STARTING_X = 22
LINE_STARTING_Y = 50
LINE_WIDTH = 2
VERT_LINE_LENGTH = 30
HOR_LINE_LENGTH = 10
X_SPACER = 256
Y_SPACER = 57

# FLU OVERVIEW/HOME PAGE LINES
OVERVIEW_LINE_STARTING_X = 37
OVERVIEW_LINE_STARTING_Y = 73
OVERVIEW_LINE_WIDTH = 3
OVERVIEW_VERT_LINE_LENGTH = 110
OVERVIEW_HOR_LINE_LENGTH = 20
OVERVIEW_X_SPACER = 1500
OVERVIEW_Y_SPACER = 226

# LINK E-STOP TO ALL BEAMS NAVIGATION BAR LINES
LINK_ESTOP_ALL_BEAMS_STARTING_X = 22
LINK_ESTOP_ALL_BEAMS_STARTING_Y = 50
LINK_ESTOP_ALL_BEAMS_VERT_LINE_LENGTH = 50
LINK_ESTOP_ALL_BEAMS_HOR_LINE_LENGTH = 15
LINK_ESTOP_ALL_BEAMS_Y_SPACER = 20

# LINK E-STOP TO ALL BEAMS OVERVIEW/HOME PAGE LINES
OVERVIEW_LINK_ESTOP_ALL_BEAMS_STARTING_X = 800
OVERVIEW_LINK_ESTOP_ALL_BEAMS_STARTING_Y = 73
OVERVIEW_LINK_ESTOP_ALL_BEAMS_VERT_LINE_LENGTH = 787
OVERVIEW_LINK_ESTOP_ALL_BEAMS_HOR_LINE_LENGTH = 55
OVERVIEW_LINK_ESTOP_ALL_BEAMS_Y_SPACER = 112
