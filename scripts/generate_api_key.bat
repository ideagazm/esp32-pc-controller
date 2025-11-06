@echo off
REM ESP32 PC Controller - API Key Generator
REM Generates a secure base64-encoded 32-byte API encryption key for ESPHome

title ESP32 API Key Generator

cls
echo.
echo  🔐 ESP32 API Key Generator
echo  ═══════════════════════════════════════════════════════════════
echo.
echo  This tool generates a secure base64-encoded 32-byte API encryption key
echo  for use with ESPHome API encryption.
echo.
echo  The generated key should be added to your ESPHome secrets file as:
echo      api_key: "generated-key-here"
echo.
echo  ═══════════════════════════════════════════════════════════════
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Trying PowerShell method...
    goto powershell_method
)

echo ✅ Python found. Generating API key using Python...
echo.

REM Generate key using Python
for /f "delims=" %%i in ('python -c "import secrets, base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"') do set API_KEY=%%i

if defined API_KEY (
    echo 🎉 SUCCESS! Your new API encryption key:
    echo.
    echo     api_key: "%API_KEY%"
    echo.
    echo 📋 Copy this line to your ESPHome secrets file.
    echo.
    echo 💾 The key has been saved to api_key.txt for your convenience.
    echo api_key: "%API_KEY%" > api_key.txt
    goto end
)

:powershell_method
echo.
echo 🔄 Generating API key using PowerShell...
echo.

REM Generate key using PowerShell
for /f "delims=" %%i in ('powershell -Command "[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))"') do set API_KEY=%%i

if defined API_KEY (
    echo 🎉 SUCCESS! Your new API encryption key:
    echo.
    echo     api_key: "%API_KEY%"
    echo.
    echo 📋 Copy this line to your ESPHome secrets file.
    echo.
    echo 💾 The key has been saved to api_key.txt for your convenience.
    echo api_key: "%API_KEY%" > api_key.txt
    goto end
) else (
    echo ❌ Failed to generate API key using PowerShell.
    goto manual_instructions
)

:manual_instructions
echo.
echo 📖 Manual Generation Instructions:
echo.
echo If automatic generation failed, you can generate a key manually:
echo.
echo 🐍 Using Python:
echo     python -c "import secrets, base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"
echo.
echo 🔧 Using OpenSSL (Linux/Mac/WSL):
echo     openssl rand -base64 32
echo.
echo 💻 Using PowerShell:
echo     [Convert]::ToBase64String((1..32 ^| ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
echo.
echo 🌐 Online Generator (⚠️ Not recommended for production):
echo     https://generate-random.org/api-key-generator
echo     → Set Length: 32, Format: Base64
echo.

:end
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📚 Next Steps:
echo  1. Copy the generated key to your ESPHome Web Dashboard secrets
echo  2. Add this line to your secrets file:
echo     api_key: "your-generated-key-here"
echo  3. Save the secrets file
echo  4. Compile and flash your ESP32 configuration
echo.
echo 🔒 Security Notes:
echo  • Keep this key secure and private
echo  • Don't share it publicly or commit it to version control
echo  • Generate a unique key for each ESP32 device
echo  • The key should be exactly 44 characters long
echo.
echo Press any key to exit...
pause >nul