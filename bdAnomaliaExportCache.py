import pymel.core as pm
import os.path, os, sys

import xml.etree.ElementTree as xml
from cStringIO import StringIO
import logging
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import pysideuic
import shiboken

import maya.OpenMayaUI



pyqtLoggers = ['pysideuic.properties','pysideuic.uiparser']
for log in pyqtLoggers:
	logger = logging.getLogger(log)
	logger.setLevel(logging.ERROR)



def loadUiType(uiFile):
		parsed = xml.parse(uiFile)
		widget_class = parsed.find('widget').get('class')
		form_class = parsed.find('class').text
	
		with open(uiFile, 'r') as f:
			o = StringIO()
			frame = {}
			
			pysideuic.compileUi(f, o, indent=0)
			pyc = compile(o.getvalue(), '<string>', 'exec')
			exec pyc in frame
			
			#Fetch the base_class and form class based on their type in the xml from designer
			form_class = frame['Ui_%s'%form_class]
			base_class = eval('QtGui.%s'%widget_class)
		return form_class, base_class
	
def wrapinstance( ptr, base = None ):
	if ptr is None:
		return None

	ptr = long( ptr ) 
	if globals().has_key( 'shiboken' ):
		if base is None:
			qObj = shiboken.wrapInstance( long( ptr ), QtCore.QObject )
			metaObj = qObj.metaObject()
			cls = metaObj.className()
			superCls = metaObj.superClass().className()
			if hasattr( QtGui, cls ):
				base = getattr( QtGui, cls )

			elif hasattr( QtGui, superCls ):
				base = getattr( QtGui, superCls )

			else:
				base = QtGui.QWidget

		return shiboken.wrapInstance( long( ptr ), base )

	elif globals().has_key( 'sip' ):
		base = QtCore.QObject

		return sip.wrapinstance( long( ptr ), base )

	else:
		return None


def get_maya_window():
	maya_window_util = maya.OpenMayaUI.MQtUtil.mainWindow()
	maya_window = wrapinstance( long( maya_window_util ), QtGui.QWidget )

	return maya_window

'''
========================================================================
---->  Start BD Script <----
========================================================================
'''  

uiFile = os.path.join(os.path.dirname(__file__),'bdAnomaliaExportCache_UI.ui' )
exportCache_form, exportCache_base= loadUiType( uiFile )
bdExportCacheWin = 'bdAAEMainWindow'

projectPath = pm.workspace.path


class bdExportCache( exportCache_base, exportCache_form ):
	def __init__( self, parent = get_maya_window(), *args ):
		super( bdExportCache, self ).__init__( parent )
		self.setupUi( self )
		self.referencesTableWidget.itemDoubleClicked.connect( self.bdToggleReference )
		self.referencesTableWidget.horizontalHeader().setStretchLastSection(True)
		self.camerasTableWidget.horizontalHeader().setStretchLastSection(True)
		self.camerasTableWidget.itemDoubleClicked.connect( self.bdToggleCameras )
		
		self.bdPopulateReferences()
		self.bdPopulateCameras()
		
		self.exportBtn.clicked.connect(self.bdExportAll)
		#self.saveRenderBtn.clicked.connect(self.bdSaveRenderFile)
		
		self.truckActive = 0
		self.branchesActive= False
		self.show()
	
	def bdPopulateReferences(self):
		self.sceneReferences = pm.getReferences()
		self.loadedReferences = []
	
		for item in self.sceneReferences:
			if self.sceneReferences[item].isLoaded():
				self.loadedReferences.append([self.sceneReferences[item].isLoaded(),item,self.sceneReferences[item].path])

		self.referencesTableWidget.setColumnCount(3)
		self.referencesTableWidget.setRowCount(len(self.loadedReferences))
		
		for i in range(len(self.loadedReferences)):
			for j in range(3):
				print self.loadedReferences[i][j]
				item = QtGui.QTableWidgetItem(str(self.loadedReferences[i][j]))
				item.setFlags(~QtCore.Qt.ItemIsEditable)
				self.referencesTableWidget.setItem(i, j, item)	
	
	def bdPopulateCameras(self):
		self.cameras = pm.listCameras(p=1)
		self.cameras.remove('persp')
		self.camerasTableWidget.setColumnCount(2)
		self.camerasTableWidget.setRowCount(len(self.cameras))
		
		for i in range(len(self.cameras)):
			exportStatus = QtGui.QTableWidgetItem('True')
			exportStatus.setFlags(~QtCore.Qt.ItemIsEditable)
			self.camerasTableWidget.setItem(i, 0, exportStatus)	
			cam = QtGui.QTableWidgetItem(self.cameras[i])
			cam.setFlags(~QtCore.Qt.ItemIsEditable)
			self.camerasTableWidget.setItem(i, 1, cam)	
		
				
				
	def bdToggleReference(self, tableWidgetItem ):
		row = tableWidgetItem.row()
		currentState = self.referencesTableWidget.item(row,0).text()
		if currentState == 'True':
			item = QtGui.QTableWidgetItem('False')
			item.setFlags(~QtCore.Qt.ItemIsEditable)
			self.referencesTableWidget.setItem(row,0,item)
		elif currentState == 'False':
			item = QtGui.QTableWidgetItem('True')
			item.setFlags(~QtCore.Qt.ItemIsEditable)
			self.referencesTableWidget.setItem(row,0,item)

	def bdToggleCameras(self, tableWidgetItem ):
		row = tableWidgetItem.row()
		currentState = self.camerasTableWidget.item(row,0).text()
		if currentState == 'True':
			item = QtGui.QTableWidgetItem('False')
			item.setFlags(~QtCore.Qt.ItemIsEditable)
			self.camerasTableWidget.setItem(row,0,item)
		elif currentState == 'False':
			item = QtGui.QTableWidgetItem('True')
			item.setFlags(~QtCore.Qt.ItemIsEditable)
			self.camerasTableWidget.setItem(row,0,item)

	def bdExportAll(self):
		timeUnit = pm.currentUnit(q=1, time=True)
		startTime = pm.playbackOptions(query=True, minTime=True)
		endTime = pm.playbackOptions(query=True, maxTime=True)
	
		animFileFullPath = pm.sceneName()
		animFileRelative = pm.sceneName().replace(projectPath,'')
	
		self.cachePath = self.bdGetCachePath(animFileRelative)
	

		loadedReferences = {}
		
		for i in range(self.referencesTableWidget.rowCount()):
			if self.referencesTableWidget.item(i,0).text() == 'True':
				ns = self.referencesTableWidget.item(i,1).text()
				nsPath = self.referencesTableWidget.item(i,2).text()
				loadedReferences[ns] = nsPath
	
	
		for ns in loadedReferences.keys():
			self.bdExportAlambic(ns,self.cachePath)
		
		for i in range(self.camerasTableWidget.rowCount()):
			if self.camerasTableWidget.item(i,0).text() == 'True':
				self.bdExportCameras(self.camerasTableWidget.item(i,1).text())
				
		if self.saveRenderCheckBox.isChecked():

			pm.newFile(force=True)
			pm.currentUnit( time=timeUnit )
			pm.currentTime( startTime, edit=True ) 
			
			pm.playbackOptions(ast=startTime)
			pm.playbackOptions(aet=endTime)
			pm.playbackOptions(minTime=startTime)
			pm.playbackOptions(maxTime=endTime)


			for ns in loadedReferences:
				fileName = loadedReferences[ns]
				self.bdImportAlambic(ns,fileName,self.cachePath)
			
			for cam in self.cameras:
				self.bdImportCamera(cam)
				
			self.animFile = animFileRelative
			self.bdSaveRenderFile()
	
	def bdExportCameras(self,cam):
		startTime = pm.playbackOptions(query=True, minTime=True)
		endTime = pm.playbackOptions(query=True, maxTime=True)
	
		pm.select(cam)
		fileName = cam + '.abc'


		jobstring="AbcExport "
		jobstring += "-j \" -fr %d %d -worldSpace" %(startTime,endTime)

		jobstring += ' -root ' + cam


		if os.path.isdir(projectPath + self.cachePath ):
			jobstring  += ' -file ' + projectPath + self.cachePath + fileName
			jobstring  += '\"'
		else:
			newDir = os.makedirs(projectPath + self.cachePath)
			jobstring  += ' -file ' + projectPath + self.cachePath + fileName
			jobstring  += '\"'
			print jobstring 

		try:
			pm.mel.eval(jobstring)
		except:
			pm.warning('Could not export %s cam'%cam) 
				
	def bdExportAlambic(self,ns,cachePath):
	
		meshes =[mesh.fullPath() for mesh in pm.ls(ns+':*REN',type='transform')]
		if 'scene' in ns:
			print ns
			bananaMeshes = [mesh.fullPath() for mesh in pm.ls(ns + ':banana*:*REN',type='transform')]
			signMeshes = [mesh.fullPath() for mesh in pm.ls(ns + ':sign*:*REN',type='transform')]
			meshes = bananaMeshes + signMeshes
			try:
				poleCtrl = pm.ls(ns + ':sign_GEO:poleSign_ctrl',type='transform')[0]
				if not poleCtrl.rotateY.isConnected():
					startTime = pm.playbackOptions(query=True, minTime=True)
					rotateY = poleCtrl.rotateY.get()
					poleCtrl.rotateY.setKey(t=startTime,v=rotateY)
					poleCtrl.rotateY.setKey(t=startTime+1,v=rotateY+0.001)
			except:
				pm.warning('Didnt find the sign')
			
		elif 'truck' in ns:
			truckAnim = pm.ls(ns + ':Main_CTRL')[0]
			self.truckActive = truckAnim.attr('Geometry').get()
		elif 'snail' in ns:
			try:
				self.branchesActive = pm.getAttr(ns + ':moveScaleRotate.branches')
			except:
				pm.warning ('%s snail has no branches'%ns)

			

	
		startTime = pm.playbackOptions(query=True, minTime=True)
		endTime = pm.playbackOptions(query=True, maxTime=True)
	
		if meshes:
			pm.select(meshes)
			fileName = ns + '.abc'
	
	
			jobstring="AbcExport "
			jobstring += "-j \" -fr %d %d -uvWrite" %(startTime,endTime)
			for mesh in meshes:
				jobstring += ' -root ' + mesh
	
	
			if os.path.isdir(projectPath + self.cachePath ):
				jobstring  += ' -file ' + projectPath + self.cachePath + fileName
				jobstring  += '\"'
				print jobstring 
			else:
				newDir = os.makedirs(projectPath + self.cachePath)
				print newDir
				jobstring  += ' -file ' + projectPath + self.cachePath + fileName
				jobstring  += '\"'
				print jobstring 
	
			try:
				pm.hide(all=True)
				pm.select(meshes)
				pm.showHidden(above=True)
				print meshes
				pm.mel.eval(jobstring)
			except:
				pm.warning('Could not export %s rig'%ns) 
	
	
	
	def bdImportCamera(self,cam):
		filePath = cam + '.abc'
		jobstring="AbcImport "
		jobstring += "-mode import " 
		jobstring += ' \"' +projectPath + self.cachePath + filePath + '\"'
		print jobstring
		try:
			pm.mel.eval(jobstring)
		except:
			pm.warning('Could not import %s cam'%ns)		

	def bdImportAlambic(self,ns,filePath,cachePath):
		rigFileName = filePath.split('/')[-1]
		shadeFileName = rigFileName.replace('RIG','SHADE')
		branchesVisibility = 0
		if 'scene' in shadeFileName:
			shadeFileName = rigFileName.replace('GEO','SHADE_master')
		elif 'para' in shadeFileName:
			shadeFileName = rigFileName.replace('RIG','SHADE_master')
		elif 'plank' in shadeFileName:
			shadeFileName = rigFileName.replace('GEO','SHADE_master')
		elif 'wooden' in shadeFileName:
			shadeFileName = rigFileName.replace('RIG','SHADE_master')		

		 
		filePath = projectPath + '/tools/shade/' + shadeFileName

		if os.path.isfile(filePath):
			pm.createReference( filePath, namespace = ns)
			if 'snailBoy' in shadeFileName:
				branchesGrp = pm.ls(ns + ':branches_GRP')[0]
				if self.branchesActive:
					branchesGrp.visibility.set(1)
				else:
					branchesGrp.visibility.set(0)
					
			meshes =[mesh.fullPath() for mesh in pm.ls(ns+':*REN',type='transform')]
			
			if 'scene' in ns:
				print ns
				bananaMeshes = [mesh.fullPath() for mesh in pm.ls(ns + ':banana*:*REN',type='transform')]
				signMeshes = [mesh.fullPath() for mesh in pm.ls(ns + ':sign*:*REN',type='transform')]
				meshes = bananaMeshes + signMeshes
			elif 'truck' in ns:
				meshes =[mesh for mesh in pm.ls(ns+':*REN',type='transform')]
				
				truck1GRP = pm.ls( ns+ ':truck1_GRP',type='transform')[0]
				truck2GRP = pm.ls( ns+ ':truck2_GRP',type='transform')[0]
				if self.truckActive == 0 or self.truckActive == 1:
					truck2GRP.visibility.set(0)
					truck1GRP.visibility.set(1)
				else:
					truck2GRP.visibility.set(1)
					truck1GRP.visibility.set(0)	


			if meshes:
				#print meshes
				pm.select(meshes)
				filePath = ns + '.abc'
				jobstring="AbcImport "
				jobstring += "-mode import -fitTimeRange -connect \"" 
				for mesh in meshes:
					jobstring += mesh + ' '
	
				jobstring += '\" \"' +projectPath + self.cachePath + filePath + '\"'
				print jobstring
				try:
					pm.mel.eval(jobstring)
				except:
					pm.warning('Could not import %s rig'%ns)



		else:
			pm.warning('Couldnt find the shaded file %s'%filePath)
	
	
	
	def bdGetCachePath(self, animPath):
		print animPath
		animFileName = animPath.split('/')[-1]
		tokensName =  animFileName.split('_')
		seqName = tokensName[0] + '_' + tokensName[1]
		shotName = seqName + '_' + tokensName[2]
	
		self.cachePath = '/lighting/' +  seqName + '/' + shotName + '/' + 'cache/'
	
		return self.cachePath
	
	def bdSaveRenderFile(self):
		animPath = self.animFile
		animFileName = animPath.split('/')[-1]
		
		renderFilePath = projectPath + self.cachePath.replace('cache','') 
		renderFile =  renderFilePath + animFileName.replace('ANIM','CACHE')

		if os.path.isdir(renderFilePath):
			if os.path.isfile(renderFile):
				multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
				renderFile = pm.fileDialog2(fm=0, fileFilter=multipleFilters, dialogStyle=2, dir = os.path.normpath(renderFilePath))[0]
			
			unknown = pm.ls(type="unknown")
			unknown = filter(lambda node: not node.isReferenced(), unknown)
			for node in unknown:
				if not pm.objExists(node):
					continue
				pm.delete(node)			
			try:
				pm.saveFile(os.path.normpath(renderFile),force=True)
			except:
				pm.warning('Cant save maya ascii')
				
			
		else:
			pm.warning('Could not save render file !!!')
			


		
def bdMain():
	if pm.window( bdExportCacheWin, exists = True, q = True ):
		pm.deleteUI( bdExportCacheWin )

	bdExportCache()