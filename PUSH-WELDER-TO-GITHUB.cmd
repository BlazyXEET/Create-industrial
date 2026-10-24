@echo off
setlocal
cd /d "%~dp0"
echo Publishing the Welder and multiblock project to a NEW GitHub branch.
echo Offline tests, a Minecraft build, and GameTests must all pass.
echo The script never force-pushes or modifies main.
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Publish-Welder-To-GitHub.ps1" -Push
if errorlevel 1 (
  echo.
  echo CHECKS OR PUSH FAILED. Review the error above; main was not changed.
) else (
  echo.
  echo Publishing script completed successfully.
)
pause
endlocal
