@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
    py -3 tools\switch_welder_model.py 3d
) else (
    python tools\switch_welder_model.py 3d
)
if errorlevel 1 (
    echo ERROR: Could not switch. Install Python 3 and extract the full Source folder.
    pause
    exit /b 1
)
echo.
echo The Welder will use the original 62-element V23 3D model in your next compiled JAR.
pause
