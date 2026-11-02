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
ECHO Bring LICENSE, README.md and requirements.txt to dist...
COPY /Y LICENSE dist\LICENSE
COPY /Y README.md dist\README.md
COPY /Y requirements.txt dist\requirements.txt
ECHO Done

ECHO -
ECHO -
ECHO Collect optional per-submodule requirements into dist\optional_dependencies...
powershell -NoProfile -Command ^
"$srcRoot = (Resolve-Path 'src').Path; ^
$destRoot = 'dist\optional_dependencies'; ^
Get-ChildItem -Path (Join-Path $srcRoot 'lib') -Recurse -Filter 'requirements.txt' -File | Where-Object { ^
    $_.FullName -notmatch '\\dist\\' -and $_.FullName -notmatch '\\.git\\' -and $_.FullName -notmatch '\\GENERATED\\' ^
} | ForEach-Object { ^
    $rel = $_.FullName.Substring($srcRoot.Length + 1); ^
    $dest = Join-Path $destRoot $rel; ^
    $destDir = Split-Path -Parent $dest; ^
    if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }; ^
    Copy-Item $_.FullName $dest -Force; ^
    Write-Host ('copying optional requirements: ' + $rel) ^
}; "
ECHO Done

ECHO -
ECHO -
ECHO Copy and adapt run_init scripts to dist...
powershell -NoProfile -Command ^
"$c = Get-Content 'run_init.bat' -Encoding 'Default'; ^
$c = $c -replace 'src\\lib', 'optional_dependencies'; ^
$c = $c -replace '-m src\.launcher', 'mdmoverlayhelper_bundle.py'; ^
Set-Content 'dist\run_init.bat' $c -Encoding 'Default'; ^
$c = Get-Content 'run_init.sh' -Encoding 'Default'; ^
$c = $c -replace 'src/lib', 'optional_dependencies'; ^
$c = $c -replace '-m src\.launcher', 'mdmoverlayhelper_bundle.py'; ^
Set-Content 'dist\run_init.sh' $c -Encoding 'Default'; "
ECHO Done

ECHO -
ECHO -
ECHO Verifying the bundle imports correctly...
python dist\mdmoverlayhelper_bundle.py --program done
if %ERRORLEVEL% NEQ 0 ( echo ERROR: Failure && pause && exit /b %errorlevel% )
ECHO Done

ECHO End

