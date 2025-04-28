# Clash of Clans Auto-Farming Bot

An automated bot for Clash of Clans that handles farming, trophy dropping, and looting operations using image recognition and ADB (Android Debug Bridge).

## Features

- **Multiple Operation Modes**:
  - **Normal Mode**: Standard farming with trophy range checks
  - **Force Drop Mode**: Dedicated trophy dropping
  - **Force Loot Mode**: Continuous looting without trophy checks
  - **Legends Mode**: Support for legends league (currently identical to normal mode)

- **Automatic Detection**:
  - Recognizes in-game elements using template matching
  - Reads trophy counts via OCR (Optical Character Recognition)
  - Handles attack sequences with randomized movements

## Prerequisites

Before you begin, ensure you have the following installed:

- Python
- Android Emulator with ADB support (BlueStacks recommended)
- Clash of Clans game
- ADB (Android Debug Bridge)
- Additional Python libraries

## Installation Guide

### 1. Install an Android Emulator

Download and install [BlueStacks](https://www.bluestacks.com/) or any other Android emulator that supports ADB connections.

### 2. Configure Emulator

1. Launch your emulator.
2. Set the resolution to **2400x1080** (critical for template matching)
   - In BlueStacks: Settings → Display → Set resolution to 2400x1080
3. Enable ADB connections:
   - In BlueStacks: Settings → Advanced → Android Debug Bridge → Enable
4. Enable pointer location information:
   - In BlueStacks: Settings → Advanced → Enable "Show pointer information for current touch data"
   - This will help with identifying screen coordinates for configuration

### 3. Install Clash of Clans

1. Open Google Play Store in your emulator.
2. Search for "Clash of Clans" and install it.
3. Launch the game and complete the initial setup.

### 4. Install ADB

#### Windows:

1. Download the [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)
2. Extract the ZIP file to a folder (e.g., `C:\adb`)
3. Add the folder to your system PATH:
   - Press Win+S, type "environment variables" and select "Edit the system environment variables"
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and add the path to your ADB folder (e.g., `C:\adb`)
   - Click "OK" on all dialogs

#### macOS:

```bash
brew install android-platform-tools
```

#### Ubuntu/Debian:

```bash
sudo apt-get install android-tools-adb
```

### 5. Install Tesseract OCR

#### Windows:

1. Download the [Tesseract installer](https://github.com/tesseract-ocr/tesseract).
2. Run the installer, noting the installation location.
3. Add Tesseract to your PATH:
   - Follow the same steps as for ADB, adding the Tesseract installation directory.
   - Default is typically `C:\Program Files\Tesseract-OCR`.

#### macOS:

```bash
brew install tesseract
```

#### Ubuntu/Linux:

```bash
sudo apt install tesseract-ocr
```

### 6. Clone the Repository

```bash
git clone https://github.com/yourusername/coc_bot.git
cd coc_bot
```

### 7. Install Python Dependencies

```bash
pip install opencv-python pytesseract numpy
```

## Configuration

Verify ADB connection to your emulator:

```bash
adb devices
```

You should see your emulator listed as a connected device.

Create the configuration file:

```bash
cp config.example.json config.json
```

Or manually create a `config.json` file in the root directory with the following structure:

```json
{
  "trophy_roi": {
    "x1": 230,
    "y1": 165,
    "x2": 325,
    "y2": 205
  }
}
```

Adjust the ROI (Region of Interest) settings:

- The default settings are calibrated for 2400x1080 resolution.
- Use BlueStacks' pointer information feature to determine exact pixel coordinates.
- Adjust the values in `config.json` to match the trophy count location on your screen.

## Usage

1. Start your emulator and launch Clash of Clans.
2. Open a terminal/command prompt.
3. Navigate to the project's `src` directory:

```bash
cd path/to/coc_bot/src
```

4. Run the bot:

```bash
python main.py
```

5. Select a mode when prompted:
   - `force_drop`: Drops trophies (enters matches and surrenders)
   - `force_loot`: Continuously farms resources without trophy checks
   - `normal`: Standard mode with trophy monitoring (drops trophies when above threshold)
   - `legends`: For legends league play (currently same as normal)

6. If prompted for iterations, enter a number or wait for automatic selection.

## Finding Coordinates for Templates and Actions

- Enable the pointer information display in BlueStacks.
- Touch areas on the screen where you want the bot to interact.
- Note the X and Y coordinates shown.
- Use these coordinates to:
  - Adjust the `trophy_roi` in `config.json`
  - Create new templates for buttons or game elements
  - Modify hardcoded coordinates in the script if needed

## Troubleshooting

### Template Matching Failures

- Verify your emulator is set to 2400x1080 resolution.
- Update template images in the `templates/` folder.

### ADB Connection Issues

Restart the ADB server:

```bash
adb kill-server
adb start-server
```

Verify your emulator is running and properly configured for ADB.

### OCR Problems

- Ensure Tesseract is properly installed and in your PATH.
- Try adjusting the ROI in `config.json` to better isolate trophy numbers.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This bot is for educational purposes only. Using bots or automation tools may violate Clash of Clans' Terms of Service. Use at your own risk.
=======