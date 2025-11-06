@echo off
REM ESP32 PC Controller - One-Click Setup Tool
REM This is the main entry point for configuring and deploying your ESP32 PC controller

title ESP32 PC Controller - One-Click Setup

:start
cls
echo.
echo  ███████╗███████╗██████╗ ██████╗ ██████╗     ██████╗  ██████╗
echo  ██╔════╝██╔════╝██╔══██╗╚════██╗╚════██╗    ██╔══██╗██╔════╝
echo  █████╗  ███████╗██████╔╝ █████╔╝ █████╔╝    ██████╔╝██║     
echo  ██╔══╝  ╚════██║██╔═══╝ ██╔═══╝ ██╔═══╝     ██╔═══╝ ██║     
echo  ███████╗███████║██║     ███████╗███████╗    ██║     ╚██████╗
echo  ╚══════╝╚══════╝╚═╝     ╚══════╝╚══════╝    ╚═╝      ╚═════╝
echo.
echo                    PC Controller Template Generator
echo                           One-Click Setup Tool
echo.
echo ========================================================================
echo.
echo Welcome! This tool will help you set up remote PC control using ESP32.
echo.
echo What you'll get:
echo  • Wake-on-LAN capability for multiple PCs
echo  • Remote shutdown with physical buttons
echo  • Organized deployment folders for each PC
echo  • Auto-generated configuration files
echo  • Secure secrets management via ESPHome
echo.
echo ⚠️  IMPORTANT: Configure ESPHome secrets BEFORE deployment!
echo     See SECURITY_SETUP.md for required WiFi credentials and API keys.
echo.
echo Choose your setup method:
echo.
echo  1. 🖥️  GUI Setup (Easy - Recommended for beginners)
echo  2. ⚙️  Advanced Configuration (Edit config.ini manually)
echo  3. 🔐 Security Setup Guide (REQUIRED - Read first!)
echo  4. 🔑 Generate API Key (For ESPHome secrets)
echo  5. 🚀 Quick Deploy (Use current settings)
echo  6. 📁 Open Deployment Folder
echo  7. 📖 View Documentation
echo  8. 📚 Open Docs Folder
echo  9. ❌ Exit
echo.

set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto gui_setup
if "%choice%"=="2" goto advanced_config
if "%choice%"=="3" goto security_setup
if "%choice%"=="4" goto generate_api_key
if "%choice%"=="5" goto quick_deploy
if "%choice%"=="6" goto open_folder
if "%choice%"=="7" goto documentation
if "%choice%"=="8" goto open_docs
if "%choice%"=="9" goto exit
goto invalid_choice

:gui_setup
cls
echo.
echo 🖥️ Starting GUI Setup...
echo.
echo The GUI will help you configure:
echo  • ESP32 network settings (WiFi, IP addresses)
echo  • Number of PCs to control (1-8 supported)
echo  • PC details (names, MAC addresses, IP addresses)
echo  • GPIO pin assignments for buttons
echo.
echo Press any key to launch the GUI...
pause >nul

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    goto start
)

echo Starting GUI...
python gui_launcher.py
echo.
echo GUI closed. Press any key to return to main menu...
pause >nul
goto start

:security_setup
cls
echo.
echo 🔐 Security Setup Guide
echo.
echo IMPORTANT: You must configure ESPHome secrets BEFORE deploying!
echo.
echo Required secrets in ESPHome Web Dashboard:
echo  • wifi_ssid: "YourWiFiNetworkName"
echo  • wifi_password: "YourWiFiPassword"
echo  • fallback_password: "SecureFallbackPassword"
echo  • api_key: "base64-encoded-32-byte-key"
echo.
echo 🔑 Generate API key: Run scripts\generate_api_key.bat
echo 📖 Full guide: Opening detailed security setup guide...
echo.
pause

if exist docs\SECURITY_SETUP.md (
    start "" docs\SECURITY_SETUP.md
) else (
    echo docs\SECURITY_SETUP.md not found.
)

echo.
echo Press any key to return to main menu...
pause >nul
goto start

:advanced_config
cls
echo.
echo ⚙️ Advanced Configuration
echo.
echo This will open config.ini for manual editing.
echo.
echo Configuration sections:
echo  [ESP32]    - Device name, WiFi, network settings
echo  [GENERAL]  - Number of PCs, deployment path
echo  [PC1-PC8]  - Individual PC configurations
echo.
echo Press any key to open config.ini...
pause >nul

if exist config.ini (
    notepad config.ini
) else (
    echo Creating default config.ini...
    python -c "from template_generator import TemplateGenerator; t = TemplateGenerator(); t.save_config()"
    notepad config.ini
)

echo.
echo Configuration file closed.
echo.
echo Would you like to generate templates now? (y/n)
set /p generate="Generate templates? (y/n): "
if /i "%generate%"=="y" goto quick_deploy
goto start

:generate_api_key
cls
echo.
echo 🔑 Generate API Key
echo.
echo This will generate a secure base64-encoded 32-byte API encryption key
echo for use with ESPHome API encryption.
echo.
echo Choose your method:
echo  1. Windows Batch Script (Recommended for Windows)
echo  2. Python Script (Cross-platform)
echo  3. Return to main menu
echo.

set /p api_choice="Enter your choice (1-3): "

if "%api_choice%"=="1" goto api_batch
if "%api_choice%"=="2" goto api_python
if "%api_choice%"=="3" goto start
goto invalid_api_choice

:api_batch
cls
echo.
echo 🔑 Running Windows API Key Generator...
echo.
if exist scripts\generate_api_key.bat (
    call scripts\generate_api_key.bat
) else (
    echo ❌ API key generator not found: scripts\generate_api_key.bat
)
echo.
pause
goto start

:api_python
cls
echo.
echo 🔑 Running Python API Key Generator...
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.7+ or use the Windows batch method.
    pause
    goto generate_api_key
)

if exist scripts\generate_api_key.py (
    python scripts\generate_api_key.py
) else (
    echo ❌ API key generator not found: scripts\generate_api_key.py
)
echo.
pause
goto start

:invalid_api_choice
cls
echo.
echo ❌ Invalid choice. Please enter 1, 2, or 3.
echo.
pause
goto generate_api_key

:quick_deploy
cls
echo.
echo 🚀 Quick Deploy - Generating Templates
echo.
echo This will create deployment folders using your current configuration.
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed
    pause
    goto start
)

echo Generating templates...
echo.
python template_generator.py

if errorlevel 1 (
    echo.
    echo ❌ Template generation failed. Check your configuration.
    pause
    goto start
)

echo.
echo ✅ Templates generated successfully!
echo.
echo Next steps:
echo  1. Flash pc_controller.yaml to your ESP32 using ESPHome
echo  2. Wire physical buttons to the configured GPIO pins
echo  3. Copy each PC folder to the respective computer
echo  4. Run the setup scripts on each PC
echo.
echo Press any key to continue...
pause >nul
goto start

:open_folder
cls
echo.
echo 📁 Opening Deployment Folder
echo.

REM Read deployment path from config.ini
for /f "tokens=2 delims== " %%a in ('findstr "deployment_path" config.ini 2^>nul') do set deploy_path=%%a

if "%deploy_path%"=="" set deploy_path=./test_deployment

if exist "%deploy_path%" (
    echo Opening: %deploy_path%
    start "" "%deploy_path%"
) else (
    echo Deployment folder not found: %deploy_path%
    echo.
    echo Run "Quick Deploy" first to generate the templates.
)

echo.
pause
goto start

:documentation
cls
echo.
echo 📖 Documentation
echo.
echo Opening README.md with system default application...
echo.

if exist README.md (
    start "" README.md
) else (
    echo README.md not found in current directory.
)

echo Press any key to return to main menu...
pause >nul
goto start

:invalid_choice
cls
echo.
echo ❌ Invalid choice. Please enter a number between 1-9.
echo.
pause
goto start

:open_docs
cls
echo.
echo 📚 Opening Documentation Folder
echo.
echo Available documentation:
echo  • SECURITY_SETUP.md - Security configuration guide
echo  • DEPLOYMENT_CHECKLIST.md - Pre-deployment checklist  
echo  • INSTALLATION_GUIDE.md - Step-by-step setup guide
echo.

if exist docs (
    echo Opening docs folder...
    start "" docs
) else (
    echo Documentation folder not found: docs
)

echo.
pause
goto start

:exit
cls
echo.
echo Thank you for using ESP32 PC Controller Template Generator!
echo.
echo If you found this tool helpful, consider:
echo  • Sharing it with others who might need it
echo  • Contributing improvements to the project
echo  • Providing feedback for future versions
echo.
echo Happy controlling! 🎮
echo.
pause
exit /b 0