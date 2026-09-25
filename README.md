# 🦀 Crafty Crab - Voice Operated Amma Wisdom Chatbot

Crafty Crab is an interactive, voice-operated AI chatbot assistant that shares Amma's spiritual philosophy and humanitarian wisdom. It uses OpenAI Whisper for Speech-to-Text (STT), OpenAI GPT models with live Tavily internet search integration, and OpenAI TTS for realistic audio vocalization.

---

## 🛠️ Prerequisites & Hardware Setup
Before installing the software stack, ensure your hardware environment meets the following conditions:
* **Audio Input:** A functional microphone interface. For **Raspberry Pi** projects, an external USB microphone dongle, USB webcam mic, or an I2S Audio HAT (e.g., ReSpeaker) is mandatory.
* **Audio Output:** Working desktop speakers, headphones, an external USB speaker, or an HDMI display panel with audio capabilities.
* **API Accounts:** Active accounts and secret keys generated for:
  * [OpenAI Developer Platform](https://openai.com) (For AI brain, STT, and TTS)
  * [Tavily AI Engine](https://tavily.com) (For live web search data integration)

---

## 💻 Environment Setup & Installation

### 🟥 Option A: Ubuntu Linux Setup (Recommended for Local/Raspberry Pi)
Open your terminal emulator panel and run the following system commands:

1. **Install Hardware Media Frameworks:**
   ```bash
   sudo apt update
   sudo apt install -y portaudio19-dev ffmpeg alsa-utils libasound2-dev python3-venv python3-dev build-essential
   ```

2. **Initialize Isolated Workspace:**
   ```bash
   cd ~/Desktop/crafty_crab/
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

### 🟦 Option B: Windows Configuration
Open PowerShell or Command Prompt (CMD) as an Administrator:

1. **Install System Binaries:**
   * Download and install Python 3.10+ from the [Official Python Web Portal](https://python.org) (Make sure to check the **"Add Python to PATH"** checkbox during setup).
   * Download and extract **FFmpeg** binaries from [Gyan.dev](https://gyan.dev), then add the extraction path folder to your Windows System environment variable paths.

2. **Initialize Workspace Environment:**
   ```powershell
   cd C:\Users\YourUsername\Desktop\crafty_crab\
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Wheel & Compilation Dependencies:**
   * *Note: PyAudio compilation on Windows may require Microsoft C++ Build Tools installed via the Visual Studio Installer.*
   ```powershell
   pip install pipwin
   pipwin install pyaudio
   pip install -r requirements.txt
   ```

---

## 🔑 Secure Key Management Configuration
Never commit your private developer authentication string records to GitHub. Create a hidden tracking file named `.env` in the root folder context:

```env
OPENAI_API_KEY="sk-proj-YOUR_SECRET_OPENAI_KEY"
TAVILY_API_KEY="tvly-dev-YOUR_SECRET_TAVILY_KEY"
```

---

## 🚀 Execution Instructions
Ensure your virtual environment wrapper layer remains active, then run the pipeline execution script:

```bash
# On Linux / Raspberry Pi
python3 crafty_crab_amma.py
# On Windows
python crafty_crab_amma.py
```
Press **Enter** once to activate the smart Voice Activity Detection microphone listener loop, speak your inquiry, and the Crab will execute search indexing and audibly respond!

## API KEYS 
take the api key of both open ai and tavily api key from the official sites

## raspberry connections requirements
```powershell
sudo apt update
sudo apt install -y portaudio19-dev python3-dev ffmpeg
```
## setup venv 
```bash
cd ~/Desktop/crafty_crab
python3 -m venv myenv
source myenv/bin/activate
```

## install required libraries
```bash
pip install --upgrade pip
pip install openai tavily-python pypdf pyaudio pydub
```




