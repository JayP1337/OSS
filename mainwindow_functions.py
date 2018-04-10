# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 10:46:06 2016

@author: ekk
"""
########################## IMPORT #######################################
import sys
import time
from mainwindow_constants import *  #holds all constant values that define GUI geometry

import numpy

from PyQt5 import QtGui, QtWidgets
if LOCAL_MODE <> 1:
    import clr
    clr.AddReference('AllseasOPC')
    import AllseasOPC
import os
dir = os.path.dirname(__file__)
sys.path.append(dir)



########################## FUNCTIONS #######################################


class Helper(object):
       

            
                         
    #################################### OPC and UDP ###############################                                           
    # Connect to OPC server on button click        
    def opcButton_clicked(self):
        print('(dis)connect OPC!' )

        tagsR=['ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.EStopButton',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.resetButton',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.uploadKey',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam0',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam1',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam2',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam3',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam4',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam5',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam6',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam7',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam8',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam9',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam10',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam11',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam12',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam13',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam14',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.buttons.writeBeam15']
        tagsW=['ns=2;s=Siemens PLC Channel.OSS Button Panel.lights.redEStopLight',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.lights.orangeAlarmLight',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.lights.orangeWarningLight',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.lights.greenSafeLight',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.lights.uploadConfirmLight',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.lights.frontBridgeLight',
               'ns=2;s=Siemens PLC Channel.OSS Button Panel.lights.resetLight']

        
        self.connected = not self.connected
        if self.connected==1:
            print('Connection attempt...')
            self.printAlarmMessage("Console IO operational: OPC connected.")
            self.opcR=AllseasOPC.UALink(HOST,tagsR)
            self.opcW=AllseasOPC.UALink(HOST,tagsW)
           
            try:
                print('Connected to server')
                self.pushConnect.setStyleSheet("background-color:green")
            except:
                print 'Connection to server failed'
                self.pushConnect.setStyleSheet("background-color:red")
        else:
            self.pushConnect.setStyleSheet("background-color:red")
            self.printAlarmMessage("Console IO failure: OPC not connected.")



    # get all OPC data for all beams when connected
    def update(self):        
        # Update the HMI for the current (active) page:
        self.updateWriteMatches() # a function that checks if the enabled write switches match the HMI selection
        self.updatePeopleInBeamButtons()   
        self.updateBeamSafeButtons()
        self.updateDriveSafeButtons()
        self.updateActiveButtons()
        self.updateIgnoreButtons()
        self.updateEstopReactionButtons()
        self.updateOutputButtons()
        self.updateVesselEstop()
        self.updateOverviewEstop()
        self.updateOverviewSafeModes()
        self.updateOverviewFLU()
        self.updateOverviewIO()
        self.updateVesselFLU()
        self.updateOutputIO()
        self.updateInputIO()
        self.updateBeamCheckButtons()
        self.updateYBrake()
     #   self.updateOverviewMatches()   # fancy FLU icon 
        self.updateLbcFunctions()
        self.updateEState()
        self.updateETimeOut()
     #   self.communicationLost()    # nice-to-have under development
                             
        # update HMI time
        self.displayTime()
        

                      
       
        if self.connected == True and (LOCAL_MODE == 0 or LOCAL_MODE == 2):

                # get all OPC data:
                opcReadData = self.opcR.Read()                
                self.eStopPressed = opcReadData[0,0]    # NC contact
                self.resetPressed = opcReadData[1,0]
                self.upLoadPressed = opcReadData[2,0]
                self.writeSwitchData[0] = opcReadData[3,0]
                self.writeSwitchData[1] = opcReadData[4,0]
                self.writeSwitchData[2] = opcReadData[5,0]
                self.writeSwitchData[3] = opcReadData[6,0]
                self.writeSwitchData[4] = opcReadData[7,0]
                self.writeSwitchData[5] = opcReadData[8,0]
                self.writeSwitchData[6] = opcReadData[9,0]
                self.writeSwitchData[7] = opcReadData[10,0]
                self.writeSwitchData[8] = opcReadData[11,0]
                self.writeSwitchData[9] = opcReadData[12,0]
                self.writeSwitchData[10] = opcReadData[13,0]
                self.writeSwitchData[11] = opcReadData[14,0]
                self.writeSwitchData[12] = opcReadData[15,0]
                self.writeSwitchData[13] = opcReadData[16,0]
                self.writeSwitchData[14] = opcReadData[17,0]
                self.writeSwitchData[15] = opcReadData[18,0]
                
                
                # Unset OSS 'set E-stop' only if E-stop button is released and OSS reset button is pressed:
                if self.eStopPressed == True and self.resetPressed == True: #E-stop switch is not pressed  and OSS reset is pressed
                    if self.reset == False:
                        self.reset = True
                        self.printMessage("OSS 'set E-stop' signals unset. Waiting for OCS E-stop reset.")
                        for i in range(NO_BEAMS):
                            for j in range(NO_ESTOPOUTPUTS):
                                self.outputStateData[0][i][j] = 0
                                self.outputStateData[1][i][j] = 0 
                                self.outputStateData[2][i][j] = 0 
                                self.oss.beams[i]['setEStops']  = self.outputStateData[1][i]
                else:
                    self.reset = False
                
                # Trigger E-stop command for all groups, and an E-stop output to E-stop for groups with not ignored setting
                if  self.eStopPressed == False:    
                    for i in range(NO_BEAMS):
                        for j in range(NO_ESTOPOUTPUTS):
                            self.outputStateData[0][i][j]   = 1
                            self.outputStateData[1][i][j]   = 1
                            self.outputStateData[2][i][j]   = 1
                           # self.lbcEStateData[i][j] = 1  # E-stop
                            self.oss.beams[i]['setEStops']  = self.outputStateData[1][i]
                
                # if E-stop button status has changed\, send E-stop message to LBC-F:
                if self.eStopPressed <> self.eStopPressedOld or self.resetPressed <> self.resetPressedOld:
                    self.oss.sendEStopMessage()
                self.eStopPressedOld = self.eStopPressed
                self.resetPressedOld = self.resetPressed
                
                # OSS communicates the E-stop status to the LBC-F (every update cycle):
                self.counter +=1
                if self.counter == 500:
                    self.oss.sendEStopMessage()
                    self.counter = 0 
              
                # run upload function when keyswitch is turned: 
                if self.upLoadPressed == True :
                    if self.uploaded == False:
                        print 'upload keyswitch turned!'
                        self.uploadButton_clicked()
                        self.uploaded = True
                else:
                    self.uploaded = False
                
                
                # write OPC status of button Warning lights: 
                writeData = [False,False,False,False,False,False,False]
                beamStates = []
                for i in range(NO_BEAMS):
                    beamState = sum(self.LbcOutputData[i])
                    beamStates.append(beamState)

                if any(items < NO_IGNOREFLAGS for items in beamStates):
                        writeData[0] = True
                        writeData[1] = False
                        writeData[2] = False
                        writeData[3] = False
                        #red light on
                else:
                        writeData[0] = False
                        writeData[1] = False
                        writeData[2] = False
                        writeData[3] = True
                        
                if any(items == 1 for items in self.lbcConnectionErrorPrinted):
                    writeData[1] = True
                    writeData[3] = False
                else:
                    writeData[1] = False
                        
                # Turn on upload config light when LBC-F config matches OSS config
                if self.ignoreFlagData[0] == self.ignoreFlagData[1] and self.activeFlagData[0] == self.activeFlagData[1] and self.eReactionData[0] == self.eReactionData[1]:
                    writeData[4] = True
                else:
                    writeData[4] = False   #uploadconfirm
                writeData[5] = True  #front bridge
                if self.reset == True:
                    self.resetCounter = 8
                    light = True
                    print 'reset resetCounter'
                elif self.resetCounter > 0:
                    self.resetCounter -=1
                    light = numpy.mod(self.resetCounter,2)
                    print light
                else:
                    light = True
                    #print 'light on'
                writeData[6] = light  #reset
                
                
                # Running light when when OPC connection is succesfully connected
                if self.startup == True and self.k<5:
                    self.writeData = writeData
                    
                    writeData = self.streetLight(writeData)
                else:
                    self.startup = False
                        
                # Write values to OPC server        
                self.opcW.Write(writeData)
      

          
        elif LOCAL_MODE == 1 or LOCAL_MODE == 3:
            # OSS communicates the E-stop status to the LBC-F (every update cycle):
            self.counter +=1
            if self.counter == 500:
                for i in range(NO_BEAMS):
                    self.oss.beams[i]['setEStops']  = self.outputStateData[1][i]
                self.oss.sendEStopMessage()
                self.counter = 0 
        
        
        
        else:
            self.startup = True
            self.k = 0
            
            
            

                    
            
#################################### HMI ####################################################
    
    def uploadButton_clicked(self): 
    
        
        if self.blockUpload == True and (LOCAL_MODE == 99):
            self.printMessage("ERROR: Enabled write switches do not match proposed HMI settings: no new config sent to LBC-F.")
        
        else:
            for i in range(NO_BEAMS):
                if self.writeSwitchData[i] == 1:
                    
                    
            # 1. Reply from OSS with OSS data equal to HMI data:
                    for k in range(len(self.outputStateData[1][i])):
                        self.outputStateData[1][i][k] = self.outputStateData[0][i][k]   
                        self.outputStateData[2][i][k] = self.outputStateData[0][i][k]   
#                        if self.outputStateData[2][i][k] == 1:
#                            self.lbcEStateData[i][k] = 1   # set LBC-F E-state
                    self.beamSafeData[1][i] = self.beamSafeData[0][i]   # only one item, no list!
                    for k in range(len(self.driveSafeData[1][i])):
                        self.driveSafeData[1][i][k] = self.driveSafeData[0][i][k]
                    for k in range(len(self.activeFlagData[1][i])):
                        self.activeFlagData[1][i][k] = self.activeFlagData[0][i][k]
                    for k in range(len(self.ignoreFlagData[1][i])):
                        self.ignoreFlagData[1][i][k] = self.ignoreFlagData[0][i][k]
                    for k in range(len(self.eReactionData[1][i])):
                        self.eReactionData[1][i][k] = self.eReactionData[0][i][k]                                
                    self.peopleInBeam[1][i] = self.peopleInBeam[0][i]
                            
                            
            # 2. send all HMI data to the OSS class, for UDP communication with the LBC-F
                    if LOCAL_MODE in [0,2,3]:
                        print 'update data beam %i' %i
                        self.oss.beams[i]['beamSafeData']               = self.beamSafeData[0][i]
                        self.oss.beams[i]['driveSafeData']              = self.driveSafeData[0][i]
                        self.oss.beams[i]['activeFlagData']             = self.activeFlagData[1][i]
                        for j in range(NO_IGNOREFLAGS):
                            self.oss.beams[i]['setSubsystemIgnoreFlags'][j]    = self.ignoreFlagData[1][i][j]    
                        self.oss.beams[i]['setEStops']                  = self.outputStateData[1][i]
                        self.oss.beams[i]['xLockingConfiguration']      = self.eReactionData[1][i][0]
                        self.oss.beams[i]['yDriveConfiguration']        = self.eReactionData[1][i][1]
                        self.oss.beams[i]['AHCConfiguration']           = self.eReactionData[1][i][2]
                        self.oss.beams[i]['yDriveDelay']                = self.eReactionData[1][i][3]
                    else:
                        pass
                    
                    
                    
            # 3. OSS communicates the configuration data to the LBC-F:
            if LOCAL_MODE == 0 or LOCAL_MODE == 2 or LOCAL_MODE == 3:
                self.oss.sendCompleteMessage(self.writeSwitchData)
                self.oss.sendEStopMessage()
            elif LOCAL_MODE == 1:
                self.oss.sendCompleteMessage(self.writeSwitchData)

                for i in range(NO_BEAMS):    
                    for k in range(len(self.activeFlagData[1][i])):
                        self.activeFlagData[2][i][k] = self.activeFlagData[1][i][k]
                    for k in range(len(self.ignoreFlagData[1][i])):
                        self.ignoreFlagData[2][i][k] = self.ignoreFlagData[1][i][k]
                    for k in range(len(self.eReactionData[1][i])):
                        self.eReactionData[2][i][k] = self.eReactionData[1][i][k]                 
                    for k in range(len(self.outputStateData[1][i])):     # set output to true if ignore is false and set is high
                        if self.ignoreFlagData[1][i][k] == 0 and self.outputStateData[1][i][k] == 1:                    
                            self.LbcOutputData[i][k] = 0
                            
            
            # 4. Print succes message
            self.printMessage("New configuration uploaded to beam(s).")
            
#################################### RUN IN LOCAL MDOE (NO OPC, NO UDP) ####################################################            

    def pushUpload_clicked(self):
        self.uploadPressed = not self.uploadPressed
        if self.uploadPressed == True:
            self.pushUpload.setStyleSheet("QPushButton{\n"
                                                "color: black;\n"
                                                "border: 2px solid white;\n"
                                                "border-radius: 2px;\n"
                                                "background-color:white;\n"
                                                "}")
            self.uploadButton_clicked()
            
            self.pushUpload.setStyleSheet(STYLEWRITE)
            self.uploadPressed = False
            
        else:
            self.pushUpload.setStyleSheet(STYLEWRITE)
                                                

    def pushEStop_clicked(self):
        self.eStopPressed = not self.eStopPressed
        if self.eStopPressed == True:
            self.pushEStop.setStyleSheet("QPushButton{\n"
                                                "color: white;\n"
                                                "border: 2px solid white;\n"
                                                "border-radius: 2px;\n"
                                                "background-color:red;\n"
                                                "}")
            for i in range(NO_BEAMS):
                        for j in range(NO_ESTOPOUTPUTS):
                            self.outputStateData[2][i][j] = 1   # ALL E_STOP COMMANDS TO E-STOP
                            self.outputStateData[1][i][j] = 1   # ALL E_STOP COMMANDS TO E-STOP
                            self.outputStateData[0][i][j] = 1
                            self.lbcEStateData[i][j] = 1  # E-stop
                            
                            if LOCAL_MODE == 1:  # only when not connected to LBC-F:
                                if self.ignoreFlagData[1][i][j] == False:
                                    self.LbcOutputData[i][j] = 0  # DE-ENERGIZE OUTPUTS WITH NOT IGNORED
                                
        else:
            self.pushEStop.setStyleSheet(STYLEWRITE)
            
    
    def pushReset_clicked(self):
        # Reset E-stop only if E-stop button is released:
        self.resetPressed = not self.resetPressed

        if self.eStopPressed == False and self.resetPressed == True: #E-stop switch is not pressed
            for i in range(NO_BEAMS):
                self.outputStateData[2][i] = [0,0,0,0,0,0,0,0,0,0,0,0,0]                    
                self.outputStateData[1][i] = [0,0,0,0,0,0,0,0,0,0,0,0,0]   
                self.outputStateData[0][i] = [0,0,0,0,0,0,0,0,0,0,0,0,0] 
            print self.outputStateData
            self.printMessage("OSS reset: OSS stopped sending E-stop signal to LBC-F's.")
            
        
        self.resetPressed = False

    def pushBeamEnable_clicked(self): 
        self.beamEnable = not self.beamEnable
        if self.beamEnable == True:
            self.pushBeamEnable.setStyleSheet(STYLELBCOSSWRITE)
            self.writeSwitchData = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        else:
            self.pushBeamEnable.setStyleSheet(STYLEWRITE)
            self.writeSwitchData = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


    def pushResetOCS_clicked(self):
        # Reset E-stop only if E-stop button is released:
        self.resetPressedOcs = not self.resetPressedOcs

        if self.eStopPressed == False and self.resetPressedOcs == True: #E-stop switch is not pressed
            for i in range(NO_BEAMS):
                for k in range(NO_ESTOPOUTPUTS):
                    if self.outputStateData[1][i][k] == 0:
                        self.LbcOutputData[i][k] = 1
                        self.lbcEStateData[i][k] = 0  # no E-stop
                        self.printMessage("OCS reset: E-stop output group on Beam " + str(i) + " are re-energized.")
            
        
        self.resetPressedOcs = False



    def configButton_clicked(self):
        print 'clicked config button'
        self.topWidget.show()
        self.topWidgetDisplayed = True
        self.topWidget.setCurrentIndex(1)

        styleOff = STYLEWRITE
        styleOffDashed = STYLEWRITEDASHED
        styleOn = STYLELBCOSSWRITE
        
        beamButtonIdx = [5,12,19,26,33,40,47,54,1,8,15,22,29,36,43,50]
        button = self.vesselLayout.sender()
        children = self.vesselWidget.findChildren(QtWidgets.QPushButton)
        
        if self.topWidgetDisplayed == True:
            for i in range(NO_BEAMS):   # all 16 beam buttons to grey or black background
                if ACTIVE_BEAMS[i] == 1:            
                    children[beamButtonIdx[i]].setStyleSheet(styleOff)
                else:
                    children[beamButtonIdx[i]].setStyleSheet(styleOffDashed)
                self.overViewButton.setStyleSheet(styleOff)
                self.warningButton.setStyleSheet(styleOff)
                self.networkButton.setStyleSheet(styleOff)
                button.setStyleSheet(styleOn)

    def fluButton_clicked(self):
        print 'clicked FLU button'
        self.topWidget.show()
        self.topWidgetDisplayed = True
        self.topWidget.setCurrentIndex(2)

        styleOff = STYLEWRITE
        styleOffDashed = STYLEWRITEDASHED
        styleOn = STYLELBCOSSWRITE

        beamButtonIdx = [5, 12, 19, 26, 33, 40, 47, 54, 1, 8, 15, 22, 29, 36, 43, 50]
        button = self.vesselLayout.sender()
        children = self.vesselWidget.findChildren(QtWidgets.QPushButton)

        if self.topWidgetDisplayed == True:
            for i in range(NO_BEAMS):  # all 16 beam buttons to grey or black background
                if ACTIVE_BEAMS[i] == 1:
                    children[beamButtonIdx[i]].setStyleSheet(styleOff)
                else:
                    children[beamButtonIdx[i]].setStyleSheet(styleOffDashed)
                self.overViewButton.setStyleSheet(styleOff)
                self.warningButton.setStyleSheet(styleOff)
                self.networkButton.setStyleSheet(styleOff)
                button.setStyleSheet(styleOn)

    def warningButton_clicked(self):
        print 'clicked warning button'
        self.topWidget.show()
        self.topWidgetDisplayed = True
        self.topWidget.setCurrentIndex(3)

        styleOff = STYLEWRITE
        styleOffDashed = STYLEWRITEDASHED
        styleOn = STYLELBCOSSWRITE
        
        beamButtonIdx = [5,12,19,26,33,40,47,54,1,8,15,22,29,36,43,50]
        button = self.vesselLayout.sender()
        children = self.vesselWidget.findChildren(QtWidgets.QPushButton)
        
        if self.topWidgetDisplayed == True:
            for i in range(NO_BEAMS):   # all 16 beam buttons to grey or black background
                if ACTIVE_BEAMS[i] == 1:            
                    children[beamButtonIdx[i]].setStyleSheet(styleOff)
                else:
                    children[beamButtonIdx[i]].setStyleSheet(styleOffDashed)
                self.overViewButton.setStyleSheet(styleOff)
                # self.fluConfigButton.setStyleSheet(styleOff)
                self.networkButton.setStyleSheet(styleOff)
                button.setStyleSheet(styleOn) 
     
    def networkButton_clicked(self):
        print 'clicked network button'
        self.topWidget.show()
        self.topWidgetDisplayed = True
        self.topWidget.setCurrentIndex(4)

        styleOff = STYLEWRITE
        styleOffDashed = STYLEWRITEDASHED
        styleOn = STYLELBCOSSWRITE
        
        beamButtonIdx = [5,12,19,26,33,40,47,54,1,8,15,22,29,36,43,50]
        button = self.vesselLayout.sender()
        children = self.vesselWidget.findChildren(QtWidgets.QPushButton)
        
        if self.topWidgetDisplayed == True:
            for i in range(NO_BEAMS):   # all 16 beam buttons to grey or black background
                if ACTIVE_BEAMS[i] == 1:            
                    children[beamButtonIdx[i]].setStyleSheet(styleOff)
                else:
                    children[beamButtonIdx[i]].setStyleSheet(styleOffDashed)
                self.overViewButton.setStyleSheet(styleOff)
                #self.fluConfigButton.setStyleSheet(styleOff)
                self.warningButton.setStyleSheet(styleOff)
                button.setStyleSheet(styleOn) 

    def sifButton_clicked(self):
        print 'clicked SIF button'
        self.topWidget.show()
        self.topWidgetDisplayed = True
        self.topWidget.setCurrentIndex(5)

        styleOff = STYLEWRITE
        styleOffDashed = STYLEWRITEDASHED
        styleOn = STYLELBCOSSWRITE

        beamButtonIdx = [5, 12, 19, 26, 33, 40, 47, 54, 1, 8, 15, 22, 29, 36, 43, 50]
        button = self.vesselLayout.sender()
        children = self.vesselWidget.findChildren(QtWidgets.QPushButton)

        if self.topWidgetDisplayed == True:
            for i in range(NO_BEAMS):  # all 16 beam buttons to grey or black background
                if ACTIVE_BEAMS[i] == 1:
                    children[beamButtonIdx[i]].setStyleSheet(styleOff)
                else:
                    children[beamButtonIdx[i]].setStyleSheet(styleOffDashed)
                self.overViewButton.setStyleSheet(styleOff)
                self.warningButton.setStyleSheet(styleOff)
                self.networkButton.setStyleSheet(styleOff)
                button.setStyleSheet(styleOn)


    def vesselButtons_clicked(self):
        print('clicked beam selection buttons' )
        self.topWidgetDispayed = False;
        self.topWidget.hide()
        
        styleOff = STYLEWRITE
        styleOffDashed = STYLEWRITEDASHED
        styleOn = STYLELBCOSSWRITE
        
        beamButtonIdx = [5,12,19,26,33,40,47,54,1,8,15,22,29,36,43,50]
        button = self.vesselLayout.sender()
        children = self.vesselWidget.findChildren(QtWidgets.QPushButton)
        for i in range(NO_BEAMS):   # all 16 beam buttons to grey or black background
            if ACTIVE_BEAMS[i] == 1:            
                children[beamButtonIdx[i]].setStyleSheet(styleOff)
            else:
                children[beamButtonIdx[i]].setStyleSheet(styleOffDashed)
            # self.fluConfigButton.setStyleSheet(styleOff)
            self.overViewButton.setStyleSheet(styleOff)
            self.warningButton.setStyleSheet(styleOff)
            self.networkButton.setStyleSheet(styleOff)
            button.setStyleSheet(styleOn)
        idx = button.text()
        if idx[0] == 'S':
            self.stackedWidget.setCurrentIndex(int(idx[1])-1);   
            print "Selected beam: ",int(idx[1])
        elif idx[0] == 'P':
            self.stackedWidget.setCurrentIndex(int(idx[1])+8-1);
            print "Selected beam: ",int(idx[1])+8

    def overviewButton_clicked(self):
        print('clicked overview button' )
        self.topWidget.show()
        self.topWidgetDisplayed = True
        self.topWidget.setCurrentIndex(0)

        styleOff = STYLEWRITE
        styleOffDashed = STYLEWRITEDASHED
        styleOn = STYLELBCOSSWRITE
        
        beamButtonIdx = [5,12,19,26,33,40,47,54,1,8,15,22,29,36,43,50]
        button = self.vesselLayout.sender()
        children = self.vesselWidget.findChildren(QtWidgets.QPushButton)
        
        if self.topWidgetDisplayed == True:
            for i in range(NO_BEAMS):   # all 16 beam buttons to grey or black background
                if ACTIVE_BEAMS[i] == 1:            
                    children[beamButtonIdx[i]].setStyleSheet(styleOff)
                else:
                    children[beamButtonIdx[i]].setStyleSheet(styleOffDashed)
#                self.fluConfigButton.setStyleSheet(styleOff)
                self.warningButton.setStyleSheet(styleOff)
                self.networkButton.setStyleSheet(styleOff)
                button.setStyleSheet(styleOn)
            
                    
    def FLU_clicked(self):

        children = self.configWidget.findChildren(QtWidgets.QComboBox)
        button = self.configWidget.sender()
        val = button.currentIndex()  # aimed for FLU number
        print "Val is:", val
        #print len(children)
        print 'clicked FLU config button'
        for k in range(NO_BEAMS):
            if k<8:
                kk = k*2+1  # button index
            elif k>=8:
                kk = (k-8)*2    # button index
                
            if button == children[kk]:  # if button is beam no. k and writeswitch k is True ...
                print "kk is:", kk
                self.FLU[k] = val  # set FLU config of beam k to the selected dropdown value
                #print self.FLU

         
    def peopleInBeamButtons_clicked(self):    
        [beamID,beamIDs, writeSwitchDataFlu] = self.sub_findFluBeams()  # get all beams and their writeswitchdata in the FLU

        if any(items == False for items in writeSwitchDataFlu)  :
                self.printMessage("ERROR: Changes not applied. Enable beam write switch to change value.")
        else:
            for i in beamIDs:   
                    print('clicked people-in-beam button of beam ' + str(i) )
                    index = self.peopleInBeamLayouts[beamID].indexOf(self.peopleInBeamLayouts[beamID].sender())
                    row, column, cols, rows = self.peopleInBeamLayouts[i].getItemPosition(index)
                    #print row, column,i   # row, clumn, beam no.        
                    self.peopleInBeam[0][beamID] = row   # 0 = people in beam, 1 = no people, 2  = custom
                    #print self.peopleInBeam
                    if self.peopleInBeam[0][beamID]== 0:
                        self.activeFlagData[0][beamID] = [1 for i in range(NO_ACTIVEFLAGS)]  # set all flags to active
                        self.activeFlagData[0][beamID][18] = self.activeFlagData[1][beamID][18]  # do not change OSS Comm timeout
                    elif self.peopleInBeam[0][beamID] == 1:
                        self.activeFlagData[0][beamID] = [0 for i in range(NO_ACTIVEFLAGS)]  # set all flags to not active
                        self.activeFlagData[0][beamID][18] = self.activeFlagData[1][beamID][18]  # do not change OSS Comm timeout
                    
                        
    def beamSafeButtons_clicked(self):
        [beamID,beamIDs, writeSwitchDataFlu] = self.sub_findFluBeams()  # get all beams and their writeswitchdata in the FLU

        if any(items == False for items in writeSwitchDataFlu)  :
                self.printMessage("ERROR: Changes not applied. Enable beam write switch to change value.")
        else:
            for i in beamIDs:   
                    print('clicked beam safe mode button ' + str(i) )
                    index = self.beamSafeLayouts[beamID].indexOf(self.beamSafeLayouts[beamID].sender())
                    row, column, cols, rows = self.beamSafeLayouts[i].getItemPosition(index)
                    #print row, column,i   # row, clumn, beam no.        
                    self.beamSafeData[0][i] = row
                    
                    # Beam safe mode results in changed Drive Safe Modes:
                    self.sub_changeBeamSafeMode(i,row)
                    # Drive safe mode result in changed ignore and reaction settings:
                    self.sub_changeDriveSafeModes(i,self.driveSafeData[0][i][0],self.driveSafeData[0][i][1],self.driveSafeData[0][i][2]) 

    
    def driveSafeButtons_clicked(self):
        [beamID,beamIDs, writeSwitchDataFlu] = self.sub_findFluBeams()  # get all beams and their writeswitchdata in the FLU

        if any(items == False for items in writeSwitchDataFlu)  :
                self.printMessage("ERROR: Changes not applied. Enable beam write switch to change value.")
        else: 
            for i in beamIDs:
                print('clicked drive safe mode buttons' )
                index = self.driveSafeLayouts[beamID].indexOf(self.driveSafeLayouts[beamID].sender())
                row, column, cols, rows = self.driveSafeLayouts[i].getItemPosition(index)
      
                if column == 0 and row in [1,2,7,8]:
                    self.driveSafeData[0][i][column] = row-1
                elif column == 1 and row in [1,2,3,4,7,8]:
                    self.driveSafeData[0][i][column] = row-1
                elif column == 2 and row in [1,2,7,8]:
                    self.driveSafeData[0][i][column] = row-1
                           
                # Beam safe mode goes to custom
                self.beamSafeData[0][i] = NO_BEAMSAFEMODES-1  #assuming CUSTOM is last element in BEAMSAFEMODES
        
                # Drive safe mode result in changed ignore and reaction settings:
                self.sub_changeDriveSafeModes(i,self.driveSafeData[0][i][0],self.driveSafeData[0][i][1],self.driveSafeData[0][i][2])  
                
            
    def sub_findFluBeams(self):
        # find other beams in this FLU:
        beamID = self.stackedWidget.currentIndex()          # Current activated beam number
        beamIDs = []
        beamIDs = [self.stackedWidget.currentIndex()]
        
        writeSwitchDataFlu = [ self.writeSwitchData[i] for i in beamIDs] # get all writeswitchdata values in the FLU
        
        return [beamID,beamIDs,writeSwitchDataFlu]
        
   
    def sub_changeBeamSafeMode(self,beamNumber,beamSafeMode):   #sub-function
        if not beamSafeMode == NO_BEAMSAFEMODES-1:        
            xDriveSafeMode = XDRIVEMAPPING[beamSafeMode]
            yDriveSafeMode = YDRIVEMAPPING[beamSafeMode]
            zDriveSafeMode = ZDRIVEMAPPING[beamSafeMode]

            self.driveSafeData[0][beamNumber][0] = xDriveSafeMode
            self.driveSafeData[0][beamNumber][1] = yDriveSafeMode
            self.driveSafeData[0][beamNumber][2] = zDriveSafeMode
                    
            self.sub_changeDriveSafeModes(beamNumber,xDriveSafeMode, yDriveSafeMode, zDriveSafeMode)
            
            self.ignoreFlagData[0][beamNumber][12] = 0   # E-stop other beam         
            
        else:
            self.driveSafeData[0][beamNumber][0] = NO_DRIVESAFEMODES-1
            self.driveSafeData[0][beamNumber][1] = NO_DRIVESAFEMODES-1
            self.driveSafeData[0][beamNumber][2] = NO_DRIVESAFEMODES-1
    

    
    def sub_changeDriveSafeModes(self, beamNumber, xDriveSafeMode, yDriveSafeMode, zDriveSafeMode):   #sub-function
        if not xDriveSafeMode == (NO_DRIVESAFEMODES-1):        
            if xDriveSafeMode == 0:
                self.ignoreFlagData[0][beamNumber][0] = 1   # afe XY
                self.ignoreFlagData[0][beamNumber][11] = 0   # x-drive motors
                self.ignoreFlagData[0][beamNumber][10] = 0   # x-locking
                self.eReactionData[0][beamNumber][0] = 1             # x-locking E-reaction

            elif xDriveSafeMode == 1:
                self.ignoreFlagData[0][beamNumber][0] = 0   # afe XY
                self.ignoreFlagData[0][beamNumber][11] = 1   # x-drive motors
                self.ignoreFlagData[0][beamNumber][10] = 0   # x-locking
                self.eReactionData[0][beamNumber][0] = 0             # x-locking E-reaction

            elif xDriveSafeMode == 6:
                self.ignoreFlagData[0][beamNumber][0] = 1   # afe XY
                self.ignoreFlagData[0][beamNumber][11] = 1   # x-drive motors
                self.ignoreFlagData[0][beamNumber][10] = 1   # x-locking
                
                self.eReactionData[0][beamNumber][0] = 1  # TODO: add a check for the initial condition of the x-locking

        if not yDriveSafeMode == (NO_DRIVESAFEMODES-1): 
            if yDriveSafeMode == 0:  # brake and lock
                self.ignoreFlagData[0][beamNumber][5] = 0   # rack lock 
                self.ignoreFlagData[0][beamNumber][3] = 0   # Y hydraulic
                if self.ignoreFlagData[0][beamNumber][0] == 1:
                    self.ignoreFlagData[0][beamNumber][7] = 0   # y-drive motors
                else:
                    self.ignoreFlagData[0][beamNumber][7] = 1   # y-drive motors      
                self.ignoreFlagData[0][beamNumber][6] = 0   # y-brakes
                self.ignoreFlagData[0][beamNumber][8] = 0   # pin lock
                if yDriveSafeMode == 6 or zDriveSafeMode == 6:
                    self.ignoreFlagData[0][beamNumber][1] = 1   # LHPU
                else:
                    self.ignoreFlagData[0][beamNumber][1] = 0   # LHPU
                    
                self.eReactionData[0][beamNumber][1] = 0             # y-hydraulic reaction
                if self.ignoreFlagData[0][beamNumber][0] == 1:
                    self.eReactionData[0][beamNumber][3] = 9.9            # y brake delay
                else:
                    self.eReactionData[0][beamNumber][3] = 0.0            # y brake delay

            elif yDriveSafeMode == 1:   # freewheel
                self.ignoreFlagData[0][beamNumber][5] = 0   # rack lock 
                self.ignoreFlagData[0][beamNumber][3] = 0   # Y hydraulic
                if self.ignoreFlagData[0][beamNumber][0] == 1:
                    self.ignoreFlagData[0][beamNumber][7] = 0   # y-drive motors
                else:
                    self.ignoreFlagData[0][beamNumber][7] = 1   # y-drive motors      
                self.ignoreFlagData[0][beamNumber][6] = 0   # y-brakes
                self.ignoreFlagData[0][beamNumber][8] = 0   # pin lock
                if yDriveSafeMode == 6 or zDriveSafeMode == 6:
                    self.ignoreFlagData[0][beamNumber][1] = 1   # LHPU
                else:
                    self.ignoreFlagData[0][beamNumber][1] = 0   # LHPU
                    
                self.eReactionData[0][beamNumber][1] = 2             # y-hydraulic reaction
                if self.ignoreFlagData[0][beamNumber][0] == 1:
                    self.eReactionData[0][beamNumber][3] = 9.9            # y brake delay
                else:
                    self.eReactionData[0][beamNumber][3] = 0.0            # y brake delay

            elif yDriveSafeMode == 2:  #freewheel+, lock-
                self.ignoreFlagData[0][beamNumber][5] = 0   # rack lock 
                self.ignoreFlagData[0][beamNumber][3] = 0   # Y hydraulic
                if self.ignoreFlagData[0][beamNumber][0] == 1:
                    self.ignoreFlagData[0][beamNumber][7] = 0   # y-drive motors
                else:
                    self.ignoreFlagData[0][beamNumber][7] = 1   # y-drive motors      
                self.ignoreFlagData[0][beamNumber][6] = 0   # y-brakes
                self.ignoreFlagData[0][beamNumber][8] = 0   # pin lock
                if yDriveSafeMode == 6 or zDriveSafeMode == 6:
                    self.ignoreFlagData[0][beamNumber][1] = 1   # LHPU
                else:
                    self.ignoreFlagData[0][beamNumber][1] = 0   # LHPU
                    
                self.eReactionData[0][beamNumber][1] = 1             # y-hydraulic reaction
                if self.ignoreFlagData[0][beamNumber][0] == 1:
                    self.eReactionData[0][beamNumber][3] = 9.9            # y brake delay
                else:
                    self.eReactionData[0][beamNumber][3] = 0.0            # y brake delay
                
            elif yDriveSafeMode == 3:   #freewheel-,lock+
                self.ignoreFlagData[0][beamNumber][5] = 0   # rack lock 
                self.ignoreFlagData[0][beamNumber][3] = 0   # Y hydraulic
                if self.ignoreFlagData[0][beamNumber][0] == 1:
                    self.ignoreFlagData[0][beamNumber][7] = 0   # y-drive motors
                else:
                    self.ignoreFlagData[0][beamNumber][7] = 1   # y-drive motors      
                self.ignoreFlagData[0][beamNumber][6] = 0   # y-brakes
                self.ignoreFlagData[0][beamNumber][8] = 0   # pin lock
                if yDriveSafeMode == 6 or zDriveSafeMode == 6:
                    self.ignoreFlagData[0][beamNumber][1] = 1   # LHPU
                else:
                    self.ignoreFlagData[0][beamNumber][1] = 0   # LHPU
                    
                self.eReactionData[0][beamNumber][1] = 3             # y-hydraulic reaction
                if self.ignoreFlagData[0][beamNumber][0] == 1:
                    self.eReactionData[0][beamNumber][3] = 9.9            # y brake delay
                else:
                    self.eReactionData[0][beamNumber][3] = 0.0            # y brake delay

            elif yDriveSafeMode == 6:   #maintain
                self.ignoreFlagData[0][beamNumber][3] = 1   # Y hydraulic
                if self.ignoreFlagData[0][beamNumber][0] == 1:
                    self.ignoreFlagData[0][beamNumber][7] = 1   # y-drive motors
                else:
                    self.ignoreFlagData[0][beamNumber][7] = 1   # y-drive motors      
                self.ignoreFlagData[0][beamNumber][6] = 1   # y-brakes
                self.ignoreFlagData[0][beamNumber][8] = 1   # pin lock
                self.ignoreFlagData[0][beamNumber][5] = 1   # rack lock              
                if yDriveSafeMode == 6 or zDriveSafeMode == 6:
                    self.ignoreFlagData[0][beamNumber][1] = 1   # LHPU
                else:
                    self.ignoreFlagData[0][beamNumber][1] = 1   # LHPU
                    
        if not zDriveSafeMode == (NO_DRIVESAFEMODES-1):    
            if zDriveSafeMode == 1:  # AHC PAsSIVE FREE
                self.ignoreFlagData[0][beamNumber][2] = 0   # Z hydraulic
                if yDriveSafeMode == 6 or zDriveSafeMode == 6:
                    self.ignoreFlagData[0][beamNumber][1] = 1   # LHPU
                else:
                    self.ignoreFlagData[0][beamNumber][1] = 0   # LHPU
                self.ignoreFlagData[0][beamNumber][4] = 0   # Air comp
                self.ignoreFlagData[0][beamNumber][9] = 0   # Z-locking    
                self.eReactionData[0][beamNumber][2] = 0  # AHC reaction
               

            elif zDriveSafeMode == 0:   # AHC PASSIVE BLOCKED
                self.ignoreFlagData[0][beamNumber][2] = 0   # Z hydraulic
                if yDriveSafeMode == 6 or zDriveSafeMode == 6:
                    self.ignoreFlagData[0][beamNumber][1] = 1   # LHPU
                else:
                    self.ignoreFlagData[0][beamNumber][1] = 0   # LHPU
                self.ignoreFlagData[0][beamNumber][4] = 0   # Air comp
                self.ignoreFlagData[0][beamNumber][9] = 0   # Z-locking 
                self.eReactionData[0][beamNumber][2] = 1  # AHC reaction


        
            elif zDriveSafeMode == 6:   # MAINTAIN
                self.ignoreFlagData[0][beamNumber][2] = 1   # Z hydraulic
                if yDriveSafeMode == 6 or zDriveSafeMode == 6:
                    self.ignoreFlagData[0][beamNumber][1] = 1   # LHPU
                else:
                    self.ignoreFlagData[0][beamNumber][1] = 1   # LHPU
                self.ignoreFlagData[0][beamNumber][4] = 0   # Air comp
                self.ignoreFlagData[0][beamNumber][9] = 0   # Z-locking 
                self.eReactionData[0][beamNumber][2] = 0  # AHC reaction


           
    def activeButtons_clicked(self):
        [beamID,beamIDs, writeSwitchDataFlu] = self.sub_findFluBeams()  # get all beams and their writeswitchdata in the FLU

        if any(items == False for items in writeSwitchDataFlu)  :
            self.printMessage("ERROR: Changes not applied. Enable beam write switch to change value.")
                
        elif self.peopleInBeam[0][beamID] <> 2:   #  [2] = custom mode not preselected
            self.printMessage("ERROR: People-in-beam not set to 'CUSTOM', changes are blocked.")
            
        else:
            for i in beamIDs :
                if all(items == False for items in self.LbcInputData[i]):        # Only accept buttonclicks if write is enabled and no beam E-stop button is pressed
                    print('clicked active flag buttons' )
                    index = self.activeLayouts[beamID].indexOf(self.activeLayouts[beamID].sender())
                    row, column, cols, rows = self.activeLayouts[i].getItemPosition(index)
                    #print row, column,i   # row, column, beam no.
                    if column == 1:
                        self.activeFlagData[0][i][row] = 1
                        self.peopleInBeam[0][i] = 2   # people-in-beam to custom
                    elif column == 2:
                        self.activeFlagData[0][i][row] = 0
                        self.peopleInBeam[0][i] = 2   # people-in-beam to custom
                    #print self.activeFlagData[0][i]
                elif any(items == True for items in self.LbcInputData[i]):
                    self.printMessage("ERROR: Unlatch beam "+ str(i) + " E-stop button to change Active Flag values.")
            
        
        
    def ignoreButtons_clicked(self):
        [beamID,beamIDs, writeSwitchDataFlu] = self.sub_findFluBeams()  # get all beams and their writeswitchdata in the FLU

        if any(items == False for items in writeSwitchDataFlu)  :
                self.printMessage("ERROR: Changes not applied. Enable beam write switch to change value.")
        else:
            for i in beamIDs:
                print('clicked ignore flag buttons' )
                index = self.ignoreLayouts[beamID].indexOf(self.ignoreLayouts[beamID].sender())
                row, column, cols, rows = self.ignoreLayouts[i].getItemPosition(index)
                #print row, column, i   # row, column, beam no.
                if self.LbcOutputData[i][row] == False:
                    self.printMessage("ERROR: Beam " + str(i) + " safety output '" + labelTextIgnore[row] + "' in E-stop. Remove E-stop to change its Ignore Flag value.")
                else:
                    if column == 1:
                        self.ignoreFlagData[0][i][row] = 1
                    elif column == 2:
                        self.ignoreFlagData[0][i][row] = 0
                    #print self.ignoreFlagData[0][i]
                
                    # beam safe mode goes to custom
                    self.beamSafeData[0][i] = NO_BEAMSAFEMODES-1  #assuming CUSTOM is last element in BEAMSAFEMODES
                    # drive safe mode goes to custom
                    self.driveSafeData[0][i] = [NO_DRIVESAFEMODES-1,NO_DRIVESAFEMODES-1,NO_DRIVESAFEMODES-1]  #assuming CUSTOM is last element in DRIVESAFEMODES

            
            
            
    def eReactionButtons_clicked(self):
        [beamID,beamIDs, writeSwitchDataFlu] = self.sub_findFluBeams()  # get all beams and their writeswitchdata in the FLU

        if any(items == False for items in writeSwitchDataFlu)  :
                self.printMessage("ERROR: Changes not applied. Enable beam write switch to change value.")
        else:
            for i in beamIDs :
                print('clicked E-stop reaction configuration buttons' )
                index = self.estopReactionLayouts[beamID].indexOf(self.estopReactionLayouts[beamID].sender())
                row, column, cols, rows = self.estopReactionLayouts[i].getItemPosition(index)
                #print row, column, i   # row, clumn, beam no.
                if column == 1 and row == 0:
                    self.eReactionData[0][i][0] = 1
                elif column == 2 and row == 0:
                    self.eReactionData[0][i][0] = 0
                elif column == 1 and row == 1:
                    self.eReactionData[0][i][1] = 0    
                elif column == 2 and row == 1:
                    self.eReactionData[0][i][1] = 1     
                elif column == 1 and row == 2:
                    self.eReactionData[0][i][1] = 2    
                elif column == 2 and row == 2:
                    self.eReactionData[0][i][1] = 3    
                elif column == 1 and row == 3:
                    self.eReactionData[0][i][2] = 1    
                elif column == 2 and row == 3:
                    self.eReactionData[0][i][2] = 0        
                #print self.eReactionData[0][i]
                #print self.eReactionData[1][i]
                
                # beam safe mode goes to custom
                self.beamSafeData[0][i] = NO_BEAMSAFEMODES-1  #assuming CUSTOM is last element in BEAMSAFEMODES
                # drive safe mode goes to custom
                self.driveSafeData[0][i] = [NO_DRIVESAFEMODES-1,NO_DRIVESAFEMODES-1,NO_DRIVESAFEMODES-1]  #assuming CUSTOM is last element in DRIVESAFEMODES
 

    
    def yBrake_clicked(self, val): # new value is passed as an argument
        [beamID,beamIDs, writeSwitchDataFlu] = self.sub_findFluBeams()  # get all beams and their writeswitchdata in the FLU

        if any(items == False for items in writeSwitchDataFlu)  :
            self.printMessage("ERROR: Changes not applied. Enable beam write switch to change value.")
            for i in beamIDs:
                child = self.groupBoxesEstopReaction[i].findChildren(QtWidgets.QDoubleSpinBox)
                child[0].setValue(self.eReactionData[0][i][3])
                       
        else:
            for i in beamIDs:
                print('Y brake delay adjusted' )
                self.eReactionData[0][i][3] = val
                child = self.groupBoxesEstopReaction[i].findChildren(QtWidgets.QDoubleSpinBox)
                child[0].setValue(self.eReactionData[0][i][3])
              #  print self.eReactionData[0][i]   


            
    def outputButtons_clicked(self):
        [beamID,beamIDs, writeSwitchDataFlu] = self.sub_findFluBeams()  # get all beams and their writeswitchdata in the FLU

        if any(items == False for items in writeSwitchDataFlu)  :
                self.printMessage("ERROR: Changes not applied. Enable beam write switch to change value.")
        else:
            for i in beamIDs:
                print('clicked output state buttons' )
                index = self.outputLayouts[beamID].indexOf(self.outputLayouts[beamID].sender())
                row, column, cols, rows = self.outputLayouts[i].getItemPosition(index)
                #print row, column, i   # row, clumn, beam no.
                if column == 0:
                    self.outputStateData[0][i][row] = 1
                elif column == 1:
                    self.outputStateData[0][i][row] = 0

            #    print self.outputStateData[0]
             #   print self.outputStateData[1]
                
                # beam safe mode goes to custom
                self.beamSafeData[0][i] = NO_BEAMSAFEMODES-1  #assuming CUSTOM is last element in BEAMSAFEMODES
                # drive safe mode goes to custom
                self.driveSafeData[0][i] = [NO_DRIVESAFEMODES-1,NO_DRIVESAFEMODES-1,NO_DRIVESAFEMODES-1]  #assuming CUSTOM is last element in DRIVESAFEMODES


    def beamCheckButtons_clicked(self):
        print("beam check button clicked!")
        button = self.beamCheckLayouts.sender()
        index = self.beamCheckLayouts.indexOf(button)
        row, column, cols, rows = self.beamCheckLayouts.getItemPosition(index)
        #print row, column,i   # row, column, beam no.
        if column == 1:
            self.beamsToBeChecked[row+8] = not self.beamsToBeChecked[row+8]
            if self.beamsToBeChecked[row+8] == True:
                button.setStyleSheet(STYLELBCOSSWRITE) 
            else:
                button.setStyleSheet(STYLEWRITE) 
                      
        elif column == 2:
            self.beamsToBeChecked[row] = not self.beamsToBeChecked[row]
            if self.beamsToBeChecked[row] == True:
                button.setStyleSheet(STYLELBCOSSWRITE) 
            else:
                button.setStyleSheet(STYLEWRITE)
 

               
    def updateOutputButtons(self):          
    # Update the HMI for the current (active) page:
        k = self.stackedWidget.currentIndex()   # Currentlt activated beam number
        
        outputStateDataHMI = self.outputStateData[0][k]
        outputStateDataOSS = self.outputStateData[1][k]
        outputStateDataLBC = self.outputStateData[2][k]
        
        if self.writeSwitchData[k] == 0:      
            styleOSS            = STYLEOSSNOWRITE  # write enabled, set in LBC, not in OSS
            styleHMI            = STYLEHMINOWRITE # write enabled, set in OSS, not in LBC
            styleLBC            = STYLELBCNOWRITE  # write enabled, set in LBC, noting set by OSS/HMI
            styleLBCmatchesOSS  = STYLELBCOSSNOWRITE   # write enabled, set in LBC and OSS
            styleLBCmatchesHMI  = STYLELBCHMINOWRITE   # write enabled, set in LBC and HMI
            style               = STYLENOWRITE
            
        else:
            styleOSS            = STYLEOSSWRITE  # write enabled, set in LBC, not in OSS
            styleHMI            = STYLEHMIWRITE # write enabled, set in OSS, not in LBC
            styleLBC            = STYLELBCWRITE  # write enabled, set in LBC, noting set by OSS/HMI
            styleLBCmatchesOSS  = STYLELBCOSSWRITE   # write enabled, set in LBC and OSS
            styleLBCmatchesHMI  = STYLELBCHMIWRITE   # write enabled, set in LBC and HMI
            style               = STYLEWRITE  
        
        for i in range(len(outputStateDataHMI)): 
            child = self.groupBoxesOutput[k].findChildren(QtWidgets.QPushButton)   
            child[2*i].setStyleSheet(style)
            child[2*i+1].setStyleSheet(style)
            if outputStateDataHMI[i] == 1 :
                child[2*i].setStyleSheet(styleHMI)
            elif outputStateDataHMI[i] == 0:      
                child[2*i+1].setStyleSheet(styleHMI)
            if outputStateDataOSS[i] == 1 :
                child[2*i].setStyleSheet(styleOSS)
            elif outputStateDataOSS[i] == 0:      
                child[2*i+1].setStyleSheet(styleOSS)
            if outputStateDataLBC[i] == 1 :
                child[2*i].setStyleSheet(styleLBC)
            elif outputStateDataLBC[i] == 0:      
                child[2*i+1].setStyleSheet(styleLBC)
            if outputStateDataLBC[i] == 1 and outputStateDataHMI[i] == 1 :
                child[2*i].setStyleSheet(styleLBCmatchesHMI)
            elif outputStateDataLBC[i] == 0 and outputStateDataHMI[i] == 0 :      
                child[2*i+1].setStyleSheet(styleLBCmatchesHMI)
            if outputStateDataOSS[i] == 1 and outputStateDataLBC[i] == 1 :
                child[2*i].setStyleSheet(styleLBCmatchesOSS)
            elif outputStateDataOSS[i] == 0 and outputStateDataLBC[i] == 0 :      
                child[2*i+1].setStyleSheet(styleLBCmatchesOSS)



    def updateBeamSafeButtons(self):          
    # Update the HMI for the current (active) page:
        k = self.stackedWidget.currentIndex()   # Currentlt activated beam number
      
        beamSafeModeHMI = self.beamSafeData[0][k];
        beamSafeModeOSS = self.beamSafeData[1][k];
               
        if self.writeSwitchData[k] == 0:      
            styleOSS = STYLEOSSNOWRITE
            styleHMI = STYLEHMINOWRITE
            styleHMIOSS = STYLELBCOSSNOWRITE
            style = STYLENOWRITE
            
        else:
            styleOSS = STYLEOSSWRITE
            styleHMI = STYLEHMIWRITE
            styleHMIOSS = STYLELBCOSSWRITE
            style = STYLEWRITE  
                         

        child = self.groupBoxesBeamSafe[k].findChildren(QtWidgets.QPushButton)
        for i in range(NO_BEAMSAFEMODES):
            child[i].setStyleSheet(style)               
            if i == beamSafeModeHMI:
                child[beamSafeModeHMI].setStyleSheet(styleHMI)
            if i == beamSafeModeOSS:
                child[beamSafeModeOSS].setStyleSheet(styleOSS)
            if i == beamSafeModeOSS and i == beamSafeModeHMI:
                child[beamSafeModeOSS].setStyleSheet(styleHMIOSS)

                
    def updatePeopleInBeamButtons(self):          
    # Update the HMI for the current (active) page:
        k = self.stackedWidget.currentIndex()   # Currentlt activated beam number
      
        peopleInBeamHMI = self.peopleInBeam[0][k]
        peopleInBeamOSS = self.peopleInBeam[1][k]
               
        if self.writeSwitchData[k] == 0:      
            styleOSS = STYLEOSSNOWRITE
            styleHMI = STYLEHMINOWRITE
            styleHMIOSS = STYLELBCOSSNOWRITE
            style = STYLENOWRITE
            
        else:
            styleOSS = STYLEOSSWRITE
            styleHMI = STYLEHMIWRITE
            styleHMIOSS = STYLELBCOSSWRITE
            style = STYLEWRITE  
                         

        child = self.groupBoxesPeopleInBeam[k].findChildren(QtWidgets.QPushButton)
        for i in range(3):
            child[i].setStyleSheet(style)       
            if peopleInBeamHMI == i :
                child[peopleInBeamHMI].setStyleSheet(styleHMI)
            if peopleInBeamOSS == i:
                child[peopleInBeamOSS].setStyleSheet(styleOSS) 
            if peopleInBeamOSS == i and peopleInBeamHMI == i:
                child[peopleInBeamOSS].setStyleSheet(styleHMIOSS) 

    def updateDriveSafeButtons(self):  
    # Update the HMI for the current (active) page:
        k = self.stackedWidget.currentIndex()   # Currentlt activated beam number
            
        driveSafeModeXHMI = self.driveSafeData[0][k][0]
        driveSafeModeYHMI = self.driveSafeData[0][k][1]
        driveSafeModeZHMI = self.driveSafeData[0][k][2]
        
        driveSafeModeXOSS = self.driveSafeData[1][k][0]
        driveSafeModeYOSS = self.driveSafeData[1][k][1]
        driveSafeModeZOSS = self.driveSafeData[1][k][2]
   
        if self.writeSwitchData[k] == 0:      
            styleOSS = STYLEOSSNOWRITE
            styleHMI = STYLEHMINOWRITE
            styleHMIOSS = STYLELBCOSSNOWRITE
            style = STYLENOWRITE
            
        else:
            styleOSS = STYLEOSSWRITE
            styleHMI = STYLEHMIWRITE
            styleHMIOSS = STYLELBCOSSWRITE
            style = STYLEWRITE  
                                        
        child = self.groupBoxesDriveSafe[k].findChildren(QtWidgets.QPushButton)
        for i in [0,1,2,3,4,5,7,10,18,19,20,21,22,23]:
            child[i].setStyleSheet(style)
            if i == (driveSafeModeXHMI*3) or i == (driveSafeModeYHMI*3+1) or i == (driveSafeModeZHMI*3+2):
                child[i].setStyleSheet(styleHMI)
            if i == (driveSafeModeXOSS*3) or i == (driveSafeModeYOSS*3+1) or i == (driveSafeModeZOSS*3+2):
                child[i].setStyleSheet(styleOSS)
            if (i == (driveSafeModeXOSS*3) or i == (driveSafeModeYOSS*3+1) or i == (driveSafeModeZOSS*3+2)) and (i == (driveSafeModeXHMI*3) or i == (driveSafeModeYHMI*3+1) or i == (driveSafeModeZHMI*3+2)):
                child[i].setStyleSheet(styleHMIOSS)

    def updateActiveButtons(self):          
        # Update the HMI for the current (active) page:
        k = self.stackedWidget.currentIndex()   # Currentlt activated beam number

        activeFlagDataHMI = self.activeFlagData[0][k]
        activeFlagDataOSS = self.activeFlagData[1][k]
        activeFlagDataLBC = self.activeFlagData[2][k]
        
        if self.writeSwitchData[k] == 0:      
            styleOSS            = STYLEOSSNOWRITE  # write enabled, set in LBC, not in OSS
            styleHMI            = STYLEHMINOWRITE # write enabled, set in OSS, not in LBC
            styleLBC            = STYLELBCNOWRITE  # write enabled, set in LBC, noting set by OSS/HMI
            styleLBCmatchesOSS  = STYLELBCOSSNOWRITE   # write enabled, set in LBC and OSS
            styleLBCmatchesHMI  = STYLELBCHMINOWRITE   # write enabled, set in LBC and HMI
            style               = STYLENOWRITE
            
        else:
            styleOSS            = STYLEOSSWRITE  # write enabled, set in LBC, not in OSS
            styleHMI            = STYLEHMIWRITE # write enabled, set in OSS, not in LBC
            styleLBC            = STYLELBCWRITE  # write enabled, set in LBC, noting set by OSS/HMI
            styleLBCmatchesOSS  = STYLELBCOSSWRITE   # write enabled, set in LBC and OSS
            styleLBCmatchesHMI  = STYLELBCHMIWRITE   # write enabled, set in LBC and HMI
            style               = STYLEWRITE   
            
        child = self.groupBoxesActive[k].findChildren(QtWidgets.QPushButton)
        for i in range(len(activeFlagDataHMI)):    
            child[i*2].setStyleSheet(style)
            child[i*2+1].setStyleSheet(style)
            
            if activeFlagDataHMI[i] == 0 :
                child[2*i+1].setStyleSheet(styleHMI)
            elif activeFlagDataHMI[i] == 1 :
                child[2*i].setStyleSheet(styleHMI)

            if activeFlagDataOSS[i] == 0 :
                child[2*i+1].setStyleSheet(styleOSS)
            elif activeFlagDataOSS[i] == 1 :
                child[2*i].setStyleSheet(styleOSS)
                
            if activeFlagDataLBC[i] == 0 :
                child[2*i+1].setStyleSheet(styleLBC)
            elif activeFlagDataLBC[i] == 1 :
                child[2*i].setStyleSheet(styleLBC)
                
            if activeFlagDataLBC[i] == 0 and activeFlagDataHMI[i] == 0:
                child[2*i+1].setStyleSheet(styleLBCmatchesHMI)
            elif activeFlagDataLBC[i] == 1 and activeFlagDataHMI[i] == 1:
                child[2*i].setStyleSheet(styleLBCmatchesHMI)  
                
            if activeFlagDataOSS[i] == 0 and activeFlagDataLBC[i] == 0:
                child[2*i+1].setStyleSheet(styleLBCmatchesOSS)
            elif activeFlagDataOSS[i] == 1 and activeFlagDataLBC[i] == 1:
                child[2*i].setStyleSheet(styleLBCmatchesOSS) 

    def updateIgnoreButtons(self):  

    # Update the HMI for the current (active) page:
        k = self.stackedWidget.currentIndex()   # Currentlt activated beam number

        ignoreFlagDataHMI = self.ignoreFlagData[0][k]
        ignoreFlagDataOSS = self.ignoreFlagData[1][k]
        ignoreFlagDataLBC = self.ignoreFlagData[2][k]
        
        if self.writeSwitchData[k] == 0:      
            styleOSS            = STYLEOSSNOWRITE  # write enabled, set in LBC, not in OSS
            styleHMI            = STYLEHMINOWRITE # write enabled, set in OSS, not in LBC
            styleLBC            = STYLELBCNOWRITE  # write enabled, set in LBC, noting set by OSS/HMI
            styleLBCmatchesOSS  = STYLELBCOSSNOWRITE   # write enabled, set in LBC and OSS
            styleLBCmatchesHMI  = STYLELBCHMINOWRITE   # write enabled, set in LBC and HMI
            style               = STYLENOWRITE
            
        else:
            styleOSS            = STYLEOSSWRITE  # write enabled, set in LBC, not in OSS
            styleHMI            = STYLEHMIWRITE # write enabled, set in OSS, not in LBC
            styleLBC            = STYLELBCWRITE  # write enabled, set in LBC, noting set by OSS/HMI
            styleLBCmatchesOSS  = STYLELBCOSSWRITE   # write enabled, set in LBC and OSS
            styleLBCmatchesHMI  = STYLELBCHMIWRITE   # write enabled, set in LBC and HMI
            style               = STYLEWRITE   
            
        child = self.groupBoxesIgnore[k].findChildren(QtWidgets.QPushButton)
        for i in range(len(ignoreFlagDataHMI)):    
            child[i*2].setStyleSheet(style)
            child[i*2+1].setStyleSheet(style)
            
            if ignoreFlagDataHMI[i] == 0 :
                child[2*i+1].setStyleSheet(styleHMI)
            elif ignoreFlagDataHMI[i] == 1 :
                child[2*i].setStyleSheet(styleHMI)
                
            if ignoreFlagDataOSS[i] == 0 :
                child[2*i+1].setStyleSheet(styleOSS)
            elif ignoreFlagDataOSS[i] == 1 :
                child[2*i].setStyleSheet(styleOSS)
                
            if ignoreFlagDataLBC[i] == 0 :
                child[2*i+1].setStyleSheet(styleLBC)
            elif ignoreFlagDataLBC[i] == 1 :
                child[2*i].setStyleSheet(styleLBC)
                
            if ignoreFlagDataLBC[i] == 0 and ignoreFlagDataHMI[i] == 0 :
                child[2*i+1].setStyleSheet(styleLBCmatchesHMI)
            elif ignoreFlagDataLBC[i] == 1 and ignoreFlagDataHMI[i] == 1 :
                child[2*i].setStyleSheet(styleLBCmatchesHMI)
                
            if ignoreFlagDataLBC[i] == 0 and ignoreFlagDataOSS[i] == 0 :
                child[2*i+1].setStyleSheet(styleLBCmatchesOSS)
            elif ignoreFlagDataLBC[i] == 1 and ignoreFlagDataOSS[i] == 1 :
                child[2*i].setStyleSheet(styleLBCmatchesOSS)
                                      
    def updateEstopReactionButtons(self):          
    # Update the HMI for the current (active) page:
        k = self.stackedWidget.currentIndex()   # Currentlt activated beam number
        
        eReactionDataHMI = self.eReactionData[0][k]
        eReactionDataOSS = self.eReactionData[1][k]
        eReactionDataLBC = self.eReactionData[2][k]
        
        
        if self.writeSwitchData[k] == 0:      
            styleOSS            = STYLEOSSNOWRITE  # write enabled, set in LBC, not in OSS
            styleHMI            = STYLEHMINOWRITE # write enabled, set in OSS, not in LBC
            styleLBC            = STYLELBCNOWRITE  # write enabled, set in LBC, noting set by OSS/HMI
            styleLBCmatchesOSS  = STYLELBCOSSNOWRITE   # write enabled, set in LBC and OSS
            styleLBCmatchesHMI  = STYLELBCHMINOWRITE   # write enabled, set in LBC and HMI
            style               = STYLENOWRITE
            
        else:
            styleOSS            = STYLEOSSWRITE  # write enabled, set in LBC, not in OSS
            styleHMI            = STYLEHMIWRITE # write enabled, set in OSS, not in LBC
            styleLBC            = STYLELBCWRITE  # write enabled, set in LBC, noting set by OSS/HMI
            styleLBCmatchesOSS  = STYLELBCOSSWRITE   # write enabled, set in LBC and OSS
            styleLBCmatchesHMI  = STYLELBCHMIWRITE   # write enabled, set in LBC and HMI
            style               = STYLEWRITE 
        
        for i in [0]: 
            child = self.groupBoxesEstopReaction[k].findChildren(QtWidgets.QPushButton)
            child[2*i].setStyleSheet(style)
            child[2*i+1].setStyleSheet(style)
            if eReactionDataHMI[i] == 1:
                child[2*i].setStyleSheet(styleHMI)
            elif eReactionDataHMI[i] == 0:      
                child[2*i+1].setStyleSheet(styleHMI)
            if eReactionDataOSS[i] == 1:
                child[2*i].setStyleSheet(styleOSS)
            elif eReactionDataOSS[i] == 0:      
                child[2*i+1].setStyleSheet(styleOSS)
            if eReactionDataLBC[i] == 1:
                child[2*i].setStyleSheet(styleLBC)
            elif eReactionDataLBC[i] == 0:      
                child[2*i+1].setStyleSheet(styleLBC)
            if eReactionDataLBC[i] == 1 and eReactionDataHMI[i] == 1 :
                child[2*i].setStyleSheet(styleLBCmatchesHMI)
            elif eReactionDataLBC[i] == 0 and eReactionDataHMI[i] == 0 :      
                child[2*i+1].setStyleSheet(styleLBCmatchesHMI)
            if eReactionDataOSS[i] == 1 and eReactionDataLBC[i] == 1 :
                child[2*i].setStyleSheet(styleLBCmatchesOSS)
            elif eReactionDataOSS[i] == 0 and eReactionDataLBC[i] == 0 :      
                child[2*i+1].setStyleSheet(styleLBCmatchesOSS)


        for i in [1]: 
            child = self.groupBoxesEstopReaction[k].findChildren(QtWidgets.QPushButton)
            child[2*i].setStyleSheet(style)
            child[2*i+1].setStyleSheet(style)
            child[2*i+2].setStyleSheet(style)
            child[2*i+3].setStyleSheet(style)
            if eReactionDataHMI[i] in range(4) :
                child[2*i+eReactionDataHMI[i]].setStyleSheet(styleHMI)
            if eReactionDataOSS[i] in range(4) :
                child[2*i+eReactionDataOSS[i]].setStyleSheet(styleOSS)
            if eReactionDataLBC[i] in range(4) :
                child[2*i+eReactionDataOSS[i]].setStyleSheet(styleLBC)
            if eReactionDataHMI[i] in range(4) and eReactionDataLBC[i] in range(4):
                child[2*i+eReactionDataOSS[i]].setStyleSheet(styleLBCmatchesHMI)
            if eReactionDataOSS[i] in range(4) and eReactionDataLBC[i] in range(4):
                child[2*i+eReactionDataOSS[i]].setStyleSheet(styleLBCmatchesOSS)
                                                                    
        for i in [2]:  
            child = self.groupBoxesEstopReaction[k].findChildren(QtWidgets.QPushButton)
            child[2*i+2].setStyleSheet(style)
            child[2*i+3].setStyleSheet(style)  
            if eReactionDataHMI[i] == 1:
                child[2*i+2].setStyleSheet(styleHMI)  
            elif eReactionDataHMI[i] == 0:      
                child[2*i+3].setStyleSheet(styleHMI)
            if eReactionDataOSS[i] == 1:
                child[2*i+2].setStyleSheet(styleOSS)  
            elif eReactionDataOSS[i] == 0:      
                child[2*i+3].setStyleSheet(styleOSS)
            if eReactionDataLBC[i] == 1:
                child[2*i+2].setStyleSheet(styleLBC)  
            elif eReactionDataLBC[i] == 0:      
                child[2*i+3].setStyleSheet(styleLBC)
            if eReactionDataLBC[i] == 1 and eReactionDataHMI[i] == 1 :
                child[2*i+2].setStyleSheet(styleLBCmatchesHMI)  
            elif eReactionDataLBC[i] == 0 and eReactionDataHMI[i] == 0 :      
                child[2*i+3].setStyleSheet(styleLBCmatchesHMI)
            if eReactionDataLBC[i] == 1 and eReactionDataOSS[i] == 1 :
                child[2*i+2].setStyleSheet(styleLBCmatchesOSS)  
            elif eReactionDataLBC[i] == 0 and eReactionDataOSS[i] == 0 :      
                child[2*i+3].setStyleSheet(styleLBCmatchesOSS)
                                                                                     
        for i in [3]:   
            child = self.groupBoxesEstopReaction[k].findChildren(QtWidgets.QDoubleSpinBox)
            if eReactionDataHMI[i] == eReactionDataLBC[i] :                 
                child[0].setStyleSheet(styleLBCmatchesHMI)  
            if eReactionDataLBC[i] == eReactionDataOSS[i] :                 
                child[0].setStyleSheet(styleLBCmatchesOSS)
            if eReactionDataHMI[i] <> eReactionDataOSS[i] :
                child[0].setStyleSheet(styleHMI)


    def updateLbcFunctions(self):          
    # Update the HMI for the current (active) page:
        k = self.stackedWidget.currentIndex()   # Currentlt activated beam number
        
    # LBC functions:
        xDriveFunction = self.xDriveFunction[k]
        yDriveElectricFunction = self.yDriveElectricFunction[k]        
        yDriveHydraulicFunction = self.yDriveHydraulicFunction[k]
        xLockingFunction = self.xLockingFunction[k]
        LCFunction = self.LCFunction[k]
        AHCFunction= self.AHCFunction[k]
        yBrakeFunction = self.yBrakeFunction[k]
        
    # Print into HMI labels:
        child = self.groupBoxesLbcFunctions[k].findChildren(QtWidgets.QLabel)  
        
        if xDriveFunction <> 99 or LOCAL_MODE in [1,4]:    # indicates that a package is received
            child[1].setText("AUTOMATIC")
        
        if yDriveHydraulicFunction == 0:      
            child[7].setText("ISOLATED ")
        elif yDriveHydraulicFunction == 1:      
            child[7].setText("POSITION CONTROL")
        elif yDriveHydraulicFunction == 2:      
            child[7].setText("BYPASS")
        elif yDriveHydraulicFunction == 3:      
            child[7].setText("ISOLATED")
        elif yDriveHydraulicFunction == 4:      
            child[7].setText("ALLOW EXTEND")
        elif yDriveHydraulicFunction == 5:      
            child[7].setText("ALLOW RETRACT")
            
        if xLockingFunction == 0:      
            child[3].setText("UNLOCKED ")
        elif xLockingFunction == 1:      
            child[3].setText("LOCKED")
            
        if AHCFunction == 0:      
            child[5].setText("OFF ")
        elif AHCFunction == 1:      
            child[5].setText("HOLD")
        elif AHCFunction == 2:      
            child[5].setText("AHC")
        elif AHCFunction == 3:      
            child[5].setText("BYPASS")
            
        if self.lbcConnectionErrorPrinted[k] == 1:      
            child[9].setText("TIME-OUT")
        else:      
            child[9].setText("REDUNDANT")
                                
                
    def updateOutputIO(self):          
    # Update the HMI for the current (active) page:
        k = self.stackedWidget.currentIndex()   # Currentlt activated beam number
        
        LbcOutputData = self.LbcOutputData[k]

        style = "background:black; \n" "color: black;\n" "border: 0px solid white;\n"
        styleEStop = "background:black; \n" "color: red;\n" "border: 0px solid white;\n" 
        styleNoEStop = "background:black; \n" "color: white;\n" "border: 0px solid white;\n"
        
        style = "background:black; \n" "color: black;\n" "border: 0px solid white;\n"
        styleEStop = "color: black;\n" "border: 2px solid grey;\n" "border-radius: 11px;\n" "background:red;\n"
        styleNoEStop = "color: black;\n" "border: 2px solid grey;\n" "border-radius: 11px;\n" "background:grey;\n"
        
        
        for i in range(len(LbcOutputData)): 
            child = self.groupBoxesOutputIO[k].findChildren(QtWidgets.QPushButton)   
            child[i].setStyleSheet(style)
            if LbcOutputData[i] == 0 : 
                child[i].setFixedWidth(23)
                child[i].setStyleSheet(styleEStop)
                child[i].setText("")
            elif LbcOutputData[i] == 1:   
                child[i].setFixedWidth(23)
                child[i].setStyleSheet(styleNoEStop)
                child[i].setText("")
                
    def updateETimeOut(self):          
    # Update the HMI for the current (active) page:
        k = self.stackedWidget.currentIndex()   # Currentlt activated beam number

        communicationError = [self.lbcConnectionErrorPrinted[k],0]
        if LOCAL_MODE in [1,4]:
            self.counter = self.counter+1
            if self.counter > 99:
                self.counter = 1
            counter = self.counter
        else:
            counter = self.lbcConnectionCounter[k]

            
        
    
        style = "background:black; \n" "color: black;\n" "border: 0px solid white;\n"
        styleEStop = "background:black; \n" "color: red;\n" "border: 0px solid white;\n" 
        styleNoEStop = "background:black; \n" "color: white;\n" "border: 0px solid white;\n"
        
        style = "background:black; \n" "color: black;\n" "border: 0px solid white;\n"
        styleEStop = "color: black;\n" "border: 2px solid grey;\n" "border-radius: 11px;\n" "background:orange;\n"
        styleNoEStop = "color: black;\n" "border: 2px solid grey;\n" "border-radius: 11px;\n" "background:grey;\n"
        
        
        for i in range(len(communicationError)): 
            child = self.groupBoxesETimeOut[k].findChildren(QtWidgets.QPushButton)   
            child[i].setStyleSheet(style)
            if communicationError[i] == 1 : 
                child[i].setFixedWidth(23)
                child[i].setStyleSheet(styleEStop)
                child[i].setText("")
            elif communicationError[i] == 0:   
                child[i].setFixedWidth(23)
                child[i].setStyleSheet(styleNoEStop)
                child[i].setText("") 
                
        child = self.groupBoxesETimeOut[k].findChildren(QtWidgets.QLabel)
        child[2].setText(str(counter))
                
    def updateEState(self):          
    # Update the HMI for the current (active) page:
        k = self.stackedWidget.currentIndex()   # Currentlt activated beam number
        
        LbcEStateData = self.lbcEStateData[k]     

        style = "background:black; \n" "color: black;\n" "border: 0px solid white;\n"
        styleEStop = "background:black; \n" "color: red;\n" "border: 0px solid white;\n" 
        styleNoEStop = "background:black; \n" "color: white;\n" "border: 0px solid white;\n"
        
        style = "background:black; \n" "color: black;\n" "border: 0px solid white;\n"
        styleEStop = "color: black;\n" "border: 2px solid grey;\n" "border-radius: 11px;\n" "background:orange;\n"
        styleNoEStop = "color: black;\n" "border: 2px solid grey;\n" "border-radius: 11px;\n" "background:grey;\n"
        
        
        for i in range(len(LbcEStateData)): 
            child = self.groupBoxesEState[k].findChildren(QtWidgets.QPushButton)   
            child[i].setStyleSheet(style)
            if LbcEStateData[i] == 1 : 
                child[i].setFixedWidth(23)
                child[i].setStyleSheet(styleEStop)
                child[i].setText("")
            elif LbcEStateData[i] == 0:   
                child[i].setFixedWidth(23)
                child[i].setStyleSheet(styleNoEStop)
                child[i].setText("")         

    def updateInputIO(self):
      # Update the HMI for the current (active) page:
        k = self.stackedWidget.currentIndex()   # Currentlt activated beam number
        
        LbcInputData = [0 for i in range(NO_SAFETYINPUTS-16)]
        
        for j in range(NO_SAFETYINPUTS-16):
            LbcInputData[j] = self.LbcInputData[k][j]

        style = "background:black; \n" "color: black;\n" "border: 0px solid white;\n"
        styleEStop = "background:black; \n" "color: red;\n" "border: 0px solid white;\n" 
        styleNoEStop = "background:black; \n" "color: white;\n" "border: 0px solid white;\n"
        
        style = "background:black; \n" "color: black;\n" "border: 0px solid white;\n"
        styleEStop = "color: black;\n" "border: 2px solid grey;\n" "border-radius: 11px;\n" "background:orange;\n"
        styleNoEStop = "color: black;\n" "border: 2px solid grey;\n" "border-radius: 11px;\n" "background:grey;\n"
        
        
        for i in range(len(LbcInputData)): 
            child = self.groupBoxesInputIO[k].findChildren(QtWidgets.QPushButton)   
            child[i].setStyleSheet(style)
            if LbcInputData[i] == 1 :
                child[i].setFixedWidth(23)
                child[i].setStyleSheet(styleEStop)
                child[i].setText("")
            elif LbcInputData[i] == 0:   
                child[i].setFixedWidth(23)
                child[i].setStyleSheet(styleNoEStop)
                child[i].setText("")
                           
                           
    def displayTime(self):
        self.dateTime.setText(time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime()))
        self.dateTime.setStyleSheet("color: #66ffff")


    def updateVesselEstop(self):
        children = self.vesselWidget.findChildren(QtWidgets.QPushButton)

        for i in range(NO_BEAMS):
            if i > 7:
                kk = (i-8)*7 + 2
            else:
                kk = i*7 + 4
             
            children[kk].setStyleSheet("QPushButton{\n"
                                                        "color: green;\n"
                                                        "border: 0px solid green;\n"
                                                        "border-radius: 0px;\n"
                                                        "background:green;\n"
                                                        "}")             
             
            if self.lbcConnectionErrorPrinted[i] == 1 : 
                children[kk].setStyleSheet("QPushButton{\n"
                                                        "color: orange;\n"
                                                        "border: 2px solid orange;\n"
                                                        "border-radius: 0px;\n"
                                                        "background:orange;\n"
                                                        "}")
                                                        
                                                        
            if any(items == 0 for items in self.LbcOutputData[i]) : #safety output de-energized
                children[kk].setStyleSheet("QPushButton{\n"
                                                        "color: red;\n"
                                                        "border: 2px solid red;\n"
                                                        "border-radius: 0px;\n"
                                                        "background:red;\n"
                                                        "}")

                                                        
    def updateOverviewEstop(self):
        for k in range(NO_BEAMS):
            children = self.groupBoxesOverview[k].findChildren(QtWidgets.QLabel)
#            childrenBeam = self.groupBoxesBeamOverview[k].findChildren(QtWidgets.QLabel)
            
            if k <8:
                kk = k+8
            else:
                kk = k-8
            
            if k<8:
                buttonEstop = children[39]
#                buttonAlarm = children[2*10-1]
#                buttonHealthy = children[4*10-1]
            else:
                buttonEstop = children[30]
#                buttonAlarm = children[1*10]
#                buttonHealthy = children[3*10]
            
#            buttonEstopBeam = childrenBeam[4]
#            buttonHealthyBeam = childrenBeam[4*10-1]
            
            
            
            buttonEstop.setStyleSheet("QLabel{\n"
                                                        "color: green;\n"
                                                        "border: 2px solid green;\n"
                                                        "border-radius: 0px;\n"
                                                        "background:green;\n"
                                                        "}")             
             
            if self.lbcConnectionErrorPrinted[kk] == 1 : 
                buttonEstop.setStyleSheet("QLabel{\n"
                                                        "color: orange;\n"
                                                        "border: 2px solid orange;\n"
                                                        "border-radius: 0px;\n"
                                                        "background:orange;\n"
                                                        "}")
                                                        
                                                        
            if any(items == 0 for items in self.LbcOutputData[kk]) : #safety output de-energized
                buttonEstop.setStyleSheet("QLabel{\n"
                                                        "color: red;\n"
                                                        "border: 2px solid red;\n"
                                                        "border-radius: 0px;\n"
                                                        "background:red;\n"
                                                        "}")
                                                        
                                                        
                                                        
#            buttonHealthy.show()  
#            if any(items == 0 for items in self.LbcOutputData[kk]) :  #safety output de-energized
#                buttonEstop.show()
#                buttonHealthy.hide()
#            else:
#                buttonEstop.hide()
#                
#                
#            if self.lbcConnectionErrorPrinted[kk] == 1 :  #safety output de-energized
#                buttonAlarm.show()
#                buttonHealthy.hide()
#            else:
#                buttonAlarm.hide()


    def updateOverviewSafeModes(self):
        for k in range(NO_BEAMS):
            children = self.groupBoxesOverview[k].findChildren(QtWidgets.QLabel)

                
            for i in [3] :
                if k <8 and i == 3 :
                    kk = k+8
                    beamSafeText =  labelTextBeamSafe[self.beamSafeData[1][kk]]
                    children[4+10*i].setText(beamSafeText )
          
                    
                if k >=8 and i == 3 :
                    kk = k-8
                    beamSafeText =  labelTextBeamSafe[self.beamSafeData[1][kk]]
                    children[5+10*i].setText(beamSafeText )

            
    def updateOverviewIO(self):
        
        for k in range(NO_BEAMS):
            children = self.groupBoxesOverview[k].findChildren(QtWidgets.QLabel)
                 
            for i in range(4):
                if k <8 and i == 0 :
                    kk = k+8
                    if True :
                        children[7+10*i].setText("AUTOMATIC")
                        children[7+10*i].setStyleSheet("color: #66ffff")


                if k >=8 and i == 0 :
                    kk = k-8
                    if  True:
                        children[3+10*i].setText("AUTOMATIC")
                        children[3+10*i].setStyleSheet("color:#66ffff")

                    
                if k <8 and i == 1 :
                    kk = k+8

                    children[7+10*i].setText(str(labelTextPeopleInBeam[self.peopleInBeam[1][kk]]))
                    children[7+10*i].setStyleSheet("color:#66ffff")


                    
                if k >=8 and i == 1 :
                    kk = k-8

                    children[3+10*i].setText(str(labelTextPeopleInBeam[self.peopleInBeam[1][kk]]))
                    children[3+10*i].setStyleSheet("color:#66ffff")
                    

                    
                if k <8 and i == 2 :
                    kk = k+8
                    if self.activeFlagData[2][kk][18] == 1 :
                        children[7+10*i].setText("ACTIVE")
                        children[7+10*i].setStyleSheet("color:#66ffff")
 
                    else:
                        children[7+10*i].setText("NOT ACTIVE")
                        children[7+10*i].setStyleSheet("color:#66ffff")
                        
                        
                if k >=8 and i == 2 :
                    kk = k-8
                    if self.activeFlagData[2][kk][18] == 1 :
                        children[3+10*i].setText("ACTIVE")
                        children[3+10*i].setStyleSheet("color:#66ffff")
     
                    else:
                        children[3+10*i].setText("NOT ACTIVE")
                        children[3+10*i].setStyleSheet("color:#66ffff")
                        
                        
                        
                if k <8 and i == 3 :
                    kk = k+8
                    if self.hmiChanges[kk] == 1 :
                        children[7+10*i].setText("NOT LOADED")
                        children[7+10*i].setStyleSheet("color:#66ffff")
 
                    else:
                        children[7+10*i].setText("LOADED")
                        children[7+10*i].setStyleSheet("color:#66ffff")
    
                    
                if k >=8 and i == 3 :
                    kk = k-8
                    if self.hmiChanges[kk] == 1 :
                        children[3+10*i].setText("NOT LOADED")
                        children[3+10*i].setStyleSheet("color:#66ffff")
     
                    else:
                        children[3+10*i].setText("LOADED")
                        children[3+10*i].setStyleSheet("color:#66ffff")
  


        # Connection warning icon on overview page
        for k in range(NO_BEAMS):
            children = self.groupBoxesOverview[k].findChildren(QtWidgets.QLabel)
            if k<8:
                kk = k+8
            else:
                kk = k-8
            
            if k <8 and self.lbcConnectionErrorPrinted[kk] ==  0:
                children[33].setPixmap(QtGui.QPixmap("images/connectionWarningBlack.PNG"))
            elif k <8 and self.lbcConnectionErrorPrinted[kk] == 1 :
                children[33].setPixmap(QtGui.QPixmap("images/connectionWarning.PNG"))
   
            if k >=8 and self.lbcConnectionErrorPrinted[kk] == 0 :
                children[36].setPixmap(QtGui.QPixmap("images/connectionWarningBlack.PNG"))
            elif k >=8 and self.lbcConnectionErrorPrinted[kk] == 1:
                children[36].setPixmap(QtGui.QPixmap("images/connectionWarning.PNG"))

                              
    def updateOverviewFLU(self):
        pass
        # for k in range(NO_BEAMS):
        #     children = self.groupBoxesOverview[k].findChildren(QtWidgets.QLabel)
        #
        #
        #     if k<8:
        #         if self.FLU[k+8] < len(STYLEFLU):
        #             text = str(self.FLU[k+8])
        #             if text == "0":
        #                 text = "-"
        #
        #             children[0].setStyleSheet(STYLEFLU[self.FLU[k+8]])
        #             children[0].setText(text)
        #             children[10].setStyleSheet(STYLEFLU[self.FLU[k+8]])
        #             children[10].setText(text)
        #             children[20].setStyleSheet(STYLEFLU[self.FLU[k+8]])
        #             children[20].setText(text)
        #             children[30].setStyleSheet(STYLEFLU[self.FLU[k+8]])
        #             children[30].setText(text)
        #
        #     elif k>=8:
        #         if self.FLU[k-8] < (len(STYLEFLU)):
        #             text = str(self.FLU[k-8])
        #             if text == "0":
        #                 text = "-"
        #             children[9].setStyleSheet(STYLEFLU[self.FLU[k-8]])
        #             children[9].setText(text)
        #             children[19].setStyleSheet(STYLEFLU[self.FLU[k-8]])
        #             children[19].setText(text)
        #             children[29].setStyleSheet(STYLEFLU[self.FLU[k-8]])
        #             children[29].setText(text)
        #             children[39].setStyleSheet(STYLEFLU[self.FLU[k-8]])
        #             children[39].setText(text)

                    
                    
    def updateVesselFLU(self):
        pass
        # children = self.vesselWidget.findChildren(QtWidgets.QPushButton)
        # #ii = self.stackedWidget.currentIndex()
        # for i in range(NO_BEAMS):
        #
        #     if i > 7:
        #         kk = (i-8)*7
        #     else:
        #         kk = i*7 + 6
        #
        #     text = str(self.FLU[i])
        #     if text == "0":
        #         text = "-"
        #     if self.FLU[i] < len(STYLEFLU):
        #         children[kk].setStyleSheet(STYLEFLU[self.FLU[i]])
        #         children[kk].setText(text)

                
    def updateBeamCheckButtons(self):
            
        #print self.beamsToBeChecked
        self.sub_checkFlagsAndReactions(self.beamsToBeChecked)
        

    def sub_checkFlagsAndReactions(self,beamsToBeChecked):
        beamVec = []
        for i in range(NO_BEAMS):
            
            if beamsToBeChecked[i] == True:
                beamVec.extend([i,i])

     #   print(beamVec)
        

        childrenActive = self.groupBoxCheckActive.findChildren(QtWidgets.QPushButton)
        for i in range(len(childrenActive)):
            childrenActive[i].setText("EQUAL")
            childrenActive[i].setStyleSheet("color:black; background-color: green")
        childrenIgnore = self.groupBoxCheckIgnore.findChildren(QtWidgets.QPushButton)
        for i in range(len(childrenIgnore)):
            childrenIgnore[i].setText("EQUAL")
            childrenIgnore[i].setStyleSheet("color:black; background-color: green")
        childrenEReaction = self.groupBoxCheckEstopReaction.findChildren(QtWidgets.QPushButton)
        for i in range(len(childrenEReaction)):
            childrenEReaction[i].setText("EQUAL")
            childrenEReaction[i].setStyleSheet("color:black; background-color: green" )
        
        if len(beamVec)>1:
            for i in range(len(beamVec)):               
                for k in range(NO_ACTIVEFLAGS):
                    if self.activeFlagData[0][beamVec[i]][k] <> self.activeFlagData[0][beamVec[i-1]][k]:
                        #self.printMessage("CHECK FAILED: Active flags '"+ labelTextActive[k] + "' do not match between all selected beams!")
                        childrenActive[k].setText("DIFFERENT")
                        childrenActive[k].setStyleSheet("color:black; background-color: yellow")

                for k in range(NO_IGNOREFLAGS):
                    if self.ignoreFlagData[0][beamVec[i]][k] <> self.ignoreFlagData[0][beamVec[i-1]][k]:
                        #self.printMessage("CHECK FAILED: Ignore flags '"+ labelTextIgnore[k] + "' do not match between all selected beams!")
                        childrenIgnore[k].setText("DIFFERENT")
                        childrenIgnore[k].setStyleSheet("color:black; background-color: yellow")

                for k in range(4):
                    if self.eReactionData[0][beamVec[i]][k] <> self.eReactionData[0][beamVec[i-1]][k]:
                        #self.printMessage("CHECK FAILED: E-stop Reactions '"+ labelTextEstopReaction[k][0] + "' do not match between all selected beams!")
                        childrenEReaction[k].setText("DIFFERENT")
                        childrenEReaction[k].setStyleSheet("color:black; background-color: yellow")


    def updateYBrake(self):
        [beamID,beamIDs, writeSwitchDataFlu] = self.sub_findFluBeams()  # get all beams and their writeswitchdata in the FLU

        if any(items == False for items in writeSwitchDataFlu)  :
            # self.printMessage("ERROR: Changes not applied. Enable beam write switch to change value.")
            for i in beamIDs:
                child = self.groupBoxesEstopReaction[i].findChildren(QtWidgets.QDoubleSpinBox)
                child[0].setValue(self.eReactionData[0][i][3])
                       
        else:
            for i in beamIDs:
                child = self.groupBoxesEstopReaction[i].findChildren(QtWidgets.QDoubleSpinBox)
                child[0].setValue(self.eReactionData[0][i][3])
            #    print self.eReactionData[0][i]   

                
    def updateWriteMatches(self):  # a function that checks if the enabled write switches match the HMI selection

        self.hmiChanges = [0 for i in range(NO_BEAMS)]
        for i in range(NO_BEAMS): 
            for k in range(NO_ACTIVEFLAGS):               
                if self.activeFlagData[0][i][k] <> self.activeFlagData[1][i][k]:
                    self.hmiChanges[i] = 1   # set change bit to true for this beam
            for k in range(NO_IGNOREFLAGS):
                if self.ignoreFlagData[0][i][k] <> self.ignoreFlagData[1][i][k]:
                    self.hmiChanges[i] = 1   # set change bit to true for this beam
            for k in range(4):
                if self.eReactionData[0][i][k] <> self.eReactionData[1][i][k]:
                    self.hmiChanges[i] = 1   # set change bit to true for this beam
            for k in range(NO_ESTOPOUTPUTS):
                if self.outputStateData[0][i][k] <> self.outputStateData[1][i][k]:
                    self.hmiChanges[i] = 1   # set change bit to true for this beam
                    
             
        if self.writeSwitchData <> self.hmiChanges:
            self.blockUpload = True
        else:
            self.blockUpload = False
            
            
            
    def updateOverviewMatches(self):  # a function that checks if HMI settings between beam in an FLU match
        
        self.hmiFluMatch = [1 for i in range(NO_BEAMS)]
        beamVec = [[] for k in range(6)]        
        
        for k in range(NO_BEAMS):
            for i in range(6):
                if self.FLU[k] == i:
                     beamVec[i].append(k)                   


        for i in range(6): 
            if len(beamVec[i]) == 1:
                pass
            else:
                for j in range(len(beamVec[i])-1):
                    
                    for k in range(NO_ACTIVEFLAGS):               
                        if self.activeFlagData[0][beamVec[i][j]][k] <> self.activeFlagData[0][beamVec[i][j+1]][k]:
                          #  self.hmiFluMatch[beamVec[i][j]] = 0   # set change bit to true for this beam
                            for kkk in beamVec[i]:
                                self.hmiFluMatch[kkk] = 0   # set change bit to true for this beam
                    for k in range(NO_IGNOREFLAGS):
                        if self.ignoreFlagData[0][beamVec[i][j]][k] <> self.ignoreFlagData[0][beamVec[i][j+1]][k]:
                          #  self.hmiFluMatch[beamVec[i][j]] = 0   # set change bit to true for this beam
                            for kkk in beamVec[i]:
                                self.hmiFluMatch[kkk] = 0   # set change bit to true for this beam
                    for k in range(4):
                        if self.eReactionData[0][beamVec[i][j]][k] <> self.eReactionData[0][beamVec[i][j+1]][k]:
                           # self.hmiFluMatch[beamVec[i][j]] = 0   # set change bit to true for this beam
                            for kkk in beamVec[i]:
                                self.hmiFluMatch[kkk] = 0   # set change bit to true for this beam

   
         
         
        for k in range(NO_BEAMS):
            children = self.groupBoxesOverview[k].findChildren(QtWidgets.QLabel)
            if k<8:
                kk = k+8
            else:
                kk = k-8
            
            if k <8 and self.hmiFluMatch[kk] == 1:
                children[34].setPixmap(QtGui.QPixmap("images/fluWarningBlack.PNG"))
            elif k <8 and self.hmiFluMatch[kk] == 0:
                children[34].setPixmap(QtGui.QPixmap("images/fluWarning.PNG"))
   
            if k >=8 and self.hmiFluMatch[kk] == 1:
                children[35].setPixmap(QtGui.QPixmap("images/fluWarningBlack.PNG"))
            elif k >=8 and self.hmiFluMatch[kk] == 0:
                children[35].setPixmap(QtGui.QPixmap("images/fluWarning.PNG"))
                    

    def printMessage(self,text):
        textNewLine = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime()) + " : " + text + "\n"
        self.console.insertPlainText(textNewLine)
        self.console.verticalScrollBar().setValue(self.console.verticalScrollBar().maximum())

    def printNetworkMessage(self,text):
        textNewLine = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime()) + " : " + text + "\n"
        self.networkList.insertPlainText(textNewLine)
        self.networkList.verticalScrollBar().setValue(self.networkList.verticalScrollBar().maximum())
    
    def printAlarmMessage(self,text):
        textNewLine = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime()) + " : " + text + "\n"
        self.warningList.insertPlainText(textNewLine)
        self.warningList.verticalScrollBar().setValue(self.warningList.verticalScrollBar().maximum())   
        
    def streetLight(self,writeData):
        self.k = self.k+1
       # print self.k
        writeData[0] = False
        writeData[1] = False
        writeData[2] = False
        writeData[3] = False
        if self.k == 1:
            writeData[0] = True
        elif self.k == 2:
            writeData[1] = True
        elif self.k == 3:
            writeData[2] = True
        elif self.k == 4:
            writeData[3] = True
            
        return writeData

    def lbcConnectionMonitor(self):
        # function that keeps track of timeouts to the 16 beams.
        for k in range(NO_BEAMS):
            if self.lbcConnectionCounter[k] == self.lbcConnectionCounterOld[k]:
                if self.lbcConnectionErrorPrinted[k] == 0:
                    self.lbcConnectionErrorPrinted[k] = 1
                    self.printAlarmMessage("Beam Connection failure: No data received from Beam " + str(k) + ".")
                #print self.lbcConnectionCounter
            self.lbcConnectionCounterOld[k] = self.lbcConnectionCounter[k]
            
#    def communicationLost(self):
#        for k in range(NO_BEAMS):
#            if self.lbcConnectionErrorPrinted[k] == 1:
#                self.groupBoxesBeamSafe[k].setStyleSheet("color:purple; border: purple;")
#            else:
#                self.groupBoxesBeamSafe[k].setStyleSheet("color:white;border: white;")

    def acknowledge_clicked(self):
        
        self.printAlarmMessage("--------------------------------------------- Alarms acknowledged -----------------------------------------------------")

        self.lbcConnectionErrorPrinted = [0]*NO_BEAMS        
        
        if self.connected == False and LOCAL_MODE <> 1:
            self.printAlarmMessage("Console IO failure: OPC not connected.")

###############################################

    def enableFluButton_clicked(self, position):
        FLUCONFIG_2[2 * position[0] + position[1]] = True
        self.fluEnabledButtonsList[2 * position[0] + position[1]].setStyleSheet(STYLEWHITE)
        self.fluDisabledButtonsList[2 * position[0] + position[1]].setStyleSheet(STYLEWRITE)

    def disableFluButton_clicked(self, position):
        FLUCONFIG_2[2* position[0] +  position[1]] = False
        self.fluEnabledButtonsList[2 * position[0] + position[1]].setStyleSheet(STYLEWRITE)
        self.fluDisabledButtonsList[2 * position[0] + position[1]].setStyleSheet(STYLEWHITE)


    def fluButtonsColorsRefresh(self):
        for flu in enumerate(self.fluEnabledButtonsList):
            if FLUCONFIG_2[flu[0]] == True:
                self.fluEnabledButtonsList[flu[0]].setStyleSheet(STYLEWHITE)
                self.fluDisabledButtonsList[flu[0]].setStyleSheet(STYLEWRITE)
            else:
                self.fluEnabledButtonsList[flu[0]].setStyleSheet(STYLEWRITE)
                self.fluDisabledButtonsList[flu[0]].setStyleSheet(STYLEWHITE)

    def enableLinkEstopAllBeamsButton_clicked(self):
        LINK_ESTOP_ALL_BEAMS = True
        print "Link E-Stop to all beams:", LINK_ESTOP_ALL_BEAMS
        self.enableLinkEstopAllBeamsButton.setStyleSheet(STYLEWHITE)
        self.disableLinkEstopAllBeamsButton.setStyleSheet(STYLEWRITE)
        for line in self.overviewFluEstopAllBeamsList:
            line.show()
        for line in self.vesselFluEstopAllBeamsList:
            line.show()

    def disableLinkEstopAllBeamsButton_clicked(self):
        LINK_ESTOP_ALL_BEAMS = False
        print "Link E-Stop to all beams:", LINK_ESTOP_ALL_BEAMS
        self.enableLinkEstopAllBeamsButton.setStyleSheet(STYLEWRITE)
        self.disableLinkEstopAllBeamsButton.setStyleSheet(STYLEWHITE)
        for line in self.overviewFluEstopAllBeamsList:
            line.hide()
        for line in self.vesselFluEstopAllBeamsList:
            line.hide()

    def linkEstopAllBeamsColorsRefresh(self):
        if LINK_ESTOP_ALL_BEAMS:
            self.enableLinkEstopAllBeamsButton.setStyleSheet(STYLEWHITE)
            self.disableLinkEstopAllBeamsButton.setStyleSheet(STYLEWRITE)
        else:
            self.enableLinkEstopAllBeamsButton.setStyleSheet(STYLEWRITE)
            self.disableLinkEstopAllBeamsButton.setStyleSheet(STYLEWHITE)

    def linkEstopAllBeamsLinesRefresh(self):
        for line in self.overviewFluEstopAllBeamsList:
            if LINK_ESTOP_ALL_BEAMS:
                line.show()
            else:
                line.hide()

        for line in self.vesselFluEstopAllBeamsList:
            if LINK_ESTOP_ALL_BEAMS:
                line.show()
            else:
                line.hide()

    def fluButtonsColorsRefresh(self):
        for flu in enumerate(self.fluEnabledButtonsList):
            if FLUCONFIG_2[flu[0]] == True:
                self.fluEnabledButtonsList[flu[0]].setStyleSheet(STYLEWHITE)
                self.fluDisabledButtonsList[flu[0]].setStyleSheet(STYLEWRITE)
            else:
                self.fluEnabledButtonsList[flu[0]].setStyleSheet(STYLEWRITE)
                self.fluDisabledButtonsList[flu[0]].setStyleSheet(STYLEWHITE)

    def fluLinesRefresh(self):
        for lineGroup in enumerate(self.vesselFluLinesList):
            if FLUCONFIG_2[lineGroup[0]] == True:
                #LINES ON NAVIGATION BAR
                self.vesselFluLinesList[lineGroup[0]][lineGroup[0]][0].show()
                self.vesselFluLinesList[lineGroup[0]][lineGroup[0]][1].show()
                self.vesselFluLinesList[lineGroup[0]][lineGroup[0]][2].show()
                #LINES ON OVERVIEW PAGE
                self.overviewFluLinesList[lineGroup[0]][lineGroup[0]][0].show()
                self.overviewFluLinesList[lineGroup[0]][lineGroup[0]][1].show()
                self.overviewFluLinesList[lineGroup[0]][lineGroup[0]][2].show()
            else:
                # LINES ON NAVIGATION BAR
                self.vesselFluLinesList[lineGroup[0]][lineGroup[0]][0].hide()
                self.vesselFluLinesList[lineGroup[0]][lineGroup[0]][1].hide()
                self.vesselFluLinesList[lineGroup[0]][lineGroup[0]][2].hide()
                # LINES ON OVERVIEW PAGE
                self.overviewFluLinesList[lineGroup[0]][lineGroup[0]][0].hide()
                self.overviewFluLinesList[lineGroup[0]][lineGroup[0]][1].hide()
                self.overviewFluLinesList[lineGroup[0]][lineGroup[0]][2].hide()

    def enableFluButton_clicked(self, position):
        FLUCONFIG_2[2 * position[0] + position[1]] = True
        # CHANGE COLOURS OF ENABLED AND DISABLED BUTTONS
        self.fluEnabledButtonsList[2 * position[0] + position[1]].setStyleSheet(STYLEWHITE)
        self.fluDisabledButtonsList[2 * position[0] + position[1]].setStyleSheet(STYLEWRITE)
        # SHOW LINES ON NAVIGATION BAR
        self.vesselFluLinesList[2 * position[0] + position[1]][2 * position[0] + position[1]][0].show()
        self.vesselFluLinesList[2 * position[0] + position[1]][2 * position[0] + position[1]][1].show()
        self.vesselFluLinesList[2 * position[0] + position[1]][2 * position[0] + position[1]][2].show()
        # SHOW LINES ON OVERVIEW PAGE
        self.overviewFluLinesList[2 * position[0] + position[1]][2 * position[0] + position[1]][0].show()
        self.overviewFluLinesList[2 * position[0] + position[1]][2 * position[0] + position[1]][1].show()
        self.overviewFluLinesList[2 * position[0] + position[1]][2 * position[0] + position[1]][2].show()

    def disableFluButton_clicked(self, position):
        FLUCONFIG_2[2* position[0] +  position[1]] = False
        # CHANGE COLOURS OF ENABLED AND DISABLED BUTTONS
        self.fluEnabledButtonsList[2 * position[0] + position[1]].setStyleSheet(STYLEWRITE)
        self.fluDisabledButtonsList[2 * position[0] + position[1]].setStyleSheet(STYLEWHITE)
        # HIDE LINES ON NAVIGATION BAR
        self.vesselFluLinesList[2 * position[0] + position[1]][2 * position[0] + position[1]][0].hide()
        self.vesselFluLinesList[2 * position[0] + position[1]][2 * position[0] + position[1]][1].hide()
        self.vesselFluLinesList[2 * position[0] + position[1]][2 * position[0] + position[1]][2].hide()
        # HIDE LINES ON OVERVIEW PAGE
        self.overviewFluLinesList[2 * position[0] + position[1]][2 * position[0] + position[1]][0].hide()
        self.overviewFluLinesList[2 * position[0] + position[1]][2 * position[0] + position[1]][1].hide()
        self.overviewFluLinesList[2 * position[0] + position[1]][2 * position[0] + position[1]][2].hide()