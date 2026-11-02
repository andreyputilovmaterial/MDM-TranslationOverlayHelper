@echo off
setlocal

echo Prep python
echo set venv

if exist ".venv\Scripts\python.exe" (
    set "pythonexecutable=.venv\Scripts\python.exe"
) else (
    echo Creating Python virtual environment...
    python -m venv .venv
    if exist ".venv\Scripts\python.exe" (
        set "pythonexecutable=.venv\Scripts\python.exe"
    ) else (
        echo No Python virtual environment found
        exit /b 1
    )
)

echo Upd dependencies
"%pythonexecutable%" -m pip install -r requirements.txt
echo done
echo.
echo.

@REM Install optional per-submodule dependencies (best-effort).
@REM The distributed copy scans optional_dependencies\ instead.
if exist "src\lib" (
    for /r "src\lib" %%f in (requirements.txt) do (
        echo Installing optional dependencies: %%f
        "%pythonexecutable%" -m pip install -r "%%f"
        if errorlevel 1 echo WARNING: optional dependencies in %%f not installed - the corresponding part will be unavailable
    )
)

"%pythonexecutable%" -m src.launcher --program done
if errorlevel 1 exit /b %errorlevel%

endlocal
