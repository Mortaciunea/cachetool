import pymel.core as pm
import os

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import shiboken
#import ALIQUAM.utilities.projectstructure as ps

import maya.OpenMayaUI

import referencestable 
reload(referencestable)
from referencestable import ReferencesTable
from cachejobstable import CacheJobsTable
from exportcachejob import ExportCacheJob

import cachesettings 
reload(cachesettings)
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
		
		centralWidget = QtGui.QWidget()

		mainLayout = QtGui.QVBoxLayout()

		cacheToolTabs = QtGui.QTabWidget()
		print cacheToolTabs
		
		self.animationsTable = AnimationFilesTable()
		cacheToolTabs.addTab(self.animationsTable , 'Animation Files')
		
		self.referencesTable = ReferencesTable()
		cacheToolTabs.addTab(self.referencesTable , 'References')
		
		self.cacheJobsTable = CacheJobsTable()
		cacheToolTabs.addTab(self.cacheJobsTable , 'Cache Jobs')
		
		
		mainLayout.addWidget(cacheToolTabs)
		
		centralWidget.setLayout(mainLayout)
		self.setCentralWidget(centralWidget)

		self.menuBar = self.menuBar()
		self.cacheMenu = self.menuBar.addMenu('Tool')
		self.cacheMenu.addAction('Settings').triggered.connect(self.setCacheToolVars)
		self.show()
		self.resize(800,600)
	
	def setCacheToolVars(self):
		settings = CacheSettingsUI()
		settings.setFixedSize(600,  300)
		settings.exec_()

def main():
	if pm.window( bdExportCacheWin, exists = True, q = True ):
		pm.deleteUI( bdExportCacheWin)

	CacheToolUI()	

