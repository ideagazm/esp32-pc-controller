#!/usr/bin/env python3
"""
ESP32 PC Controller - GUI Configuration and Deployment Tool
Simple GUI for configuring and deploying ESP32 PC controller templates
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import configparser
import os
from pathlib import Path
import subprocess
import sys
import shutil
import platform

class ESP32ConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ESP32 PC Controller - Template Generator")
        self.root.geometry("800x600")
        
        # Load config
        self.config = configparser.ConfigParser()
        self.template_config_file = "config.ini"  # Template config (read-only reference)
        self.deployment_config_file = None  # Will be set based on deployment path
        self.load_config()
        
        self.create_widgets()
        
    def load_config(self):
        """Load configuration from deployment or template file"""
        # First, load the template config to get deployment path
        if os.path.exists(self.template_config_file):
            temp_config = configparser.ConfigParser()
            temp_config.read(self.template_config_file)
            deployment_path = temp_config.get('GENERAL', 'deployment_path', fallback='./test_deployment')
        else:
            deployment_path = './test_deployment'
            
        # Set deployment config file path
        self.deployment_config_file = os.path.join(deployment_path, "config.ini")
        
        # Try to load from deployment config first, then template, then create default
        if os.path.exists(self.deployment_config_file):
            self.log_status(f"📋 Loading config from deployment: {self.deployment_config_file}")
            self.config.read(self.deployment_config_file)
        elif os.path.exists(self.template_config_file):
            self.log_status(f"📋 Loading template config: {self.template_config_file}")
            self.config.read(self.template_config_file)
        else:
            # Create default config
            self.create_default_config()

            
    def create_default_config(self):
        """Create default configuration"""
        self.config['ESP32'] = {
            'device_name': 'pc-controller',
            'friendly_name': 'PC Controller',
            'static_ip': '192.168.1.50',
            'gateway': '192.168.1.1',
            'subnet': '255.255.255.0',
            'dns': '192.168.1.1'
        }
        
        self.config['GENERAL'] = {
            'num_pcs': '2',
            'max_pcs': '8',
            'deployment_path': 'C:\\ESP_PC_Controller'
        }
        
        # Default PC configurations
        gpio_pairs = [
            ('GPIO16', 'GPIO17'), ('GPIO18', 'GPIO19'), ('GPIO21', 'GPIO22'),
            ('GPIO23', 'GPIO25'), ('GPIO26', 'GPIO27'), ('GPIO32', 'GPIO33'),
            ('GPIO12', 'GPIO13'), ('GPIO14', 'GPIO15')
        ]
        
        for i in range(8):
            pc_num = i + 1
            self.config[f'PC{pc_num}'] = {
                'name': f'PC{pc_num}',
                'mac_address': f'AA:BB:CC:DD:EE:{pc_num:02d}',
                'ip_address': f'192.168.1.{100 + i}',
                'on_button_gpio': gpio_pairs[i][0],
                'off_button_gpio': gpio_pairs[i][1]
            }
        
        # Don't auto-save default config - let user save when ready
        
    def save_config(self):
        """Save configuration to deployment directory"""
        # Ensure deployment directory exists
        deployment_path = self.deploy_path_var.get()
        os.makedirs(deployment_path, exist_ok=True)
        
        # Update deployment config file path
        self.deployment_config_file = os.path.join(deployment_path, "config.ini")
        
        with open(self.deployment_config_file, 'w') as f:
            self.config.write(f)
        
        self.log_status(f"✅ Configuration saved to: {self.deployment_config_file}")
        self.log_status(f"📄 Template config remains unchanged: {self.template_config_file}")
            
    def create_widgets(self):
        """Create GUI widgets"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ESP32 Configuration Tab
        esp32_frame = ttk.Frame(notebook)
        notebook.add(esp32_frame, text="ESP32 Config")
        self.create_esp32_tab(esp32_frame)
        
        # General Settings Tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General Settings")
        self.create_general_tab(general_frame)
        
        # PC Configuration Tab
        pc_frame = ttk.Frame(notebook)
        notebook.add(pc_frame, text="PC Configuration")
        self.create_pc_tab(pc_frame)
        
        # Deployment Tab
        deploy_frame = ttk.Frame(notebook)
        notebook.add(deploy_frame, text="Deploy")
        self.create_deploy_tab(deploy_frame)
        
    def create_esp32_tab(self, parent):
        """Create ESP32 configuration tab"""
        # Scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # ESP32 settings
        ttk.Label(scrollable_frame, text="ESP32 Configuration", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Security notice
        security_text = "⚠️ SECURITY: WiFi credentials and API keys must be configured in ESPHome Web Dashboard secrets.\nSee docs/SECURITY_SETUP.md for detailed instructions.\n🔑 Generate API key: Run scripts/generate_api_key.py"
        security_label = ttk.Label(scrollable_frame, text=security_text, font=('Arial', 9), foreground='red', wraplength=400)
        security_label.grid(row=1, column=0, columnspan=2, pady=5, padx=5)
        
        self.esp32_vars = {}
        row = 2
        
        esp32_fields = [
            ('device_name', 'Device Name'),
            ('friendly_name', 'Friendly Name'),
            ('static_ip', 'Static IP Address'),
            ('gateway', 'Gateway'),
            ('subnet', 'Subnet Mask'),
            ('dns', 'DNS Server')
        ]
        
        for key, label in esp32_fields:
            ttk.Label(scrollable_frame, text=f"{label}:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
            var = tk.StringVar(value=self.config.get('ESP32', key, fallback=''))
            entry = ttk.Entry(scrollable_frame, textvariable=var, width=30)
            entry.grid(row=row, column=1, padx=5, pady=2)
            self.esp32_vars[key] = var
            row += 1
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_general_tab(self, parent):
        """Create general settings tab"""
        ttk.Label(parent, text="General Settings", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        self.general_vars = {}
        
        # Number of PCs
        ttk.Label(parent, text="Number of PCs:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.num_pcs_var = tk.StringVar(value=self.config.get('GENERAL', 'num_pcs', fallback='2'))
        self.num_pcs_var.trace('w', self.on_num_pcs_changed)  # Add callback for changes
        num_pcs_spin = ttk.Spinbox(parent, from_=1, to=8, textvariable=self.num_pcs_var, width=10)
        num_pcs_spin.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        # Deployment path
        ttk.Label(parent, text="Deployment Path:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.deploy_path_var = tk.StringVar(value=self.config.get('GENERAL', 'deployment_path', fallback='C:\\ESP_PC_Controller'))
        deploy_frame = ttk.Frame(parent)
        deploy_frame.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Entry(deploy_frame, textvariable=self.deploy_path_var, width=40).pack(side='left')
        ttk.Button(deploy_frame, text="Browse", command=self.browse_deploy_path).pack(side='left', padx=5)
        
        # Add info label about active PCs
        self.active_pcs_label = ttk.Label(parent, text="", font=('Arial', 9), foreground='blue')
        self.active_pcs_label.grid(row=3, column=0, columnspan=2, pady=5)
        self.update_active_pcs_label()
        
        # Add config file status
        self.config_status_label = ttk.Label(parent, text="", font=('Arial', 8), foreground='green')
        self.config_status_label.grid(row=4, column=0, columnspan=2, pady=5)
        self.update_config_status_label()
        
    def browse_deploy_path(self):
        """Browse for deployment path"""
        path = filedialog.askdirectory(initialdir=self.deploy_path_var.get())
        if path:
            self.deploy_path_var.set(path)
            # Update deployment config file path and try to load existing config
            new_deployment_config = os.path.join(path, "config.ini")
            if os.path.exists(new_deployment_config):
                self.deployment_config_file = new_deployment_config
                self.config.read(new_deployment_config)
                self.refresh_gui_from_config()
                self.log_status(f"📋 Loaded existing config from: {new_deployment_config}")
            else:
                self.deployment_config_file = new_deployment_config
                self.log_status(f"📁 New deployment path set: {path}")
                
    def refresh_gui_from_config(self):
        """Refresh GUI fields from loaded config"""
        try:
            # Update ESP32 fields
            for key, var in self.esp32_vars.items():
                if self.config.has_option('ESP32', key):
                    var.set(self.config.get('ESP32', key))
                    
            # Update general fields
            if self.config.has_option('GENERAL', 'num_pcs'):
                self.num_pcs_var.set(self.config.get('GENERAL', 'num_pcs'))
            if self.config.has_option('GENERAL', 'deployment_path'):
                self.deploy_path_var.set(self.config.get('GENERAL', 'deployment_path'))
                
            # Update PC fields
            num_pcs = int(self.num_pcs_var.get())
            for pc_num in range(1, num_pcs + 1):
                if pc_num in self.pc_vars and self.config.has_section(f'PC{pc_num}'):
                    for key, var in self.pc_vars[pc_num].items():
                        if self.config.has_option(f'PC{pc_num}', key):
                            var.set(self.config.get(f'PC{pc_num}', key))
                            
            self.update_pc_tabs(num_pcs)
            self.update_active_pcs_label()
        except Exception as e:
            self.log_status(f"⚠️ Warning: Error refreshing GUI: {e}")
            
    def on_num_pcs_changed(self, *args):
        """Callback when number of PCs changes"""
        try:
            num_pcs = int(self.num_pcs_var.get())
            
            # Validate range
            if num_pcs < 1:
                num_pcs = 1
                self.num_pcs_var.set("1")
            elif num_pcs > 8:
                num_pcs = 8
                self.num_pcs_var.set("8")
                
            self.update_pc_tabs(num_pcs)
            self.update_active_pcs_label()
        except ValueError:
            pass  # Ignore invalid values during typing
            
    def update_pc_tabs(self, num_pcs):
        """Update PC tab visibility based on number of PCs"""
        # Get total number of tabs
        total_tabs = self.pc_notebook.index("end")
        
        # Hide all tabs first
        for i in range(total_tabs):
            try:
                self.pc_notebook.tab(i, state="hidden")
            except tk.TclError:
                pass
        
        # Show only the required number of tabs
        for i in range(min(num_pcs, total_tabs)):
            try:
                self.pc_notebook.tab(i, state="normal")
                # Update tab text to show if it's active
                pc_num = i + 1
                pc_name = self.pc_vars[pc_num]['name'].get() if pc_num in self.pc_vars and 'name' in self.pc_vars[pc_num] else f"PC{pc_num}"
                tab_text = f"PC{pc_num}" if not pc_name or pc_name == f"PC{pc_num}" else f"PC{pc_num} ({pc_name})"
                self.pc_notebook.tab(i, text=tab_text)
            except (tk.TclError, KeyError):
                pass
                
        # Select the first visible tab if current selection is hidden
        try:
            current_tab = self.pc_notebook.index(self.pc_notebook.select())
            if current_tab >= num_pcs:
                self.pc_notebook.select(0)
        except (tk.TclError, AttributeError):
            if num_pcs > 0:
                self.pc_notebook.select(0)
                
    def on_pc_name_changed(self, pc_num):
        """Callback when PC name changes"""
        try:
            num_pcs = int(self.num_pcs_var.get())
            if pc_num <= num_pcs:
                # Update the tab title for this PC
                tab_index = pc_num - 1
                pc_name = self.pc_vars[pc_num]['name'].get()
                tab_text = f"PC{pc_num}" if not pc_name or pc_name == f"PC{pc_num}" else f"PC{pc_num} ({pc_name})"
                self.pc_notebook.tab(tab_index, text=tab_text)
        except (ValueError, KeyError, tk.TclError):
            pass
            
    def update_active_pcs_label(self):
        """Update the label showing active PCs"""
        try:
            num_pcs = int(self.num_pcs_var.get())
            if num_pcs == 1:
                label_text = "ℹ️ 1 PC will be configured (PC1 tab active)"
            else:
                label_text = f"ℹ️ {num_pcs} PCs will be configured (PC1-PC{num_pcs} tabs active)"
            self.active_pcs_label.config(text=label_text)
        except (ValueError, AttributeError):
            pass
            
    def update_config_status_label(self):
        """Update the label showing which config file is being used"""
        try:
            if hasattr(self, 'deployment_config_file') and self.deployment_config_file:
                if os.path.exists(self.deployment_config_file):
                    status_text = f"📁 Using deployment config: {os.path.basename(os.path.dirname(self.deployment_config_file))}/config.ini"
                else:
                    status_text = f"📝 Will create: {os.path.basename(os.path.dirname(self.deployment_config_file))}/config.ini"
            else:
                status_text = "📄 Using template config (will save to deployment when ready)"
            self.config_status_label.config(text=status_text)
        except AttributeError:
            pass
            
    def create_pc_tab(self, parent):
        """Create PC configuration tab"""
        # Create notebook for PC tabs
        self.pc_notebook = ttk.Notebook(parent)
        self.pc_notebook.pack(fill='both', expand=True)
        
        self.pc_vars = {}
        
        # Create tabs for each PC (up to max)
        for pc_num in range(1, 9):  # Support up to 8 PCs
            pc_frame = ttk.Frame(self.pc_notebook)
            self.pc_notebook.add(pc_frame, text=f"PC{pc_num}")
            self.create_pc_config(pc_frame, pc_num)
            
        # Initialize tab visibility based on current number of PCs
        try:
            initial_num_pcs = int(self.num_pcs_var.get())
            self.update_pc_tabs(initial_num_pcs)
        except ValueError:
            self.update_pc_tabs(2)  # Default to 2 PCs
            
    def create_pc_config(self, parent, pc_num):
        """Create configuration for a specific PC"""
        ttk.Label(parent, text=f"PC{pc_num} Configuration", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        self.pc_vars[pc_num] = {}
        
        pc_fields = [
            ('name', 'PC Name'),
            ('mac_address', 'MAC Address'),
            ('ip_address', 'IP Address'),
            ('on_button_gpio', 'ON Button GPIO'),
            ('off_button_gpio', 'OFF Button GPIO')
        ]
        
        row = 1
        for key, label in pc_fields:
            ttk.Label(parent, text=f"{label}:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
            var = tk.StringVar(value=self.config.get(f'PC{pc_num}', key, fallback=''))
            
            # Add callback for name changes to update tab titles
            if key == 'name':
                var.trace('w', lambda *args, pc=pc_num: self.on_pc_name_changed(pc))
            
            entry = ttk.Entry(parent, textvariable=var, width=30)
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.pc_vars[pc_num][key] = var
            row += 1
            
        # Add help text
        help_text = """
GPIO Pin Guidelines:
• Safe pins: GPIO12-19, GPIO21-27, GPIO32-33
• Avoid: GPIO0, 2, 6-11, 15 (boot/flash pins)
• GPIO34-39 are input-only (no pullup)

MAC Address Format: AA:BB:CC:DD:EE:FF
IP Address Format: 192.168.1.100
        """
        ttk.Label(parent, text=help_text, font=('Arial', 8), foreground='gray').grid(row=row, column=0, columnspan=2, pady=10)
        
    def create_deploy_tab(self, parent):
        """Create deployment tab"""
        ttk.Label(parent, text="Deployment", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Instructions
        instructions = """
1. Configure ESP32 settings in the ESP32 Config tab
2. Set the number of PCs and deployment path in General Settings
3. Configure each PC in the PC Configuration tab
4. Click 'Save Configuration' to save to deployment directory
5. Click 'Generate Templates' to create deployment files
6. Copy the generated PC folders to each respective computer

Note: Configuration is saved to the deployment directory, keeping the root config.ini as a clean template.
        """
        
        ttk.Label(parent, text=instructions, justify='left').pack(pady=10)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Save Configuration", command=self.save_configuration).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Generate API Key", command=self.generate_api_key).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Generate Templates", command=self.generate_templates).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Backup Config", command=self.backup_config).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Open Deployment Folder", command=self.open_deploy_folder).pack(side='left', padx=5)
        
        # Status text
        self.status_text = tk.Text(parent, height=15, width=80)
        self.status_text.pack(pady=10, fill='both', expand=True)
        
        # Add system info to status
        system_info = f"System: {platform.system()} {platform.release()}"
        self.log_status(f"🖥️ {system_info}")
        self.log_status("Ready for configuration and deployment...")
        
        # Scrollbar for status text
        status_scroll = ttk.Scrollbar(parent, command=self.status_text.yview)
        self.status_text.config(yscrollcommand=status_scroll.set)
        
    def save_configuration(self):
        """Save current configuration"""
        try:
            # Update ESP32 config
            for key, var in self.esp32_vars.items():
                self.config.set('ESP32', key, var.get())
                
            # Update general config
            self.config.set('GENERAL', 'num_pcs', self.num_pcs_var.get())
            self.config.set('GENERAL', 'deployment_path', self.deploy_path_var.get())
            
            # Update deployment config file path
            self.deployment_config_file = os.path.join(self.deploy_path_var.get(), "config.ini")
            
            # Update PC configs
            num_pcs = int(self.num_pcs_var.get())
            for pc_num in range(1, num_pcs + 1):
                if pc_num in self.pc_vars:
                    for key, var in self.pc_vars[pc_num].items():
                        self.config.set(f'PC{pc_num}', key, var.get())
                        
            self.save_config()
            self.update_config_status_label()
            self.log_status("✅ Configuration saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            
    def generate_templates(self):
        """Generate deployment templates"""
        try:
            self.save_configuration()
            
            # Import and run template generator
            from template_generator import TemplateGenerator
            
            self.log_status("🚀 Starting template generation...")
            
            # Use deployment config file if it exists, otherwise use template config
            config_to_use = self.deployment_config_file if self.deployment_config_file and os.path.exists(self.deployment_config_file) else self.template_config_file
            
            generator = TemplateGenerator(config_to_use)
            generator.generate_all()
            
            self.log_status("✅ Template generation completed!")
            deploy_path = self.deploy_path_var.get()
            messagebox.showinfo("Success", f"Templates generated successfully!\n\nNext steps:\n1. Edit config.ini in {deploy_path} for further customization\n2. Copy PC folders to respective computers\n3. Flash pc_controller.yaml to ESP32")
            
        except Exception as e:
            error_msg = f"Failed to generate templates: {e}"
            self.log_status(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)
            
    def generate_api_key(self):
        """Generate API key using the script"""
        try:
            script_path = Path("scripts/generate_api_key.py")
            if script_path.exists():
                # Run the API key generator
                result = subprocess.run([sys.executable, str(script_path)], 
                                      capture_output=True, text=True, cwd=".")
                if result.returncode == 0:
                    self.log_status("🔑 API key generated successfully!")
                    self.log_status("Check the console output or api_key.txt file")
                    
                    # Try to read the generated key file
                    key_file = Path("api_key.txt")
                    if key_file.exists():
                        with open(key_file, 'r') as f:
                            key_content = f.read().strip()
                        self.log_status(f"Generated: {key_content}")
                        messagebox.showinfo("Success", f"API key generated!\n{key_content}\n\nAdd this to your ESPHome secrets file.")
                    else:
                        messagebox.showinfo("Success", "API key generated! Check the console output.")
                else:
                    self.log_status(f"❌ API key generation failed: {result.stderr}")
                    messagebox.showerror("Error", f"Failed to generate API key: {result.stderr}")
            else:
                messagebox.showerror("Error", "API key generator script not found: scripts/generate_api_key.py")
        except Exception as e:
            error_msg = f"Failed to run API key generator: {e}"
            self.log_status(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)

    def backup_config(self):
        """Backup current configuration"""
        try:
            import time
            backup_name = f"config_backup_{int(time.time())}.ini"
            
            # Use deployment config if it exists, otherwise use template config
            config_to_backup = self.deployment_config_file if self.deployment_config_file and os.path.exists(self.deployment_config_file) else self.template_config_file
            
            if os.path.exists(config_to_backup):
                shutil.copy2(config_to_backup, backup_name)
                self.log_status(f"✅ Configuration backed up to: {backup_name}")
                messagebox.showinfo("Success", f"Configuration backed up to:\n{backup_name}")
            else:
                messagebox.showwarning("Warning", "No configuration file to backup")
        except Exception as e:
            error_msg = f"Failed to backup configuration: {e}"
            self.log_status(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)

    def open_deploy_folder(self):
        """Open deployment folder in file explorer"""
        try:
            deploy_path = self.deploy_path_var.get()
            if os.path.exists(deploy_path):
                os.startfile(deploy_path)
            else:
                messagebox.showwarning("Warning", f"Deployment folder does not exist: {deploy_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {e}")
            
    def log_status(self, message):
        """Log status message"""
        # Handle case where status_text might not exist yet (during init)
        if hasattr(self, 'status_text'):
            self.status_text.insert(tk.END, f"{message}\n")
            self.status_text.see(tk.END)
            self.root.update()
        else:
            print(message)  # Fallback to console during initialization


def main():
    """Main function"""
    root = tk.Tk()
    app = ESP32ConfigGUI(root)
    
    # Configure window properties using app reference
    app.root.resizable(True, True)
    app.root.minsize(600, 400)
    
    root.mainloop()


if __name__ == "__main__":
    main()
