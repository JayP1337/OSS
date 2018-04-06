# -*- coding: utf-8 -*-
"""
Created on Tue Feb 03 16:28:18 2015

@author: adj
"""

from numpy import *
from mainwindow_constants import *  #holds all constant values that define GUI geometry

class OverallSafetySystem:
    
    def __init__(self, udpCommunication):

        if LOCAL_MODE <> 1:
            # == INIT ==
            self.udpCommunication = udpCommunication
        
        if LOCAL_MODE == 0:
            self.simulatorIP = '10.10.0.1'  # whitepark main PC
            self.simulatorPort = 55000 
        elif LOCAL_MODE == 1:
            self.simulatorIP = '127.0.0.1'  # local machine , for standalone testing       
            self.simulatorPort = 55000 
        elif LOCAL_MODE ==2 :
            self.simulatorIP = '10.10.0.30'  # whitepark testing PC
            self.simulatorPort = 55000 
        elif LOCAL_MODE == 3:
            self.simulatorIP = '10.10.0.30'  # whitepark testing PC without OPC button panel
            self.simulatorPort = 55000 
            
            
        if LOCAL_MODE <> 1:
            # add listener to udp comm.
            self.udpCommunication.addReceiver('OSS', self)        
        
        
        # == CONSTANTS ==         
        self.numBeams = 16                                  # number of beams
        self.beams = []
        for i in range(self.numBeams):
            self.beams.append({})
        # self.beams = [{}]*self.numBeams                     # list of dicts for each beams, for storing EStop data
        
        
        # == VARIABLES == 
               
        # states
        for i in range(0,self.numBeams):
            self.beams[i]['setEStops']               = [0]*13
            self.beams[i]['setSubsystemIgnoreFlags'] = [0]*13    
            self.beams[i]['setGeneralEStop']         = 0
            self.beams[i]['xLockingConfiguration']   = 0
            self.beams[i]['yDriveConfiguration']     = 0
            self.beams[i]['AHCConfiguration']        = 0
            self.beams[i]['yDriveDelay']             = 0.
            self.beams[i]['activeFlagData']          = [0]*19
            self.beams[i]['beamSafeData']            = 0
            self.beams[i]['driveSafeData']           = [0, 0, 0]




    def addMainWindow(self,mainWindow):
        self.mainWindow = mainWindow
        
        
    def update(self):
#        print self.beams[0]['setEStops']
        pass


    def handleRequest(self, msg, key):
#        print 'received message: '        
#        print msg        
#        print ' '        
        
        if ('beamNo' in msg):
            k = msg['beamNo']-1
            
            #reset timeout for 
            self.mainWindow.lbcConnectionCounter[k] = self.mainWindow.lbcConnectionCounter[k] + 1   # update the received message counter
           
            self.mainWindow.printNetworkMessage("Received: LBC-F config from Beam " + str(k) + ". Message no.: " + str(self.mainWindow.lbcConnectionCounter[k]))

#            # update E-stop states
            if ('EStopStates' in msg):
                for i in range(NO_ESTOPOUTPUTS):
                    self.mainWindow.lbcEStateData[k][i] = msg['EStopStates'][i]
                    
            # update safety outputs
            if ('EStopOutputs' in msg):
                for i in range(NO_ESTOPOUTPUTS):
                    self.mainWindow.LbcOutputData[k][i] = msg['EStopOutputs'][i]

   
            # update ignore flags
            if ('subsystemIgnoreFlags' in msg):
           #     print 'tada!'
                for i in range(NO_IGNOREFLAGS):
                    self.mainWindow.ignoreFlagData[2][k][i] = msg['subsystemIgnoreFlags'][i]  # index [2] indicates it is LBC-F data

            
            # update active flags
            if ('activeFlags' in msg):
                for i in range(NO_ACTIVEFLAGS):
                    self.mainWindow.activeFlagData[2][k][i] = msg['activeFlags'][i]   # index [2] indicates it is LBC-F data
                    
            # update eReaction configuration
            if ('xLockingConfiguration' in msg):
                self.mainWindow.eReactionData[2][k][0] = msg['xLockingConfiguration']
            if ('yDriveConfiguration' in msg):
                self.mainWindow.eReactionData[2][k][1] = msg['yDriveConfiguration']
            if ('AHCConfiguration' in msg):
                print 'AHC received!'
                self.mainWindow.eReactionData[2][k][2] = msg['AHCConfiguration']
                #print self.mainWindow.eReactionData[1][k][2] 
            if ('yLockDelay' in msg):
                self.mainWindow.eReactionData[2][k][3] = msg['yLockDelay']
                        
                        
            # receive LBC operational function
            if ('xDriveFunction' in msg):
                self.mainWindow.xDriveFunction[k] = msg['xDriveFunction']
            if ('yDriveElectricFunction' in msg):
                self.mainWindow.yDriveElectricFunction[k] = msg['yDriveElectricFunction']
            if ('yDriveHydraulicFunction' in msg):
                self.mainWindow.yDriveHydraulicFunction[k] = msg['yDriveHydraulicFunction']
            if ('xLockingFunction' in msg):
                self.mainWindow.xLockingFunction[k] = msg['xLockingFunction']
            if ('LCFunction' in msg):
                self.mainWindow.LCFunction[k] = msg['LCFunction']
            if ('AHCFunction' in msg):
                self.mainWindow.AHCFunction[k] = msg['AHCFunction']
            if ('yBrakeFunction' in msg):
                self.mainWindow.yBrakeFunction[k] = msg['yBrakeFunction']        


    # send the complete OSS configuration to the LBC-F of the beams in 'beamNumbers'
    def sendCompleteMessage(self, activeBeams):
        for i in range(self.numBeams):
            if activeBeams[i] == 1:   
                self.mainWindow.printNetworkMessage("Sent: New LBC-F config to Beam " + str(i) + ".")
                msg = {}
         #       msg['setEStops']                = self.beams[i]['setEStops']
                msg['setSubsystemIgnoreFlags']  = self.beams[i]['setSubsystemIgnoreFlags']
                msg['setXLockingConfiguration'] = self.beams[i]['xLockingConfiguration']
                msg['setYDriveConfiguration']   = self.beams[i]['yDriveConfiguration']
                msg['setAHCConfiguration']      = self.beams[i]['AHCConfiguration']
                msg['setYLockDelay']            = self.beams[i]['yDriveDelay']
                msg['activeFlagData']           = self.beams[i]['activeFlagData']
                
                udpTag = 'LBC-F-%i' %(i+1)
                msgFinal = {udpTag: msg}
                if LOCAL_MODE <> 1: 
                    self.udpCommunication.send(msgFinal, self.simulatorIP, self.simulatorPort)
                print msgFinal
        
    def sendEStopMessage(self):
        self.mainWindow.printNetworkMessage("Sent: Current E-stop status")
        for i in range(self.numBeams):
            msg = {}
            msg['setEStops']                = self.beams[i]['setEStops']
           
            udpTag = 'LBC-F-%i' %(i+1)
            msgFinal = {udpTag: msg}
            if LOCAL_MODE <> 1:
                self.udpCommunication.send(msgFinal, self.simulatorIP, self.simulatorPort)
            print msgFinal
                
    # send Test message to the LBC-F
    def sendTestMessage(self):
        # test
        self.beams[0]['setEStops'][0] = 1
        self.beams[0]['setEStops'][1] = 1
        self.beams[0]['setEStops'][2] = 1
        self.beams[0]['setEStops'][3] = 1
        self.beams[0]['setSubsystemIgnoreFlags'][1] = 1
        self.sendMessage([1, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0])
        
        
        
        
        
        