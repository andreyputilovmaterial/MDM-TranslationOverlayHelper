@ECHO OFF

ECHO Clear up dist\...
IF EXIST dist (
    REM -
) ELSE (
    MKDIR dist
)
DEL /F /Q dist\*

ECHO -
ECHO -
ECHO Update program version
IF NOT EXIST src\GENERATED MKDIR src\GENERATED
ECHO '''For auto-generated files''' > src\GENERATED\__init__.py
ECHO # THIS IS AUTO-GENERATED > src\GENERATED\_VERSION.py
python -c "from datetime import datetime; print(f'# {datetime.now()}')" >> src\GENERATED\_VERSION.py
ECHO _VERSION = ''' >> src\GENERATED\_VERSION.py
git describe --tags --dirty >> src\GENERATED\_VERSION.py
ECHO ''' >> src\GENERATED\_VERSION.py
ECHO Done

ECHO -
ECHO -
ECHO Build submodule src\lib\mdmreadpy (generates its GENERATED files)...
PUSHD src\lib\mdmreadpy
CALL build.bat
if %ERRORLEVEL% NEQ 0 ( echo ERROR: Failure && pause && exit /b %errorlevel% )
POPD
ECHO Done

ECHO Calling pinliner...
REM REM :: comment: please delete .pyc files before every call of the mdmoverlayhelper_bundle - this is implemented in my fork of the pinliner
@REM python src_dev_build\lib\pinliner\pinliner\pinliner.py src -o dist/mdmoverlayhelper_bundle.py --verbose
python src_dev_build\lib\pinliner\pinliner\pinliner.py src -o dist/mdmoverlayhelper_bundle.py
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


ECHO -
ECHO -
ECHO Bring LICENSE and README.md to dist...
COPY /Y LICENSE dist\LICENSE
COPY /Y README.md dist\README.md
ECHO Done

ECHO -
ECHO -
ECHO Inline run_init - venv setup + explicit pip installs - into dist launchers...
python src_dev_build\inline_run_init.py
if %ERRORLEVEL% NEQ 0 ( echo ERROR: Failure && pause && exit /b %errorlevel% )
ECHO Done

ECHO -
ECHO -
ECHO Verify the bundle: run --program done...
python dist\mdmoverlayhelper_bundle.py --program done
if %ERRORLEVEL% NEQ 0 ( echo ERROR: Failure && pause && exit /b %errorlevel% )
ECHO Done

ECHO End

