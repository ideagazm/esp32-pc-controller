# ESP32 PC Controller - Installation Guide

## Quick Start (5 Minutes)

### Step 1: Download and Setup
1. Download this development folder to your computer
2. Double-click `ESP32_PC_Controller_Setup.bat`
3. Choose option 1 (GUI Setup)

### Step 2: Configure Your Settings
In the GUI:
1. **ESP32 Config Tab**: Enter your WiFi credentials and network settings
2. **General Settings Tab**: Set number of PCs and deployment path
3. **PC Configuration Tab**: Configure each PC (name, MAC, IP, GPIO pins)
4. Click "Save Configuration" then "Generate Templates"

### Step 3: Deploy to ESP32
1. Install ESPHome: `pip install esphome`
2. Flash the generated `pc_controller.yaml` to your ESP32
3. Wire buttons to the configured GPIO pins

### Step 4: Deploy to Each PC
For each generated PC folder:
1. Copy the folder to the target PC
2. Right-click `run_pcX.bat` and "Run as administrator"
3. Test shutdown from ESP32 web interface
4. Run `install_pcX_service.bat` as administrator for auto-startup

## Detailed Configuration

### Finding Your PC Information

#### MAC Address
**Windows:**
```cmd
ipconfig /all
```
Look for "Physical Address" of your network adapter.

**Linux:**
```bash
ip link show
```
Look for the MAC address next to your network interface.

#### IP Address
**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address".

**Linux:**
```bash
ip addr show
```
Look for inet address of your network interface.

### GPIO Pin Selection

**Recommended GPIO pins for ESP32:**
- GPIO16, GPIO17 (PC1 buttons)
- GPIO18, GPIO19 (PC2 buttons)  
- GPIO21, GPIO22 (PC3 buttons)
- GPIO23, GPIO25 (PC4 buttons)
- GPIO26, GPIO27 (PC5 buttons)
- GPIO32, GPIO33 (PC6 buttons)

**Avoid these pins:**
- GPIO0, GPIO2, GPIO15 (boot pins)
- GPIO6-11 (connected to flash)
- GPIO34-39 (input only, no pullup)

### Network Configuration

#### Example Network Setup
```
Router: 192.168.1.1
ESP32: 192.168.1.50
PC1: 192.168.1.100
PC2: 192.168.1.101
PC3: 192.168.1.102
...
```

#### WiFi Configuration
Make sure your ESP32 can connect to your WiFi network:
- Use 2.4GHz network (ESP32 doesn't support 5GHz)
- Check signal strength at ESP32 location
- Ensure network allows device-to-device communication

## Hardware Setup

### Required Components
- ESP32 development board
- 2-8 momentary push buttons (depending on number of PCs)
- Breadboard or PCB for connections
- Jumper wires
- USB cable for programming
- 5V power supply (optional, can use USB)

### Wiring Diagram
```
ESP32 Pin    →    Component
GPIO16       →    PC1 ON Button  → GND
GPIO17       →    PC1 OFF Button → GND
GPIO18       →    PC2 ON Button  → GND
GPIO19       →    PC2 OFF Button → GND
...

Note: Internal pullup resistors are enabled in software
```

### Button Wiring
Each button connects between a GPIO pin and GND:
```
[ESP32 GPIO] ──── [Button] ──── [GND]
```

## Software Requirements

### Development Machine
- Windows 10/11
- Python 3.7 or newer
- Text editor (optional, for manual config editing)

### ESP32
- ESPHome framework
- Arduino framework support

### Target PCs
- Python 3.7 or newer
- Network connectivity
- Administrator privileges (for shutdown)

## Troubleshooting

### Common Issues

#### "Python not found"
**Solution:** Install Python from python.org
- Download Python 3.7+
- During installation, check "Add Python to PATH"
- Restart command prompt after installation

#### "Template generation failed"
**Solution:** Check config.ini syntax
- Ensure all required fields are filled
- Check for typos in IP addresses and MAC addresses
- Verify GPIO pin assignments don't conflict

#### "ESP32 won't connect to WiFi"
**Solution:** Check network settings
- Verify WiFi SSID and password
- Use 2.4GHz network only
- Check signal strength
- Try static IP configuration

#### "PC won't shutdown"
**Solution:** Check PC setup
- Ensure Python script is running as administrator
- Verify firewall allows port 5000
- Check network connectivity between ESP32 and PC
- Test manually: `curl -X POST http://PC_IP:5000/shutdown -d '{"command":"shutdown"}'`

#### "Wake-on-LAN not working"
**Solution:** Enable WOL in BIOS and OS
- Enable "Wake on LAN" in BIOS
- Disable "ErP" or "Deep Sleep" mode in BIOS
- Enable WOL in network adapter properties (Windows)
- Test with another WOL tool first

### Testing Steps

#### Test ESP32 Connectivity
1. Open web browser
2. Navigate to ESP32 IP (e.g., http://192.168.1.50)
3. You should see the control interface

#### Test PC Shutdown Server
1. Open command prompt on PC
2. Run: `curl -X POST http://localhost:5000/status`
3. Should return: `{"status": "online"}`

#### Test End-to-End
1. Press physical button on ESP32
2. Check ESP32 web interface for status updates
3. Verify PC receives and responds to commands

## Advanced Configuration

### Custom Deployment Paths
Edit `config.ini`:
```ini
[GENERAL]
deployment_path = D:\MyESP32Project
```

### Multiple Network Segments
If your PCs are on different network segments, adjust IP ranges:
```ini
[PC1]
ip_address = 192.168.1.100

[PC2]  
ip_address = 10.0.0.100
```

### Custom GPIO Assignments
Assign any available GPIO pins:
```ini
[PC1]
on_button_gpio = GPIO12
off_button_gpio = GPIO13
```

## Security Considerations

### Network Security
- System operates on local network only
- No authentication implemented by default
- Consider VPN for remote access
- Use firewall rules to restrict access

### PC Security
- Python scripts require administrator privileges
- Consider running with minimal required permissions
- Monitor shutdown logs for unauthorized access

## Support and Updates

### Getting Help
1. Check this installation guide
2. Review generated README.txt files in PC folders
3. Test individual components
4. Check network connectivity

### Updating Configuration
1. Edit `config.ini` or use GUI
2. Re-run template generator
3. Copy updated files to PCs
4. Restart services if needed

## License and Credits

This project is provided as-is for educational and personal use.

Built with:
- ESPHome for ESP32 firmware
- Flask for PC shutdown servers
- Python for template generation
- Windows Task Scheduler for auto-startup