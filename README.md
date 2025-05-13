# 🗣️ VocoType Tool

**VocoType** is a speech-to-text tool that lets you type anywhere on your screen wherever the cursor is active, be it in a text editor, a chatting app, programming, or in a search bar, using just your voice. It's perfect for scenarios where accessing the keyboard is inconvenient — for example, when you're lying in bed and using a mouse from a distance.


## ✨ Features

- 🎤 Real-time voice recognition
- ✍️ Types directly where the cursor is active using `pyperclip`
- 🧠 Hotword support:
  - `stop` — Stops the voice typing
  - `enter` / `new line` — Simulates Enter key
  - `tab` — Simulates Tab key
  - `backspace` — Simulates Backspace
- 🧰 System tray integration with start/stop/quit controls
- 🪟 Windows `.exe` version available (via PyInstaller)


## 📦 Requirements

- Python 3.7 or higher
- Packages:
  - `speechrecognition`
  - `pyaudio`
  - `pyperclip`
  - `pyautogui`
  - `pystray`
  - `Pillow`
  - `tkinter` (usually preinstalled)


### 🔧 Installation

1. **Clone this repository:**

```bash
git clone https://github.com/Aniket7013/VocoType.git
cd VocoType
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the tool:**

```bash
python Ease.py
```

### 🛠 Create Executable (Optional)

To build a `.exe` version:

```bash
pyinstaller --onefile --noconsole --icon=mic.ico --add-data "mic.ico;." Ease.py
```

Make sure `mic.ico` is in the same folder.



## 🙋‍♂️ Author

**Aniket Rai**  
Cybersecurity Enthusiast | Python Developer  
Connect with me on [LinkedIn](https://www.linkedin.com/in/aniket-rai/)
