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

        grp1Layout.addLayout(rigRowLayout)
        grp1Layout.addLayout(shadeRowLayout)
        grp1Layout.addLayout(animRowLayout)

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
        
        grp2Layout.addLayout(animLayout)
        grp2Layout.addLayout(rigsLayout)
        grp2Layout.addLayout(shadeLayout)
        grp2.setLayout(grp2Layout)

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)


        mainLayout.addWidget(grp1)
        mainLayout.addWidget(grp2)
        mainLayout.addItem(spacerItem)

        self.setLayout(mainLayout)

        self.getCacheVars()
        print pm.workspace.name
        self.setWindowTitle('Tool settings')

    def getCacheVars(self):
        rigString = pm.optionVar.get('rigString','RIG')
        shadeString = pm.optionVar.get('shadeString','SHADE')
        animString = pm.optionVar.get('animString','ANIM')
        animFolderString = pm.optionVar.get('animFolderString','Path to the animations')
        rigsFolderString = pm.optionVar.get('rigsFolderString','Path to the rigs')
        shadeFolderString = pm.optionVar.get('shadeFolderString','Path to the shade')

        self.rigEdit.setText(rigString)
        self.shadeEdit.setText(shadeString)
        self.animFileEdit.setText(animString)
        self.animFolderEdit.setText(animFolderString)
        self.rigsFolderEdit.setText(rigsFolderString)
        self.shadeFolderEdit.setText(shadeFolderString)

    def closeEvent(self,event):
        pm.optionVar['rigString'] = self.rigEdit.text()
        pm.optionVar['shadeString'] = self.shadeEdit.text()
        pm.optionVar['animString'] = self.animFileEdit.text()
        pm.optionVar['animFolderString'] = self.animFolderEdit.text()
        pm.optionVar['rigsFolderString'] = self.rigsFolderEdit.text()
        pm.optionVar['shadeFolderString'] = self.shadeFolderEdit.text()

    def getFolder(self,folder):
        projectPath = pm.workspace.name
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
            
