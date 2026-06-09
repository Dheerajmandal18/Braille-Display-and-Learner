# ⠃ Braille Learner Device

An assistive technology project that helps visually impaired users **learn and practice Braille** using physical solenoid actuators controlled by an Arduino, paired with a Python desktop application for real-time feedback.

---

## 📸 Project Overview

The device uses **6 solenoids** arranged in the standard Braille cell layout (2 columns × 3 rows) to physically raise and lower pins, mimicking real Braille dots. Users can:

- **Feel** Braille characters produced by the solenoids (Display Mode)
- **Input** Braille characters using 6 push buttons mapped to dots 1–6 (Keyboard Mode)
- **See** the typed characters appear on a live Python PyQt5 dashboard
- **Hear** characters spoken aloud via Text-to-Speech (TTS)

---

## 🛠️ Hardware Components

| Component | Quantity | Purpose |
|---|---|---|
| Arduino Uno | 1 | Microcontroller |
| Solenoids (5V/12V push-pull) | 6 | Actuate Braille dots 1–6 |
| MOSFET (e.g. IRF540N) | 6 | Switch solenoids from Arduino signal |
| Flyback Diode (1N4007) | 6 | Protect MOSFETs from back-EMF |
| Resistor 330Ω | 6 | Gate resistors for MOSFETs |
| Push Buttons | 6 | Braille keyboard input (dots 1–6) |
| Toggle Switch | 2 | Mode switch (Display/Keyboard) & Type switch (Alphabet/Number) |
| 24V DC Power Supply | 1 | Power solenoids |
| Breadboard + Jumper Wires | — | Prototyping |
| USB Cable | 1 | Arduino ↔ Laptop serial communication |

---

## 🔌 Circuit Design

```
Arduino Pin 2–7  →  330Ω Resistor  →  MOSFET Gate
                                        |
                                    MOSFET Drain  →  Solenoid (–)
                                        |
                                    MOSFET Source  →  GND

24V Supply (+)  →  Solenoid (+)
Flyback Diode   →  across each Solenoid (cathode to +24V rail)

Arduino A0–A5  →  Push Buttons (INPUT_PULLUP, other end to GND)
Arduino Pin 9   →  Character Type Switch (Alphabet / Number)
Arduino Pin 10  →  Mode Switch (Display / Keyboard)
```

> ⚠️ **Important:** The 24V solenoid circuit shares GND with the Arduino but the solenoids are powered separately. Never connect 24V directly to Arduino pins.

---

## 🧩 Braille Cell Layout

```
Dot Layout (standard Braille):

  [1] [4]
  [2] [5]
  [3] [6]

Button → Solenoid mapping:
  Button on A0 → Dot 1 → Solenoid on Pin 2
  Button on A1 → Dot 2 → Solenoid on Pin 3
  Button on A2 → Dot 3 → Solenoid on Pin 4
  Button on A3 → Dot 4 → Solenoid on Pin 5
  Button on A4 → Dot 5 → Solenoid on Pin 6
  Button on A5 → Dot 6 → Solenoid on Pin 7
```

---

## ⚙️ Operating Modes

### 🔵 Display Mode (`modeSwitch = LOW`)
- Arduino listens for characters sent from the Python app via serial
- On receiving a character, it fires the corresponding solenoids to form the Braille cell
- Solenoids stay active for 1 second, then reset

### 🟢 Keyboard Mode (`modeSwitch = HIGH`)
- User presses combinations of 6 buttons simultaneously
- Arduino decodes the bit pattern and maps it to a letter (A–Z) or digit (0–9)
- The decoded character is sent back to the Python app via serial

### Character Type Switch
- `LOW` → Alphabet mode (A–Z)
- `HIGH` → Number mode (0–9)

---

## 💻 Software

### Arduino (`main.ino`)
- Written in C++ using the Arduino framework
- Handles both Display Mode (solenoid actuation) and Keyboard Mode (button reading)
- Communicates with Python app at **9600 baud** over USB serial

**Key functions:**

| Function | Description |
|---|---|
| `readBrailleButtons()` | Reads 6-bit pattern from buttons |
| `handleAlphabetInput()` | Matches bit pattern to A–Z |
| `handleNumberInput()` | Matches bit pattern to 0–9 |
| `updateSolenoids()` | Activates solenoids per Braille pattern |
| `resetSolenoids()` | Turns all solenoids off |

---

### Python App (`braille_app.py`)

Built with **PyQt5** for the GUI, with:
- `pyserial` — serial communication with Arduino
- `pyttsx3` — offline Text-to-Speech
- `pygame` — sound feedback on send/receive

**Features:**
- Live serial monitor with timestamps
- Send text to Arduino (triggers Display Mode)
- Mode indicator (Keyboard 🟢 / Display 🔵)
- Toggle: TTS, sound effects, auto file logging
- Clear log button

---

## 🚀 Getting Started

### 1. Flash Arduino
Open `arduino/main.ino` in Arduino IDE and upload to your board.

### 2. Install Python Dependencies
```bash
pip install pyserial pyqt5 pyttsx3 pygame
```

### 3. Set Your COM Port
In `braille_app.py`, update:
```python
PORT = 'COM3'   # Windows example
# PORT = '/dev/ttyUSB0'  # Linux/Mac example
```

### 4. Run the App
```bash
python braille_app.py
```

### 5. Optional: Sound Files
Place `sent.wav` and `received.wav` in the same directory as `braille_app.py` for audio feedback.

---

## 📁 Repository Structure

```
braille-learner/
│
├── arduino/
│   └── main.ino              # Arduino firmware
│
├── python/
│   └── braille_app.py        # PyQt5 desktop application
│
├── docs/
│   └── circuit_diagram.png   # Wiring diagram (add yours here)
│
├── media/
│   └── (project photos)
│
└── README.md
```

---

## 📋 Braille Reference

### Alphabet (Dots 1–6)

```
A: ●○  B: ●○  C: ●●  D: ●●  E: ●○
   ○○     ●○     ○○     ○●     ○●
   ○○     ○○     ○○     ○○     ○○
```

Full standard Grade 1 Braille mapping is implemented in the Arduino firmware for A–Z and 0–9.

---

## 🔧 Known Issues / Future Improvements

- [ ] Add support for punctuation and special characters
- [ ] Add Grade 2 Braille contractions
- [ ] Wireless communication (Bluetooth) to remove USB dependency
- [ ] Mobile app companion (Android/iOS)
- [ ] Add physical enclosure / 3D printed housing
- [ ] Word-level TTS (buffer characters and speak full words)

---

## 👥 Contributors

| Name | Role |
|Dheeraj | Python app|
| Piyush Lahot|  Arduino firmware |
| Ritesh  | Hardware design |

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- Inspired by the need for affordable Braille learning tools for visually impaired students
- Standard Braille encoding reference: [Braille Authority](https://www.brailleauthority.org/)
- Built as part of an assistive technology initiative

---

> *"The only disability in life is a bad attitude."* — Scott Hamilton

