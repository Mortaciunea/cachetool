import pymel.core as pm
import os.path

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui


animationsTableTitles = ['Animation File','Export Cache']



class AnimationFilesTable(QtGui.QWidget):
	def __init__(self,parent=None):
		super(AnimationFilesTable,self).__init__(parent)

		mainLayout = QtGui.QVBoxLayout()

		self.setLayout(mainLayout)

		self.animFilesTable = self.createAnimTable()
		#self.camerasGroup = self.createCamerasGroup()
		mainLayout.addWidget(self.animFilesTable)
		
		self.scanProjectBtn = QtGui.QPushButton('Get Final Animations')
		mainLayout.addWidget(self.scanProjectBtn)
		self.scanProjectBtn.clicked.connect(self.getFinalAnimations)
		
		
	def createAnimTable(self):
		colNum = len(animationsTableTitles)
		
		table = QtGui.QTableWidget(0,colNum)
		
		hheader = QtGui.QHeaderView(QtCore.Qt.Orientation.Horizontal)
		hheader.setStretchLastSection(True)
		table.setHorizontalHeader(hheader)
		table.setHorizontalHeaderLabels(animationsTableTitles)
		
		return table
	
	def getFinalAnimations(self):
		workspace = pm.workspace.name
		print workspace,'asd'




