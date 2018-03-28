# -*- coding: utf-8 -*-
"""
Created on Tue Feb 03 16:28:18 2015

@author: adj
"""

from numpy import *


class LocalBeamControlSafety:
    
    
    def __init__(self, beamIndex, udpCommunication, config):     
        
        # == INPUT == #
        self.index = beamIndex
        self.udpCommunication = udpCommunication
        self.config = config
                
        udpTag = 'LBC-F-%i' %self.index
        self.udpCommunication.addReceiver(udpTag, self)

        # == CONSTANTS == #       

        # simulator 
        self.ossIP = config.data['OSS']['General']['OSSIP']
        self.ossPort = int(config.data['OSS']['General']['OSSPort'])
        
        # local test        
#        self.ossIP = '127.0.0.1'
#        self.ossPort = 55021
        
        
#        self.numOutputGroups = self.config.data['OSS']['OutputGroups']['number']
        self.numOutputGroups = 13
        self.numActiveFlags = 19


        # output group numbers           
#        self.groupNr = self.config.data['OSS']['OutputGroups'] 
        self.groupNr = {'AFE_X&Y':          0,      'LHPU':             1,
                        'ZDriveHydraulics': 2,      'YDriveHydraulics': 3,
                        'HPAirSystem':      4,      'rackLocks':        5,
                        'YDriveBrakes':     6,      'YDriveMotors':     7,
                        'pinLockMotor':     8,      'XHPU':             9,
                        'XLockingSubsystem':10,     'XDriveMotors':     11,
                        'EStopOtherBeam':   12}
        
        # configurations
#        self.xLockingConfigs = self.config.data['OSS']['xLockingConfigs']
#        self.yDriveConfigs = self.config.data['OSS']['yDriveConfigs']
#        self.ahcConfigs = self.config.data['OSS']['ahcConfigs']
        self.xLockingConfigs = {'Unlock': 0, 'Lock': 1}
        self.yDriveConfigs =   {'Stop': 0, 'Bypass': 2, 'AllowExtend': 1, 'AllowRetract': 3}
        self.ahcConfigs =      {'Bypass': 0, 'Stop': 1}
        
        
        # == VARIABLES == #        
        
        # inputs from OSS
        self.generalEStopInput =        0                                       # general E-Stop command from OSS       (1 = E-stop, 0 = no E-stop)
        self.EStopInputs =              [0]*self.numOutputGroups                # E-stop input commands per output group
        
        # LBC states        
        self.EStopStates =              [0]*self.numOutputGroups
        self.subsystemIgnoreFlags =     [0]*self.numOutputGroups                        
        self.EStopOutputs =             [0]*self.numOutputGroups
        
        self.activeFlags =              [0]*self.numActiveFlags 
        
        self.xLockingConfigurationInput =    0
        self.yDriveConfigurationInput =      0
        self.AHCConfigurationInput =         0
        self.yLockDelayInput =               0.        
        
        self.xLockingConfiguration =    0
        self.yDriveConfiguration =      0
        self.AHCConfiguration =         0
        self.yLockDelay =               0.

        # counter
        self.count = 0



    def addLBCN(self,localBeamControlRegular):
        self.localBeamControlRegular = localBeamControlRegular



    # method called by udpCommincation upon new message
    def handleRequest(self, msg, key):
        #print 'received OSS message on beam %s: ' %self.index
        #%print msg
        #print ' '
        
        # update E-Stop Input command
        self.EStopInputs = [0]*self.numOutputGroups
        if ('setEStops' in msg):
            for i in range(0,self.numOutputGroups):
                self.EStopInputs[i] = msg['setEStops'][i]
        if ('setGeneralEStop' in msg) and msg['setGeneralEStop'] == 1:
            self.EStopInputs = [1]*self.numOutputGroups
        
        # update E-Stop states
        for i in range(0,self.numOutputGroups):
            if self.EStopInputs[i] == 1:
                self.EStopStates[i] = 1
                if i == 10:
                    print 'X-lock Estop state true!!!'
        
        # update ignore flags
        if ('setSubsystemIgnoreFlags' in msg):
            for i in range(0,self.numOutputGroups):
                if self.EStopStates[i] != 1:
                    self.subsystemIgnoreFlags[i] = msg['setSubsystemIgnoreFlags'][i]
                    
        # active flags
        if ('activeFlagData' in msg):
            for i in range(0,self.numActiveFlags):
                self.activeFlags[i] = msg['activeFlagData'][i]
        
        # update config inputs
        if ('setXLockingConfiguration' in msg):
            self.xLockingConfigurationInput = msg['setXLockingConfiguration']

        if ('setYDriveConfiguration' in msg):
            # Interlocks?                      
            self.yDriveConfigurationInput = msg['setYDriveConfiguration']
        if ('setAHCConfiguration' in msg):
            self.AHCConfigurationInput = msg['setAHCConfiguration']

        if ('setYLockDelay' in msg):
            self.yLockDelayInput = msg['setYLockDelay']        
                
        # update configs
        self.updateConfigurations()
        
        # update E-Stop outputs
        self.updateEStopOutputs()
        
        # send return message
        self.returnMessage()



    def update(self):
        
        # Send return message
        self.count += 1
        if self.count == 100:
            self.returnMessage()
            self.count = 0
            
        self.updateConfigurations()                                             # why? because interlocks     
    
    
        
    def updateConfigurations(self):
        # X-locking
        if self.localBeamControlRegular.xDriveDynamics.xLockMode == 1: # lock
            self.xLockingConfiguration = self.xLockingConfigs['Lock']
        else:
            self.xLockingConfiguration = self.xLockingConfigurationInput

        # YH-Drive (no interlocks?)  
        self.yDriveConfiguration = self.yDriveConfigurationInput
        
        # AHC
        if self.localBeamControlRegular.zDriveDynamics.zMode_AHC == 3: # bypass
            self.AHCConfiguration = self.ahcConfigs['Bypass']
        elif self.localBeamControlRegular.zDriveDynamics.zMode_AHC == 2: # AHC
            self.AHCConfiguration = self.AHCConfigurationInput
        else:
            self.AHCConfiguration = self.ahcConfigs['Stop']

        # Y-Lock Delay
        self.yLockDelay = self.yLockDelayInput
        
        
    
    # method called internally to send a message to the OSS
    def returnMessage(self):
        msg = {}
        msg['beamNo'] = self.index
        msg['EStopStates'] = self.EStopStates
        msg['EStopOutputs'] = [0]*self.numOutputGroups
        for i in range(self.numOutputGroups):
            msg['EStopOutputs'][i] = 1-self.EStopOutputs[i]
        
        # Flags
        msg['subsystemIgnoreFlags'] = self.subsystemIgnoreFlags
        msg['activeFlags'] = self.activeFlags
        
        # EStop reaction configurations        
        msg['xLockingConfiguration'] = self.xLockingConfiguration
        msg['yDriveConfiguration'] =  self.yDriveConfiguration

        msg['AHCConfiguration'] = self.AHCConfiguration
        msg['yLockDelay'] = self.yLockDelay
        
        # X-drive functions
        msg['xLockingFunction'] = self.localBeamControlRegular.xDriveDynamics.xLockMode
        if self.EStopStates[self.groupNr['AFE_X&Y']] == 1:
            AFEOn = 0 # AFE NOT ENABLED
        else:
            AFEOn = 1 # AFE ENABLED
        msg['xDriveFunction'] = AFEOn
        # msg['xHPUFunction']
            
        # Y-drive functions
        msg['yBrakeFunction'] = self.localBeamControlRegular.yDriveDynamics.yLockMode
        msg['yDriveElectricFunction'] = AFEOn
        msg['yDriveHydraulicFunction'] = self.localBeamControlRegular.yDriveDynamics.yHMode
        # msg['rackLockFunction']
        # msg['turnBuckleFunction']
        # msg['pinLockFunction']
        # msg['zGuideWheel']
        
        # Z-drive functions
        msg['AHCFunction'] = self.localBeamControlRegular.zDriveDynamics.zMode_AHC
        msg['LCFunction'] = self.localBeamControlRegular.zDriveDynamics.zMode_FLC
        msg['lockingPawlFunction'] = self.localBeamControlRegular.zDriveDynamics.zMode_LP
        
        self.udpCommunication.send({'OSS': msg}, self.ossIP, self.ossPort)
        #x = {'OSS': msg}
        #print 'sent message to OSS:'
        #print msg
        
        

    # method called from the OCS to reset the E-Stop states   
    def resetEStops(self, generalReset, resetPerGroup):
        print 'try reset EStop'
        for i in range(0,self.numOutputGroups):
            if (generalReset == 1 or resetPerGroup[i] == 1) and not (self.EStopInputs[i] == 1 or self.generalEStopInput == 1):
                print 'reset EStop State of Group %i!!' %i
                self.EStopStates[i] = 0
        self.updateEStopOutputs()
        
        # send return message
        self.returnMessage()
    
    
    
    # method called internally to update the E-Stop outputs (after E-stop trigger or reset)
    def updateEStopOutputs(self):
        for i in range(0,self.numOutputGroups):
            if self.EStopStates[i] == 1 and self.subsystemIgnoreFlags[i] == 0:
                self.EStopOutputs[i] = 1
            elif self.EStopStates[i] == 0 and self.subsystemIgnoreFlags[i] == 0:
                self.EStopOutputs[i] = 0

    
