import json
import os

import pymel.core as pm


class ExportCacheJob():
  #animFile is the path to the open animation file
  def __init__(self,animFile=''):
    self.animFileJob = animFile
    self.loadedReferences = {}
    self.cacheJob = ''

    self.cachePath = ''
    self.alembicFiles = []
    self.meshesList = []
    self.cameraName = ''
    
    print self.animFileJob

  def createExportJob(self):
    timeUnit = pm.currentUnit(q=1, time=True)
    startTime = pm.playbackOptions(query=True, minTime=True)
    endTime = pm.playbackOptions(query=True, maxTime=True)

    animFileFullPath = pm.sceneName()
    animFileRelative = pm.sceneName().replace(pm.workspace.name,'')

    self.getCachePath(animFileRelative)

    for i in range(self.referencesTableWidget.rowCount()):
      if self.referencesTableWidget.item(i,0).text() == 'True':
        ns = self.referencesTableWidget.item(i,1).text()
        nsPath = self.referencesTableWidget.item(i,2).text()
        self.loadedReferences[ns] = nsPath
    
    print self.loadedReferences
    
    '''
    for ns in self.loadedReferences.keys():
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


      for ns in self.loadedReferences:
        fileName = self.loadedReferences[ns]
        self.bdImportAlambic(ns,fileName,self.cachePath)

      for cam in self.cameras:
        self.bdImportCamera(cam)

      self.animFile = animFileRelative
      self.bdSaveRenderFile()
    '''
  def getCachePath(self, animPath):

    animFileName = animPath.split('/')[-1]
    projectFolder = pm.workspace.name
    
    self.cachePath = projectFolder + '/cache/' + animFileName 
    
    if os.path.isdir(self.cachePath):
      print 'Cache folder for %s animation file exists'%animFileName
    else:
      os.mkdir(self.cachePath)



