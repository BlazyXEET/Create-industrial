@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
    py -3 tools\switch_welder_model.py 2d
) else (
    python tools\switch_welder_model.py 2d
)
if errorlevel 1 (
    echo ERROR: Could not switch. Install Python 3 and extract the full Source folder.
    pause
    exit /b 1
)
echo.
echo The Welder will use the flat 2D icon in your next compiled JAR.
echo For an already installed mod, use the optional 2D resource pack instead.
pause
