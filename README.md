
# IRAQI-RAT v1.0


## Features
- **Dynamic Theme Switching**: Choose from multiple themes like Matrix, Ghost in Shell, Baghdad Nights, and more.
- **Remote Keylogging**: Start and stop keylogging on the remote device.
- **Screen Sharing**: Capture the remote screen in real-time.
- **Webcam Capture**: Access the remote device's webcam feed.
- **File Transfer**: Upload and download files to/from the remote device.
- **Custom Commands**: Execute shell commands on the remote device.
- **Audio Recording**: Record audio from the remote device's microphone.
- **Process Manager**: View and manage processes on the remote device.
- **Credential Harvester**: Retrieve saved credentials from browsers and the system.
- **Encryption/Decryption**: Encrypt and decrypt files on the remote device.
- **Persistence**: Ensure the client remains active even after a system restart.

## Interface Themes
The GUI supports multiple themes to provide a customizable user experience:
- Matrix
- Ghost in Shell
- Baghdad Nights
- Neon Glow
- Cyberpunk Retro
- Oceanic Wave
- Many more...

## Installation
### Prerequisites
- Python 3.9+
- Tkinter (included in the standard Python library)
- PIL (Python Imaging Library)
- OpenCV
- Numpy
- Psutil
- PyInstaller

### Steps to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/apkaless/IRAQI-RAT.git
   cd IRAQI-RAT
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python iraqiRAT.py
   ```

## Usage
1. Launch the GUI application.
2. Configure the server IP and port in the builder section.
3. Build the client executable using the built-in builder.
4. Deploy the client executable on the target machine.
5. Manage connections, perform actions like keylogging, file transfer, webcam capture, and more.

## Security Notice
This tool is intended for educational and ethical purposes only. Unauthorized use on devices you do not own or have permission to control is illegal and punishable by law. The creators of this tool are not responsible for any misuse.

## How to Build a Client
1. Go to the "RAT Client Builder" section.
2. Enter the server IP and port.
3. Enable optional features such as persistence, UAC bypass, and antivirus evasion.
4. Click "Build EXE" to create the client executable.
5. Deploy the generated client on the target machine.

## Functionality Overview
| Feature                | Description                                  |
|------------------------|----------------------------------------------|
| Keylogging             | Logs keystrokes from the target device       |
| Screen Sharing         | Captures and streams the target's screen     |
| Webcam Capture         | Accesses the target's webcam feed            |
| File Transfer          | Uploads and downloads files                  |
| Custom Commands        | Executes shell commands on the target        |
| Process Manager        | Displays and manages target processes        |
| Credential Harvester   | Collects saved credentials                  |
| Audio Recording        | Records audio from the target's microphone   |
| Encryption/Decryption  | Encrypts and decrypts files on the target    |

## Disclaimer
This project is intended for educational and ethical use only. The author does not condone illegal or unethical use of this software. Use responsibly.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
