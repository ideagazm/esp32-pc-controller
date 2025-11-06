@echo off
REM ESP32 PC Controller Template Generator Launcher
REM This script provides an easy way to configure and deploy ESP32 PC controller templates

title ESP32 PC Controller - Template Generator

echo ========================================
echo   ESP32 PC Controller Template Generator
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from python.org
    echo.
    pause
    exit /b 1
)

echo Choose your interface:
echo.
echo 1. GUI Interface (Recommended)
echo 2. Command Line Interface
echo 3. Edit config.ini manually
echo 4. Generate templates with current config
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto gui
if "%choice%"=="2" goto cli
if "%choice%"=="3" goto edit_config
if "%choice%"=="4" goto generate
if "%choice%"=="5" goto exit
goto invalid

:gui
echo.
echo Starting GUI interface...
python gui_launcher.py
goto end

:cli
echo.
echo Starting command line interface...
python template_generator.py
goto end

:edit_config
echo.
echo Opening config.ini for editing...
if exist config.ini (
    notepad config.ini
) else (
    echo config.ini not found. Creating default configuration...
    python -c "from template_generator import TemplateGenerator; TemplateGenerator().config.read('config.ini')"
    notepad config.ini
)
goto end

:generate
echo.
echo Generating templates with current configuration...
python template_generator.py
goto end

:invalid
echo.
echo Invalid choice. Please enter 1-5.
echo.
pause
goto start

:exit
echo.
echo Goodbye!
goto end

:end
echo.
echo Press any key to exit...
pause >nul