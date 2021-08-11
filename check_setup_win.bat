
@echo.
@echo Python Found: 
@where python

@echo off

REM check python install
echo.
echo Python Version:  (Python for Windows)
python --version
REM check pip install (generally included in python install)
echo.
echo Pip Version:  (Python for Windows)
pip --version
REM check GIT install
echo.
echo GIT Version:  (GIT for Windows)
git --version

REM check ssh-keygen.exe exists:
if exist "%ProgramFiles%\Git\usr\bin\ssh-keygen.exe" (
    REM file exists
) else (
    REM file doesn't exist
    echo ERROR: "C:\Program Files\Git\usr\bin\ssh-keygen.exe" is missing
    echo.
    echo  - Did you install GIT for Windows? -
    echo.
    exit 2
)

REM check SSH keys (ssh-keygen included with GIT, but must be run)
REM must generate SSH keys
REM must copy public key to github
echo.
echo check ssh keys exist: (~\.ssh\id_rsa.pub)
if exist %UserProfile%\.ssh\id_rsa.pub (
    REM file exists
    echo    ~\.ssh\id_rsa.pub file found!
) else (
    REM file doesn't exist
    echo ERROR: ~\.ssh\id_rsa.pub missing!
    echo RUN: cmd /C "C:\Program Files\Git\usr\bin\ssh-keygen.exe"
    echo          to generate ~\.ssh\id_rsa.pub
    echo          NOTE: just hit enter at "Enter file in which to save the key (/c/Users/_USER_/.ssh/id_rsa):" prompt
    echo      then copy the contents of ~\.ssh\id_rsa.pub to your GitHub account SSH keys at https://github.com/settings/keys
    exit 3
)
type %UserProfile%\.ssh\id_rsa.pub

REM check if autopkg config file exists
REM %UserProfile%\AppData\Local\AutoPkg\config.json
echo.
if exist %UserProfile%\AppData\Local\Autopkg\config.json (
    REM file exists
    echo Autopkg config found:
    type %UserProfile%\AppData\Local\Autopkg\config.json
    echo.
) else (
    REM file doesn't exist
    if not exist %UserProfile%\AppData\Local\Autopkg (
        REM autopkg folder doesn't exist
        echo creating missing Autopkg user config folder
        mkdir %UserProfile%\AppData\Local\Autopkg
        echo.
    )
    echo Autopkg config does not exist
    echo  creating blank Autopkg config
    echo {} > %UserProfile%\AppData\Local\Autopkg\config.json
)

REM TODO: check visual studio build tools
REM VSWhere check:
REM   .\vswhere.exe -all -legacy -products * -format json
REM WMI Relevance check:
REM   selects "* from MSFT_VSInstance" of wmis
REM Install Powershell VSSetup module
REM   powershell -ExecutionPolicy Bypass -command "Import-Module PowerShellGet ; Install-Module VSSetup -Scope CurrentUser -AcceptLicense -Confirm ; Get-VSSetupInstance"
REM   powershell -ExecutionPolicy Bypass -command "Import-Module PowerShellGet ; Install-Module VSSetup -Scope CurrentUser -AcceptLicense -Confirm ; (Get-VSSetupInstance | Select-VSSetupInstance -Product *).packages"
REM Install command:
REM   vs_BuildTools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools
REM distutils.errors.DistutilsPlatformError: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
REM ParentFolder: C:\ProgramData\Microsoft\VisualStudio\Packages\
REM   SubFolders:
REM     Microsoft.VisualCpp.Redist.14*
REM     Microsoft.Build*
REM     Microsoft.PythonTools.BuildCore*
REM     Microsoft.VisualStudio.PackageGroup.VC.Tools*
REM     Microsoft.VisualStudio.Workload.MSBuildTools*
REM     Microsoft.VisualStudio.Workload.VCTools*
REM     Win10SDK*
if not exist %ProgramData%\Microsoft\VisualStudio\Packages\Microsoft.VisualCpp.Redist.14* (
    REM folder missing
    echo.
    echo ERROR: missing required Visual Studio Build Tools - Required for Python Pip installs
    echo ERROR: missing folder %ProgramData%\Microsoft\VisualStudio\Packages\Microsoft.VisualCpp.Redist.14*
    echo Install Command:
    echo   vs_BuildTools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools
    echo.
    exit 9
)
if not exist %ProgramData%\Microsoft\VisualStudio\Packages\Microsoft.Build* (
    REM folder missing
    echo.
    echo ERROR: missing required Visual Studio Build Tools - Required for Python Pip installs
    echo ERROR: missing folder %ProgramData%\Microsoft\VisualStudio\Packages\Microsoft.Build*
    echo Install Command:
    echo   vs_BuildTools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools
    echo.
    exit 9
)
if not exist %ProgramData%\Microsoft\VisualStudio\Packages\Microsoft.PythonTools.BuildCore* (
    REM folder missing
    echo.
    echo ERROR: missing required Visual Studio Build Tools - Required for Python Pip installs
    echo ERROR: missing folder %ProgramData%\Microsoft\VisualStudio\Packages\Microsoft.PythonTools.BuildCore*
    echo Install Command:
    echo   vs_BuildTools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools
    echo.
    exit 9
)
if not exist %ProgramData%\Microsoft\VisualStudio\Packages\Microsoft.VisualStudio.PackageGroup.VC.Tools* (
    REM folder missing
    echo.
    echo ERROR: missing required Visual Studio Build Tools - Required for Python Pip installs
    echo ERROR: missing folder %ProgramData%\Microsoft\VisualStudio\Packages\Microsoft.VisualStudio.PackageGroup.VC.Tools*
    echo Install Command:
    echo   vs_BuildTools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools
    echo.
    exit 9
)
if not exist %ProgramData%\Microsoft\VisualStudio\Packages\Microsoft.VisualStudio.Workload.MSBuildTools* (
    REM folder missing
    echo.
    echo ERROR: missing required Visual Studio Build Tools - Required for Python Pip installs
    echo ERROR: missing folder %ProgramData%\Microsoft\VisualStudio\Packages\Microsoft.VisualStudio.Workload.MSBuildTools*
    echo Install Command:
    echo   vs_BuildTools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools
    echo.
    exit 9
)
if not exist %ProgramData%\Microsoft\VisualStudio\Packages\Microsoft.VisualStudio.Workload.VCTools* (
    REM folder missing
    echo.
    echo ERROR: missing required Visual Studio Build Tools - Required for Python Pip installs
    echo ERROR: missing folder %ProgramData%\Microsoft\VisualStudio\Packages\Microsoft.VisualStudio.Workload.VCTools*
    echo Install Command:
    echo   vs_BuildTools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools
    echo.
    exit 9
)
@REM if not exist %ProgramData%\Microsoft\VisualStudio\Packages\Microsoft.VisualStudio.ComponentGroup.NativeDesktop* (
@REM     REM folder missing
@REM     echo.
@REM     echo ERROR: missing required Visual Studio Build Tools - Required for Python Pip installs
@REM     echo ERROR: missing folder %ProgramData%\Microsoft\VisualStudio\Packages\Microsoft.VisualStudio.ComponentGroup.NativeDesktop*
@REM     echo Install Command:
@REM     echo   vs_BuildTools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools
@REM     echo.
@REM     exit 9
@REM )
if not exist %ProgramData%\Microsoft\VisualStudio\Packages\Win10SDK* (
    REM folder missing
    echo.
    echo ERROR: missing required Visual Studio Build Tools - Required for Python Pip installs
    echo ERROR: missing folder %ProgramData%\Microsoft\VisualStudio\Packages\Win10SDK*
    echo Install Command:
    echo   vs_BuildTools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools
    echo.
    exit 9
)

echo.
echo Upgrade pip:
echo python -m pip install --upgrade pip
python -m pip install --upgrade pip

REM NOTE: The following must be run from within the cloned git "bigfix-recipes" folder:
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

echo.
echo check pip install requirements for bigfix-recipes:
echo pip install -r .\requirements.txt --quiet --quiet
pip install -r .\requirements.txt --quiet --quiet
if errorlevel 0 (
    echo   - pip install for bigfix-recipes succeeded!  exit code: %errorlevel%
) else (
    echo ERROR: pip install for bigfix-recipes failed! exit code: %errorlevel%
    echo   - Have you installed visual studio build tools?
    REM https://github.com/bigfix/bigfix-recipes/issues/10
    echo vs_BuildTools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools
    exit %errorlevel%
)
REM https://stackoverflow.com/a/334890/861745

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
    REM TODO: Consider attempt at automatic fix with the following:
    REM CMD /C "cd .. && git clone https://github.com/jgstew/autopkg.git"
    exit 4
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
if errorlevel 0 (
    echo   - pip install for autopkg succeeded!  exit code: %errorlevel%
) else (
    echo ERROR: pip install for autopkg failed!  exit code: %errorlevel%
    echo   - Have you installed visual studio build tools?
    REM https://github.com/bigfix/bigfix-recipes/issues/10
    echo vs_BuildTools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools
    exit %errorlevel%
)

echo.
echo AutoPkg Version Check: (WARNINGS are expected on Windows)
REM this is assuming you ran check_setup_win.bat from within the bigfix-recipes folder and that Autopkg is in a sibling folder
echo python ..\autopkg\Code\autopkg version
python ..\autopkg\Code\autopkg version
echo      --- AutoPkg version (expected 2.3 or later)

echo.
echo Check the _setup folder for other items
echo.
pause
