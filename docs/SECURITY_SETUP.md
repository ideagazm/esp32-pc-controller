# ESP32 PC Controller - Security Setup Guide

## 🔐 ESPHome Secrets Configuration

Before deploying your ESP32 PC Controller, you must configure secrets in the ESPHome Web Dashboard. This ensures sensitive information like WiFi passwords and API keys are not stored in plain text.

## Required Secrets

### 1. WiFi Credentials
```yaml
# In ESPHome Web Dashboard Secrets:
wifi_ssid: "YourWiFiNetworkName"
wifi_password: "YourWiFiPassword"
```

### 2. Fallback Access Point
```yaml
# In ESPHome Web Dashboard Secrets:
fallback_password: "YourSecureFallbackPassword"
```

### 3. API Encryption Key
```yaml
# In ESPHome Web Dashboard Secrets:
api_key: "your-base64-encoded-32-byte-key"
```

## 🚀 Step-by-Step Setup

### Step 1: Access ESPHome Web Dashboard
1. Open your ESPHome Web Dashboard (usually http://homeassistant.local:6052 or your HA instance)
2. Click on "Secrets" in the top menu
3. If no secrets file exists, it will be created automatically

### Step 2: Add Required Secrets
Add these entries to your secrets file:

```yaml
# WiFi Network Configuration
wifi_ssid: "Your_Network_Name"
wifi_password: "Your_WiFi_Password"

# Fallback Access Point (for recovery)
fallback_password: "SecureFallbackPass123"

# API Encryption (generate a secure base64-encoded 32-byte key)
api_key: "zvPf8xZaPkhE8LvZosIC8jYJcB8qHnGLyRdDG7vFDxY="
```

### Step 3: Generate Secure API Key

# ─── HOW TO GENERATE API ENCRYPTION KEY ─────────────────────────
# The API encryption key must be a base64-encoded 32-byte random string.
# Here are several ways to generate one:

## ① Using OpenSSL (Linux/Mac/WSL)
```bash
openssl rand -base64 32
```

## ② Using Python (Windows/Linux/Mac)
```bash
python -c "import secrets, base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"
```

## ③ Using PowerShell (Windows)
```powershell
powershell -Command "[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))"
```

## ④ Using Our Key Generator Tools (Easy!)
```bash
# Windows:
scripts\generate_api_key.bat

# Cross-platform:
python scripts\generate_api_key.py
```

## ⑤ Let ESPHome Generate It Automatically
1. In YAML → `key: !secret api_key`
2. Leave `api_key` empty in secrets.yaml initially
3. Click "Install" — ESPHome will generate a key automatically
4. Copy the generated key from logs into secrets.yaml

## ⑥ Online Generator (⚠️ Not recommended for production)
- Visit: https://generate-random.org/api-key-generator
- Set Length: 32, Format: Base64
- **Warning**: Only use for testing, not production systems

**Example valid key format:**
```yaml
api_key: "zvPf8xZaPkhE8LvZosIC8jYJcB8qHnGLyRdDG7vFDxY="
```

**Note**: The key should be ~44 characters long and end with "=" or "=="

### Step 4: Verify Secrets
Your ESPHome secrets file should look like this:
```yaml
# ESPHome Secrets File
wifi_ssid: "MyHomeNetwork"
wifi_password: "MySecureWiFiPassword123"
fallback_password: "ESP32Fallback456"
api_key: "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"
```

## 🛡️ Security Best Practices

### WiFi Security
- **Use WPA3** or WPA2 encryption on your router
- **Strong passwords** - minimum 12 characters with mixed case, numbers, symbols
- **Guest network** - consider putting IoT devices on a separate network
- **MAC filtering** - optionally restrict access by device MAC address

### API Security
- **Unique keys** - generate a unique API key for each device
- **Key rotation** - periodically change API keys
- **Network isolation** - keep ESP32 on local network only

### Fallback Security
- **Strong fallback password** - don't use default passwords
- **Limited time** - fallback AP only activates when WiFi fails
- **Monitor access** - check ESPHome logs for unauthorized connections

### PC Security
- **Firewall rules** - only allow connections from ESP32 IP
- **User accounts** - run Python scripts with minimal required privileges
- **Log monitoring** - review shutdown logs regularly
- **Network segmentation** - consider VLANs for IoT devices

## 🔍 Pre-Deployment Checklist

### Before Generating Templates:
- [ ] ESPHome Web Dashboard is accessible
- [ ] Secrets file is configured with all required entries
- [ ] WiFi credentials are correct and tested
- [ ] API key is generated (32 characters)
- [ ] Fallback password is set (strong password)

### Before Flashing ESP32:
- [ ] ESP32 is connected and detected
- [ ] ESPHome can compile the configuration
- [ ] No syntax errors in YAML
- [ ] Secrets are properly referenced (no plain text passwords)

### Network Security Verification:
- [ ] Router uses WPA2/WPA3 encryption
- [ ] WiFi password is strong (12+ characters)
- [ ] ESP32 will be on correct network segment
- [ ] Firewall rules are configured if needed
- [ ] Guest network is considered for IoT isolation

### PC Security Verification:
- [ ] Each PC has unique IP address
- [ ] Firewall allows port 5000 from ESP32 only
- [ ] Python will run with appropriate privileges
- [ ] Wake-on-LAN is enabled in BIOS and OS
- [ ] Network adapter supports WOL

## 🚨 Security Warnings

### ⚠️ Never Do This:
- **Don't hardcode passwords** in YAML files
- **Don't share secrets files** publicly
- **Don't use default passwords** for fallback AP
- **Don't expose ESP32** to the internet directly
- **Don't run Python scripts** with unnecessary admin privileges

### ✅ Always Do This:
- **Use ESPHome secrets** for all sensitive data
- **Generate unique API keys** for each device
- **Use strong passwords** for all accounts
- **Monitor logs** for suspicious activity
- **Keep firmware updated** on all devices

## 🔧 Troubleshooting Secrets

### "Secret not found" Error
```yaml
# Check secrets file syntax:
wifi_ssid: "NetworkName"  # ✅ Correct
wifi_ssid: NetworkName    # ❌ Missing quotes
```

### "Invalid API key" Error
- Ensure API key is exactly 32 characters
- Use only hexadecimal characters (0-9, a-f)
- Regenerate if corrupted

### "WiFi connection failed" Error
- Verify SSID and password in secrets
- Check 2.4GHz vs 5GHz (ESP32 only supports 2.4GHz)
- Test credentials with another device

### "Fallback AP not accessible" Error
- Check fallback password in secrets
- Look for "ESP32 Fallback" network
- Connect within 1 minute of ESP32 boot failure

## 🏠 Home Assistant Integration Notes

# ────────────────────────────────────────────────────────────────
# 🧩 NOTE: HOME ASSISTANT INTEGRATION QUIRK (as of Nov 2025)

## Common Issue: "The device is disabled by Config entry"
If you see this error with a greyed-out "Enable" button in Home Assistant:

### 🔍 Cause (common scenario):
1. You first added this ESPHome node *without API encryption*
2. Later enabled `api.encryption.key` in the YAML
3. Home Assistant kept the old unencrypted config entry
4. Home Assistant refuses to connect to the new encrypted API

### 🛠️ Solution that works:
1. **Disable** the existing device entry in Home Assistant
2. **Delete** the integration entry completely
3. **Re-add** the ESPHome node with the correct encryption key
4. **Re-enable** the device — connection should restore instantly

### 💡 Prevention Tips:
- Always configure API encryption from the start
- If changing encryption settings, expect to re-add to Home Assistant
- Verify API encryption keys match between ESPHome and Home Assistant

### ⚠️ Disclaimer:
This workaround has been tested with ESPHome v2024.11.x and Home Assistant 
core 2024.11.x. Future versions may behave differently.

**Tip**: If you see a disabled ESPHome device with a greyed-out enable button,
verify your API encryption keys before rebuilding the whole setup.
# ────────────────────────────────────────────────────────────────

## 📚 Additional Resources

### ESPHome Documentation:
- [Secrets Documentation](https://esphome.io/guides/faq.html#how-do-i-use-secrets-yaml)
- [WiFi Component](https://esphome.io/components/wifi.html)
- [API Component](https://esphome.io/components/api.html)

### Security Resources:
- [IoT Security Best Practices](https://www.nist.gov/cybersecurity/iot)
- [Home Network Security](https://www.cisa.gov/secure-our-world)
- [Password Security Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)

## 🎯 Quick Reference

### Minimum Required Secrets:
```yaml
wifi_ssid: "YourNetwork"
wifi_password: "YourPassword"
fallback_password: "SecurePassword"
api_key: "32-character-hex-key"
```

### Security Checklist:
1. ✅ Secrets configured in ESPHome Dashboard
2. ✅ Strong passwords used everywhere
3. ✅ Network security verified
4. ✅ Firewall rules configured
5. ✅ Monitoring plan in place

Remember: Security is not a one-time setup - regularly review and update your configuration!