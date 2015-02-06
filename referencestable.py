import pymel.core as pm
import os.path

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui

from exportcachejob import ExportCacheJob
referencesTableTitles = ['Export?','Reference Name','RIG path','SHADE path']


class ReferencesTable(QtGui.QWidget):
	def __init__(self,parent=None):
		super(ReferencesTable,self).__init__(parent)
		self.cacheJobs = []
		mainLayout = QtGui.QVBoxLayout()

		self.setLayout(mainLayout)

		self.referencesTable = self.createReferencesTable()
		self.populateReferences()
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
		table.setHorizontalHeader(hheader)
		table.setHorizontalHeaderLabels(referencesTableTitles)
		
		return table
	
	def populateReferences(self):
		print 'populate'
		self.sceneReferences = pm.getReferences()
		self.loadedReferences = []
		
		for item in self.sceneReferences:
			if self.sceneReferences[item].isLoaded():
				self.loadedReferences.append([self.sceneReferences[item].isLoaded(),item,self.sceneReferences[item].path])

		#self.referencesTableWidget.setColumnCount(3)
		self.referencesTable.setRowCount(len(self.loadedReferences))
		for i in range(len(self.loadedReferences)):
			for j in range(3):
				print self.loadedReferences[i][j]
				item = QtGui.QTableWidgetItem(str(self.loadedReferences[i][j]))
				item.setFlags(~QtCore.Qt.ItemIsEditable)
				self.referencesTable.setItem(i, j, item)	

	def createCacheJob(self):
		self.cacheJobs.append(ExportCacheJob(animFile=pm.sceneName()))

