import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import pymel.core as pm

class CacheSettingsUI(QtGui.QDialog):
    def __init__(self,parent=None):
        super(CacheSettingsUI,self).__init__(parent)
        mainLayout = QtGui.QVBoxLayout()

        grp1 = QtGui.QGroupBox('Suffixes')
        grp1Layout = QtGui.QVBoxLayout()

        rigRowLayout = QtGui.QHBoxLayout()
        rigLabel = QtGui.QLabel('Rig file suffix')
        self.rigEdit = QtGui.QLineEdit()
        rigRowLayout .addWidget(rigLabel)
        rigRowLayout .addWidget(self.rigEdit)

        shadeRowLayout = QtGui.QHBoxLayout()
        shadeLabel = QtGui.QLabel('Shade file suffix')
        self.shadeEdit = QtGui.QLineEdit()
        shadeRowLayout .addWidget(shadeLabel)
        shadeRowLayout .addWidget(self.shadeEdit)        

        animRowLayout = QtGui.QHBoxLayout()
        animLabel = QtGui.QLabel('Anim file suffix')
        self.animFileEdit = QtGui.QLineEdit()
        animRowLayout  .addWidget(animLabel)
        animRowLayout  .addWidget(self.animFileEdit) 

        geoRowLayout = QtGui.QHBoxLayout()
        geoLabel = QtGui.QLabel('Geometry suffix')
        self.geoFileEdit = QtGui.QLineEdit()
        geoRowLayout.addWidget(geoLabel)
        geoRowLayout.addWidget(self.geoFileEdit) 
        
        lightingRowLayout = QtGui.QHBoxLayout()
        lightingLabel = QtGui.QLabel('Lighting file suffix')
        self.lightingFileEdit = QtGui.QLineEdit()
        lightingRowLayout.addWidget(lightingLabel)
        lightingRowLayout.addWidget(self.lightingFileEdit) 
        
        grp1Layout.addLayout(rigRowLayout)
        grp1Layout.addLayout(shadeRowLayout)
        grp1Layout.addLayout(animRowLayout)
        grp1Layout.addLayout(lightingRowLayout)
        grp1Layout.addLayout(geoRowLayout)

        grp1.setLayout(grp1Layout)

        grp2 = QtGui.QGroupBox('Folders')
        grp2Layout = QtGui.QVBoxLayout()
        #anim folder row
        animLayout = QtGui.QHBoxLayout()
        animFolderLabel = QtGui.QLabel('Final Animations')
        self.animFolderEdit = QtGui.QLineEdit()
        self.animBrowseBtn = QtGui.QPushButton('Browse')
        animLayout.addWidget(animFolderLabel)
        animLayout.addWidget(self.animFolderEdit)
        animLayout.addWidget(self.animBrowseBtn)
        self.animBrowseBtn.clicked.connect(lambda:self.getFolder('animations'))
        #rigs folder row
        rigsLayout = QtGui.QHBoxLayout()
        rigsFolderLabel = QtGui.QLabel('Rigs')
        self.rigsFolderEdit = QtGui.QLineEdit()
        self.rigsBrowseBtn = QtGui.QPushButton('Browse')
        rigsLayout.addWidget(rigsFolderLabel)
        rigsLayout.addWidget(self.rigsFolderEdit)
        rigsLayout.addWidget(self.rigsBrowseBtn)
        self.rigsBrowseBtn.clicked.connect(lambda:self.getFolder('rigs'))
        #shade folders row
        shadeLayout = QtGui.QHBoxLayout()
        shadeFolderLabel = QtGui.QLabel('Shade')
        self.shadeFolderEdit = QtGui.QLineEdit()
        self.shadeBrowseBtn = QtGui.QPushButton('Browse')
        shadeLayout.addWidget(shadeFolderLabel)
        shadeLayout.addWidget(self.shadeFolderEdit)
        shadeLayout.addWidget(self.shadeBrowseBtn)
        self.shadeBrowseBtn.clicked.connect(lambda:self.getFolder('shade'))
        #lighting folders row
        lightingLayout = QtGui.QHBoxLayout()
        lightingFolderLabel = QtGui.QLabel('Lighting')
        self.lightingFolderEdit = QtGui.QLineEdit()
        self.lightingBrowseBtn = QtGui.QPushButton('Browse')
        lightingLayout.addWidget(lightingFolderLabel)
        lightingLayout.addWidget(self.lightingFolderEdit)
        lightingLayout.addWidget(self.lightingBrowseBtn)
        self.lightingBrowseBtn.clicked.connect(lambda:self.getFolder('lighting'))
        
        grp2Layout.addLayout(animLayout)
        grp2Layout.addLayout(rigsLayout)
        grp2Layout.addLayout(shadeLayout)
        grp2Layout.addLayout(lightingLayout)
        grp2.setLayout(grp2Layout)
        
        self.saveSettingsBtn = QtGui.QPushButton('Save Settings')
        self.saveSettingsBtn.clicked.connect(self.saveSettings)

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        

        mainLayout.addWidget(grp1)
        mainLayout.addWidget(grp2)
        mainLayout.addWidget(self.saveSettingsBtn)
        mainLayout.addItem(spacerItem)

        self.setLayout(mainLayout)

        self.getCacheVars()
        print pm.workspace.path
        self.setWindowTitle('Tool settings')

    def getCacheVars(self):
        rigString = pm.optionVar.get('rigString','Enter rig files suffix')
        shadeString = pm.optionVar.get('shadeString','Enter shade files suffix')
        animString = pm.optionVar.get('animString','Enter anim files suffix')
        geoString = pm.optionVar.get('geoString','Enter mesh suffix')
        lightingString = pm.optionVar.get('lightingString','Enter lighting files suffix')
        
        animFolderString = pm.optionVar.get('animFolderString','Path to the animations folder')
        rigsFolderString = pm.optionVar.get('rigsFolderString','Path to the rigs folder')
        shadeFolderString = pm.optionVar.get('shadeFolderString','Path to the shade folder')
        lightingFolderString = pm.optionVar.get('lightingFolderString','Path to the lighting folder')
        
        

        self.rigEdit.setText(rigString)
        self.shadeEdit.setText(shadeString)
        self.animFileEdit.setText(animString)
        self.geoFileEdit.setText(geoString)
        self.lightingFileEdit.setText(lightingString)
        
        self.animFolderEdit.setText(animFolderString)
        self.rigsFolderEdit.setText(rigsFolderString)
        self.shadeFolderEdit.setText(shadeFolderString)
        self.lightingFolderEdit.setText(lightingFolderString)
    '''
    def closeEvent(self,event):
        self.saveSettings()
    '''
    def getFolder(self,folder):
        projectPath = pm.workspace.path
        path = ''
        try:
            path = pm.fileDialog2(dir=projectPath,ds=2,fm=3,okc='Select Folder')[0]
        except:
            pm.warning('No folder was selected, defaulting to workspace folder')
            path = projectPath


        if folder == 'animations':
            self.animFolderEdit.setText(path)
        elif folder == 'rigs':
            self.rigsFolderEdit.setText(path)
        elif folder == 'shade':
            self.shadeFolderEdit.setText(path)
        elif folder == 'lighting':
            self.lightingFolderEdit.setText(path)
            
    def saveSettings(self):
        pm.optionVar['rigString'] = self.rigEdit.text()
        pm.optionVar['shadeString'] = self.shadeEdit.text()
        pm.optionVar['animString'] = self.animFileEdit.text()
        pm.optionVar['geoString'] = self.geoFileEdit.text()
        pm.optionVar['lightingString'] = self.lightingFileEdit.text()
        pm.optionVar['animFolderString'] = self.animFolderEdit.text()
        pm.optionVar['rigsFolderString'] = self.rigsFolderEdit.text()
        pm.optionVar['shadeFolderString'] = self.shadeFolderEdit.text()   
        pm.optionVar['lightingFolderString'] = self.lightingFolderEdit.text()
        
        cacheTool =  self.parent()
        print cacheTool
        
    def deleteOptionVars(self):
        pm.optionVar(remove= 'rigString')
        pm.optionVar(remove= 'shadeString')
        pm.optionVar(remove= 'animString')
        pm.optionVar(remove= 'geoString')
        pm.optionVar(remove= 'lightingString')
        pm.optionVar(remove= 'animFolderString')
        pm.optionVar(remove= 'rigsFolderString')
        pm.optionVar(remove= 'shadeFolderString')
        pm.optionVar(remove= 'lightingFolderString')