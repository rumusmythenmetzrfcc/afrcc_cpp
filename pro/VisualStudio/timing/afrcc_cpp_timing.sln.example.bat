Rem First we set some environment vars for use inside the solution
set AFRCC_CPP_SRC_ROOT=C:/Software/AFRCC/C++/L/afrcc_cpp/src

Rem Then we make sure that the preferred build environment is setup.
Rem vcvarsall.bat: If you prefer to set the build environment in an existing command prompt window, you can use one of the command files created by the installer. We recommend you set the environment in a new command prompt window. We don't recommend you later switch environments in the same command window.
Rem See https://docs.microsoft.com for more infos on vcvarsall.bat.
call "C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Auxiliary/Build/vcvarsall.bat" x64
call set PreferredToolArchitecture=x64

Rem Finally we call the .sln File
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\devenv.exe" /useenv "afrcc_cpp_timing.sln"