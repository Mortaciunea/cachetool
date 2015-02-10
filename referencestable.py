import pymel.core as pm
import os,fnmatch

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui

from exportcachejob import ExportCacheJob
referencesTableTitles = ['RIG file','SHADE file','Cache rig ?']


class ReferencesTable(QtGui.QWidget):
    def __init__(self,parent=None):
        super(ReferencesTable,self).__init__(parent)
        
        self.cacheJobs = []
        self.rigShadePairs = {}
        self.rigFiles = []
        self.shadeFiles=[]
        
        mainLayout = QtGui.QVBoxLayout()

        self.setLayout(mainLayout)

        self.referencesTable = self.createReferencesTable()
        self.populateReferences(0)
        #self.camerasGroup = self.createCamerasGroup()
        mainLayout.addWidget(self.referencesTable)

        self.createJobBtn = QtGui.QPushButton('Create Cache Job')
        mainLayout.addWidget(self.createJobBtn)

        self.createJobBtn.clicked.connect(self.createCacheJob)

    def createReferencesTable(self):
        colNum = len(referencesTableTitles)

        table = QtGui.QTableWidget(0,colNum)

        hheader = QtGui.QHeaderView(QtCore.Qt.Orientation.Horizontal)
        hheader.setStretchLastSection(True)
        hheader.setClickable(1)
        table.setHorizontalHeader(hheader)
        table.setHorizontalHeaderLabels(referencesTableTitles)
        table.setAlternatingRowColors(1)
        return table

    def populateReferences(self,inScene):
        if inScene:
            self.sceneReferences = pm.getReferences()
            self.loadedReferences = []

            for item in self.sceneReferences:
                if self.sceneReferences[item].isLoaded():
                    self.loadedReferences.append([self.sceneReferences[item].isLoaded(),item,self.sceneReferences[item].path])

            self.referencesTable.setRowCount(len(self.loadedReferences))
            for i in range(len(self.loadedReferences)):
                for j in range(3):
                    #print self.loadedReferences[i][j]
                    item = QtGui.QTableWidgetItem(str(self.loadedReferences[i][j]))
                    item.setFlags(~QtCore.Qt.ItemIsEditable)
                    self.referencesTable.setItem(i, j, item)
        else:
            rigSuffix= pm.optionVar.get('rigString')
            cacheSuffix = pm.optionVar.get('cacheString')            
            rigsFolderString = pm.optionVar.get('rigsFolderString')
            shadeFolderString = pm.optionVar.get('shadeFolderString')
            
            if os.path.isdir(rigsFolderString):
                rigsPath = os.path.abspath(rigsFolderString)
                for root, dirnames, filenames in os.walk(rigsPath):
                    for filename in fnmatch.filter(filenames, '*' + rigSuffix + '*.*'):
                        if filename.endswith('.ma') or filename.endswith('.mb'):
                            shadeFile = self.getShadeFile(filename)
                            self.rigShadePairs[filename] = shadeFile 
            
                print self.rigShadePairs
        pairsLen = len(self.rigShadePairs)
        if pairsLen:
            self.referencesTable.setRowCount(pairsLen)
            i=0
            for rig,shade in self.rigShadePairs.iteritems():
                item = QtGui.QTableWidgetItem(rig)
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                self.referencesTable.setItem(i, 0, item)
 
                item = QtGui.QTableWidgetItem(shade)
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                self.referencesTable.setItem(i, 1, item)
                
                if shade == 'None':
                    item = QtGui.QTableWidgetItem('No')
                else:
                    item = QtGui.QTableWidgetItem('Yes')
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                self.referencesTable.setItem(i, 2, item)                
                i+=1
                
            self.referencesTable.resizeColumnsToContents()
            self.referencesTable.setSortingEnabled(1)        

    def getShadeFile(self,rigFile):
        rigSuffix= pm.optionVar.get('rigString')
        shadeSuffix = pm.optionVar.get('shadeString')            
        
        shadeFolderString = pm.optionVar.get('shadeFolderString') 
        if os.path.isdir(shadeFolderString):
            shadePath = os.path.abspath(shadeFolderString)
            print shadePath 
            for root, dirnames, filenames in os.walk(shadePath):
                if rigFile.replace(rigSuffix,shadeSuffix) in filenames:
                    return rigFile.replace(rigSuffix,shadeSuffix)
                else:
                    return 'None'

    def createCacheJob(self):
        self.cacheJobs.append(ExportCacheJob(animFile=pm.sceneName()))
