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
        self.setttingsFolder  = self.getSettingsFolder()
        self.pairsFile = 'rig2shade.txt'

        mainLayout = QtGui.QVBoxLayout()

        self.setLayout(mainLayout)

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
        
        #REFERENCES TABLE
        self.referencesTable = self.createReferencesTable()
        self.populateReferences(0)
        self.addPairsBtn = QtGui.QPushButton('Add pairs')
        
        #self.camerasGroup = self.createCamerasGroup()
        
        mainLayout.addWidget(self.selectGrp)
        mainLayout.addWidget(self.referencesTable)
        mainLayout.addWidget(self.addPairsBtn)

        self.addPairsBtn.clicked.connect(self.savePairs)
        self.referencesTable.itemDoubleClicked.connect( self.toggleCacheStatus )
        self.selectAllBtn.clicked.connect(self.selectAll)
        self.selectNoneBtn.clicked.connect(self.selectNone)
        self.selectInvertBtn.clicked.connect(self.selectInvert)        
        

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
            rigSuffix= pm.optionVar.get('rigString','')
            cacheSuffix = pm.optionVar.get('cacheString','')
            rigsFolderString = pm.optionVar.get('rigsFolderString','')
            shadeFolderString = pm.optionVar.get('shadeFolderString','')

            if os.path.isdir(rigsFolderString):
                rigsPath = os.path.abspath(rigsFolderString)
                for root, dirnames, filenames in os.walk(rigsPath):
                    for filename in fnmatch.filter(filenames, '*' + rigSuffix + '*.*'):
                        if filename.endswith('.ma') or filename.endswith('.mb'):
                            shadeFile = self.getShadeFile(filename)
                            rigFile = os.path.join(root,filename)
                            if shadeFile is not 'None':
                                self.rigShadePairs[rigFile] = shadeFile 

        pairsLen = len(self.rigShadePairs)
        if pairsLen:
            self.referencesTable.setRowCount(pairsLen)
            i=0
            for rig,shade in self.rigShadePairs.iteritems():
                if shade is not 'None':
                    item = QtGui.QTableWidgetItem(rig)
                    item.setFlags(~QtCore.Qt.ItemIsEditable)
                    self.referencesTable.setItem(i, 0, item)
    
                    item = QtGui.QTableWidgetItem(shade)
                    item.setFlags(~QtCore.Qt.ItemIsEditable)
                    self.referencesTable.setItem(i, 1, item)
                    
    
                    item = QtGui.QTableWidgetItem('No')
    
                    item.setFlags(~QtCore.Qt.ItemIsEditable)
                    item.setBackground(QtGui.QColor(180,0,0))
                    self.referencesTable.setItem(i,2,item)                    
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
    
                    self.referencesTable.setItem(i, 2, item)                
                    i+=1
            
            self.addUserPair()
            self.referencesTable.resizeColumnsToContents()
            self.referencesTable.setSortingEnabled(1)        

    def getShadeFile(self,rigFile):
        rigSuffix= pm.optionVar.get('rigString')
        shadeSuffix = pm.optionVar.get('shadeString')            

        shadeFolderString = pm.optionVar.get('shadeFolderString') 
        if os.path.isdir(shadeFolderString):
            shadePath = os.path.abspath(shadeFolderString)
            #print shadePath 
            for root, dirnames, filenames in os.walk(shadePath):
                if rigFile.replace(rigSuffix,shadeSuffix) in filenames:
                    shadeFile = os.path.join(root,rigFile.replace(rigSuffix,shadeSuffix))
                    return shadeFile
                else:
                    return 'None'

    def savePairs(self):
        settingsFile = os.path.join(self.setttingsFolder,self.pairsFile)

        
        rigFile = self.pairBrowse('Rig')
        shadeFile = self.pairBrowse('Shade')
        
        if rigFile and shadeFile:
            if not os.path.isfile(settingsFile):
                f = open(settingsFile, 'w')
            f = open(settingsFile, 'a')
            pair = rigFile + ">" + shadeFile + '\n'
            f.write(pair)
            self.addPair(rigFile,shadeFile)
            f.close()
        

    def getSettingsFolder(self):
        workspace = pm.workspace.path
        settingsFolder  = os.path.join(workspace,'cachetool')
        if not os.path.isdir(settingsFolder):
            os.mkdir(settingsFolder)

        return settingsFolder

    def pairBrowse(self,which):
        projectPath = pm.workspace.path
        okc = caption = ''
        if which == 'Rig':
            okc = caption = 'Rig'
        elif which == 'Shade':
            okc = caption = 'Shade'

        mayaFilesFilter = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb)"
        mayaFile = ''
        try:
            mayaFile = pm.fileDialog2(dir=projectPath,ds=2,fm=1,okc=okc,caption = caption,ff=mayaFilesFilter)[0]
        except:
            pm.warning('No file was selected')

        return os.path.abspath(mayaFile)
            
    def addPair(self,rigFile,shadeFile):
        self.rigShadePairs[rigFile] = shadeFile
        self.referencesTable.setSortingEnabled(0)
        rowCount = self.referencesTable.rowCount()
        #self.referencesTable.insertRow(rowCount )
        self.referencesTable.insertRow(rowCount)
        
        item = QtGui.QTableWidgetItem(rigFile)
        item.setFlags(~QtCore.Qt.ItemIsEditable)
        self.referencesTable.setItem(rowCount, 0, item)

        item = QtGui.QTableWidgetItem(shadeFile)
        item.setFlags(~QtCore.Qt.ItemIsEditable)
        self.referencesTable.setItem(rowCount, 1, item)


        item = QtGui.QTableWidgetItem('No')
        item.setFlags(~QtCore.Qt.ItemIsEditable)
        item.setBackground(QtGui.QColor(180,0,0))
        self.referencesTable.setItem(rowCount,2,item)        
        item.setTextAlignment(QtCore.Qt.AlignCenter)

        self.referencesTable.setItem(rowCount, 2, item) 
        self.referencesTable.setSortingEnabled(0)

    def addUserPair(self):
        settingsFolder = self.getSettingsFolder()
        userPairs = os.path.join(settingsFolder,self.pairsFile)
        
        rowCount = self.referencesTable.rowCount()
        if os.path.isfile(userPairs):
            with open(userPairs) as f:
                for line in f:
                    rigFile,shadeFile = line.split('>')
                    self.addPair(rigFile, shadeFile)
                    
    
    def toggleCacheStatus(self, tableWidgetItem ):
        row = tableWidgetItem.row()
        currentState = self.referencesTable.item(row,2).text()
        if currentState == 'Yes':
            item = QtGui.QTableWidgetItem('No')
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(180,0,0))
            self.referencesTable.setItem(row,2,item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
        elif currentState == 'No':
            item = QtGui.QTableWidgetItem('Yes')
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(0,180,0))
            self.referencesTable.setItem(row,2,item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            
    def selectAll(self):
        rowCount = self.referencesTable.rowCount()
        for i in range(rowCount):
            item = QtGui.QTableWidgetItem('Yes')
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(0,180,0))
            self.referencesTable.setItem(i,2,item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            


    def selectNone(self):
        rowCount = self.referencesTable.rowCount()
        for i in range(rowCount):
            item = QtGui.QTableWidgetItem('No')
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(180,0,0))
            self.referencesTable.setItem(i,2,item) 
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            

    def selectInvert(self):
        rowCount = self.referencesTable.rowCount()
        for i in range(rowCount):
            currentState = self.referencesTable.item(i,2).text()
            if currentState == 'Yes':
                item = QtGui.QTableWidgetItem('No')
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(180,0,0))
                self.referencesTable.setItem(i,2,item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
            elif currentState == 'No':
                item = QtGui.QTableWidgetItem('Yes')
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(0,180,0))
                self.referencesTable.setItem(i,2,item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
