import sys
from PyQt5 import QtWidgets, QtCore, QtGui

FLUCONFIG_2 = [False, False, False, False, False, False, False, True] # P1P2, S1S2, P3P4, S3S4, P5P6, S5S6, P7P8, S7S8

STYLEWRITE          = "background:#a6a6a6; \n"  "color: black;\n"       "border: 5px solid #a6a6a6;\n"
STYLEWHITE          = "background-color: white"


class Example(QtWidgets.QWidget):
    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        self.fluEnabledButtonsList = []
        self.fluDisabledButtonsList = []
        self.linkEstopAllBeams = False
        self.vesselOneFluGroupLines = []
        self.vesselFluLinesList = []
        self.initUI()

    # def linkEstopAllBeamsColorsRefresh(self):
    #     if self.linkEstopAllBeams:
    #         self.linkEstopAllBeamsEnableButton.setStyleSheet(STYLEWHITE)
    #         self.linkEstopAllBeamsDisableButton.setStyleSheet(STYLEWRITE)
    #     else:
    #         self.linkEstopAllBeamsEnableButton.setStyleSheet(STYLEWRITE)
    #         self.linkEstopAllBeamsDisableButton.setStyleSheet(STYLEWHITE)


    def fluButtonsColorsRefresh(self):
        for flu in enumerate(self.fluEnabledButtonsList):
            if FLUCONFIG_2[flu[0]] == True:
                self.fluEnabledButtonsList[flu[0]].setStyleSheet(STYLEWHITE)
                self.fluDisabledButtonsList[flu[0]].setStyleSheet(STYLEWRITE)
            else:
                self.fluEnabledButtonsList[flu[0]].setStyleSheet(STYLEWRITE)
                self.fluDisabledButtonsList[flu[0]].setStyleSheet(STYLEWHITE)

    def enableFluButton_clicked(self, position):
        FLUCONFIG_2[2 * position[0] + position[1]] = True
        print FLUCONFIG_2
        self.fluEnabledButtonsList[2 * position[0] + position[1]].setStyleSheet(STYLEWHITE)
        self.fluDisabledButtonsList[2 * position[0] + position[1]].setStyleSheet(STYLEWRITE)
        self.showOrHideFluLines()

    def disableFluButton_clicked(self, position):
        FLUCONFIG_2[2* position[0] +  position[1]] = False
        print FLUCONFIG_2
        self.fluEnabledButtonsList[2 * position[0] + position[1]].setStyleSheet(STYLEWRITE)
        self.fluDisabledButtonsList[2 * position[0] + position[1]].setStyleSheet(STYLEWHITE)
        self.showOrHideFluLines()

    def showOrHideFluLines(self):
        print len(self.vesselFluLinesList)
        print len(self.vesselOneFluGroupLines[1])

        for fluLinesGroup in enumerate(self.vesselFluLinesList):
            if FLUCONFIG_2[fluLinesGroup[0]] == True:

                for lineGroup in self.vesselFluLinesList[fluLinesGroup[0]]:
                    for line in lineGroup: line.show()
            else:
                for lineGroup in self.vesselFluLinesList[fluLinesGroup[0]]:
                    for line in lineGroup: line.hide()

        # if FLUCONFIG_2[0] == True:
        #     for line in self.vesselOneFluGroupLines:
        #         line.show()
        # elif FLUCONFIG_2[1] == False:
        #     for line in self.vesselOneFluGroupLines:
        #         line.hide()


    def initUI(self):

        NO_BEAMS = 16

        self.setGeometry(50, 50, 1000, 800)
        self.setWindowTitle('OSS UI Testing')
        self.setAutoFillBackground(True)
        self.setStyleSheet("QWidget {background: 'black';}")

        # Groupbox for linking FLUs
        self.fluGroupBox = QtWidgets.QGroupBox(self)
        self.fluGroupBox.setGeometry(QtCore.QRect(20, 100, 500, 500))
        self.fluGroupBox.setTitle("Link Settings and E-Stop")
        self.fluGroupBox.setStyleSheet("color:white;")

        STARTING_X = 35
        STARTING_Y = 125
        BOX_WIDTH = 220
        BOX_HIGHT = 100
        SPACER = 20
        BEAMBOX_SIZE = 30
        BEAMLABEL_SIZE = 25
        STARTING_BEAMBOX_X = 215
        STARTING_BEAMBOX_Y = 143

        BUTTON_HOR = 90
        BUTTON_VERT = 23
        STYLEWRITE = "background:#a6a6a6; \n"  "color: black;\n"       "border: 5px solid #a6a6a6;\n"

        beamIDtext = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]

        self.fontBeamLabel = QtGui.QFont()
        self.fontBeamLabel.setPointSize(15)
        self.fontBeamLabel.setWeight(25)
        self.fontBeamLabel.setFamily("Arial")

        # drawing FLU lines

        LINE_STARTING_X = 800
        LINE_STARTING_Y = 200
        LINE_WIDTH = 2
        VERT_LINE_LENGTH = 35
        HOR_LINE_LENGTH = 10


        positions = [(i,j) for i in range(4) for j in range(2)]
        x = 8
        y = 0
        for position in positions:
            # draw FLU boxes
            self.smallBox = QtWidgets.QGroupBox(self)
            self.smallBox.setGeometry(QtCore.QRect(STARTING_X + position[1] * BOX_WIDTH + position[1] * SPACER, STARTING_Y + position[0] * (BOX_HIGHT + SPACER), BOX_WIDTH, BOX_HIGHT))

            # draw Link FLU labels
            self.linkFLUlabel = QtWidgets.QLabel(self)
            self.linkFLUlabel.setGeometry(QtCore.QRect(STARTING_X + 50 + position[1] * (BOX_WIDTH + 55), STARTING_Y + 15 + position[0] * (BOX_HIGHT + SPACER), 80, 20))
            self.linkFLUlabel.setText("Link FLU")
            self.linkFLUlabel.setFont(self.fontBeamLabel)
            self.linkFLUlabel.setStyleSheet("color:#cccccc")

            # draw Enable/Disable buttons
            self.enableFluButton = QtWidgets.QPushButton(self)
            self.enableFluButton.setGeometry(QtCore.QRect(STARTING_X + 20 + position[1] * (BOX_WIDTH + 55), STARTING_Y + 60 + position[0] * (BOX_HIGHT + SPACER), BUTTON_HOR-20, BUTTON_VERT))
            self.enableFluButton.setText("ENABLED")
            self.enableFluButton.setStyleSheet(STYLEWRITE)
            self.enableFluButton.clicked.connect(lambda ignore, x=position: self.enableFluButton_clicked(x))
            self.fluEnabledButtonsList.append(self.enableFluButton)

            self.disableFluButton = QtWidgets.QPushButton(self)
            self.disableFluButton.setGeometry(QtCore.QRect(STARTING_X + 100 + position[1] * (BOX_WIDTH + 55), STARTING_Y + 60 + position[0] * (BOX_HIGHT + SPACER), BUTTON_HOR-20, BUTTON_VERT))
            self.disableFluButton.setText("DISABLED")
            self.disableFluButton.setStyleSheet(STYLEWRITE)
            self.disableFluButton.clicked.connect(lambda ignore, x=position: self.disableFluButton_clicked(x))
            self.fluDisabledButtonsList.append(self.disableFluButton)

            # draw P and S upper boxes
            self.beamBoxUpper = QtWidgets.QGroupBox(self)
            self.beamBoxUpper.setGeometry(QtCore.QRect(STARTING_BEAMBOX_X + 68 * position[1], STARTING_BEAMBOX_Y + position[0] * (BOX_HIGHT + SPACER), BEAMBOX_SIZE, BEAMBOX_SIZE))
            self.beamBoxUpper.setStyleSheet("color:#cccccc")

            # draw P and S lower boxes
            self.beamBoxLower = QtWidgets.QGroupBox(self)
            self.beamBoxLower.setGeometry(QtCore.QRect(STARTING_BEAMBOX_X + 68 * position[1], STARTING_BEAMBOX_Y + position[0] * (
            BOX_HIGHT + SPACER) + BEAMBOX_SIZE + 3, BEAMBOX_SIZE, BEAMBOX_SIZE))
            self.beamBoxLower.setStyleSheet("color:#cccccc")

            # put lables in the boxes
            if position[1] == 0: #P beams
                self.beamLabelUpper = QtWidgets.QLabel(self)
                self.beamLabelUpper.setGeometry(QtCore.QRect(STARTING_BEAMBOX_X + 3, STARTING_BEAMBOX_Y + 3 + position[0] * (BOX_HIGHT + SPACER),BEAMLABEL_SIZE, BEAMLABEL_SIZE))
                self.beamLabelUpper.setText(beamIDtext[x])
                self.beamLabelUpper.setFont(self.fontBeamLabel)
                self.beamLabelUpper.setStyleSheet("color:#cccccc")

                self.beamLabelLower = QtWidgets.QLabel(self)
                self.beamLabelLower.setGeometry(QtCore.QRect(STARTING_BEAMBOX_X + 3, STARTING_BEAMBOX_Y + 11 + BEAMLABEL_SIZE + position[0] * (BOX_HIGHT + SPACER), BEAMLABEL_SIZE,BEAMLABEL_SIZE))
                self.beamLabelLower.setText(beamIDtext[x+1])
                self.beamLabelLower.setFont(self.fontBeamLabel)
                self.beamLabelLower.setStyleSheet("color:#cccccc")

                x += 2

            if position[1] == 1:  # S beams
                self.beamLabelUpper = QtWidgets.QLabel(self)
                self.beamLabelUpper.setGeometry(QtCore.QRect(STARTING_BEAMBOX_X + 71, STARTING_BEAMBOX_Y + 3 + position[0] * (BOX_HIGHT + SPACER),BEAMLABEL_SIZE, BEAMLABEL_SIZE))
                self.beamLabelUpper.setText(beamIDtext[y])
                self.beamLabelUpper.setFont(self.fontBeamLabel)
                self.beamLabelUpper.setStyleSheet("color:#cccccc")

                self.beamLabelLower = QtWidgets.QLabel(self)
                self.beamLabelLower.setGeometry(QtCore.QRect(STARTING_BEAMBOX_X + 71, STARTING_BEAMBOX_Y + 11 + BEAMLABEL_SIZE + position[0] * (BOX_HIGHT + SPACER), BEAMLABEL_SIZE,BEAMLABEL_SIZE))
                self.beamLabelLower.setText(beamIDtext[y+1])
                self.beamLabelLower.setFont(self.fontBeamLabel)
                self.beamLabelLower.setStyleSheet("color:#cccccc")

                y += 2

            # Draw FLU lines

            self.FluLineVert = QtWidgets.QLabel(self)
            self.FluLineVert.setGeometry(QtCore.QRect(LINE_STARTING_X + position[1] * (50 + HOR_LINE_LENGTH + LINE_WIDTH), LINE_STARTING_Y + position[0]* 50, LINE_WIDTH, VERT_LINE_LENGTH))
            self.FluLineVert.setStyleSheet("background-color:#7AAFFF")
            # self.vesselOneFluGroupLines.append(self.FluLineVert)

            self.FluLineHorUp = QtWidgets.QLabel(self)
            self.FluLineHorUp.setGeometry(QtCore.QRect(LINE_STARTING_X + LINE_WIDTH + position[1] * 50, LINE_STARTING_Y + position[0]* 50, HOR_LINE_LENGTH, LINE_WIDTH))
            self.FluLineHorUp.setStyleSheet("background-color:#7AAFFF")
            # self.vesselOneFluGroupLines.append(self.FluLineHorUp)

            self.FluLineHorDwn = QtWidgets.QLabel(self)
            self.FluLineHorDwn.setGeometry(QtCore.QRect(LINE_STARTING_X + LINE_WIDTH + position[1] * 50, LINE_STARTING_Y + VERT_LINE_LENGTH - LINE_WIDTH + position[0]* 50, HOR_LINE_LENGTH, LINE_WIDTH))
            self.FluLineHorDwn.setStyleSheet("background-color:#7AAFFF")
            # self.vesselOneFluGroupLines.append(self.FluLineHorDwn)

            self.vesselOneFluGroupLines.append([self.FluLineVert, self.FluLineHorUp, self.FluLineHorDwn])

            self.vesselFluLinesList.append(self.vesselOneFluGroupLines)



#############

        self.fluButtonsColorsRefresh()
        self.showOrHideFluLines()
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())