import pymel.core as pm
import os
import fnmatch
import re

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui


animationsTableTitles = ['Animation File','Export Cache?']



class AnimationFilesTable(QtGui.QWidget):
    def __init__(self,parent=None):
        super(AnimationFilesTable,self).__init__(parent)

        self.finalAnimationFiles = {}
        self.mainLayout = QtGui.QVBoxLayout()

        self.setLayout(self.mainLayout)
        
        #Get Final Animations button
        self.scanProjectBtn = QtGui.QPushButton('Get Final Animations')
        
        #Select group
        self.selectGrp = QtGui.QGroupBox('Selection')
        self.selectGrpLayout = QtGui.QHBoxLayout()
        self.selectAllBtn = QtGui.QPushButton('Select All')
        self.selectNoneBtn = QtGui.QPushButton('Select None')
        self.selectInvertBtn = QtGui.QPushButton('Invert selection')        
        self.selectGrpLayout.addWidget(self.selectAllBtn)
        self.selectGrpLayout.addWidget(self.selectNoneBtn)
        self.selectGrpLayout.addWidget(self.selectInvertBtn)
        self.selectGrp.setLayout(self.selectGrpLayout)
        
        #Refine animation list group
 
        self.refineGrp = QtGui.QGroupBox('Refine list group')
        self.refineLayout = QtGui.QHBoxLayout()
        self.refineLabel = QtGui.QLabel('Pattern string')
        self.refineEdit = QtGui.QLineEdit()
        self.refineBtn = QtGui.QPushButton('Refine list')
        self.restoreAllBtn = QtGui.QPushButton('Restore to full list')
        self.refineLayout.addWidget(self.refineLabel)
        self.refineLayout.addWidget(self.refineEdit)
        self.refineLayout.addWidget(self.refineBtn)
        self.refineLayout.addWidget(self.restoreAllBtn)
        self.refineGrp.setLayout(self.refineLayout)
        

        #Final Animations Table
        self.animFilesTable = self.createAnimTable()
        
        self.spacerItem = QtGui.QSpacerItem(1, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        
        self.mainLayout.addWidget(self.scanProjectBtn)
        self.mainLayout.addWidget(self.selectGrp)
        self.mainLayout.addWidget(self.refineGrp)
        self.mainLayout.addWidget(self.animFilesTable)
        #self.mainLayout.addItem(self.patternLayout)
        
        #Buttons connections
        self.scanProjectBtn.clicked.connect(self.getFinalAnimations)
        self.selectAllBtn.clicked.connect(self.selectAll)
        self.selectNoneBtn.clicked.connect(self.selectNone)
        self.selectInvertBtn.clicked.connect(self.selectInvert)

        self.animFilesTable.itemDoubleClicked.connect( self.toggleExportStatus )
        self.refineBtn.clicked.connect(self.refineAnimList)
        self.restoreAllBtn.clicked.connect(self.restoreAnimList)



    def createAnimTable(self):
        colNum = len(animationsTableTitles)

        table = QtGui.QTableWidget(0,colNum)

        hheader = QtGui.QHeaderView(QtCore.Qt.Orientation.Horizontal)
        hheader.setStretchLastSection(True)
        hheader.setClickable(True)
        table.setHorizontalHeader(hheader)
        table.setHorizontalHeaderLabels(animationsTableTitles)

        return table

    def getFinalAnimations(self):
        workspace = pm.workspace.path

        animSuffix = pm.optionVar.get('animString','ANIM')
        animFolderString = pm.optionVar.get('animFolderString','Path to the animations')

        finalAnimations = []
        if os.path.isdir(os.path.abspath(animFolderString)):
            path = os.path.abspath(animFolderString)
            for root, dirnames, filenames in os.walk(path):
                for filename in fnmatch.filter(filenames, '*' + animSuffix + '.ma'):
                    #finalAnimations.append(os.path.join(root, filename))
                    self.finalAnimationFiles[os.path.join(root, filename)] = 'No'

        #self.animFilesTable.setRowCount(len(finalAnimations))
        self.animFilesTable.setRowCount(len(self.finalAnimationFiles))
        i=0
        for k,v in self.finalAnimationFiles.iteritems():
            item = QtGui.QTableWidgetItem(k)
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            self.animFilesTable.setItem(i, 0, item)

            item = QtGui.QTableWidgetItem(v)
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setBackground(QtGui.QColor(180,0,0))
            self.animFilesTable.setItem(i, 1, item)
            i+=1

        self.animFilesTable.resizeColumnsToContents()
        #self.animFilesTable.setSortingEnabled(1)


    def selectAll(self):
        rowCount = self.animFilesTable.rowCount()
        for i in range(rowCount):
            item = QtGui.QTableWidgetItem('Yes')
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(0,180,0))
            self.animFilesTable.setItem(i,1,item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.finalAnimationFiles[self.animFilesTable.item(i,0).text()]='Yes'
            


    def selectNone(self):
        rowCount = self.animFilesTable.rowCount()
        for i in range(rowCount):
            item = QtGui.QTableWidgetItem('No')
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(180,0,0))
            self.animFilesTable.setItem(i,1,item) 
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.finalAnimationFiles[self.animFilesTable.item(i,0).text()]='No'

    def selectInvert(self):
        rowCount = self.animFilesTable.rowCount()
        for i in range(rowCount):
            currentState = self.animFilesTable.item(i,1).text()
            if currentState == 'Yes':
                item = QtGui.QTableWidgetItem('No')
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(180,0,0))
                self.animFilesTable.setItem(i,1,item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.finalAnimationFiles[self.animFilesTable.item(i,0).text()]='No'                
            elif currentState == 'No':
                item = QtGui.QTableWidgetItem('Yes')
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(0,180,0))
                self.animFilesTable.setItem(i,1,item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.finalAnimationFiles[self.animFilesTable.item(i,0).text()]='Yes'

    def toggleExportStatus(self, tableWidgetItem ):
        #self.animFilesTable.setSortingEnabled(0)
        column =  tableWidgetItem.column()
        if column == 1:
            row = tableWidgetItem.row()
            currentState = self.animFilesTable.item(row,1).text()
            if currentState == 'Yes':
                item = QtGui.QTableWidgetItem('No')
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(180,0,0))
                self.animFilesTable.setItem(row,1,item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.finalAnimationFiles[self.animFilesTable.item(row,0).text()]='No'
                
            elif currentState == 'No':
                item = QtGui.QTableWidgetItem('Yes')
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(0,180,0))
                self.animFilesTable.setItem(row,1,item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.finalAnimationFiles[self.animFilesTable.item(row,0).text()]='Yes'
        
        #self.animFilesTable.setSortingEnabled(1)
    
    def refineAnimList(self):
        print self.refineEdit.text()
        patterns = self.refineEdit.text().split(';')
        #remove duplicates
        patterns = list(set(patterns))
        print patterns
        
        refineList = []
        
        animFiles = self.finalAnimationFiles.keys()

        for pat in patterns:
            for anim in animFiles:
                if pat in anim:
                    refineList.append(anim)
                    
        self.animFilesTable.clearContents()
        self.animFilesTable.setRowCount(len(refineList))
        #self.animFilesTable.setSortingEnabled(0)
        for i in range(len(refineList)):
            item = QtGui.QTableWidgetItem(str(refineList[i]))
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            self.animFilesTable.setItem(i, 0, item)

            currentState = self.finalAnimationFiles[refineList[i]]
            if currentState == 'No':
                item = QtGui.QTableWidgetItem('No')
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(180,0,0))
                self.animFilesTable.setItem(i,1,item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
            elif currentState == 'Yes':
                item = QtGui.QTableWidgetItem('Yes')
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(0,180,0))
                self.animFilesTable.setItem(i,1,item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
        #self.animFilesTable.setSortingEnabled(1)
        
    def restoreAnimList(self):
        self.animFilesTable.clearContents()

        self.refineEdit.setText('')
        self.animFilesTable.setSortingEnabled(0)
        self.animFilesTable.setRowCount(len(self.finalAnimationFiles))
        i=0
        for k,v in self.finalAnimationFiles.iteritems():
            item = QtGui.QTableWidgetItem(k)
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            self.animFilesTable.setItem(i, 0, item)

            currentState = v
            if currentState == 'No':
                item = QtGui.QTableWidgetItem('No')
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(180,0,0))
                self.animFilesTable.setItem(i,1,item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
            elif currentState == 'Yes':
                item = QtGui.QTableWidgetItem('Yes')
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(0,180,0))
                self.animFilesTable.setItem(i,1,item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
            i+=1
        #self.animFilesTable.setSortingEnabled(1)