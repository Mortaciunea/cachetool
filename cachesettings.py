import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import pymel.core as pm

class CacheSettingsUI(QtGui.QDialog):
    def __init__(self,parent=None):
        super(CacheSettingsUI,self).__init__(parent)
        mainLayout = QtGui.QVBoxLayout()
        
        rigRowLayout = QtGui.QHBoxLayout()
        rigLabel = QtGui.QLabel('Rig file string')
        self.rigEdit = QtGui.QLineEdit()
        rigRowLayout .addWidget(rigLabel)
        rigRowLayout .addWidget(self.rigEdit)
        
        shadeRowLayout = QtGui.QHBoxLayout()
        shadeLabel = QtGui.QLabel('Shade file string')
        self.shadeEdit = QtGui.QLineEdit()
        shadeRowLayout .addWidget(shadeLabel)
        shadeRowLayout .addWidget(self.shadeEdit)        
        
        mainLayout.addLayout(rigRowLayout)
        mainLayout.addLayout(shadeRowLayout)
        self.setLayout(mainLayout)
        
        self.getCacheVars()
        
        self.setWindowTitle('Cache settings')
        
    def getCacheVars(self):
        rigString = pm.optionVar.get('rigString','RIG')
        cacheString = pm.optionVar.get('cacheString','CACHE')
        
        self.rigEdit.setText(rigString)
        self.shadeEdit.setText(cacheString)
        
    def closeEvent(self,event):
        pm.optionVar['rigString'] = self.rigEdit.text()
        pm.optionVar['cacheString'] = self.shadeEdit.text()