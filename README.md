# 🎛️ ESP32 PC Controller - Template Generator

> **Note:** A one-click deployment system for ESP32-based PC remote control with Wake-on-LAN and shutdown capabilities.

A modular ESP32-based PC controller featuring Wake-on-LAN, remote shutdown, physical button control, and web interface integration. Generate organized deployment packages for multiple PCs with customized configurations.

## 📋 Project Overview

This project provides complete remote control over multiple PCs through an ESP32 microcontroller. Control PC power states via physical buttons, web interface, or Home Assistant integration with real-time status feedback.

### Key Features

- **🔊 Wake-on-LAN**: Magic packet transmission for remote PC power-on
- **💻 Remote Shutdown**: Graceful shutdown via HTTP commands with countdown
- **🎮 Physical Controls**: Dedicated ON/OFF buttons for each PC
- **📱 Web Interface**: Browser-based control panel with real-time status
- **🌐 Home Assistant**: Native ESPHome integration for smart home automation
- **🛡️ Security-First**: ESPHome secrets integration, no hardcoded credentials
- **📦 Organized Deployment**: Individual PC folders with all required files
- **⚙️ Template Generator**: GUI and CLI tools for easy configuration

## 🏗️ Project Structure

```
development/
├── ESP32_PC_Controller_Setup.bat  # 🚀 Main launcher
├── gui_launcher.py                # 🖥️ GUI configuration tool
├── template_generator.py          # ⚙️ Core template generator
├── launcher.bat                   # 🔧 CLI launcher
├── config.ini                     # 📝 Configuration template
├── README.md                      # 📚 This file
├── docs/                          # 📖 Documentation
│   ├── SECURITY_SETUP.md          # 🔐 Security configuration
│   ├── DEPLOYMENT_CHECKLIST.md    # ✅ Pre-deployment guide
│   └── INSTALLATION_GUIDE.md      # 📋 Setup instructions
└── scripts/                       # 🛠️ Utility tools
    ├── generate_api_key.bat       # 🔑 Windows key generator
    └── generate_api_key.py        # 🐍 Cross-platform generator

Generated Deployment:
deployment_folder/
├── config.ini                     # 📝 Editable configuration
├── pc_controller.yaml             # 🎛️ ESP32 firmware
├── README.md                      # 📚 Deployment guide
├── kusanagi/                      # 💻 PC1 folder
│   ├── kusanagi_shutdown.py       # 🐍 Shutdown server
│   ├── run_kusanagi.bat           # ▶️ Manual launcher
│   ├── install_kusanagi_service.bat # 🔧 Auto-startup
│   └── README.txt                 # 📄 PC instructions
└── madara/                        # 💻 PC2 folder
    └── ... (same structure)
```

## 🔧 Hardware Requirements

### Core Components
- **ESP32-WROOM-32 DevKit** - Main microcontroller
- **Momentary Push Buttons** - 2 per PC (ON/OFF)
- **Breadboard/PCB** - For prototyping connections
- **Jumper Wires** - GPIO connections
- **USB Cable** - Programming and power
- **5V Power Supply** - Optional external power

### Network Requirements
- **WiFi Router** - 2.4GHz network (ESP32 compatible)
- **Local Network** - All devices on same subnet
- **Static IPs** - Recommended for ESP32 and PCs

## 📦 Software Dependencies

### ESP32 Firmware (ESPHome)
```yaml
# ESPHome configuration
esphome:
  name: pc-controller
  
esp32:
  board: esp32dev
  framework:
    type: arduino

# Required components
api:
  encryption:
    key: !secret api_key

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

wake_on_lan:
http_request:
```

### PC Integration (Python)
```bash
# Required packages
pip install flask>=2.0.0
pip install requests>=2.25.0
```

### Development Tools
```bash
# Template generator dependencies
pip install tkinter        # GUI interface
pip install configparser   # Configuration management
```

## 🚀 Quick Start

### 1. Security Setup (REQUIRED FIRST!)
```bash
# Configure ESPHome secrets BEFORE deployment
# See docs/SECURITY_SETUP.md for detailed instructions

# Required secrets in ESPHome Web Dashboard:
wifi_ssid: "YourWiFiNetwork"
wifi_password: "YourWiFiPassword"  
fallback_password: "SecureFallbackPass"
api_key: "32-character-base64-key"
```

### 2. Generate API Key
```bash
# Windows
scripts\generate_api_key.bat

# Cross-platform
python scripts\generate_api_key.py
```

### 3. Configure and Deploy
```bash
# GUI Method (Recommended)
ESP32_PC_Controller_Setup.bat
# Choose: 1. GUI Setup

# CLI Method
python template_generator.py
```

### 4. Flash ESP32
```bash
# Using ESPHome
esphome run pc_controller.yaml

# Or via Home Assistant ESPHome add-on
```

### 5. Deploy to PCs
```bash
# Copy PC folders to respective computers
# Run setup scripts as Administrator
run_kusanagi.bat              # Manual start
install_kusanagi_service.bat  # Auto-startup
```

## 📖 Documentation

- **[Security Setup](docs/SECURITY_SETUP.md)** - ESPHome secrets configuration
- **[Deployment Checklist](docs/DEPLOYMENT_CHECKLIST.md)** - Pre-deployment verification
- **[Installation Guide](docs/INSTALLATION_GUIDE.md)** - Step-by-step setup

## 🎯 Implementation Phases

### Phase 1: Core System ✅
- [x] Template generator with GUI
- [x] ESPHome YAML generation
- [x] Python shutdown servers
- [x] Security-first design

### Phase 2: Enhanced Features ✅
- [x] Multi-PC support (1-8 PCs)
- [x] Dynamic configuration
- [x] Organized deployment folders
- [x] Auto-startup services

### Phase 3: Advanced Integration 🚧
- [ ] Home Assistant blueprints
- [ ] Voice control integration
- [ ] Mobile app interface
- [ ] OTA update system

## 🛡️ Security Features

- **ESPHome Secrets**: All credentials stored securely
- **API Encryption**: 32-byte base64-encoded keys
- **Local Network Only**: No internet exposure by default
- **Minimal Privileges**: PC scripts run with required permissions only
- **Firewall Integration**: Port-specific access controls

## 🔌 Hardware Wiring

```
ESP32 GPIO Connections (Safe Pins):
┌─────────────┬──────────────┬─────────────┐
│ Function    │ GPIO Pin     │ Connection  │
├─────────────┼──────────────┼─────────────┤
│ PC1 ON      │ GPIO16       │ Button→GND  │
│ PC1 OFF     │ GPIO17       │ Button→GND  │
│ PC2 ON      │ GPIO18       │ Button→GND  │
│ PC2 OFF     │ GPIO19       │ Button→GND  │
│ PC3 ON      │ GPIO21       │ Button→GND  │
│ PC3 OFF     │ GPIO22       │ Button→GND  │
└─────────────┴──────────────┴─────────────┘

Notes:
• Internal pullup resistors enabled
• No external resistors required
• Avoid boot pins (GPIO0, 2, 15)
```

## 🌐 Network Architecture

```
┌─────────────┐    WOL/HTTP   ┌─────────────┐    WOL/HTTP   ┌─────────────┐
│  KUSANAGI   │◄────────────► │    ESP32    │◄────────────► │   MADARA    │
│192.168.0.100│               │192.168.0.50 │               │192.168.0.200│
│  Port 5000  │               │   Port 80   │               │  Port 5000  │
└─────────────┘               └─────────────┘               └─────────────┘
       │                             │                             │
       └─────────────────────────────┼─────────────────────────────┘
                                     │
                              ┌─────────────┐
                              │   Router    │
                              │192.168.0.1  │
                              └─────────────┘
```

## 🔄 How It Works

### Wake-on-LAN Process
1. **Button Press** → ESP32 detects GPIO input
2. **Magic Packet** → ESP32 sends WOL packet to target MAC
3. **PC Boot** → Network adapter wakes PC from sleep/shutdown
4. **Status Update** → ESP32 displays "WOL packet sent"

### Shutdown Process  
1. **Button Press** → ESP32 sends HTTP POST to PC
2. **Command Received** → Python server processes shutdown request
3. **Status Updates** → Real-time countdown sent to ESP32
4. **Graceful Shutdown** → OS shutdown command executed

## 🛠️ Troubleshooting

### Template Generator Issues
- **Python not found**: Install Python 3.7+ from [python.org](https://python.org)
- **Permission errors**: Run launcher as Administrator
- **Config syntax**: Verify INI file format and values

### ESP32 Connection Issues
- **WiFi failure**: Check 2.4GHz network and credentials
- **API errors**: Verify encryption key in secrets
- **Button unresponsive**: Check GPIO wiring and pin assignments

### PC Integration Issues
- **Shutdown fails**: Run Python script as Administrator
- **Connection timeout**: Verify firewall allows port 5000
- **WOL not working**: Enable in BIOS and network adapter settings

## ⚙️ Advanced Configuration

### Multi-Network Setup
```ini
[ESP32]
static_ip = 10.0.0.50
gateway = 10.0.0.1
subnet = 255.255.255.0

[PC1]
ip_address = 10.0.0.100  # Same subnet as ESP32
```

### Custom GPIO Mapping
```ini
[PC1]
on_button_gpio = GPIO12   # Custom pin assignment
off_button_gpio = GPIO13
```

### Deployment Path Customization
```ini
[GENERAL]
deployment_path = D:\ESP32_Controllers\Office_Setup
```

## 🤝 Contributing

This is a personal project, but feedback and suggestions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests for improvements
- Share your deployment configurations
- Contribute to documentation

## 📄 License

This project is provided as-is for educational and personal use. See LICENSE file for details.

## 🙏 Acknowledgments

- **ESPHome Community** - Excellent framework and documentation
- **Home Assistant Team** - Smart home integration platform
- **Arduino/ESP32 Community** - Hardware support and libraries
- **Python Flask Team** - Web framework for PC integration

## 📞 Contact

- **GitHub**: [@IdeaGazm](https://github.com/IdeaGazm)
- **Project**: [ESP32 PC Controller](https://github.com/IdeaGazm/esp32-pc-controller)
- **Issues**: [Report bugs or request features](https://github.com/IdeaGazm/esp32-pc-controller/issues)

---

**⚠️ Disclaimer**: This project involves network communication and PC control. Always test in a safe environment and follow security best practices. Ensure proper network isolation and access controls for production deployments.