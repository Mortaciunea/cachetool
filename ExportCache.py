import pymel.core as pm
import os

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import shiboken
#import ALIQUAM.utilities.projectstructure as ps

import maya.OpenMayaUI

from referencestable import ReferencesTable
from cachejobstable import CacheJobsTable
from exportcachejob import ExportCacheJob
from cachesettings import CacheSettingsUI
import animfilestable 
reload(animfilestable)
from animfilestable import AnimationFilesTable



bdExportCacheWin = 'bdAAEMainWindow'
referencesTableTitles = ['Export?','Reference Name','Path']
camerasTableTitles = ['Export?','Camera Name']

def get_maya_window():
	maya_window_util = maya.OpenMayaUI.MQtUtil.mainWindow()
	maya_window = shiboken.wrapInstance( long( maya_window_util ), QtGui.QWidget )
	return maya_window


class CacheToolUI(QtGui.QMainWindow):
	def __init__(self,parent=get_maya_window()):
		super(CacheToolUI,self).__init__(parent)
		self.setObjectName(bdExportCacheWin)
		
		
		self.setWindowTitle('Export Cache Tool')
		
		mainLayout = QtGui.QVBoxLayout()
		
		
		okButton = QtGui.QPushButton(self.tr("OK"))
		cancelButton = QtGui.QPushButton(self.tr("Cancel"))
		
		buttonLayout = QtGui.QHBoxLayout()
		buttonLayout.addStretch(1)
		buttonLayout.addWidget(okButton)
		buttonLayout.addWidget(cancelButton)		

		#self.tabs= QtGui.QTabWidget()
		cacheToolTabs = QtGui.QTabWidget()
		print cacheToolTabs
		
		self.animationsTable = AnimationFilesTable()
		cacheToolTabs.addTab(self.animationsTable , 'Animation Files')
		
		self.referencesTable = ReferencesTable()
		cacheToolTabs.addTab(self.referencesTable , 'References')
		
		self.cacheJobsTable = CacheJobsTable()
		cacheToolTabs.addTab(self.cacheJobsTable , 'Cache Jobs')
		
		#self.tabs.addTab(self.cacheToolTabs,'Cache Tool')
		mainLayout.addWidget(cacheToolTabs)
		#mainLayout.addWidget(self.tabs)
		#self.setCentralWidget( self.tabs )
		self.setLayout(mainLayout)
		self.menuBar = self.menuBar()
		self.cacheMenu = self.menuBar.addMenu('Tool')
		self.cacheMenu.addAction('Settings').triggered.connect(self.setCacheToolVars)
		self.show()
	
	def setCacheToolVars(self):
		settings = CacheSettingsUI()
		settings.setFixedSize(300,  80)
		settings.exec_()

def main():
	if pm.window( bdExportCacheWin, exists = True, q = True ):
		pm.deleteUI( bdExportCacheWin)

	CacheToolUI()	

