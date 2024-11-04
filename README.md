# Flask Remote Desktop

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Downloads](https://img.shields.io/github/downloads/DJJJNabba/flask-remote-desktop/total.svg)](https://github.com/DJJJNabba/flask-remote-desktop/releases)
[![Last Commit](https://img.shields.io/github/last-commit/DJJJNabba/flask-remote-desktop)](https://github.com/DJJJNabba/flask-remote-desktop/commits/main)

<p align="center">
  <img src="static/favicon.png" alt="Favicon" width="600">
</p>

A powerful remote desktop streaming application that allows you to view and control your computer through any web browser. Features high-quality video streaming, remote keyboard/mouse control, and audio streaming support.

<details>
<summary>🚀 Features</summary>

- High-quality screen streaming with adjustable quality (1-100) and FPS (1-60)
- Remote keyboard and mouse control with full support for special keys
- Audio streaming through VB-Cable
- Secure password protection
- User-friendly server control interface
- Fullscreen mode support
- Support for custom domains and secure tunneling
</details>

## Installation

### Option 1: Run Pre-built Executable
1. Download the latest release from the releases page
2. Extract all files to a desired location
3. Run `ServerGUI.exe`
4. Configure your settings in the interface
5. Click "Start Server"
6. Connect through your web browser at the shown address

### Option 2: Run from Source
1. Install Python 3.8 or higher
2. Clone this repository:
   ```bash
   git clone https://github.com/DJJJNabba/flask-remote-desktop.git
   cd flask-remote-desktop
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask App:
   ```bash
   python app.py
   ```

### Option 3: Build from Source
1. Follow steps 1-3 from Option 2
2. Run the build script:
   ```bash
   python build.py
   ```
3. Find the compiled executables in the `dist` folder:
   - `ServerGUI.exe` - The main server control panel interface
   - `AppServer.exe` - The backend server component running the Flask App

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Windows 10 | Windows 10/11 |
| CPU | Dual Core 2GHz | Quad Core 2.5GHz+ |
| RAM | 4GB | 8GB+ |
| Network | 5Mbps Upload | 10Mbps+ Upload |
| Python | 3.8 | 3.11+ |

## Audio Streaming Setup

### Installing VB-Cable Driver
1. Download VB-Cable from [VB-Audio website](https://vb-audio.com/Cable/)
2. Run the installer (VBCABLE_Driver_Pack43.zip)
3. Restart your computer
4. Set up audio routing:
   - Open Windows Sound Settings
   - Under Output, select "CABLE Input (VB-Audio Virtual Cable)"
   - Any audio played will now be streamed to connected clients

## Configuration
Use the server control interface to configure:
- Port number (default: 5000)
- Password (default: your_password)

## Remote Access Setup

### Method 1: Port Forwarding (Basic)
1. Access your router's admin panel
2. Forward port 5000 (or your chosen port) to your computer's local IP
3. Access your stream from anywhere using your public IP

### Method 2: Cloudflare Tunnel (Recommended)

#### Setting Up Cloudflare Tunnel
1. Install cloudflared from [Cloudflare Downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/)
2. Authenticate cloudflared:
   ```bash
   cloudflared tunnel login
   ```
3. Create a tunnel:
   ```bash
   cloudflared tunnel create flask-remote-desktop
   ```
4. Configure the tunnel (create config.yml):
   ```yaml
   url: http://localhost:5000
   tunnel: <Your-Tunnel-ID>
   credentials-file: <Path-to-credentials.json>
   ```
5. Run the tunnel:
   ```bash
   cloudflared tunnel run flask-remote-desktop
   ```

### Setting Up Custom Domain

#### Purchase Domain from Porkbun
1. Visit [Porkbun](https://porkbun.com)
2. Search for your desired domain (many .xyz domains are $1 per YEAR)
3. Complete purchase and account setup

#### Configure DNS with Cloudflare
1. Add your domain to Cloudflare
2. Update nameservers at Porkbun with Cloudflare's nameservers
3. In Cloudflare DNS settings, add a CNAME record:
   - Name: stream (or subdomain of choice)
   - Target: your-tunnel-id.cfargotunnel.com
4. Wait for DNS propagation (usually 5-30 minutes)

Now you can access your stream at: `https://stream.yourdomain.com`

## Security Recommendations
- Change the default password immediately
- Use HTTPS when possible (automatic with Cloudflare)
- Enable 2FA on your Cloudflare account
- Regularly update the application
- Use strong, unique passwords
- Consider IP whitelisting in Cloudflare
- Monitor access logs regularly

## Troubleshooting

### Common Issues
1. Black Screen
   - Ensure you have permission to capture screen
   - Try running as administrator

2. No Audio
   - Verify VB-Cable is installed correctly
   - Check Windows audio settings
   - Ensure CABLE Input is set as default playback device

3. Connection Issues
   - Verify firewall settings
   - Check port availability
   - Ensure correct IP/domain configuration

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=DJJJNabba/flask-remote-desktop&type=Date)](https://star-history.com/#DJJJNabba/flask-remote-desktop&Date)

## 🤝 Contributing

<a href="https://github.com/DJJJNabba/flask-remote-desktop/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=DJJJNabba/flask-remote-desktop" />
</a>

Contributions are welcome! Please feel free to submit a Pull Request. Check out our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💖 Support the Project

If you find this project helpful, please consider:
- Giving it a ⭐️ on GitHub
- Sharing it with friends
- [Buying me a coffee](https://buymeacoffee.com/djjj)

<p align="center">Made with 💻 and no 😴 by the one and only <a href="https://github.com/DJJJNabba">DJJJNabba</a></p>