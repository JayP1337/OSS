# -*- coding: utf-8 -*-
"""
Created on Tue Feb 03 16:28:18 2015

@author: adj
testing testing git push
"""
import os, sys
from PyQt5 import QtCore, QtWidgets
import mainwindow_class
from mainwindow_constants import *  #holds all constant values that define GUI geometry and parameters

filePath  = os.path.dirname(os.path.abspath(__file__)) 
tlsPath = os.path.dirname(filePath)
pythonPath = os.path.dirname(tlsPath)
sys.path.append(tlsPath)
sys.path.append(pythonPath)

# reload(mainwindow_class)

if LOCAL_MODE <> 1:
    import udp_communication
import overall_safety_system

# ===================== MAIN FILE  ==============================

if LOCAL_MODE <> 1:
    # make UDP send and receive class
    UDPCommunication = udp_communication.UDPCommunication(PORT=55021)
    
    # make OSS object
    oss = overall_safety_system.OverallSafetySystem(UDPCommunication)
else:
    # make UDP send and receive class
    UDPCommunication = []
    
    # make OSS object
    oss = overall_safety_system.OverallSafetySystem(UDPCommunication)
    
    
# make OSS UI
try:
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()

    ui = mainwindow_class.Ui_MainWindow(oss)

    print "[+] Starting ui!"
    ui.setupUi(MainWindow)
    oss.addMainWindow(ui)
    print "[+] Starting MainWondow!"
    MainWindow.show()
except:
    print "[-] Something went wrong!"

def pushExit_clicked(self):   
    # switch off OPC if connected:
    if ui.connected == True:
        ui.opcButton_clicked()
         
    # close GUI:
    MainWindow.close()
        
# define update function
def update():
    if LOCAL_MODE <> 1:
        UDPCommunication.update()
    oss.update()   
    ui.update()

def updateUdpMonitor():
    if LOCAL_MODE <> 1:
        ui.lbcConnectionMonitor()

# Cyclic 10Hz check on OPC data:
timer = QtCore.QTimer()
timer.setInterval(10)
timer.start()
timer.timeout.connect(update)
    
# Cyclic 0.333Hz check on UDP data:
udpTimer = QtCore.QTimer()
udpTimer.setInterval(10000)  #3 second timeout
udpTimer.start()
udpTimer.timeout.connect(updateUdpMonitor)
   
# close GUI on button click:
ui.pushExit.clicked.connect(pushExit_clicked)

# exit application upon closure of UI
sys.exit(app.exec_())