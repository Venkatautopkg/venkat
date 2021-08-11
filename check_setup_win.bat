
@echo.
@echo Python Found: 
@where python

@echo off

echo.
echo Check Current Directory contains "bigfix-recipes"
REM https://stackoverflow.com/a/25539569/861745
echo.%CD% | FIND /I "\bigfix-recipes">Nul && ( 
  Echo Run from within the correct directory: "bigfix-recipes"
) || (
  Echo ERROR: not run from "bigfix-recipes" directory
  echo run from within the ~\Documents\_Code\bigfix-recipes or similar folder
  echo.
  exit 1
)

REM check python install
echo.
echo Python Version:
python --version
REM check pip install (generally included in python install)
echo.
echo Pip Version:
pip --version
REM check GIT install
echo.
echo GIT Version:
git --version

REM check SSH keys (ssh-keygen included with GIT, but must be run)
REM must generate SSH keys
REM must copy public key to github
echo.
echo check ssh keys exist:
type %UserProfile%\.ssh\id_rsa.pub

REM check if autopkg config file exists
REM %UserProfile%\AppData\Local\AutoPkg\config.json
if exist %UserProfile%\AppData\Local\Autopkg\config.json (
    REM file exists
    echo.
    echo Autopkg config found:
    type %UserProfile%\AppData\Local\Autopkg\config.json
    echo.
) else (
    REM file doesn't exist
    if not exist %UserProfile%\AppData\Local\Autopkg (
        REM autopkg folder doesn't exist
        echo creating missing Autopkg user config folder
        mkdir %UserProfile%\AppData\Local\Autopkg
    )
    echo.
    echo Autopkg config does not exist
    echo  creating blank Autopkg config
    echo {} > %UserProfile%\AppData\Local\Autopkg\config.json
)



REM TODO: check visual studio build tools
REM distutils.errors.DistutilsPlatformError: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
REM TODO: end script here if this requirement is not satisfied due to it being required for later pip commands


echo.
echo Upgrade pip:
echo python -m pip install --upgrade pip
python -m pip install --upgrade pip

echo.
echo check pip install requirements for bigfix-recipes:
echo pip install -r .\requirements.txt --quiet --quiet
REM pip install -r .\requirements.txt --quiet --quiet

echo.
echo besapi python module version:
python -c "import besapi ; print(besapi.__version__)"

echo.
echo Check if besapi config file exists:
REM %UserProfile%\.besapi.conf
if exist %UserProfile%\.besapi.conf (
    REM file exists
    echo ~\.besapi.conf file found!
    echo.
    echo Test besapi config and login:
    python -m besapi ls quit
) else (
    echo ERROR: ~\.besapi.conf file does not exist!
    echo  copying blank besapi config
    echo copy _setup\.besapi.conf %UserProfile%\.besapi.conf
    copy _setup\.besapi.conf %UserProfile%\.besapi.conf
)

echo.
echo Check for ..\autopkg git repo folder:
if not exist ..\autopkg (
    echo ERROR: autopkg git folder missing!
    REM CMD /C "cd .. && git clone https://github.com/jgstew/autopkg.git"
    exit 2
) else (
    echo ..\autopkg folder found!
)

echo.
echo check autopkg on dev branch:
CMD /C "cd ..\autopkg && git checkout dev"

echo.
echo check pip install requirements for AutoPkg:
echo pip install -r ..\autopkg\requirements.txt --quiet --quiet
pip install -r ..\autopkg\requirements.txt --quiet --quiet

echo.
echo AutoPkg Version: (WARNINGS are expected on Windows)
REM this is assuming you ran check_setup_win.bat from within the bigfix-recipes folder and that Autopkg is in a sibling folder
python ..\autopkg\Code\autopkg version

echo.
echo Check the _setup folder for other items
echo.
pause
