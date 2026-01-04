@ECHO OFF

ECHO Clear up dist\...
IF EXIST dist (
    REM -
) ELSE (
    MKDIR dist
)
DEL /F /Q dist\*

ECHO Calling pinliner...
REM REM :: comment: please delete .pyc files before every call of the mdmoverlayhelper_bundle - this is implemented in my fork of the pinliner
@REM python src-make\lib\pinliner\pinliner\pinliner.py src -o dist/mdmoverlayhelper_bundle.py --verbose
python src-make\lib\pinliner\pinliner\pinliner.py src -o dist/mdmoverlayhelper_bundle.py
if %ERRORLEVEL% NEQ 0 ( echo ERROR: Failure && pause && exit /b %errorlevel% )
ECHO Done

ECHO Patching mdmoverlayhelper_bundle.py...
ECHO # ... >> dist/mdmoverlayhelper_bundle.py
ECHO # print('within mdmoverlayhelper_bundle') >> dist/mdmoverlayhelper_bundle.py
REM REM :: no need for this, the root package is loaded automatically
@REM ECHO # import mdmoverlayhelper_bundle >> dist/mdmoverlayhelper_bundle.py
ECHO from src import launcher >> dist/mdmoverlayhelper_bundle.py
ECHO launcher.main() >> dist/mdmoverlayhelper_bundle.py
ECHO # print('out of mdmoverlayhelper_bundle') >> dist/mdmoverlayhelper_bundle.py

PUSHD dist
COPY ..\run_make_excel.bat .\run_overlayhelper_excel.bat
powershell -Command "(gc 'run_overlayhelper_excel.bat' -encoding 'Default') -replace '(dist[/\\])?mdmoverlayhelper_bundle.py', 'mdmoverlayhelper_bundle.py' | Out-File -encoding 'Default' 'run_overlayhelper_excel.bat'"
COPY ..\run_produce_scripts.bat .\run_overlayhelper_scripts.bat
powershell -Command "(gc 'run_overlayhelper_scripts.bat' -encoding 'Default') -replace '(dist[/\\])?mdmoverlayhelper_bundle.py', 'mdmoverlayhelper_bundle.py' | Out-File -encoding 'Default' 'run_overlayhelper_scripts.bat'"
POPD


ECHO End

