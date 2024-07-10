@echo off
REM Check if pip is installed
python -m pip --version > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installing pip...
    python get-pip.py
)

REM Install numpy
echo Installing Dependencies
python -m pip install numpy
python -m pip install tkinter
python -m pip install tkcalendar
python -m pip install pandas
REM Pause to see output (optional)
pause
