@echo off
echo Starting Batch Graph Converter...
python convert_all_gui.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python is not installed or not added to PATH.
    echo Please make sure Python is installed and 'Add Python to PATH' option was checked during installation.
    echo.
    pause
)
