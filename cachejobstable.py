import pymel.core as pm
import os.path

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui


jobsTableTitles = ['Job Name','Camera','Animation file path']



class CacheJobsTable(QtGui.QWidget):
	def __init__(self,parent=None):
		super(CacheJobsTable,self).__init__(parent)

		mainLayout = QtGui.QVBoxLayout()

		self.setLayout(mainLayout)

		self.cacheJobsTable = self.createJobsTable()
		#self.camerasGroup = self.createCamerasGroup()
		mainLayout.addWidget(self.cacheJobsTable)
		
	def createJobsTable(self):
		colNum = len(jobsTableTitles)
		
		table = QtGui.QTableWidget(0,colNum)
		
		hheader = QtGui.QHeaderView(QtCore.Qt.Orientation.Horizontal)
		hheader.setStretchLastSection(True)
		table.setHorizontalHeader(hheader)
		table.setHorizontalHeaderLabels(jobsTableTitles)
		
		return table





