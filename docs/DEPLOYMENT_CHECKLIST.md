# ESP32 PC Controller - Deployment Checklist

## 🔐 Pre-Deployment Security Setup (REQUIRED)

### ✅ ESPHome Secrets Configuration
- [ ] **ESPHome Web Dashboard** is accessible
- [ ] **Secrets file** is configured with required entries:
  - [ ] `wifi_ssid: "YourNetworkName"`
  - [ ] `wifi_password: "YourWiFiPassword"`
  - [ ] `fallback_password: "SecureFallbackPassword"`
  - [ ] `api_key: "32-character-hex-key"`
- [ ] **API key** is generated (32 characters, hexadecimal)
- [ ] **WiFi credentials** are tested and working
- [ ] **No plain text passwords** in any configuration files

### ✅ Network Security Verification
- [ ] **Router security**: WPA2/WPA3 encryption enabled
- [ ] **Strong WiFi password**: 12+ characters, mixed case, numbers, symbols
- [ ] **Network segmentation**: Consider IoT VLAN if available
- [ ] **ESP32 IP range**: Static IP assigned and available
- [ ] **Firewall rules**: Configured if needed (allow port 5000 from ESP32)

## 🛠️ Hardware Preparation

### ✅ ESP32 Setup
- [ ] **ESP32 board** is functional and detected
- [ ] **USB cable** connected for programming
- [ ] **Power supply** available (USB or 5V adapter)
- [ ] **GPIO pins** identified for button connections
- [ ] **Breadboard/PCB** ready for wiring

### ✅ Button Wiring
- [ ] **Momentary buttons** available (2 per PC)
- [ ] **Jumper wires** for connections
- [ ] **Wiring plan** documented:
  - PC1: ON=GPIO16, OFF=GPIO17
  - PC2: ON=GPIO18, OFF=GPIO19
  - (etc. as configured)

## 🖥️ PC Preparation

### ✅ Each Target PC
- [ ] **Python 3.7+** installed and working
- [ ] **Network connectivity** verified
- [ ] **Static IP** assigned or DHCP reservation set
- [ ] **MAC address** documented for Wake-on-LAN
- [ ] **Administrator access** available for shutdown scripts
- [ ] **Firewall configured** to allow port 5000 from ESP32 IP only

### ✅ Wake-on-LAN Setup
- [ ] **BIOS/UEFI settings**:
  - [ ] Wake-on-LAN enabled
  - [ ] ErP/Deep Sleep disabled
  - [ ] Fast Boot disabled (if causing issues)
- [ ] **Operating System settings**:
  - [ ] Network adapter WOL enabled
  - [ ] "Allow this device to wake computer" checked
  - [ ] "Only allow magic packet" enabled

## 📝 Configuration

### ✅ Template Generator Setup
- [ ] **Config.ini** configured with your settings:
  - [ ] ESP32 device name and network settings
  - [ ] Number of PCs (1-8)
  - [ ] Deployment path chosen
  - [ ] Each PC configured (name, MAC, IP, GPIO pins)
- [ ] **GPIO pin assignments** verified (no conflicts)
- [ ] **IP addresses** unique and available
- [ ] **MAC addresses** correct and verified

### ✅ Generated Files Review
- [ ] **pc_controller.yaml** generated successfully
- [ ] **PC folders** created for each machine
- [ ] **No sensitive data** in generated files (uses !secret references)
- [ ] **File permissions** appropriate for deployment

## 🚀 Deployment Process

### ✅ ESP32 Deployment
1. [ ] **Compile configuration** in ESPHome (no errors)
2. [ ] **Flash firmware** to ESP32 successfully
3. [ ] **WiFi connection** established (check logs)
4. [ ] **Web interface** accessible at configured IP
5. [ ] **Physical buttons** wired and tested

### ✅ PC Deployment (for each PC)
1. [ ] **Copy PC folder** to target computer
2. [ ] **Install Python dependencies**: `pip install flask requests`
3. [ ] **Test manual run**: Right-click `run_pcX.bat` → "Run as administrator"
4. [ ] **Verify connectivity**: Check ESP32 web interface for status
5. [ ] **Test shutdown**: Use ESP32 button or web interface
6. [ ] **Setup auto-start**: Run `install_pcX_service.bat` as administrator

## 🧪 Testing & Verification

### ✅ Connectivity Tests
- [ ] **ESP32 web interface** loads correctly
- [ ] **PC status** shows "Online" on ESP32 interface
- [ ] **Button presses** register on ESP32 (check logs)
- [ ] **Network communication** working both directions

### ✅ Wake-on-LAN Tests
- [ ] **PC powered off** completely
- [ ] **WOL button press** on ESP32 sends magic packet
- [ ] **PC powers on** within 10-30 seconds
- [ ] **Status updates** appear on ESP32 interface

### ✅ Shutdown Tests
- [ ] **PC running** and Python script active
- [ ] **Shutdown button press** sends HTTP command
- [ ] **Status countdown** appears ("Shutting down in 5s...")
- [ ] **PC shuts down** gracefully
- [ ] **No data loss** or corruption

### ✅ Recovery Tests
- [ ] **WiFi failure**: ESP32 creates fallback AP
- [ ] **PC offline**: ESP32 shows connection error
- [ ] **Service restart**: Auto-startup works after reboot
- [ ] **Button failure**: Web interface still functional

## 🔍 Security Verification

### ✅ Final Security Check
- [ ] **No plain text passwords** in any files
- [ ] **ESPHome secrets** properly configured
- [ ] **Firewall rules** restrict access appropriately
- [ ] **PC scripts** run with minimal required privileges
- [ ] **Network traffic** stays on local network only
- [ ] **Logs reviewed** for any security concerns

### ✅ Access Control
- [ ] **Physical security**: ESP32 and buttons in secure location
- [ ] **Network security**: No external access to ESP32
- [ ] **PC security**: Shutdown scripts protected from unauthorized use
- [ ] **Monitoring**: Plan for reviewing logs and access

## 📋 Documentation

### ✅ Record Keeping
- [ ] **Network diagram** with all IP addresses
- [ ] **GPIO pin assignments** documented
- [ ] **MAC addresses** recorded for each PC
- [ ] **Troubleshooting notes** for future reference
- [ ] **Security configuration** documented
- [ ] **Recovery procedures** written down

## 🎯 Go-Live Checklist

### ✅ Final Verification
- [ ] **All PCs** respond to WOL and shutdown commands
- [ ] **Physical buttons** work for all functions
- [ ] **Web interface** accessible and functional
- [ ] **Auto-startup** configured on all PCs
- [ ] **Security measures** in place and verified
- [ ] **Documentation** complete and accessible
- [ ] **Team trained** on operation and troubleshooting

## 🚨 Emergency Procedures

### ✅ Backup Plans
- [ ] **Manual PC access** available if remote fails
- [ ] **ESP32 recovery**: Fallback AP password known
- [ ] **Network recovery**: Alternative access methods
- [ ] **Service recovery**: Manual restart procedures
- [ ] **Contact information**: Support contacts documented

---

## 📞 Support Resources

- **docs/SECURITY_SETUP.md** - Detailed security configuration
- **docs/INSTALLATION_GUIDE.md** - Step-by-step setup instructions
- **README.md** - Complete project documentation
- **ESPHome Documentation** - https://esphome.io/
- **Project Issues** - Check troubleshooting sections

Remember: Security first, test thoroughly, document everything!