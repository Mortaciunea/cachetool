import pymel.core as pm
import os.path

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui

from difflib import Differ

jobsTableTitles = ['Job Name','Camera','Animation file path']



class CacheJobsTable(QtGui.QWidget):
    def __init__(self,parent=None):
        super(CacheJobsTable,self).__init__(parent)

        mainLayout = QtGui.QVBoxLayout()

        self.setLayout(mainLayout)

        self.cacheJobsTable = self.createJobsTable()
        #self.camerasGroup = self.createCamerasGroup()
        mainLayout.addWidget(self.cacheJobsTable)
        self.createCacheBtn = QtGui.QPushButton('Create Cache')
        self.createLightingBtn = QtGui.QPushButton('Create Lighting File')

        self.createCacheBtn.clicked.connect(self.createCache)
        mainLayout.addWidget(self.createCacheBtn)

        self.cacheFolder = self.setCacheFolder()
        #exportReferences  - list of lists , sublists format is [loadedStatus,namespace,reference path]
        self.exportReferences = []

        self.userCameras = []

    def createJobsTable(self):
        colNum = len(jobsTableTitles)

        table = QtGui.QTableWidget(0,colNum)

        hheader = QtGui.QHeaderView(QtCore.Qt.Orientation.Horizontal)
        hheader.setStretchLastSection(True)
        table.setHorizontalHeader(hheader)
        table.setHorizontalHeaderLabels(jobsTableTitles)

        return table


    def createCache(self):
        print 'creating cache'
        cacheTool =  self.parent().parent().parent().parent()
        animTable = QtGui.QTableWidget()
        animTable = cacheTool.animationsTable.animFilesTable

        rowCount = animTable.rowCount()
        print rowCount 
        for i in range(rowCount):
            cacheStatus = animTable.item(i,1).text()
            if cacheStatus == 'Yes':
                self.exportCache(animTable.item(i,0).text())

    def exportCache(self,animFile):
        if os.path.isfile(animFile):
            pm.openFile(animFile,f=1)
            self.exportReferences = self.getSceneReferences()
            cacheFolder = self.createShotCacheFolder(animFile)
            for reference in self.exportReferences :
                print 'Export Alembuc for reference %s'%reference
                self.exportAlembic(reference[1],cacheFolder)

            self.exportCameras(cacheFolder)
            self.saveRenderFile(animFile,cacheFolder)



    def exportAlembic(self,namespace,cacheFolder):
        print 'actually exporting'
        geoSuffix = pm.optionVar.get('geoString','REN')

        meshes =[mesh.fullPath() for mesh in pm.ls(namespace+':*' + geoSuffix,type='transform')]

        startTime = pm.playbackOptions(query=True, minTime=True)
        endTime = pm.playbackOptions(query=True, maxTime=True)
        logFile = os.path.join(cacheFolder,'log.txt')
        f = open(logFile,'w')
        f.writelines('Exporting %s, path %s'%(namespace,cacheFolder) )
        if meshes:
            pm.select(meshes)
            
            f.writelines('Exporting meshes %s'%( ', '.join(meshes)))
            fileName = namespace + '.abc'

            fileName = os.path.join(cacheFolder,fileName).replace('\\','/')
            print fileName 
            jobstring="AbcExport "
            jobstring += "-j \" -fr %d %d -uvWrite" %(startTime,endTime)
            for mesh in meshes:
                jobstring += ' -root ' + mesh



            jobstring  += ' -file ' + fileName
            jobstring  += '\"'


            try:
                pm.hide(all=True)
                pm.select(meshes)
                pm.showHidden(above=True)
                pm.mel.eval(jobstring)
            except:
                pm.warning('Could not export %s rig'%namespace)
        f.close()

    def exportCameras(self,cacheFolder):
        perspCameras = pm.listCameras(o=0,p=1)
        userCameras = []
        for cam in perspCameras:
            if 'persp' not in cam:
                userCameras.append(cam)
        self.userCameras = userCameras
        for cam in userCameras:
            startTime = pm.playbackOptions(query=True, minTime=True)
            endTime = pm.playbackOptions(query=True, maxTime=True)

            pm.select(cam)
            fileName = cam + '.abc'
            fileName = os.path.join(cacheFolder,fileName).replace('\\','/')

            jobstring="AbcExport "
            jobstring += "-j \" -fr %d %d -worldSpace" %(startTime,endTime)

            jobstring += ' -root ' + cam

            jobstring  += ' -file ' + fileName
            jobstring  += '\"'
            print jobstring 

            try:
                pm.hide(all=True)
                pm.select(cam)
                pm.showHidden(above=True)
                pm.mel.eval(jobstring)
            except:
                pm.warning('Could not export %s cam'%cam) 

    def saveRenderFile(self,forAnim,cacheFolder):
        lightingFolder = pm.optionVar.get('lightingFolderString','')
        lightingString = pm.optionVar.get('lightingString','')
        animString = pm.optionVar.get('animString','')
        
        timeUnit = pm.currentUnit(q=1, time=True)
        startTime = pm.playbackOptions(query=True, minTime=True)
        endTime = pm.playbackOptions(query=True, maxTime=True)

        print 'Saving render file asfasfasfsfasf'
        pm.newFile(force=True)
        pm.currentUnit( time=timeUnit )
        pm.currentTime( startTime, edit=True ) 

        pm.playbackOptions(ast=startTime)
        pm.playbackOptions(aet=endTime)
        pm.playbackOptions(minTime=startTime)
        pm.playbackOptions(maxTime=endTime)
        
        workspace = pm.workspace.path
        print workspace
        print forAnim
        
        animRoot = forAnim.replace('\\','/').replace(workspace,'')
        lightingFile = animRoot.split('/')[-1].replace(animString,lightingString)
        
        foldersToFile =  animRoot.split('/')[2:-1]

        for folder in foldersToFile :
            if not os.path.isdir(os.path.join(lightingFolder,folder)):
                os.mkdir(os.path.join(lightingFolder,folder))
                lightingFolder = os.path.join(lightingFolder,folder)
            else:
                lightingFolder = os.path.join(lightingFolder,folder)

        fullPath = os.path.join(lightingFolder,lightingFile)
        
        f,ext = os.path.splitext(lightingFile)
        print ext
        filetype = 'mayaAscii'
        if ext == '.mb':
            filetype = 'mayaBinary'
        

        pm.saveAs(fullPath,f=1,type=filetype)
        for reference in self.exportReferences :
            self.importAlembic(reference[1],reference[2],cacheFolder)

        for cam in self.userCameras:
            self.importAlembicCamera(cam,cacheFolder)
        
        pm.saveFile()

    def importAlembic(self,ns,rigPath,cacheFolder):
        shadeFile = self.getShadePath(rigPath)
        geoSuffix = pm.optionVar.get('geoString','REN')
        if os.path.isfile(shadeFile):
            pm.createReference( shadeFile, namespace = ns)
            meshes =[mesh.fullPath() for mesh in pm.ls(ns+':*' + geoSuffix,type='transform')]

            if meshes:
                #print meshes
                pm.select(meshes)
                filePath = ns + '.abc'
                filePath = os.path.join(cacheFolder,filePath).replace('\\','/')

                jobstring="AbcImport "
                jobstring += "-mode import -fitTimeRange -connect \"" 
                for mesh in meshes:
                    jobstring += mesh + ' '

                jobstring += '\" \"'  + filePath + '\"'
                print jobstring
                try:
                    pm.mel.eval(jobstring)
                except:
                    pm.warning('Could not import %s rig'%ns)     
    def importAlembicCamera(self,cam,cacheFolder):
        filePath = cam + '.abc'
        filePath = os.path.join(cacheFolder,filePath).replace('\\','/')
        jobstring="AbcImport "
        jobstring += "-mode import " 
        jobstring += ' \"'  + filePath + '\"'
        print jobstring
        try:
            pm.mel.eval(jobstring)
        except:
            pm.warning('Could not import %s cam'%cam)        


    def setCacheFolder(self):
        workspace = pm.workspace.path
        cacheFolder = os.path.join(workspace,'cache')
        if not os.path.isdir(cacheFolder):
            os.mkdir(cacheFolder)
        cacheFolder = os.path.join(workspace,'alembic')
        if not os.path.isdir(cacheFolder):
            os.mkdir(cacheFolder)
        return os.path.abspath(cacheFolder)

    def createShotCacheFolder(self,animFile):
        path,anim = os.path.split(animFile)
        anim,extension = os.path.splitext(anim)

        shotFolder = os.path.join(self.cacheFolder,anim + '_CACHE')

        if not os.path.isdir(shotFolder):
            os.mkdir(shotFolder)

        return os.path.abspath(shotFolder)

    def getSceneReferences(self):
        sceneReferences = pm.getReferences()
        loadedReferences = []
        #print '___________SCENE REFERENCES _____________ %s'%sceneReferences
        for item in sceneReferences:
            #print '___________REFERENCE _____________ %s'%sceneReferences[item]
            #print '___________REFERENCE LOADED _____________ %s'%sceneReferences[item].isLoaded()
            #print '___________REFERENCE path _____________ %s'%sceneReferences[item].path
            if sceneReferences[item].isLoaded() and self.toExport(sceneReferences[item]):
                loadedReferences.append([sceneReferences[item].isLoaded(),item,os.path.abspath(sceneReferences[item].path)])

        #print '___________LOADED REFERENCES _____________ %s'%loadedReferences
        return loadedReferences

    def toExport(self,reference):
        #print '_________TO EXPORT_____ %s'%reference
        referencePath = os.path.abspath(reference.path)

        cacheTool =  self.parent().parent().parent().parent()
        referencesTable = QtGui.QTableWidget()
        referencesTable = cacheTool.referencesTable.referencesTable

        items = referencesTable.findItems(referencePath,QtCore.Qt.MatchExactly)
        for item in items:
            if referencesTable.item(item.row(),2).text() == 'Yes':
                return 1
            else:
                return 0

    def getShadePath(self,rigPath):
        shadeFile = ''
        referencePath = os.path.abspath(rigPath)

        cacheTool =  self.parent().parent().parent().parent()
        referencesTable = QtGui.QTableWidget()
        referencesTable = cacheTool.referencesTable.referencesTable

        items = referencesTable.findItems(rigPath,QtCore.Qt.MatchExactly)
        if items:
            shadeFile =  referencesTable.item(items[0].row(),1).text()

        return shadeFile