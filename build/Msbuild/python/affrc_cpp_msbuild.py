# DestIncludeSubDir = include
# DestLibSubDir = lib

# LibSubDir = x64/Release
# IncludeSubDir = include

# Command for MSBUILD:
# msbuild pathToSolutionFile MSVC_Options

import parseConfig
import filesystemUtility

import sys
import os
import subprocess

CONFIG_DEFAULT_PATH = "./build_affrc_cpp_full_vc142_1.x.x_default.json"

def main():
  configPath = CONFIG_DEFAULT_PATH 
  if len(sys.argv) > 1:
    configPath = sys.argv[1]

  config = parseConfig.parse(configPath)

  config.repoDir = os.path.expandvars(config.repoDir)
  config.deployDir = os.path.expandvars(config.deployDir)

  filesystemUtility.createDirs(config.deployDir)

  logFilePath = config.deployDir + '/MsBuildDeployOwnLibs_log.txt'
  logFile = open(logFilePath, 'w', newline='\r\n')

  everythingDidCompile = True

  print("Solutions ---------:\n")

  for slnFileSubPath in config.slnFileSubPaths:
    slnFilePath = config.repoDir + '/' + slnFileSubPath

    if not filesystemUtility.pathExists(slnFilePath):
      print("!Exists: %s" %slnFilePath)

    lastSlashPos = slnFilePath.rfind('/')
    slnFileDir = slnFilePath[:lastSlashPos]
    
    print()
    print(slnFilePath)

    msbuildArgs = ["msbuild", slnFilePath, "/v:quiet", "/p:PreferredToolArchitecture=x64", "/p:Configuration=release"]
    msbuildArgs.extend(config.msbuildOptions.split(' '))

    msbuildSubprocess = subprocess.Popen(msbuildArgs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = msbuildSubprocess.communicate()
    returnCode = msbuildSubprocess.returncode

    containsErrors = returnCode != 0
    containsWarnings = stdout.find(b'warning :') != -1

    if containsErrors:
      everythingDidCompile = False

    if containsErrors or containsWarnings:
      print(stdout)
  	  
      logFile.write(slnFilePath)
      logFile.write(" - ")
      if containsErrors and containsWarnings:
        logFile.write("Errors and Warnings\n")
      elif containsErrors:
        logFile.write("Errors\n")
      elif containsWarnings:
        logFile.write("Warnings\n")
      logFile.write(str(stdout))
      logFile.write("\n\n\n")

    if not containsErrors:
      srcIncludeDir = slnFileDir + "/include"
      destIncludeDir = config.deployDir + "/include"
      filesystemUtility.copyDirTree(srcIncludeDir, destIncludeDir)

      srcLibDir = slnFileDir + "/x64/Release"
      destLibDir = config.deployDir + "/lib/x64/Release"
      filesystemUtility.copyDirTree(srcLibDir, destLibDir)
  
  print("---------:\n")

  print("HeaderOnly ---------:\n")
  for headerOnlySubDir in config.headerOnlySubDirs:
    headerOnlyDir = config.repoDir + '/' + headerOnlySubDir
    print()
    print(headerOnlyDir)

    srcIncludeDir = headerOnlyDir + "/include"
    destIncludeDir = config.deployDir + "/include"
    filesystemUtility.copyDirTree(srcIncludeDir, destIncludeDir)

  print("\n---------\n")
  if everythingDidCompile:
    print("EXIT_SUCCESS")
    logFile.write("EXIT_SUCCESS")
  else:
    print("EXIT some thing did not compile")
    logFile.write("EXIT some thing did not compile")


main()