#!/usr/bin/env python3
"""
ESP32 PC Controller - API Key Generator
Generates a secure base64-encoded 32-byte API encryption key for ESPHome
"""

import secrets
import base64
import os
import sys

def generate_api_key():
    """Generate a secure base64-encoded 32-byte API key"""
    try:
        # Generate 32 random bytes
        random_bytes = secrets.token_bytes(32)
        
        # Encode as base64
        api_key = base64.b64encode(random_bytes).decode('utf-8')
        
        return api_key
    except Exception as e:
        print(f"❌ Error generating API key: {e}")
        return None

def save_key_to_file(api_key):
    """Save the API key to a text file"""
    try:
        with open('api_key.txt', 'w') as f:
            f.write(f'api_key: "{api_key}"\n')
        return True
    except Exception as e:
        print(f"⚠️ Warning: Could not save to file: {e}")
        return False

def main():
    print("🔐 ESP32 API Key Generator")
    print("═" * 60)
    print()
    print("Generating a secure base64-encoded 32-byte API encryption key")
    print("for use with ESPHome API encryption.")
    print()
    print("═" * 60)
    print()
    
    # Generate the API key
    api_key = generate_api_key()
    
    if api_key:
        print("🎉 SUCCESS! Your new API encryption key:")
        print()
        print(f'    api_key: "{api_key}"')
        print()
        print("📋 Copy this line to your ESPHome Web Dashboard secrets file.")
        print()
        
        # Save to file
        if save_key_to_file(api_key):
            print("💾 The key has been saved to 'api_key.txt' for your convenience.")
        
        print()
        print("═" * 60)
        print()
        print("📚 Next Steps:")
        print("  1. Open ESPHome Web Dashboard")
        print("  2. Click on 'Secrets' in the top menu")
        print("  3. Add the generated line to your secrets file")
        print("  4. Save the secrets file")
        print("  5. Compile and flash your ESP32 configuration")
        print()
        print("🔒 Security Notes:")
        print("  • Keep this key secure and private")
        print("  • Don't share it publicly or commit it to version control")
        print("  • Generate a unique key for each ESP32 device")
        print(f"  • The key should be exactly {len(api_key)} characters long")
        print()
        
    else:
        print("❌ Failed to generate API key.")
        print()
        print("📖 Manual Generation Instructions:")
        print()
        print("🐍 Using Python:")
        print('    python -c "import secrets, base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"')
        print()
        print("🔧 Using OpenSSL (Linux/Mac/WSL):")
        print("    openssl rand -base64 32")
        print()
        print("💻 Using PowerShell (Windows):")
        print("    [Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))")
        print()
        print("🌐 Online Generator (⚠️ Not recommended for production):")
        print("    https://generate-random.org/api-key-generator")
        print("    → Set Length: 32, Format: Base64")
        print()
        
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        
        # Wait for user input if running interactively
        if sys.stdin.isatty():
            input("Press Enter to exit...")
            
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)