@echo off
chcp 65001 >nul
cd /d "%~dp0"

set "VENV=.venv-media-client"
set "PY=%VENV%\Scripts\python.exe"

if exist "%PY%" goto run

echo Creating local Python environment...
py -3.11 -m venv "%VENV%" 2>nul
if errorlevel 1 py -3 -m venv "%VENV%" 2>nul
if errorlevel 1 python -m venv "%VENV%"
if errorlevel 1 (
  echo Could not create a Python virtual environment.
  pause
  exit /b 1
)

echo Installing dependencies...
"%PY%" -m pip install --upgrade pip
"%PY%" -m pip install -r requirements-app.txt
if errorlevel 1 (
  echo Dependency installation failed.
  pause
  exit /b 1
)

:run
set "CUDA12_DIR="
for /d %%D in ("C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.*") do set "CUDA12_DIR=%%~fD"
if defined CUDA12_DIR set "PATH=%CUDA12_DIR%\bin;%PATH%"
if exist "%~dp0cuda-dlls" set "PATH=%~dp0cuda-dlls;%PATH%"
if exist "%~dp0.venv-media-client\Lib\site-packages\ctranslate2" set "PATH=%~dp0.venv-media-client\Lib\site-packages\ctranslate2;%PATH%"

netstat -ano | findstr /R /C:":7860 .*LISTENING" >nul
if not errorlevel 1 (
  echo Port 7860 is already in use.
  echo Please close the old client window first, then run this file again.
  echo If you cannot find it, open Task Manager and end the old python.exe process using port 7860.
  pause
  exit /b 1
)

echo Starting local web client at http://127.0.0.1:7860
if not exist "server_logs" mkdir "server_logs"
start "" "http://127.0.0.1:7860"

:server_loop
echo Server running. Logs: server_logs\server.log and server_logs\server.err.log
"%PY%" app.py --host 127.0.0.1 --port 7860 >> "server_logs\server.log" 2>> "server_logs\server.err.log"
set "EXITCODE=%ERRORLEVEL%"
echo [%date% %time%] Server exited with code %EXITCODE%. Restarting in 5 seconds... >> "server_logs\server.err.log"
echo Server exited with code %EXITCODE%. Restarting in 5 seconds...
timeout /t 5 /nobreak >nul
goto server_loop
pause
