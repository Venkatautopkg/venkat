
@echo Python Found: 
@where python

@echo off

REM check python install
echo Python Version:
python --version
REM check pip install (generally included in python install)
echo Pip Version:
pip --version
REM check GIT install
echo GIT Version:
git --version
REM check SSH keys (ssh-keygen included with GIT, but must be run)
REM must generate SSH keys
REM must copy public key to github
echo check ssh keys exist
type %UserProfile%\.ssh\id_rsa.pub

REM check if autopkg config file exists
REM %UserProfile%\AppData\Local\AutoPkg\config.json
if exist %UserProfile%\AppData\Local\Autopkg\config.json (
    REM file exists
    echo Autopkg config found:
    type %UserProfile%\AppData\Local\Autopkg\config.json
) else (
    REM file doesn't exist
    if not exist %UserProfile%\AppData\Local\Autopkg (
        REM autopkg folder doesn't exist
        echo creating missing Autopkg user config folder
        mkdir %UserProfile%\AppData\Local\Autopkg
    )
    echo Autopkg config does not exist
    echo  creating blank Autopkg config
    echo {} > %UserProfile%\AppData\Local\Autopkg\config.json
)

REM check visual studio build tools
REM distutils.errors.DistutilsPlatformError: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/

