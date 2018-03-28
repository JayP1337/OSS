# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 16:38:07 2016

@author: ekk
"""

########################## IMPORT #######################################
from PyQt5 import QtCore
import sys
from mainwindow_constants import *  #holds all constant values that define GUI geometry
from mainwindow_functions import *  #holds all functions that define GUI status

if LOCAL_MODE <> 1:
    import clr
    clr.AddReference('AllseasOPC')
    import AllseasOPC
import os
dir = os.path.dirname(__file__)
sys.path.append(dir)



########################## CLASS #######################################

    
class Ui_MainWindow(Helper):
    
    def __init__(self, oss):
         Helper.__init__(self)
         self.oss = oss
         self.counter = 0
         self.reset = False
         self.uploaded = False
         self.resetCounter = 0
         
         # initial HMI and OSS values        
         self.writeSwitchData = [0 for i in range(NO_BEAMS)]
         self.beamSafeData = [[0 for i in range(NO_BEAMS)] for k in range(2)]   #start in custom
         self.driveSafeData = [[[0 for i in range(3)] for j in range(NO_BEAMS)]  for k in range(2)]   #start in custom
         self.activeFlagData = [[[1 for i in range(NO_ACTIVEFLAGS)] for j in range(NO_BEAMS)]     for k in range(3)]   # 0 = HMI, 1=OSS, 2=LBC-F
         self.ignoreFlagData = [[[0 for i in range(NO_IGNOREFLAGS)] for j in range(NO_BEAMS)]    for k in range(3)]    # 0 = HMI, 1=OSS, 2=LBC-F 
         for k in range(NO_BEAMS):         
             self.ignoreFlagData[0][k][0] = 1
             self.ignoreFlagData[1][k][0] = 1
             self.ignoreFlagData[2][k][0] = 1
             
         self.eReactionData = [[[0 for i in range(4)] for j in range(NO_BEAMS)] for k in range(3)]  # 0 = HMI, 1=OSS, 2=LBC-F 
         for k in range(NO_BEAMS): 
             self.eReactionData[0][k][0] = 1
             self.eReactionData[1][k][0] = 1
             self.eReactionData[2][k][0] = 1
             self.eReactionData[0][k][2] = 1
             self.eReactionData[1][k][2] = 1
             self.eReactionData[2][k][2] = 1
             
         self.outputStateData = [[[0 for i in range(NO_ESTOPOUTPUTS)] for j in range(NO_BEAMS)] for k in range(3)]  # 0 = HMI, 1=OSS, 2=LBC-F 
         self.FLU = FLUCONFIG
         self.peopleInBeam = [[0 for i in range(NO_BEAMS)] for k in range(2)]   #start in custom

         self.LbcOutputData = [[1 for i in range(NO_ESTOPOUTPUTS)] for j in range(NO_BEAMS)]  # 1 = HEALTHY = ENERGIZED
         self.LbcInputData = [[0 for i in range(NO_SAFETYINPUTS-16)] for j in range(NO_BEAMS)]
         self.lbcEStateData = [[0 for i in range(NO_ESTOPOUTPUTS)] for j in range(NO_BEAMS)]  # 0 = HEALTHY = NO E-STOP
    
         self.xDriveFunction                 = [99]*NO_BEAMS
         self.yDriveElectricFunction         = [99]*NO_BEAMS
         self.yDriveHydraulicFunction        = [99]*NO_BEAMS
         self.xLockingFunction               = [99]*NO_BEAMS
         self.LCFunction                     = [99]*NO_BEAMS
         self.AHCFunction                    = [99]*NO_BEAMS
         self.yBrakeFunction                 = [99]*NO_BEAMS 
         

    
         self.styleOSSnowrite = STYLEOSSNOWRITE
         self.styleHMInowrite = STYLEHMINOWRITE
         self.styleNowrite = STYLENOWRITE
         self.styleOSSwrite = STYLEOSSWRITE
         self.styleHMIwrite = STYLEHMIWRITE
         self.styleWrite  = STYLEWRITE
         
         
         self.fontBiggest = QtGui.QFont()
         self.fontBiggest.setPointSize(30)
         self.fontBiggest.setWeight(75)
         self.fontBiggest.setFamily("Arial")    
         
         self.fontTitle = QtGui.QFont()
         self.fontTitle.setPointSize(30)
         self.fontTitle.setWeight(50)
         self.fontTitle.setFamily("Arial")  
         
         self.fontBig = QtGui.QFont()
         self.fontBig.setPointSize(11)
         self.fontBig.setWeight(75)
         self.fontBig.setFamily("Arial")
         
         self.fontSmall = QtGui.QFont()
         self.fontSmall.setPointSize(8)  #smaller than 8 not a good idea
         self.fontSmall.setWeight(50)
         self.fontSmall.setFamily("Arial")
         
         self.eStopPressed = False
         self.resetPressed = False
         self.uploadPressed = False
         self.connected = False
         self.beamEnable = False
         
         self.beamsToBeChecked = [0 for i in range(NO_BEAMS)]
         
         self.startup = True   # bit that is only high at startup
         self.k = 0
         
         self.hmiChanges =  [0 for i in range(NO_BEAMS)]
         self.blockUpload = False  
         
         self.hmiFluMatch = [1 for i in range(NO_BEAMS)]
         
         self.lbcConnectionCounter = [0 for i in range(NO_BEAMS)]
         self.lbcConnectionCounterOld = [0 for i in range(NO_BEAMS)]
         self.lbcConnectionErrorPrinted = [0 for i in range(NO_BEAMS)]
         

         self.eStopPressedOld = True   #NC contact
         self.resetPressedOld = False
         
         self.counter = 0

         
   
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(HOR_RES, VERT_RES)
        if FULLSCREEN == 1:
            MainWindow.showFullScreen()
        MainWindow.setStyleSheet("#MainWindow {\n"
                                            "     background-color: black;\n"
                                            "}\n"
                                            "\n"
                                            "\n"
                                            "#MainWindow QPushButton {\n"
                                            "color:#c1c1c1;\n"
                                            "background: #c1c1c1;\n"
                                            "}\n"
                                            "\n"
                                            "")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setStyleSheet("background-color: black;\n" )
        self.centralWidget.setObjectName("centralWidget")

############################### EXIT  BUTTON #############################
        self.pushExit = QtWidgets.QPushButton(self.centralWidget)
        self.pushExit.setGeometry(QtCore.QRect(HOR_RES-70, VERT_RES-60, 50, 50))
        self.pushExit.setIcon(QtGui.QIcon("images/exitButton.PNG"))
        self.pushExit.setIconSize(QtCore.QSize(50,50))
        self.pushExit.setStyleSheet(STYLEWRITE)
        
############################### HOME  BUTTON #############################
        self.pushHome = QtWidgets.QPushButton(self.centralWidget)
        self.pushHome.setGeometry(QtCore.QRect(HOR_RES-70-70-70-70-70, VERT_RES-60, 50, 50))
        self.pushHome.setIcon(QtGui.QIcon("images/homeButton.PNG"))
        self.pushHome.setIconSize(QtCore.QSize(50,50))
        self.pushHome.setStyleSheet(STYLEWRITE)    
        self.pushHome.clicked.connect(self.overviewButton_clicked)
        

        if LOCAL_MODE in [0,2]:
    ############################### OPC  BUTTON #############################
            self.pushConnect = QtWidgets.QPushButton(self.centralWidget)
            self.pushConnect.setGeometry(QtCore.QRect(HOR_RES-70-70, VERT_RES-60, 50, 50))
            self.pushConnect.setFont(self.fontBig)
            self.pushConnect.setText("OPC")
            self.pushConnect.setStyleSheet(STYLEWRITE)
            self.pushConnect.clicked.connect(self.opcButton_clicked)
            self.connected = 0
            
        elif LOCAL_MODE in [1,3]:
    ############################## UPLOAD  BUTTON #############################
            self.pushUpload = QtWidgets.QPushButton(self.centralWidget)
            self.pushUpload.setGeometry(QtCore.QRect(HOR_RES-280-1000, VERT_RES-BUTTON_VERT-25, 75, BUTTON_VERT))
            self.pushUpload.setText("UPLOAD CONF")
            self.pushUpload.setStyleSheet(STYLEWRITE)
            self.pushUpload.clicked.connect(self.pushUpload_clicked)
    
    ############################## E-STOP  BUTTON #############################
            self.pushEStop = QtWidgets.QPushButton(self.centralWidget)
            self.pushEStop.setGeometry(QtCore.QRect(HOR_RES-280-200, VERT_RES-BUTTON_VERT-25, 75, BUTTON_VERT))
            self.pushEStop.setText("GEN E-STOP")
            self.pushEStop.setStyleSheet(STYLEWRITE)
            self.pushEStop.clicked.connect(self.pushEStop_clicked)
     
    
    ############################## OSS E-STOP RESET #############################
            self.pushReset = QtWidgets.QPushButton(self.centralWidget)
            self.pushReset.setGeometry(QtCore.QRect(HOR_RES-280-300, VERT_RES-BUTTON_VERT-25, 75, BUTTON_VERT))
            self.pushReset.setText("OSS RESET")
            self.pushReset.setStyleSheet(STYLEWRITE)
            self.pushReset.clicked.connect(self.pushReset_clicked) 
            self.resetPressed = False
            
    ############################## BEAM ENABLE BUTTON #############################
            self.pushBeamEnable = QtWidgets.QPushButton(self.centralWidget)
            self.pushBeamEnable.setGeometry(QtCore.QRect(HOR_RES-280-400, VERT_RES-BUTTON_VERT-25, 75, BUTTON_VERT))
            self.pushBeamEnable.setText("BEAM ENABLE")
            self.pushBeamEnable.setStyleSheet(STYLEWRITE)
            self.pushBeamEnable.clicked.connect(self.pushBeamEnable_clicked) 

            if LOCAL_MODE == 1:
        ############################## OCS E-STOP RESET #############################
                self.pushResetOCS = QtWidgets.QPushButton(self.centralWidget)
                self.pushResetOCS.setGeometry(QtCore.QRect(HOR_RES-280-500, VERT_RES-BUTTON_VERT-25, 75, BUTTON_VERT))
                self.pushResetOCS.setText("OCS RESET")
                self.pushResetOCS.setStyleSheet(STYLEWRITE)
                self.pushResetOCS.clicked.connect(self.pushResetOCS_clicked)  
                self.resetPressedOcs = False
                
############################## LINE GRID  ##############################3######
        self.TopLine1 = QtWidgets.QLabel(self.centralWidget)
        self.TopLine1.setGeometry(QtCore.QRect(0, TOPBAR_RES, HOR_RES, LINEWIDTH))
        self.TopLine1.setMaximumSize(QtCore.QSize(HOR_RES, LINEWIDTH))
        self.TopLine1.setStyleSheet("#TopLine1{\n"
"background-color:white;\n"
"}")
        self.TopLine1.setObjectName("TopLine1")
        self.BottomLine0 = QtWidgets.QLabel(self.centralWidget)
        self.BottomLine0.setGeometry(QtCore.QRect(0, VERT_RES-BOTTOMBAR_RES, HOR_RES, LINEWIDTH))
        self.BottomLine0.setMaximumSize(QtCore.QSize(HOR_RES, LINEWIDTH))
        self.BottomLine0.setStyleSheet("#BottomLine0{\n"
"background-color:white;\n"
"}")
        self.BottomLine0.setObjectName("BottomLine0")
        self.VertLine0 = QtWidgets.QLabel(self.centralWidget)
        self.VertLine0.setGeometry(QtCore.QRect(HOR_RES-RIGHTBAR_RES, TOPBAR_RES, 3, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES))
        self.VertLine0.setMinimumSize(QtCore.QSize(LINEWIDTH, RIGHTBAR_RES))
        self.VertLine0.setMaximumSize(QtCore.QSize(LINEWIDTH, VERT_RES))
        self.VertLine0.setStyleSheet("#VertLine0{\n"
"background-color:white;\n"
"}")
        self.VertLine0.setObjectName("VertLine0")
        self.MiddleLine0 = QtWidgets.QLabel(self.centralWidget)
        self.MiddleLine0.setGeometry(QtCore.QRect(HOR_RES-RIGHTBAR_RES, TOPBAR_RES+30+VESSEL_VERT, RIGHTBAR_RES, LINEWIDTH))
        self.MiddleLine0.setMaximumSize(QtCore.QSize(HOR_RES, LINEWIDTH))
        self.MiddleLine0.setStyleSheet("#MiddleLine0{\n"
"background-color:white;\n"
"}")
        self.MiddleLine0.setObjectName("MiddleLine0")
        self.VertLine1 = QtWidgets.QLabel(self.centralWidget)
        self.VertLine1.setGeometry(QtCore.QRect(HOR_RES-RIGHTBAR_RES, 0, LINEWIDTH, TOPBAR_RES))
        self.VertLine1.setMinimumSize(QtCore.QSize(LINEWIDTH, TOPBAR_RES))
        self.VertLine1.setMaximumSize(QtCore.QSize(LINEWIDTH, TOPBAR_RES))
        self.VertLine1.setStyleSheet("#VertLine1{\n"
"background-color:white;\n"
"}")
        self.VertLine1.setObjectName("VertLine1")
        
        
############################## ALLSEAS LOGO #############################
        self.logo = QtWidgets.QLabel(self.centralWidget)
        self.logo.setGeometry(QtCore.QRect(0, 0, (TOPBAR_RES-3)*3.24, TOPBAR_RES-3))
        self.logo.setPixmap(QtGui.QPixmap("images/AllseasLogoBlack.PNG"))
        self.logo.setScaledContents(True)

############################## DATE AND TIME #############################
        self.dateTime = QtWidgets.QLabel(self.centralWidget)
        self.dateTime.setGeometry(QtCore.QRect(HOR_RES-(RIGHTBAR_RES), 0, RIGHTBAR_RES, TOPBAR_RES/2))
        self.dateTime.setText(QtCore.QDateTime.currentDateTime().toString())
        self.dateTime.setAlignment(QtCore.Qt.AlignCenter)
        self.dateTime.setFont(self.fontSmall)
        self.dateTime.setStyleSheet("color:white;")
        
############################## OPERATOR #############################
        self.operator = QtWidgets.QLabel(self.centralWidget)
        self.operator.setGeometry(QtCore.QRect(HOR_RES-(RIGHTBAR_RES), TOPBAR_RES/2, RIGHTBAR_RES, TOPBAR_RES/2))
        self.operator.setText(OPERATOR)
        self.operator.setAlignment(QtCore.Qt.AlignCenter)
        self.operator.setFont(self.fontSmall)
        self.operator.setStyleSheet("color: #66ffff")
        
        
############################## CONSOLE #############################
        self.console = QtWidgets.QTextBrowser(self.centralWidget)
        self.console.setGeometry(QtCore.QRect(HOR_RES-RIGHTBAR_RES+10, TOPBAR_RES+40+VESSEL_VERT, RIGHTBAR_RES-20, VERT_RES-TOPBAR_RES-VESSEL_VERT-BOTTOMBAR_RES-60))
        self.console.setFont(self.fontSmall)
        self.console.setStyleSheet("color: white;\n"
                                   "border: 0px solid white;\n")
        self.console.insertPlainText("Console messages... \n")
        
############################# HMI PS ####################################
        self.hmiIndication = QtWidgets.QLabel(self.centralWidget)
        self.hmiIndication.setGeometry(QtCore.QRect(HOR_RES/2-125, VERT_RES - 70+15, 250,40 ))
        self.hmiIndication.setText("FORE-DESK")
        self.hmiIndication.setAlignment(QtCore.Qt.AlignCenter)
        self.hmiIndication.setFont(self.fontBiggest)
        self.hmiIndication.setStyleSheet("color:white;")
        
############################## OVERVIEW PAGE #############################
        self.topWidget = QtWidgets.QStackedWidget(self.centralWidget)  #stacked widget that holds overview[0], configCheck[1], FLU[2], alarms/warning[3], network[4], SIF[5] screens
        self.topWidget.setGeometry(QtCore.QRect(-LINEWIDTH, TOPBAR_RES, HOR_RES-RIGHTBAR_RES+LINEWIDTH, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES+22))   # start at -3 to remove left vertical white line
        self.topWidget.show()
        self.topWidgetDisplayed = True
        self.overviewWidget = QtWidgets.QWidget()
        self.topWidget.addWidget(self.overviewWidget)
                
############################## Config Check Page #############################
        self.configWidget = QtWidgets.QWidget()
        self.topWidget.addWidget(self.configWidget)
        
        # Title
        self.configWidgetTitle = QtWidgets.QLabel(self.configWidget)
        self.configWidgetTitle.setGeometry(QtCore.QRect(20, 20, 500,50 ))
        self.configWidgetTitle.setText("Beam Settings Comparison")
        self.configWidgetTitle.setFont(self.fontTitle)
        self.configWidgetTitle.setStyleSheet("color:#cccccc")

        # Groupbox for 16 beam selection buttons 
        self.groupBoxCheckBeams = QtWidgets.QGroupBox(self.configWidget)
        self.groupBoxCheckBeams.setGeometry(QtCore.QRect(1600-(2*BUTTON_HOR+4*BUTTON_VERT)-50-20, 20, (2*BUTTON_HOR+4*BUTTON_VERT)+50, NO_BEAMS/2*(BUTTON_VERT+7)+20))
        self.groupBoxCheckBeams.setTitle("Select beams for comparison")
        self.groupBoxCheckBeams.setFont(self.fontBig)
        self.groupBoxCheckBeams.setStyleSheet("color:white;")
        
       # Groupbox for active flags
        self.groupBoxCheckActive = QtWidgets.QGroupBox(self.configWidget)
        self.groupBoxCheckActive.setGeometry(QtCore.QRect(20, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-30-(NO_ACTIVEFLAGS*(BUTTON_VERT+7)+10), 370, NO_ACTIVEFLAGS*(BUTTON_VERT+7)+10))
        self.groupBoxCheckActive.setFont(self.fontBig)
        self.groupBoxCheckActive.setTitle("Active Flags")
        self.groupBoxCheckActive.setStyleSheet("color:white;")
        
        # Groupbox for ignore flags     
        self.groupBoxCheckIgnore = QtWidgets.QGroupBox(self.configWidget)
        self.groupBoxCheckIgnore.setGeometry(QtCore.QRect(410, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-30-(NO_IGNOREFLAGS*(BUTTON_VERT+7)+10+180), 370, NO_IGNOREFLAGS*(BUTTON_VERT+7)+10))
        self.groupBoxCheckIgnore.setFont(self.fontBig)
        self.groupBoxCheckIgnore.setTitle("Ignore Flags")
        self.groupBoxCheckIgnore.setStyleSheet("color:white;")           
            
        # Groupbox for E-stop reaction configuration
        self.groupBoxCheckEstopReaction = QtWidgets.QGroupBox(self.configWidget)
        self.groupBoxCheckEstopReaction.setGeometry(QtCore.QRect(410, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-30-(4*(BUTTON_VERT+7)+15), 370, 4*(BUTTON_VERT+7)+15))
        self.groupBoxCheckEstopReaction.setFont(self.fontBig)
        self.groupBoxCheckEstopReaction.setTitle("E-Stop Reactions")
        self.groupBoxCheckEstopReaction.setStyleSheet("color:white;")

        # Groupbox for Safe modes configuration
        self.groupBoxSafeModes = QtWidgets.QGroupBox(self.configWidget)
        self.groupBoxSafeModes.setGeometry(QtCore.QRect(410+390, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-30-(4*(BUTTON_VERT+7)+15), 370, 4*(BUTTON_VERT+7)+15))
        self.groupBoxSafeModes.setFont(self.fontBig)
        self.groupBoxSafeModes.setTitle("Safe Mode")
        self.groupBoxSafeModes.setStyleSheet("color:white;")

############################## FLU PAGE #############################

        self.fluWidget = QtWidgets.QWidget()
        self.topWidget.addWidget(self.fluWidget)

        # Title
        self.fluWidgetTitle = QtWidgets.QLabel(self.fluWidget)
        self.fluWidgetTitle.setGeometry(QtCore.QRect(20, 20, 500, 50))
        self.fluWidgetTitle.setText("FLU CONFIGURATION")
        self.fluWidgetTitle.setFont(self.fontTitle)
        self.fluWidgetTitle.setStyleSheet("color:#cccccc")

        # Groupbox for linking FLUs
        self.fluGroupBox = QtWidgets.QGroupBox(self.fluWidget)
        self.fluGroupBox.setGeometry(QtCore.QRect(20, 100, 500, 500))
        self.fluGroupBox.setFont(self.fontBig)
        self.fluGroupBox.setTitle("Link Settings and E-Stop")
        self.fluGroupBox.setStyleSheet("color:white;")
# -------------------------------------

        self.fontBeamLabel = QtGui.QFont()
        self.fontBeamLabel.setPointSize(15)
        self.fontBeamLabel.setWeight(25)
        self.fontBeamLabel.setFamily("Arial")

        positions = [(i, j) for i in range(4) for j in range(2)] # generate tuples for 8 positions
        x = 8
        y = 0
        for position in positions:
            # draw FLU boxes
            self.smallBox = QtWidgets.QGroupBox(self.fluWidget)
            self.smallBox.setGeometry(QtCore.QRect(STARTING_X + position[1] * BOX_WIDTH + position[1] * SPACER,
                                                   STARTING_Y + position[0] * (BOX_HIGHT + SPACER), BOX_WIDTH,
                                                   BOX_HIGHT))

            # draw Link FLU labels
            self.linkFLUlabel = QtWidgets.QLabel(self.fluWidget)
            self.linkFLUlabel.setGeometry(QtCore.QRect(STARTING_X + 50 + position[1] * (BOX_WIDTH + 55),
                                                       STARTING_Y + 15 + position[0] * (BOX_HIGHT + SPACER), 80, 20))
            self.linkFLUlabel.setText("Link FLU")
            self.linkFLUlabel.setFont(self.fontBeamLabel)
            self.linkFLUlabel.setStyleSheet("color:#cccccc")

            # draw Enable/Disable buttons
            self.enableFluButton = QtWidgets.QPushButton(self.fluWidget)
            self.enableFluButton.setGeometry(QtCore.QRect(STARTING_X + 20 + position[1] * (BOX_WIDTH + 55),
                                                          STARTING_Y + 60 + position[0] * (BOX_HIGHT + SPACER),
                                                          BUTTON_HOR - 20, BUTTON_VERT))
            self.enableFluButton.setText("ENABLED")
            self.enableFluButton.setStyleSheet(STYLEWRITE)
            self.enableFluButton.clicked.connect(lambda ignore, x=position: self.enableFluButton_clicked(x))

            self.disableFluButton = QtWidgets.QPushButton(self.fluWidget)
            self.disableFluButton.setGeometry(QtCore.QRect(STARTING_X + 100 + position[1] * (BOX_WIDTH + 55),
                                                           STARTING_Y + 60 + position[0] * (BOX_HIGHT + SPACER),
                                                           BUTTON_HOR - 20, BUTTON_VERT))
            self.disableFluButton.setText("DISABLED")
            self.disableFluButton.setStyleSheet(STYLEWRITE)
            self.disableFluButton.clicked.connect(lambda ignore, x=position: self.disableFluButton_clicked(x))

            # draw P and S upper boxes
            self.beamBoxUpper = QtWidgets.QGroupBox(self.fluWidget)
            self.beamBoxUpper.setGeometry(QtCore.QRect(STARTING_BEAMBOX_X + 68 * position[1],
                                                       STARTING_BEAMBOX_Y + position[0] * (BOX_HIGHT + SPACER),
                                                       BEAMBOX_SIZE, BEAMBOX_SIZE))
            self.beamBoxUpper.setStyleSheet("color:#cccccc")

            # draw P and S lower boxes
            self.beamBoxLower = QtWidgets.QGroupBox(self.fluWidget)
            self.beamBoxLower.setGeometry(
                QtCore.QRect(STARTING_BEAMBOX_X + 68 * position[1], STARTING_BEAMBOX_Y + position[0] * (
                    BOX_HIGHT + SPACER) + BEAMBOX_SIZE + 3, BEAMBOX_SIZE, BEAMBOX_SIZE))
            self.beamBoxLower.setStyleSheet("color:#cccccc")

            # put lables in the boxes
            if position[1] == 0:  # P beams
                self.beamLabelUpper = QtWidgets.QLabel(self.fluWidget)
                self.beamLabelUpper.setGeometry(
                    QtCore.QRect(STARTING_BEAMBOX_X + 3, STARTING_BEAMBOX_Y + 3 + position[0] * (BOX_HIGHT + SPACER),
                                 BEAMLABEL_SIZE, BEAMLABEL_SIZE))
                self.beamLabelUpper.setText(beamIDtext[x])
                self.beamLabelUpper.setFont(self.fontBeamLabel)
                self.beamLabelUpper.setStyleSheet("color:#cccccc")

                self.beamLabelLower = QtWidgets.QLabel(self.fluWidget)
                self.beamLabelLower.setGeometry(QtCore.QRect(STARTING_BEAMBOX_X + 3,
                                                             STARTING_BEAMBOX_Y + 11 + BEAMLABEL_SIZE + position[0] * (
                                                             BOX_HIGHT + SPACER), BEAMLABEL_SIZE, BEAMLABEL_SIZE))
                self.beamLabelLower.setText(beamIDtext[x + 1])
                self.beamLabelLower.setFont(self.fontBeamLabel)
                self.beamLabelLower.setStyleSheet("color:#cccccc")

                x += 2

            if position[1] == 1:  # S beams
                self.beamLabelUpper = QtWidgets.QLabel(self.fluWidget)
                self.beamLabelUpper.setGeometry(
                    QtCore.QRect(STARTING_BEAMBOX_X + 71, STARTING_BEAMBOX_Y + 3 + position[0] * (BOX_HIGHT + SPACER),
                                 BEAMLABEL_SIZE, BEAMLABEL_SIZE))
                self.beamLabelUpper.setText(beamIDtext[y])
                self.beamLabelUpper.setFont(self.fontBeamLabel)
                self.beamLabelUpper.setStyleSheet("color:#cccccc")

                self.beamLabelLower = QtWidgets.QLabel(self.fluWidget)
                self.beamLabelLower.setGeometry(QtCore.QRect(STARTING_BEAMBOX_X + 71,
                                                             STARTING_BEAMBOX_Y + 11 + BEAMLABEL_SIZE + position[0] * (
                                                             BOX_HIGHT + SPACER), BEAMLABEL_SIZE, BEAMLABEL_SIZE))
                self.beamLabelLower.setText(beamIDtext[y + 1])
                self.beamLabelLower.setFont(self.fontBeamLabel)
                self.beamLabelLower.setStyleSheet("color:#cccccc")
                y += 2


# -------------------------------------
        # Groupbox for linking E-Stop to all beams
        self.linkEstopsGroupBox = QtWidgets.QGroupBox(self.fluWidget)
        self.linkEstopsGroupBox.setGeometry(QtCore.QRect(20, 700, 500, 70))
        self.linkEstopsGroupBox.setFont(self.fontBig)
        self.linkEstopsGroupBox.setTitle("Link E-Stops to all beams")
        self.linkEstopsGroupBox.setStyleSheet("color:white;")

        self.enableLinkEstopAllBeamsButton = QtWidgets.QPushButton(self.fluWidget)
        self.enableLinkEstopAllBeamsButton.setGeometry(QtCore.QRect(35, 700 + 10 + BUTTON_VERT, 150, BUTTON_VERT))
        self.enableLinkEstopAllBeamsButton.setText("ENABLED")
        self.enableLinkEstopAllBeamsButton.setStyleSheet(STYLEWRITE)
#        self.enableLinkEstopAllBeamsButton.clicked.connect(self.enableLinkEstopAllBeamsButton_clicked)

        self.disableLinkEstopAllBeamsButton = QtWidgets.QPushButton(self.fluWidget)
        self.disableLinkEstopAllBeamsButton.setGeometry(QtCore.QRect(500 - 150, 700 + 10 + BUTTON_VERT, 150, BUTTON_VERT))
        self.disableLinkEstopAllBeamsButton.setText("DISABLED")
        self.disableLinkEstopAllBeamsButton.setStyleSheet(STYLEWRITE)
        #        self.disableLinkEstopAllBeamsButton.clicked.connect(self.disableLinkEstopAllBeamsButton_clicked)

############################## WARNING PAGE #############################
        self.warningWidget = QtWidgets.QWidget()
        self.topWidget.addWidget(self.warningWidget)
        self.warningList = QtWidgets.QTextBrowser(self.warningWidget)
        self.warningList.setGeometry(QtCore.QRect(30, 30, HOR_RES-RIGHTBAR_RES-60, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-60))
        self.warningList.setFont(self.fontSmall)
        self.warningList.setStyleSheet("color: white;\n"
                                   "border: 1px solid white;\n")
        self.warningList.insertPlainText("Warning messages... \n")
        
        self.acknowledgeButton = QtWidgets.QPushButton(self.warningWidget)
        self.acknowledgeButton.setGeometry(QtCore.QRect(HOR_RES-RIGHTBAR_RES-60-BUTTON_HOR+10, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-60-BUTTON_VERT+10,BUTTON_HOR ,BUTTON_VERT ))
        self.acknowledgeButton.setText("ACKNOWLEDGE")
        self.acknowledgeButton.setStyleSheet(STYLEWRITE)
        # CONNECT TO FUNCTION
        self.acknowledgeButton.clicked.connect(self.acknowledge_clicked)

############################## NETWORK PAGE #############################
        self.networkWidget = QtWidgets.QWidget()
        self.topWidget.addWidget(self.networkWidget)
        self.networkList = QtWidgets.QTextBrowser(self.networkWidget)
        self.networkList.setGeometry(QtCore.QRect(30, 30, HOR_RES-RIGHTBAR_RES-60, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-60))
        self.networkList.setFont(self.fontSmall)
        self.networkList.setStyleSheet("color: white;\n"
                                   "border: 1px solid white;\n")
        self.networkList.insertPlainText("Network messages... \n")

############################## SIF PAGE #############################

        self.sifWidget = QtWidgets.QWidget()
        self.topWidget.addWidget(self.sifWidget)

        # Title
        self.sifWidgetTitle = QtWidgets.QLabel(self.sifWidget)
        self.sifWidgetTitle.setGeometry(QtCore.QRect(20, 20, 500, 50))
        self.sifWidgetTitle.setText("Safety Instrumented Functions")
        self.sifWidgetTitle.setFont(self.fontTitle)
        self.sifWidgetTitle.setStyleSheet("color:#cccccc")

############################## 16 BEAM PAGES #############################
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralWidget)
        self.stackedWidget.setGeometry(QtCore.QRect(-LINEWIDTH, TOPBAR_RES, HOR_RES-RIGHTBAR_RES+LINEWIDTH, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES+22))   # start at -3 to remove left vertical white line
        
        self.beams = []   # contains the 16 beam widgets, each containing 2 tabs (see next comment)
        self.tabs = []   # the 16 tabcontainers in the 16 beam widgets
        self.overviewTabs = []
        self.statusTabs = []
        self.beamTabs = []
        self.ioTabs = []
        self.estopTabs = []
        
        for i in range (NO_BEAMS):
            # create 16 beam widgets
            self.beam = QtWidgets.QWidget()
            self.beams.append(self.beam)
            self.stackedWidget.addWidget(self.beams[i])
            
            # add a tab widget to the beam widget
            self.tab = QtWidgets.QTabWidget(self.beams[i])
            self.tabs.append(self.tab)
            self.tab.setGeometry(QtCore.QRect(0, 0, HOR_RES-RIGHTBAR_RES+(2*LINEWIDTH), VERT_RES-TOPBAR_RES-BOTTOMBAR_RES+22))   # add 3 in widt to overlap with vertical divider line, also, add 22 in height to have tabs in lower bar
            self.tab.setTabPosition(QtWidgets.QTabWidget.South)
            
            # create OVERVIEW tab
            self.overviewTab = QtWidgets.QWidget()
            self.overviewTabs.append(self.overviewTab)
            self.overviewTab.setObjectName("Safe mode")
            self.tab.addTab(self.overviewTab, "Safe mode")
            
            # create beam tab
            self.beamTab = QtWidgets.QWidget()
            self.beamTabs.append(self.beamTab)
            self.beamTab.setObjectName("Status")
            self.tab.addTab(self.beamTab, "Status")
            
            # create status tab
            self.statusTab = QtWidgets.QWidget()
            self.statusTabs.append(self.statusTab)
            self.statusTab.setObjectName("Custom mode")
            self.tab.addTab(self.statusTab, "Custom mode")
            
            # create io tab
            self.ioTab = QtWidgets.QWidget()
            self.ioTabs.append(self.ioTab)
            self.ioTab.setObjectName("io")
            self.tab.addTab(self.ioTab, "IO")
            
            # create E-Stop tab
            self.estopTab = QtWidgets.QWidget()
            self.estopTabs.append(self.estopTab)
            self.estopTab.setObjectName("estop")
            self.tab.addTab(self.estopTab, "E-Stop")
            
            
        self.groupBoxesOverview = []
        for i in range (NO_BEAMS):  
            if i<8:
                k = 0
                ii = i
                kk = i+8
            else:
                k = 1
                ii = i-8
                kk = i-8
                
            self.groupBox = QtWidgets.QGroupBox(self.overviewWidget)
            self.groupBoxesOverview.append(self.groupBox)
            self.groupBoxesOverview[i].setGeometry(QtCore.QRect(60+k*(1600-60)/2, 30+(((940-10*20)/8)+20)*ii , (1600-180)/2, (940-10*20)/8));
            self.groupBoxesOverview[i].setFont(self.fontBig)
            
            if ACTIVE_BEAMS[kk] == 0:
                self.groupBoxesOverview[i].setStyleSheet("QGroupBox{\n"
                                                            "border: 1px dashed white;\n"
                                                            "}")
                self.groupBoxesOverview[i].hide()
                                                            
            else:
                self.groupBoxesOverview[i].setStyleSheet("QGroupBox{\n"
                                                            "border: 1px solid white;\n"
                                                            "}")

        # BeamID and isometric view 
        self.beamISOs = []
        self.beamIDs = []
#        beamIDtext = ["S1","S2","S3","S4","S5","S6","S7","S8","P1","P2","P3","P4","P5","P6","P7","P8"]
        for i in range (NO_BEAMS):  
            self.beamISO = QtWidgets.QLabel(self.beams[i])
            self.beamISOs.append(self.beamISO)
            self.beamISOs[i].setGeometry(QtCore.QRect(HOR_RES-RIGHTBAR_RES-30-300-BEAMISO_HOR-30, 30, BEAMISO_HOR, BEAMISO_VERT))
            self.beamISOs[i].setText("")
            self.beamISOs[i].setPixmap(QtGui.QPixmap("images/beamIsometric.PNG"))
            self.beamISOs[i].setScaledContents(True)

        #    self.beamISO[i].setObjectName(_fromUtf8("beamISO_2"))          
            self.beamID = QtWidgets.QLabel(self.beams[i])
            self.beamIDs.append(self.beamID)
            self.beamIDs[i].setFont(self.fontBiggest)
            self.beamIDs[i].setStyleSheet("QLabel{\n"
                                                "color:white;\n"
                                                "}")
            self.beamIDs[i].setGeometry(QtCore.QRect(HOR_RES-RIGHTBAR_RES-30-300-100, 30, 100, 100))
            self.beamIDs[i].setText(beamIDtext[i])


        # Groupbox for PEOPLE-IN-BEAM
        self.groupBoxesPeopleInBeam = []
        for i in range (NO_BEAMS):       
            self.groupBox = QtWidgets.QGroupBox(self.overviewTabs[i])
            self.groupBoxesPeopleInBeam.append(self.groupBox)
            self.groupBoxesPeopleInBeam[i].setGeometry(QtCore.QRect(60, 300 , (SAFEMODEBUTTON_HOR+20)+20, 3*(SAFEMODEBUTTON_VERT+7)+30))
            self.groupBoxesPeopleInBeam[i].setFont(self.fontBig)
            self.groupBoxesPeopleInBeam[i].setTitle("PEOPLE IN BEAM")
            self.groupBoxesPeopleInBeam[i].setStyleSheet("color:white;")
            
            
            # Groupbox for BEAM SAFE STATES
        self.groupBoxesBeamSafe = []
        for i in range (NO_BEAMS):       
            self.groupBox = QtWidgets.QGroupBox(self.overviewTabs[i])
            self.groupBoxesBeamSafe.append(self.groupBox)
            self.groupBoxesBeamSafe[i].setGeometry(QtCore.QRect(390, 300 , (SAFEMODEBUTTON_HOR+20)+20, NO_BEAMSAFEMODES*(SAFEMODEBUTTON_VERT+7)+30))
            self.groupBoxesBeamSafe[i].setFont(self.fontBig)
            self.groupBoxesBeamSafe[i].setTitle("BEAM SAFE MODES")
            self.groupBoxesBeamSafe[i].setStyleSheet("color:white;")
            
        # Groupbox for DRIVE SYSTEM SAFE STATES
        self.groupBoxesDriveSafe = []
        for i in range (NO_BEAMS):       
            self.groupBox = QtWidgets.QGroupBox(self.overviewTabs[i])
            self.groupBoxesDriveSafe.append(self.groupBox)
            self.groupBoxesDriveSafe[i].setGeometry(QtCore.QRect(680, 300 , 3*(SAFEMODEBUTTON_HOR+20)+20, (NO_DRIVESAFEMODES+1)*(SAFEMODEBUTTON_VERT+7)+30))
            self.groupBoxesDriveSafe[i].setFont(self.fontBig)
            self.groupBoxesDriveSafe[i].setTitle("DRIVE SAFE MODES")
            self.groupBoxesDriveSafe[i].setStyleSheet("color:white;")     
            
         
        # Groupbox for active flags
        self.groupBoxesActive = []
        for i in range (NO_BEAMS):       
            self.groupBox = QtWidgets.QGroupBox(self.statusTabs[i])
            self.groupBoxesActive.append(self.groupBox)
            self.groupBoxesActive[i].setGeometry(QtCore.QRect(20, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-30-(NO_ACTIVEFLAGS*(BUTTON_VERT+7)+10), 370, NO_ACTIVEFLAGS*(BUTTON_VERT+7)+10))
            self.groupBoxesActive[i].setFont(self.fontBig)
            self.groupBoxesActive[i].setTitle("Configure Active Flags")
            self.groupBoxesActive[i].setStyleSheet("color:white;")
        
        # Groupbox for ignore flags
        self.groupBoxesIgnore = []
        for i in range (NO_BEAMS):       
            self.groupBox = QtWidgets.QGroupBox(self.statusTabs[i])
            self.groupBoxesIgnore.append(self.groupBox)
            self.groupBoxesIgnore[i].setGeometry(QtCore.QRect(410, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-30-(NO_IGNOREFLAGS*(BUTTON_VERT+7)+10), 370, NO_IGNOREFLAGS*(BUTTON_VERT+7)+10))
            self.groupBoxesIgnore[i].setFont(self.fontBig)
            self.groupBoxesIgnore[i].setTitle("Configure Ignfore Flags")
            self.groupBoxesIgnore[i].setStyleSheet("color:white;")           
            
        # Groupbox for E-stop reaction configuration
        self.groupBoxesEstopReaction = []
        for i in range (NO_BEAMS):
            self.groupBox = QtWidgets.QGroupBox(self.statusTabs[i])
            self.groupBoxesEstopReaction.append(self.groupBox)
            self.groupBoxesEstopReaction[i].setGeometry(QtCore.QRect(800, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-30-(10*(BUTTON_VERT+7)+10), 370, 10*(BUTTON_VERT+7)+10))
            self.groupBoxesEstopReaction[i].setFont(self.fontBig)
            self.groupBoxesEstopReaction[i].setTitle("E-Stop Reaction")
            self.groupBoxesEstopReaction[i].setStyleSheet("color:white;") 


        # Groupbox for LBC interlock status
        self.groupBoxesLbcInterlocks = []
        for i in range (NO_BEAMS):       
            self.groupBox = QtWidgets.QGroupBox(self.beamTabs[i])
            self.groupBoxesLbcInterlocks.append(self.groupBox)
            self.groupBoxesLbcInterlocks[i].setGeometry(QtCore.QRect(20, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-30-((NO_SAFETYINPUTS-16)*(BUTTON_VERT+7)+10), 230, (NO_SAFETYINPUTS-16)*(BUTTON_VERT+7)+10))
            self.groupBoxesLbcInterlocks[i].setFont(self.fontBig)
            self.groupBoxesLbcInterlocks[i].setTitle("Interlocks")
            self.groupBoxesLbcInterlocks[i].setStyleSheet("color:white;") 
            
        # Groupbox for SAFETY INPUTS
        self.groupBoxesInputIO = []
        for i in range (NO_BEAMS):       
            self.groupBox = QtWidgets.QGroupBox(self.beamTabs[i])
            self.groupBoxesInputIO.append(self.groupBox)
            self.groupBoxesInputIO[i].setGeometry(QtCore.QRect(270, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-30-((NO_SAFETYINPUTS-16)*(BUTTON_VERT+7)+10), 230, (NO_SAFETYINPUTS-16)*(BUTTON_VERT+7)+10))
            self.groupBoxesInputIO[i].setFont(self.fontBig)
            self.groupBoxesInputIO[i].setTitle("E-Stop Button")
            self.groupBoxesInputIO[i].setStyleSheet("color:white;")     
            
        # Groupbox for SAFETY OUTPUTS
        self.groupBoxesOutputIO = []
        for i in range (NO_BEAMS):       
            self.groupBox = QtWidgets.QGroupBox(self.beamTabs[i])
            self.groupBoxesOutputIO.append(self.groupBox)
            self.groupBoxesOutputIO[i].setGeometry(QtCore.QRect(520, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-30-(NO_ESTOPOUTPUTS*(BUTTON_VERT+7)+10) - 120, 230, NO_ESTOPOUTPUTS*(BUTTON_VERT+7)+10))
            self.groupBoxesOutputIO[i].setFont(self.fontBig)
            self.groupBoxesOutputIO[i].setTitle("E-Stop Outputs")
            self.groupBoxesOutputIO[i].setStyleSheet("color:white;") 
        
        
        # Groupbox for LBC-F E-STOP STATE
        self.groupBoxesEState = []
        for i in range (NO_BEAMS):       
            self.groupBox = QtWidgets.QGroupBox(self.beamTabs[i])
            self.groupBoxesEState.append(self.groupBox)
            self.groupBoxesEState[i].setGeometry(QtCore.QRect(770, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-30-(NO_ESTOPOUTPUTS*(BUTTON_VERT+7)+10) - 120, 230, NO_ESTOPOUTPUTS*(BUTTON_VERT+7)+10))
            self.groupBoxesEState[i].setFont(self.fontBig)
            self.groupBoxesEState[i].setTitle("E-Stop State")
            self.groupBoxesEState[i].setStyleSheet("color:white;") 
        
        # Groupbox for LBC-F E-STOP TIMEOUT
        self.groupBoxesETimeOut = []
        for i in range (NO_BEAMS):       
            self.groupBox = QtWidgets.QGroupBox(self.beamTabs[i])
            self.groupBoxesETimeOut.append(self.groupBox)
            self.groupBoxesETimeOut[i].setGeometry(QtCore.QRect(520, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-30-120+20, 3*230+40, 3*(BUTTON_VERT+7)+10))
            self.groupBoxesETimeOut[i].setFont(self.fontBig)
            self.groupBoxesETimeOut[i].setTitle("E-Stop Timeout")
            self.groupBoxesETimeOut[i].setStyleSheet("color:white;") 
            
            
        # Groupbox for output state triggering
        self.groupBoxesOutput = []
        for i in range (NO_BEAMS):       
            self.groupBox = QtWidgets.QGroupBox(self.beamTabs[i])
            self.groupBoxesOutput.append(self.groupBox)
            self.groupBoxesOutput[i].setGeometry(QtCore.QRect(770+250, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-30-(NO_ESTOPOUTPUTS*(BUTTON_VERT+7)+10)-120, 230, NO_ESTOPOUTPUTS*(BUTTON_VERT+7)+10))
            self.groupBoxesOutput[i].setFont(self.fontBig)
            self.groupBoxesOutput[i].setTitle("E-Stop State Set")
            self.groupBoxesOutput[i].setStyleSheet("color:white;") 
            

            
        # Groupbox for LBC control mode and opertional functions
        self.groupBoxesLbcFunctions = []
        for i in range (NO_BEAMS):       
            self.groupBox = QtWidgets.QGroupBox(self.beams[i])
            self.groupBoxesLbcFunctions.append(self.groupBox)
            self.groupBoxesLbcFunctions[i].setGeometry(QtCore.QRect(HOR_RES-RIGHTBAR_RES-30-300, 30, 300, 5*(BUTTON_VERT+7)+10))
            self.groupBoxesLbcFunctions[i].setFont(self.fontBig)
            self.groupBoxesLbcFunctions[i].setTitle("General")
            self.groupBoxesLbcFunctions[i].setStyleSheet("color:white;") 
            
        # Groupbox fornon E-stop button SAFETY INPUTS
        self.groupBoxesExtraInputIO = []
        for i in range (NO_BEAMS):       
            self.groupBox = QtWidgets.QGroupBox(self.ioTabs[i])
            self.groupBoxesExtraInputIO.append(self.groupBox)
            self.groupBoxesExtraInputIO[i].setGeometry(QtCore.QRect(20, VERT_RES-TOPBAR_RES-BOTTOMBAR_RES-30-((16)*(BUTTON_VERT+7)+10), 230, (16)*(BUTTON_VERT+7)+10))
            self.groupBoxesExtraInputIO[i].setFont(self.fontBig)
            self.groupBoxesExtraInputIO[i].setTitle("Digital Inputs")
            self.groupBoxesExtraInputIO[i].setStyleSheet("color:white;")  
            

            
 
            
            
            



################################# OVERVIEW GROUP BOXES ########################  
        # Active flag buttons 
        self.overViewLayouts = []
        self.buttonsOverView = {}
        
        self.safeModeText = ["SAFE MODE: ","X-DRIVE: ","Y-DRIVE: ","Z-DRIVE: "]
        self.beamIOText = ["Control Mode: ","People in Beam: ","OSS Timeout Flag: ","Config Change: "]
        

        
        for k in range(NO_BEAMS):  # 16 beams
            self.overViewLayout = QtWidgets.QGridLayout()  
#            self.overViewLayout.setColumnMinimumWidth(0)
           # self.overViewLayout.setColumnMinimumWidth(4,10)
            self.overViewLayouts.append(self.overViewLayout)
            for i in range(4):   #vertical
                for j in range(10):   #horizontal
                    self.buttonsOverView[(i, j)] = QtWidgets.QLabel()  
                    self.buttonsOverView[(i, j)].setStyleSheet("color:white;")
                    self.buttonsOverView[(i, j)].setFont(self.fontSmall)
      
                     # add to the layout
      
                    if j == 0 and k<8:
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], 0, j,4,1)
                        self.buttonsOverView[(i, j)].setFixedWidth(20)
                        self.buttonsOverView[(i, j)].setAlignment(QtCore.Qt.AlignCenter)

                    elif j == 9 and k>=8:
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], 0, j,4,1)
                        self.buttonsOverView[(i, j)].setFixedWidth(20)
                        self.buttonsOverView[(i, j)].setAlignment(QtCore.Qt.AlignCenter)
                        
                    elif j == 1 and k<8:
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], 0, j,4,1)
                        self.buttonsOverView[(i, j)].setText(beamIDtext[k+8])
                        self.buttonsOverView[(i, j)].setFixedWidth(60)
                        self.buttonsOverView[(i, j)].setAlignment(QtCore.Qt.AlignCenter)
                        self.buttonsOverView[(i, j)].setFont(self.fontBiggest)
                        
                    elif (j == 2 or j ==5 or j == 8 )and k<8:
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], 0, j,4,1)
                        self.buttonsOverView[(i, j)].setFixedWidth(1)
                        self.buttonsOverView[(i, j)].setStyleSheet("background:white;")
                        
                    elif (j == 1 or j ==4 or j == 7 )and k>=8:
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], 0, j,4,1)
                        self.buttonsOverView[(i, j)].setFixedWidth(1)
                        self.buttonsOverView[(i, j)].setStyleSheet("background:white;")

                    elif j == 8 and k>=8:
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], 0, j,4,1)
                        self.buttonsOverView[(i, j)].setText(beamIDtext[k-8])
                        self.buttonsOverView[(i, j)].setFixedWidth(60)
                        self.buttonsOverView[(i, j)].setAlignment(QtCore.Qt.AlignCenter)
                        self.buttonsOverView[(i, j)].setFont(self.fontBiggest)
                        
                    elif j == 3 and k<8:
                        #self.buttonsOverView[(i, j)].setText(self.safeModeText[0])
                        self.buttonsOverView[(i, j)].setPixmap(QtGui.QPixmap("images/connectionWarningBlack.PNG"))
                        self.buttonsOverView[(i, j)].setScaledContents(True)
                        self.buttonsOverView[(i, j)].setFixedSize(40,40)
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], 0, j,4,1)
                        if True:
                            self.buttonsOverView[(i, j)].setFont(self.fontBig)
                        else:
                            self.buttonsOverView[(i, j)].setFont(self.fontSmall)
                        self.buttonsOverView[(i, j)].setAlignment(QtCore.Qt.AlignCenter)
                        
                    elif j == 4 and k<8:
                        self.buttonsOverView[(i, j)].setText("-")
                        self.buttonsOverView[(i, j)].setFixedWidth(240)
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], 0, j,4,1)
                        if True:
                            self.buttonsOverView[(i, j)].setFont(self.fontBig)
                            self.buttonsOverView[(i, j)].setStyleSheet("color: #66ffff")
                        else:
                            self.buttonsOverView[(i, j)].setFont(self.fontSmall)
                        self.buttonsOverView[(i, j)].setAlignment(QtCore.Qt.AlignCenter)

                        
                    elif j == 6 and k>=8:
                        #self.buttonsOverView[(i, j)].setText(self.safeModeText[0])
                        self.buttonsOverView[(i, j)].setPixmap(QtGui.QPixmap("images/connectionWarningBlack.PNG"))
                        self.buttonsOverView[(i, j)].setScaledContents(True)
                        self.buttonsOverView[(i, j)].setFixedSize(40,40)
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], 0, j,4,1)
                        if True:
                            self.buttonsOverView[(i, j)].setFont(self.fontBig)
                        else:
                            self.buttonsOverView[(i, j)].setFont(self.fontSmall)
                        self.buttonsOverView[(i, j)].setAlignment(QtCore.Qt.AlignCenter)

                        
                    elif j == 5 and k>=8:
                        self.buttonsOverView[(i, j)].setText("-")
                        self.buttonsOverView[(i, j)].setFixedWidth(240)
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], 0, j,4,1)
                        if True:
                            self.buttonsOverView[(i, j)].setFont(self.fontBig)
                            self.buttonsOverView[(i, j)].setStyleSheet("color: #66ffff")
                        else:
                            self.buttonsOverView[(i, j)].setFont(self.fontSmall)
                        self.buttonsOverView[(i, j)].setAlignment(QtCore.Qt.AlignCenter)

                        
                    elif j == 6 and k<8:
                        self.buttonsOverView[(i, j)].setText(self.beamIOText[i])
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], i, j,1,1)
                        self.buttonsOverView[(i, j)].setAlignment(QtCore.Qt.AlignLeft)

                        
                    elif j == 7 and k<8:
                        self.buttonsOverView[(i, j)].setText("-")
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], i, j,1,1)
                        self.buttonsOverView[(i, j)].setAlignment(QtCore.Qt.AlignLeft)


                    elif j == 2 and k>=8:
                        self.buttonsOverView[(i, j)].setText(self.beamIOText[i])
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], i, j,1,1)
                        self.buttonsOverView[(i, j)].setAlignment(QtCore.Qt.AlignLeft)

                        
                    elif j == 3 and k>=8:
                        self.buttonsOverView[(i, j)].setText("-")
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], i, j,1,1)
                        self.buttonsOverView[(i, j)].setAlignment(QtCore.Qt.AlignLeft)
                        
                    elif j == 9 and k<8:
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], 0, j,4,1)
                        self.buttonsOverView[(i, j)].setStyleSheet("color: green;\n"
                                                                "border: 2px solid green;\n"
                                                                "border-radius: 0px;\n"
                                                                "background:green;\n")
                        self.buttonsOverView[(i, j)].setFixedWidth(20)
                        self.buttonsOverView[(i, j)].setAlignment(QtCore.Qt.AlignCenter)

                    elif j == 0 and k>=8:
                        self.buttonsOverView[(i, j)].setText("")
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], 0, j,4,1)
                        self.buttonsOverView[(i, j)].setStyleSheet("color: green;\n"
                                                                "border: 2px solid green;\n"
                                                                "border-radius: 0px;\n"
                                                                "background:green;\n")
                        self.buttonsOverView[(i, j)].setFixedWidth(20)
                        self.buttonsOverView[(i, j)].setAlignment(QtCore.Qt.AlignCenter)
                        

                        
              #          if self.FLU[k-8] < (len(STYLEFLU)):
              #              self.buttonsOverView[(i, j)].setStyleSheet(STYLEFLU[self.FLU[k-8]])

                    else:
                        self.overViewLayouts[k].addWidget(self.buttonsOverView[(i, j)], i, j,1,1)
                    
                    # CONNECT TO FUNCTION
#                    self.buttonsOverView[(i, j)].clicked.connect(self.beamSafeButtons_clicked)
            self.groupBoxesOverview[k].setLayout(self.overViewLayouts[k])
            
            
################################# PEOPLE-IN-BEAM ########################      
        # Active flag buttons 
        self.peopleInBeamLayouts = []
        self.buttonspeopleInBeam = {}
        
        N = 3
        
        for k in range(NO_BEAMS):  # 16 beams
            self.peopleInBeamLayout = QtWidgets.QGridLayout()  
            self.peopleInBeamLayout.setRowStretch(N, 2) 
            self.peopleInBeamLayouts.append(self.peopleInBeamLayout)
            for i in range(N):   #vertical
                for j in range(1):   #horizontal
                    # keep a reference to the buttons
                    self.buttonspeopleInBeam[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                    self.buttonspeopleInBeam[(i, j)].setFixedSize(SAFEMODEBUTTON_HOR,SAFEMODEBUTTON_VERT)
                    self.buttonspeopleInBeam[(i, j)].setStyleSheet(STYLENOWRITE)
                    
                    self.buttonspeopleInBeam[(i , j)].setText(labelTextPeopleInBeam[i])
                        
                    # add to the layout
                    self.peopleInBeamLayouts[k].addWidget(self.buttonspeopleInBeam[(i, j)], i, j)
                    
                    # CONNECT TO FUNCTION
                    self.buttonspeopleInBeam[(i, j)].clicked.connect(self.peopleInBeamButtons_clicked)
      
            self.groupBoxesPeopleInBeam[k].setLayout(self.peopleInBeamLayouts[k])
          #  self.groupBoxesActive[k].setStyleSheet("background-color:transparent;")

################################# BEAM SAFE STATES ########################      
        # Active flag buttons 
        self.beamSafeLayouts = []
        self.buttonsBeamSafe = {}
        
        N = NO_BEAMSAFEMODES #len(labelTextActive)
        
        for k in range(NO_BEAMS):  # 16 beams
            self.beamSafeLayout = QtWidgets.QGridLayout()  
            self.beamSafeLayout.setRowStretch(N, 2) 
            self.beamSafeLayouts.append(self.beamSafeLayout)
            for i in range(N):   #vertical
                for j in range(1):   #horizontal
                    # keep a reference to the buttons
                    self.buttonsBeamSafe[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                    self.buttonsBeamSafe[(i, j)].setFixedSize(SAFEMODEBUTTON_HOR,SAFEMODEBUTTON_VERT)
                    self.buttonsBeamSafe[(i, j)].setStyleSheet(STYLENOWRITE)
                    
                    self.buttonsBeamSafe[(i , j)].setText(labelTextBeamSafe[i])
                        
                    # add to the layout
                    self.beamSafeLayouts[k].addWidget(self.buttonsBeamSafe[(i, j)], i, j)
                    
                    # CONNECT TO FUNCTION
                    self.buttonsBeamSafe[(i, j)].clicked.connect(self.beamSafeButtons_clicked)
      
            self.groupBoxesBeamSafe[k].setLayout(self.beamSafeLayouts[k])
          #  self.groupBoxesActive[k].setStyleSheet("background-color:transparent;")

################################# DRIVE SAFE STATES ########################      
        # Active flag buttons 
        self.driveSafeLayouts = []
        self.buttonsDriveSafe = {}
        
        N = NO_DRIVESAFEMODES #len(labelTextActive)
        
        for k in range(NO_BEAMS):  # 16 beams
            self.driveSafeLayout = QtWidgets.QGridLayout()  
            self.driveSafeLayout.setRowStretch(N, 2) 
            self.driveSafeLayouts.append(self.driveSafeLayout)
            for i in range(N+1):   #vertical
                for j in range(3):   #horizontal
                    if i == 0:
                        self.buttonsDriveSafe[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                        self.buttonsDriveSafe[(i, j)].setFixedSize(SAFEMODEBUTTON_HOR,SAFEMODEBUTTON_VERT)
                    else:
                        # keep a reference to the buttons
                        self.buttonsDriveSafe[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                        self.buttonsDriveSafe[(i, j)].setFixedSize(SAFEMODEBUTTON_HOR,SAFEMODEBUTTON_VERT)
                        self.buttonsDriveSafe[(i, j)].setStyleSheet(STYLENOWRITE)
                        
                    self.buttonsDriveSafe[(i , j)].setText(labelTextDriveSafe[j][i])
                    if labelTextDriveSafe[j][i] == "":
                        self.buttonsDriveSafe[(i, j)].setStyleSheet("QPushButton{\n"
                                                                "color: black;\n"
                                                                "border: 0px solid black;\n"
                                                                "border-radius: 2px;\n"
                                                                "background:transparent;\n"
                                                                "}")
                        
                        
                    # add to the layout
                    self.driveSafeLayouts[k].addWidget(self.buttonsDriveSafe[(i, j)], i, j)
                    
                    # CONNECT TO FUNCTION
                    if i<>0:
                        self.buttonsDriveSafe[(i, j)].clicked.connect(self.driveSafeButtons_clicked)
      
            self.groupBoxesDriveSafe[k].setLayout(self.driveSafeLayouts[k])
          #  self.groupBoxesActive[k].setStyleSheet("background-color:transparent;")
            
################################# ACTIVE FLAG BUTTONS ########################      
        # Active flag buttons 
        self.activeLayouts = []
        self.buttonsActive = {}
        
        N = NO_ACTIVEFLAGS #len(labelTextActive)
        
        for k in range(NO_BEAMS):  # 16 beams
            self.activeLayout = QtWidgets.QGridLayout()  
            self.activeLayout.setRowStretch(N, 2) 
            self.activeLayouts.append(self.activeLayout)
            for i in range(N):   #vertical
                for j in range(3):   #horizontal
                    # keep a reference to the buttons
                    if j == 0:
                        self.buttonsActive[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                        self.buttonsActive[(i, j)].setFixedSize(150,23)
                    else:
                        self.buttonsActive[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                        self.buttonsActive[(i, j)].setFixedSize(BUTTON_HOR,BUTTON_VERT)
                        self.buttonsActive[(i, j)].setStyleSheet(STYLENOWRITE)
                    
                    if j == 1:
                        self.buttonsActive[(i , 1)].setText("ACTIVE")
                    if j == 2:  
                        self.buttonsActive[(i , 2)].setText("NOT ACTIVE")
                    if j==0:
                        self.buttonsActive[(i , 0)].setText(labelTextActive[i])
                        
                    # add to the layout
                    self.activeLayouts[k].addWidget(self.buttonsActive[(i, j)], i, j)
                    
                    # CONNECT TO FUNCTION
                    if j>0:
                        self.buttonsActive[(i, j)].clicked.connect(self.activeButtons_clicked)
      
            self.groupBoxesActive[k].setLayout(self.activeLayouts[k])
          #  self.groupBoxesActive[k].setStyleSheet("background-color:transparent;")
        

################################# IGNORE FLAG BUTTONS ########################      
        # IGNORE flag buttons 
        self.ignoreLayouts = []
        self.buttonsIgnore = {}
        
        N = NO_IGNOREFLAGS #len(labelTextIgnore)
        
        for k in range(NO_BEAMS):  # 16 beams
            self.ignoreLayout = QtWidgets.QGridLayout()  
            self.ignoreLayout.setRowStretch(N, 2) 
            self.ignoreLayouts.append(self.ignoreLayout)
            for i in range(N):   #vertical
                for j in range(3):   #horizontal
                    # keep a reference to the buttons
                    if j == 0:
                        self.buttonsIgnore[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                        self.buttonsIgnore[(i, j)].setFixedSize(BUTTON_HOR*2,BUTTON_VERT)
                    else:
                        self.buttonsIgnore[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                        self.buttonsIgnore[(i, j)].setFixedSize(BUTTON_HOR,BUTTON_VERT)
                        self.buttonsIgnore[(i, j)].setStyleSheet(STYLENOWRITE)
                    
                    if j == 1:
                        self.buttonsIgnore[(i , 1)].setText("IGNORED")
                    if j == 2:  
                        self.buttonsIgnore[(i , 2)].setText("NOT IGNORED")
                    if j==0:
                        self.buttonsIgnore[(i , 0)].setText(labelTextIgnore[i])
                        
                    # add to the layout
                    self.ignoreLayouts[k].addWidget(self.buttonsIgnore[(i, j)], i, j)
                    
                    # CONNECT TO FUNCTION
                    if j>0:
                        self.buttonsIgnore[(i, j)].clicked.connect(self.ignoreButtons_clicked)
      
            self.groupBoxesIgnore[k].setLayout(self.ignoreLayouts[k])
            #self.groupBoxesIgnore[k].setStyleSheet("background-color:transparent;")


################################# E-STOP reaction BUTTONS ########################      
        # E-STOP REACTION BUTTONS
        self.estopReactionLayouts = []
        self.buttonsEstopReaction = {}
        
        N = len(labelTextEstopReaction)
        
        for k in range(NO_BEAMS):  # 16 beams
            self.estopReactionLayout = QtWidgets.QGridLayout()  
            self.estopReactionLayout.setRowStretch(N, 2) 
            self.estopReactionLayouts.append(self.estopReactionLayout)
            for i in range(N):   #vertical
                for j in range(3):   #horizontal
                    # keep a reference to the buttons
                    if j == 0:
                        self.buttonsEstopReaction[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                        self.buttonsEstopReaction[(i, j)].setFixedSize(BUTTON_HOR*2,BUTTON_VERT*2)
                    elif i == N-1 and j == 1:
                        self.buttonsEstopReaction[(i, j)] = QtWidgets.QDoubleSpinBox()
                        self.buttonsEstopReaction[(i, j)].setFixedSize(BUTTON_HOR,BUTTON_VERT)
                        self.buttonsEstopReaction[(i, j)].setDecimals(1)
                        self.buttonsEstopReaction[(i, j)].setSingleStep(0.1)
                        self.buttonsEstopReaction[(i, j)].setRange(0,20)
                        self.buttonsEstopReaction[(i, j)].setStyleSheet(STYLENOWRITE)
                    elif i == N-1 and j == 2:
                        self.buttonsEstopReaction[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                        self.buttonsEstopReaction[(i, j)].setFixedSize(BUTTON_HOR,BUTTON_VERT)  
                        self.buttonsEstopReaction[(i, j)].setText("")
                    else:
                        self.buttonsEstopReaction[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                        self.buttonsEstopReaction[(i, j)].setFixedSize(BUTTON_HOR,BUTTON_VERT)
                        self.buttonsEstopReaction[(i, j)].setStyleSheet("QPushButton{\n"
                                                            "color: black;\n"
                                                            "border: 2px solid #ff0066;\n"
                                                            "border-radius: 2px;\n"
                                                            "background:transparent;\n"
                                                            "}")                
                    # add labels
                    if i == N-1 and j ==1:
                        self.buttonsEstopReaction[(i, j)].setRange(0,20)
                    else:                        
                        self.buttonsEstopReaction[(i , j)].setText(labelTextEstopReaction[i][j])
       
                    # add to the layout
                    self.estopReactionLayouts[k].addWidget(self.buttonsEstopReaction[(i, j)], i, j)
                    
                    # CONNECT TO FUNCTION
                    if j<>0 and i<>N-1:
                        self.buttonsEstopReaction[(i, j)].clicked.connect(self.eReactionButtons_clicked)
                    elif j==1 and i==N-1:
                        self.buttonsEstopReaction[(i, j)].valueChanged[float].connect(self.yBrake_clicked)
      
            self.groupBoxesEstopReaction[k].setLayout(self.estopReactionLayouts[k])

################################# LBC INTERLOCKS ########################      
        # OUTPUT STATE buttons 
        self.lbcInterlocksLayouts = []
        self.buttonsLbcInterlocks = {}
        
        N = (NO_SAFETYINPUTS-16) #len(labelTextOutput)
        
        for k in range(NO_BEAMS):  # 16 beams
            self.lbcInterlocksLayout = QtWidgets.QGridLayout()  
            self.lbcInterlocksLayout.setRowStretch(N, 2) 
            self.lbcInterlocksLayouts.append(self.lbcInterlocksLayout)
            for i in range(N):   #vertical
                for j in range(2):   #horizontal
                    # keep a reference to the buttons
                    if j == 1:
                        self.buttonsLbcInterlocks[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                        self.buttonsLbcInterlocks[(i, j)].setFixedSize(BUTTON_HOR*2,BUTTON_VERT)
                    else:
                        self.buttonsLbcInterlocks[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                        self.buttonsLbcInterlocks[(i, j)].setFixedSize(23,BUTTON_VERT)
                    self.buttonsLbcInterlocks[(i, j)].setStyleSheet("QPushButton{\n"
                                                            "color: black;\n"
                                                            "border: 0px solid white;\n"
                                                            "border-radius: 2px;\n"
                                                            "background:black;\n"
                                                            "}")
                    
                    if j == 0:
                        self.buttonsLbcInterlocks[(i , j)].setText("")
                        self.buttonsLbcInterlocks[(i, j)].setStyleSheet("color: black;\n" "border: 2px solid grey;\n" "border-radius: 11px;\n" "background:grey;\n")
#                    if j == 2:  
#                        self.buttonsIOInput[(i , 2)].setText("NOT TRIGGERED")
                    if j==1:
                        self.buttonsLbcInterlocks[(i , j)].setText("N/A in Simulator")
                        
                    # add to the layout
                    self.lbcInterlocksLayouts[k].addWidget(self.buttonsLbcInterlocks[(i, j)], i, j)

            self.groupBoxesLbcInterlocks[k].setLayout(self.lbcInterlocksLayouts[k])


################################# LBC MODE AND FUNCTIONS ########################      
        labelTextLbc = ["Control Mode: ", "X-locking function: ","AHC system function: ","Y-hydraulic function: ", "OSS-LBC communication:"]


    # LBC functions:
        xDriveFunction = self.xDriveFunction[k]
        yDriveElectricFunction = self.yDriveElectricFunction[k]
        yDriveHydraulicFunction = self.yDriveHydraulicFunction[k]
        xLockingFunction = self.xLockingFunction[k]
        LCFunction = self.LCFunction[k]
        AHCFunction= self.AHCFunction[k]
        yBrakeFunction = self.yBrakeFunction[k]
        
        
        # OUTPUT STATE buttons 
        self.lbcFunctionsLayouts = []
        self.buttonsLbcFunctions = {}
        
        N = len(labelTextLbc)
        
        for k in range(NO_BEAMS):  # 16 beams
            self.lbcFunctionsLayout = QtWidgets.QGridLayout()  
            self.lbcFunctionsLayout.setRowStretch(N, 2) 
            self.lbcFunctionsLayouts.append(self.lbcFunctionsLayout)
            for i in range(N):   #vertical
                for j in range(2):   #horizontal
                    # keep a reference to the buttons

                    self.buttonsLbcFunctions[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                    self.buttonsLbcFunctions[(i, j)].setFixedSize(BUTTON_HOR*1.5,BUTTON_VERT)
                    
                    
                    if j == 1:
                        self.buttonsLbcFunctions[(i , 1)].setText("...")
                        self.buttonsLbcFunctions[(i, j)].setStyleSheet("color: #66ffff")

                    if j==0:
                        self.buttonsLbcFunctions[(i , 0)].setText(labelTextLbc[i])
                        
                    # add to the layout
                    self.lbcFunctionsLayouts[k].addWidget(self.buttonsLbcFunctions[(i, j)], i, j)

            self.groupBoxesLbcFunctions[k].setLayout(self.lbcFunctionsLayouts[k])


################################# SET E-STOP OUTPUT GROUP BUTTONS ########################      
        # OUTPUT STATE buttons 
        self.outputLayouts = []
        self.buttonsOutput = {}
        
        N = NO_ESTOPOUTPUTS #len(labelTextOutput)
        
        for k in range(NO_BEAMS):  # 16 beams
            self.outputLayout = QtWidgets.QGridLayout()  
            self.outputLayout.setRowStretch(N, 2) 
            self.outputLayouts.append(self.outputLayout)
            for i in range(N):   #vertical
                for j in range(2):   #horizontal
                    # keep a reference to the buttons
#                    if j == 0:
#                        self.buttonsOutput[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
#                        self.buttonsOutput[(i, j)].setFixedSize(BUTTON_HOR*2,BUTTON_VERT)
#                    else:
                    self.buttonsOutput[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                    self.buttonsOutput[(i, j)].setFixedSize(BUTTON_HOR,BUTTON_VERT)
                    self.buttonsOutput[(i, j)].setStyleSheet(STYLENOWRITE)
                    
                    if j == 0:
                        self.buttonsOutput[(i , 0)].setText("SET")
                    if j == 1:  
                        self.buttonsOutput[(i , 1)].setText("NOT SET")
                   # if j==0:
                   #     self.buttonsOutput[(i , 0)].setText(labelTextOutput[i])
                        
                    # add to the layout
                    self.outputLayouts[k].addWidget(self.buttonsOutput[(i, j)], i, j)
                    
                    # CONNECT TO FUNCTION
                    #if j>0:
                    self.buttonsOutput[(i, j)].clicked.connect(self.outputButtons_clicked)
      
            self.groupBoxesOutput[k].setLayout(self.outputLayouts[k])
            #self.groupBoxesIgnore[k].setStyleSheet("background-color:transparent;")
            
################################# E-STOP OUTPUT GROUPS ########################      
        # OUTPUT STATE buttons 
        self.outputIOLayouts = []
        self.buttonsIOOutput = {}
        
        N = NO_ESTOPOUTPUTS #len(labelTextOutput)
        
        for k in range(NO_BEAMS):  # 16 beams
            self.outputIOLayout = QtWidgets.QGridLayout()  
            self.outputIOLayout.setRowStretch(N, 2) 
            self.outputIOLayouts.append(self.outputIOLayout)
            for i in range(N):   #vertical
                for j in range(2):   #horizontal
                    # keep a reference to the buttons
                    if j == 1:
                        self.buttonsIOOutput[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                        self.buttonsIOOutput[(i, j)].setFixedSize(BUTTON_HOR*2,BUTTON_VERT)
                    else:
                        self.buttonsIOOutput[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                        self.buttonsIOOutput[(i, j)].setFixedSize(23,BUTTON_VERT)
                    self.buttonsIOOutput[(i, j)].setStyleSheet("QPushButton{\n"
                                                            "color: black;\n"
                                                            "border: 0px solid white;\n"
                                                            "border-radius: 2px;\n"
                                                            "background:black;\n"
                                                            "}")
                    
                    if j == 0:
                        self.buttonsIOOutput[(i , j)].setText("...")
#                    if j == 2:  
#                        self.buttonsIOOutput[(i , 2)].setText("NO E-STOP")
                    if j==1:
                        self.buttonsIOOutput[(i , j)].setText(labelTextOutput[i])
                        
                    # add to the layout
                    self.outputIOLayouts[k].addWidget(self.buttonsIOOutput[(i, j)], i, j)

            self.groupBoxesOutputIO[k].setLayout(self.outputIOLayouts[k])
   



################################ E-STOP STATES ########################      
        # OUTPUT STATE buttons 
        self.eStateLayouts = []
        self.buttonsEState = {}
        
        N = NO_ESTOPOUTPUTS #len(labelTextOutput)
        
        for k in range(NO_BEAMS):  # 16 beams
            self.eStateLayout = QtWidgets.QGridLayout()  
            self.eStateLayout.setRowStretch(N, 2) 
            self.eStateLayouts.append(self.eStateLayout)
            for i in range(N):   #vertical
                for j in range(2):   #horizontal
                    # keep a reference to the buttons
                    if j == 1:
                        self.buttonsEState[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                        self.buttonsEState[(i, j)].setFixedSize(BUTTON_HOR*2,BUTTON_VERT)
                    else:
                        self.buttonsEState[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                        self.buttonsEState[(i, j)].setFixedSize(23,BUTTON_VERT)
                    self.buttonsEState[(i, j)].setStyleSheet("QPushButton{\n"
                                                            "color: black;\n"
                                                            "border: 0px solid white;\n"
                                                            "border-radius: 2px;\n"
                                                            "background:black;\n"
                                                            "}")
                    
                    if j == 0:
                        self.buttonsEState[(i , j)].setText("...")
#                    if j == 2:  
#                        self.buttonsIOOutput[(i , 2)].setText("NO E-STOP")
                    if j==1:
                        self.buttonsEState[(i , j)].setText(labelTextOutput[i])
                        
                    # add to the layout
                    self.eStateLayouts[k].addWidget(self.buttonsEState[(i, j)], i, j)

            self.groupBoxesEState[k].setLayout(self.eStateLayouts[k])
        
################################# E-STOP BUTTON STATUS ########################      
        # OUTPUT STATE buttons 
        self.inputIOLayouts = []
        self.buttonsIOInput = {}
        
        N = NO_SAFETYINPUTS-16 #len(labelTextOutput)
        
        for k in range(NO_BEAMS):  # 16 beams
            self.inputIOLayout = QtWidgets.QGridLayout()  
            self.inputIOLayout.setRowStretch(N, 2) 
            self.inputIOLayouts.append(self.inputIOLayout)
            for i in range(N):   #vertical
                for j in range(2):   #horizontal
                    # keep a reference to the buttons
                    if j == 1:
                        self.buttonsIOInput[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                        self.buttonsIOInput[(i, j)].setFixedSize(BUTTON_HOR*2,BUTTON_VERT)
                    else:
                        self.buttonsIOInput[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                        self.buttonsIOInput[(i, j)].setFixedSize(23,BUTTON_VERT)
                    self.buttonsIOInput[(i, j)].setStyleSheet("QPushButton{\n"
                                                            "color: black;\n"
                                                            "border: 0px solid white;\n"
                                                            "border-radius: 2px;\n"
                                                            "background:black;\n"
                                                            "}")
                    
                    if j == 0:
                        self.buttonsIOInput[(i , j)].setText("...")
#                    if j == 2:  
#                        self.buttonsIOInput[(i , 2)].setText("NOT TRIGGERED")
                    if j==1:
                        self.buttonsIOInput[(i , j)].setText(labelTextInput[i])
                        
                    # add to the layout
                    self.inputIOLayouts[k].addWidget(self.buttonsIOInput[(i, j)], i, j)

            self.groupBoxesInputIO[k].setLayout(self.inputIOLayouts[k])
            


################################# E-STOP TIME-OUT ########################      
        # OUTPUT STATE buttons 
        self.eTimeOutLayouts = []
        self.buttonsETimeOut = {}
        
        N = 3 #len(labelTextOutput)
        labelTextTimeOut = ["OSS-LBC communication time-out","ABC-LBC communication time-out","OSS-LBC frame counter"]        
        
        for k in range(NO_BEAMS):  # 16 beams
            self.eTimeOutLayout = QtWidgets.QGridLayout()  
            self.eTimeOutLayout.setRowStretch(N, 2) 
            self.eTimeOutLayouts.append(self.eTimeOutLayout)
            for i in range(N):   #vertical
                for j in range(2):   #horizontal
                    # keep a reference to the buttons
                    if j == 1:
                        self.buttonsETimeOut[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                        self.buttonsETimeOut[(i, j)].setFixedSize(BUTTON_HOR*2,BUTTON_VERT)
                        self.buttonsETimeOut[(i, j)].setFixedWidth(3*230+40-50)
                    elif j == 0 and i ==2:
                        self.buttonsETimeOut[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                        self.buttonsETimeOut[(i, j)].setFixedSize(23,23)
                        self.buttonsETimeOut[(i, j)].setAlignment(QtCore.Qt.AlignCenter)
                        self.buttonsETimeOut[(i, j)].setText("...")
                    else:
                        self.buttonsETimeOut[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                        self.buttonsETimeOut[(i, j)].setFixedSize(BUTTON_HOR*2,23)
                    self.buttonsETimeOut[(i, j)].setStyleSheet("QPushButton{\n"
                                                            "color: black;\n"
                                                            "border: 0px solid white;\n"
                                                            "border-radius: 2px;\n"
                                                            "background:black;\n"
                                                            "}")
                    
                    if j==1:
                        self.buttonsETimeOut[(i , j)].setText(labelTextTimeOut[i])
                        
                    # add to the layout
                    self.eTimeOutLayouts[k].addWidget(self.buttonsETimeOut[(i, j)], i, j)

            self.groupBoxesETimeOut[k].setLayout(self.eTimeOutLayouts[k])
            
            
################################# ADDITIONAL BEAM SAFETY INPUTS ########################      
        # OUTPUT STATE buttons 
        self.extraInputIOLayouts = []
        self.buttonsExtraIOInput = {}
        
        N = 16
        
        for k in range(NO_BEAMS):  # 16 beams
            self.extraInputIOLayout = QtWidgets.QGridLayout()  
            self.extraInputIOLayout.setRowStretch(N, 2) 
            self.extraInputIOLayouts.append(self.extraInputIOLayout)
            for i in range(N):   #vertical
                for j in range(2):   #horizontal
                    # keep a reference to the buttons
                    if j == 1:
                        self.buttonsExtraIOInput[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                        self.buttonsExtraIOInput[(i, j)].setFixedSize(BUTTON_HOR*2,BUTTON_VERT)
                    else:
                        self.buttonsExtraIOInput[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                        self.buttonsExtraIOInput[(i, j)].setFixedSize(23,BUTTON_VERT)
                    self.buttonsExtraIOInput[(i, j)].setStyleSheet("QPushButton{\n"
                                                            "color: black;\n"
                                                            "border: 0px solid white;\n"
                                                            "border-radius: 2px;\n"
                                                            "background:black;\n"
                                                            "}")
                    
                    if j == 0:
                        self.buttonsExtraIOInput[(i , j)].setText("")
                        self.buttonsExtraIOInput[(i, j)].setStyleSheet("color: black;\n" "border: 2px solid grey;\n" "border-radius: 11px;\n" "background:grey;\n")
#                    if j == 2:  
#                        self.buttonsIOInput[(i , 2)].setText("NOT TRIGGERED")
                    if j==1:
                        self.buttonsExtraIOInput[(i , j)].setText("N/A in Simulator")
                        
                    # add to the layout
                    self.extraInputIOLayouts[k].addWidget(self.buttonsExtraIOInput[(i, j)], i, j)

            self.groupBoxesExtraInputIO[k].setLayout(self.extraInputIOLayouts[k])




############### BEAM NAVIGATOR with navigation buttons to the 16 beams ##########
        # vessel gemoetry top view (moved to central widget to not interfere with button grid):
        self.VesselTopView = QtWidgets.QLabel(self.centralWidget)
        self.VesselTopView.setGeometry(QtCore.QRect(HOR_RES-VESSEL_HOR, TOPBAR_RES, VESSEL_HOR, VESSEL_VERT))
        self.VesselTopView.setPixmap(QtGui.QPixmap("images/vessel.PNG"))
        
        self.overViewButton = QtWidgets.QPushButton(self.centralWidget)
        self.overViewButton.setGeometry(QtCore.QRect(HOR_RES-RIGHTBAR_RES+(RIGHTBAR_RES-90)/2, TOPBAR_RES+30+8*30+10, 90, 23))
        self.overViewButton.setText("OVERVIEW")
        self.overViewButton.setStyleSheet(STYLELBCOSSWRITE)
        self.overViewButton.clicked.connect(self.overviewButton_clicked)
        self.overViewButton.hide()
                                                    
        
        # self.fluConfigButton = QtWidgets.QPushButton(self.centralWidget)
        # self.fluConfigButton.setGeometry(QtCore.QRect(HOR_RES-RIGHTBAR_RES+(RIGHTBAR_RES-90)/2, TOPBAR_RES+30+9*30+10, 90, 23))
        # self.fluConfigButton.setText("CONFIG CHECK")
        # self.fluConfigButton.setStyleSheet(STYLEWRITE)
        # self.fluConfigButton.clicked.connect(self.configButton_clicked)

        self.fluButton = QtWidgets.QPushButton(self.centralWidget)
        self.fluButton.setGeometry(QtCore.QRect(HOR_RES-RIGHTBAR_RES+(RIGHTBAR_RES-45)/2, TOPBAR_RES+30+9*30+10+50, 50, 50))
        self.fluButton.setIcon(QtGui.QIcon("images/fluButton.PNG"))
        self.fluButton.setIconSize(QtCore.QSize(50, 50))
        self.fluButton.setStyleSheet(STYLEWRITE)
        self.fluButton.clicked.connect(self.fluButton_clicked)

        self.configCheckButton = QtWidgets.QPushButton(self.centralWidget)
        self.configCheckButton.setGeometry(QtCore.QRect(HOR_RES-RIGHTBAR_RES+(RIGHTBAR_RES-190)/2, TOPBAR_RES+30+9*30+10+50, 50, 50))
        self.configCheckButton.setIcon(QtGui.QIcon("images/checkConfigButton.PNG"))
        self.configCheckButton.setIconSize(QtCore.QSize(50, 50))
        self.configCheckButton.setStyleSheet(STYLEWRITE)
        self.configCheckButton.clicked.connect(self.configButton_clicked)

        self.sifButton = QtWidgets.QPushButton(self.centralWidget)
        self.sifButton.setGeometry(QtCore.QRect(HOR_RES-RIGHTBAR_RES+(RIGHTBAR_RES+90)/2, TOPBAR_RES+30+9*30+10+50, 50, 50))
        self.sifButton.setIcon(QtGui.QIcon("images/sifButton.PNG"))
        self.sifButton.setIconSize(QtCore.QSize(50, 50))
        self.sifButton.setStyleSheet(STYLEWRITE)
        self.sifButton.clicked.connect(self.sifButton_clicked)

        self.warningButton = QtWidgets.QPushButton(self.centralWidget)
        self.warningButton.setGeometry(QtCore.QRect(HOR_RES-70-70-70, VERT_RES-60, 50, 50))
        self.warningButton.setIcon(QtGui.QIcon("images/alarmButton.PNG"))
        self.warningButton.setIconSize(QtCore.QSize(50,50))
        self.warningButton.setStyleSheet(STYLEWRITE)
        self.warningButton.clicked.connect(self.warningButton_clicked)  
                                        
        self.networkButton = QtWidgets.QPushButton(self.centralWidget)
        self.networkButton.setGeometry(QtCore.QRect(HOR_RES-70-70-70-70, VERT_RES-60, 50, 50))
        self.networkButton.setIcon(QtGui.QIcon("images/networkButton.PNG"))
        self.networkButton.setIconSize(QtCore.QSize(50,50))
        self.networkButton.setStyleSheet(STYLEWRITE)
        self.networkButton.clicked.connect(self.networkButton_clicked)                                                         
        
        self.vesselLayout = QtWidgets.QGridLayout()
        self.vesselWidget = QtWidgets.QWidget(self.centralWidget)
        self.vesselWidget.setGeometry(QtCore.QRect(HOR_RES-RIGHTBAR_RES, TOPBAR_RES+30, RIGHTBAR_RES, 8*30))
        

        # Nav buttons
        self.buttons = {}
        self.buttonsText = (beamIDtext[NO_BEAMS/2:NO_BEAMS],beamIDtext[0:NO_BEAMS/2])
        
        for i in range(NO_BEAMS/2):   #vertical
            for j in range(7):   #horizontal
                # keep a reference to the buttons
                if j ==1:
                    kk = i+8
                else:
                    kk = i
                    
                self.buttons[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                self.buttons[(i, j)].setFixedSize(10,10)
                self.buttons[(i, j)].setStyleSheet("QPushButton{\n"
                                                        "color: black;\n"
                                                        "border: 0px solid black;\n"
                                                        "border-radius: 5px;\n"
                                                        "background:transparent;\n"
                                                        "}")
                                                        
                
                if j in [2,4]:
                    self.buttons[(i, j)].setFixedSize(14,14)
                    
                    
                if j in [0,6]:
                    self.buttons[(i, j)].setFixedSize(20,19)

                                                            
                if j == 1 and i < (NO_BEAMS/2):
                    self.buttons[(i, j)].setText(self.buttonsText[0][i])
                    self.buttons[(i, j)].setFixedSize(90,23)
                    self.buttons[(i, j)].setStyleSheet(STYLEWRITE)
                    
                    
                    if ACTIVE_BEAMS[kk] == 0:
                        self.buttons[(i, j)].setStyleSheet(STYLEWRITEDASHED)
                     
                    self.buttons[(i, j)].clicked.connect(self.vesselButtons_clicked)
                    
                elif j == 5 and i < (NO_BEAMS/2):
                    self.buttons[(i, j)].setText(self.buttonsText[1][i])
                    self.buttons[(i, j)].setFixedSize(90,23)
                    self.buttons[(i, j)].setStyleSheet(STYLEWRITE)
                    
                    if ACTIVE_BEAMS[kk] == 0:
                        self.buttons[(i, j)].setStyleSheet(STYLEWRITEDASHED)

                    self.buttons[(i, j)].clicked.connect(self.vesselButtons_clicked)
                                    
                self.vesselLayout.addWidget(self.buttons[(i, j)], i, j)    


        # add to the alyout
        self.vesselWidget.setLayout(self.vesselLayout)
        
################################# 16 BEAM CHECK BUTTONS ########################      
        # Active flag buttons 
        self.beamCheckLayouts = []
        self.buttonsCheckBeams = {}
        self.buttonsFLU = []
        
        N = NO_BEAMS/2 #len(labelTextActive)
        

        self.beamCheckLayouts = QtWidgets.QGridLayout()  

        for i in range(N):   #vertical
            for j in range(4):   #horizontal
   
                if j==0:
                    self.buttonsCheckBeams[(i, j)] = QtWidgets.QComboBox()
                    self.buttonsCheckBeams[(i, j)].addItem("-")
                    self.buttonsCheckBeams[(i, j)].addItem("1")
                    self.buttonsCheckBeams[(i, j)].addItem("2")
                    self.buttonsCheckBeams[(i, j)].addItem("3")
                    self.buttonsCheckBeams[(i, j)].addItem("4")
                    self.buttonsCheckBeams[(i, j)].addItem("5")
                    self.buttonsCheckBeams[(i, j)].addItem("6")
                    self.buttonsCheckBeams[(i, j)].addItem("7")
                    self.buttonsCheckBeams[(i, j)].addItem("8")
                    self.buttonsCheckBeams[(i, j)].setFixedSize(2*BUTTON_VERT,BUTTON_VERT)
                    self.buttonsCheckBeams[(i, j)].setCurrentIndex(self.FLU[i+8])
                    self.buttonsCheckBeams[(i, j)].currentIndexChanged.connect(self.FLU_clicked)
                    self.buttonsCheckBeams[(i, j)].setStyleSheet("color: white;\n"
                                                        "border: 0px solid black;\n"
                                                        "border-radius: 0px;\n"
                                                        "background:transparent;\n")
                elif j==3:
                    self.buttonsCheckBeams[(i, j)] = QtWidgets.QComboBox()
                    self.buttonsCheckBeams[(i, j)].addItem("-")
                    self.buttonsCheckBeams[(i, j)].addItem("1")
                    self.buttonsCheckBeams[(i, j)].addItem("2")
                    self.buttonsCheckBeams[(i, j)].addItem("3")
                    self.buttonsCheckBeams[(i, j)].addItem("4")
                    self.buttonsCheckBeams[(i, j)].addItem("5")
                    self.buttonsCheckBeams[(i, j)].addItem("6")
                    self.buttonsCheckBeams[(i, j)].addItem("7")
                    self.buttonsCheckBeams[(i, j)].addItem("8")
                    self.buttonsCheckBeams[(i, j)].setFixedSize(2*BUTTON_VERT,BUTTON_VERT)
                    self.buttonsCheckBeams[(i, j)].setCurrentIndex(self.FLU[i])
                    self.buttonsCheckBeams[(i, j)].currentIndexChanged.connect(self.FLU_clicked)
                    self.buttonsCheckBeams[(i, j)].setStyleSheet("color: white;\n"
                                                        "border: 0px solid black;\n"
                                                        "border-radius: 0px;\n"
                                                        "background:transparent;\n")
                else:
                    self.buttonsCheckBeams[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                    self.buttonsCheckBeams[(i, j)].setFixedSize(BUTTON_HOR,BUTTON_VERT)
                    self.buttonsCheckBeams[(i, j)].setStyleSheet(STYLEWRITE)

              
                if j == 2:
                    self.buttonsCheckBeams[(i , j)].setText(beamIDtext[i])
                    # CONNECT TO FUNCTION
                    self.buttonsCheckBeams[(i, j)].clicked.connect(self.beamCheckButtons_clicked)
                if j==1:
                    self.buttonsCheckBeams[(i , j)].setText(beamIDtext[i+8])
                    # CONNECT TO FUNCTION
                    self.buttonsCheckBeams[(i, j)].clicked.connect(self.beamCheckButtons_clicked)
                    
                # add to the layout
                self.beamCheckLayouts.addWidget(self.buttonsCheckBeams[(i, j)], i, j)
                
                
            self.groupBoxCheckBeams.setLayout(self.beamCheckLayouts)
            
################################# ACTIVE FLAG CHECK BUTTONS ########################      
        # Active flag buttons 
        self.activeCheckLayouts = []
        self.buttonsCheckActive = {}
        
        N = NO_ACTIVEFLAGS #len(labelTextActive)
        

        self.activeCheckLayouts = QtWidgets.QGridLayout()  
        self.activeCheckLayouts.setRowStretch(N, 2) 

        for i in range(N):   #vertical
            for j in range(2):   #horizontal
                # keep a reference to the buttons
                if j == 0:
                    self.buttonsCheckActive[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                    self.buttonsCheckActive[(i, j)].setFixedSize(150,23)
                else:
                    self.buttonsCheckActive[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                    self.buttonsCheckActive[(i, j)].setFixedSize(BUTTON_HOR,BUTTON_VERT)
                self.buttonsCheckActive[(i, j)].setStyleSheet("QPushButton{\n"
                                                        "color: white;\n"
                                                        "border: 0px solid white;\n"
                                                        "border-radius: 2px;\n"
                                                        "background:black;\n"
                                                        "}")
                
                if j == 1:
                    self.buttonsCheckActive[(i , 1)].setText("...")
                if j==0:
                    self.buttonsCheckActive[(i , 0)].setText(labelTextActive[i])
                    
                # add to the layout
                self.activeCheckLayouts.addWidget(self.buttonsCheckActive[(i, j)], i, j)
                
                    # CONNECT TO FUNCTION
#                    if j>0:
#                        self.buttonsActive[(i, j)].clicked.connect(self.activeButtons_clicked)
      
            self.groupBoxCheckActive.setLayout(self.activeCheckLayouts)
          #  self.groupBoxesActive[k].setStyleSheet("background-color:transparent;")
            
################################# IGNORE FLAG CHECK BUTTONS ########################      
        # IGNORE flag buttons 
        self.ignoreCheckLayouts = []
        self.buttonsCheckIgnore = {}
        
        N = NO_IGNOREFLAGS #len(labelTextIgnore)
        
        self.ignoreCheckLayouts = QtWidgets.QGridLayout()  
        self.ignoreCheckLayouts.setRowStretch(N, 2) 
        for i in range(N):   #vertical
            for j in range(2):   #horizontal
                # keep a reference to the buttons
                if j == 0:
                    self.buttonsCheckIgnore[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                    self.buttonsCheckIgnore[(i, j)].setFixedSize(BUTTON_HOR*2,BUTTON_VERT)
                else:
                    self.buttonsCheckIgnore[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                    self.buttonsCheckIgnore[(i, j)].setFixedSize(BUTTON_HOR,BUTTON_VERT)
                self.buttonsCheckIgnore[(i, j)].setStyleSheet("QPushButton{\n"
                                                        "color: white;\n"
                                                        "border: 0px solid white;\n"
                                                        "border-radius: 2px;\n"
                                                        "background:black;\n"
                                                        "}")
                
                if j == 1:
                    self.buttonsCheckIgnore[(i , 1)].setText("...")
                if j==0:
                    self.buttonsCheckIgnore[(i , 0)].setText(labelTextIgnore[i])
                    
                # add to the layout
                self.ignoreCheckLayouts.addWidget(self.buttonsCheckIgnore[(i, j)], i, j)
                
                # CONNECT TO FUNCTION
#                if j>0:
#                    self.buttonsIgnore[(i, j)].clicked.connect(self.ignoreButtons_clicked)
  
        self.groupBoxCheckIgnore.setLayout(self.ignoreCheckLayouts)
            #self.groupBoxesIgnore[k].setStyleSheet("background-color:transparent;")  
        
        
################################# E-STOP reaction CHECK BUTTONS ########################      
        # E-STOP REACTION BUTTONS
        self.estopReactionCheckLayouts = []
        self.buttonsCheckEstopReaction = {}
        
        N = len(labelTextEstopReaction)
        

        self.estopReactionCheckLayouts = QtWidgets.QGridLayout()  
        self.estopReactionCheckLayouts.setRowStretch(N, 2) 

        text = ["X-locking E-stop reaction \nduring unlock","Y hydraulic E-stop reaction","AHC E-stop reaction during AHC","Y-brakes E-stop delay"]
        
     
        
        
        for i in range(4):   #vertical
            for j in range(2):   #horizontal
                # keep a reference to the buttons
                if j == 0:
                    self.buttonsCheckEstopReaction[(i, j)] = QtWidgets.QLabel('row %d, col %d' % (i, j))
                    self.buttonsCheckEstopReaction[(i, j)].setFixedSize(BUTTON_HOR*2,BUTTON_VERT)

                else:
                    self.buttonsCheckEstopReaction[(i, j)] = QtWidgets.QPushButton('row %d, col %d' % (i, j))
                    self.buttonsCheckEstopReaction[(i, j)].setFixedSize(BUTTON_HOR,BUTTON_VERT)
                    self.buttonsCheckEstopReaction[(i, j)].setStyleSheet("QPushButton{\n"
                                                        "color: white;\n"
                                                        "border: 0px solid white;\n"
                                                        "border-radius: 2px;\n"
                                                        "background:black;\n"
                                                        "}")  
                    self.buttonsCheckEstopReaction[(i, j)].setText("...")
                # add labels
#                if i == N-1 and j ==1:
#                    self.buttonsCheckEstopReaction[(i, j)].setRange(0,20)
                if j == 0:                        
                    self.buttonsCheckEstopReaction[(i , j)].setText(text[i])  #
   
                # add to the layout
                self.estopReactionCheckLayouts.addWidget(self.buttonsCheckEstopReaction[(i, j)], i, j)
                
#                # CONNECT TO FUNCTION
#                if j<>0 and i<>N-1:
#                    self.buttonsEstopReaction[(i, j)].clicked.connect(self.eReactionButtons_clicked)
#                elif j==1 and i==N-1:
#                    self.buttonsEstopReaction[(i, j)].valueChanged[float].connect(self.yBrake_clicked)
  
        self.groupBoxCheckEstopReaction.setLayout(self.estopReactionCheckLayouts)
            
########################## ASSEMBLE GUI #######################################
    #    self.pushConnect.raise_()
        
        self.topWidget.raise_()        
        self.BottomLine0.raise_()
        self.MiddleLine0.raise_()
        self.TopLine1.raise_()
        self.VertLine0.raise_()
        self.VertLine1.raise_()
        self.hmiIndication.raise_()
        self.pushHome.raise_()
        
     #   self.vesselWidget.raise_()
        
        MainWindow.setCentralWidget(self.centralWidget)


########################## FUNCTIONS #######################################
# moved to mainwindow_functions.py for clarity                


# Reminder to connect OPC button panel  
        if LOCAL_MODE <> 1:       
            self.printAlarmMessage("Console IO failure: OPC not connected.")



######################################## MAIN ##################################3
# moved to runOSS.py
