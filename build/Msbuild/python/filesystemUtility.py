import os
import shutil
import distutils.dir_util

def getAvailableSpaceInGB(path):
  sizeInBytes = getAvailableDiskSpace(path)
  return sizeInBytes / (2**30)

def getAvailableDiskSpace(path):
  total, used, free = shutil.disk_usage(path)
  return free

def getDirSizeInGB(path):
  sizeInBytes = getDirSize(path)
  return sizeInBytes / 10**9

def getDirSize(dirPath):
  r = 0
  
  for path, dirs, files in os.walk(dirPath):
    for f in files:
      fp = os.path.join(path, f)
      r += os.path.getsize(fp)
    
  return r

def getFilenamesFromDir(dir):
  return [f.name for f in os.scandir(dir) if f.is_file()]

def getFoldernamesFromDir(dir):
  return [f.name for f in os.scandir(dir) if f.is_dir()]

def pathExists(path):
  return os.path.exists(path)

def createDirs(path):
  if not pathExists(path):
    os.makedirs(path)

def copyFile(srcImagePath, destImagePath):
  shutil.copyfile(srcImagePath, destImagePath)

def copyDirTree(src, dest):
  distutils.dir_util.copy_tree(src, dest)

def copyFilesFromDir(src, dest):
  if not pathExists(dest):
    os.makedirs(dest)

  for e in os.scandir(src):
    if e.is_file():
      destFilePath = dest + '/' + e.name
      copyFile(e.path, destFilePath)
