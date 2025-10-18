# ♿ Braille Display and Learner

## 📘 Overview
This project presents a **low-cost refreshable Braille display** system designed to assist visually impaired individuals in reading digital text.  
The system uses **Arduino** to control solenoids representing Braille dots, while a **Python Tkinter GUI** sends English characters to be displayed in Braille.  
It aims to create an **affordable, portable, and interactive** solution to help visually impaired learners understand Braille characters digitally.

---

## ⚙️ System Components
1. **Python GUI (Tkinter):**
   - Takes English character input.
   - Sends the character to Arduino through Serial Communication (USB or Bluetooth).
2. **Arduino Controller:**
   - Receives character from Python.
   - Looks up the Braille dot pattern for that letter.
   - Activates the corresponding solenoids (or LEDs for prototype testing).
3. **Braille Display:**
   - Uses 6 solenoids to represent one Braille character at a time.
   - Each solenoid corresponds to one of the six Braille dots.

---

## 💻 Code Files

### 🐍 Python GUI Code – `braille_gui.py`
```python
import tkinter as tk
import serial

# Create a serial connection with the Arduino Uno
# Replace 'COM11' with the port your Arduino is connected to
ser = serial.Serial('COM11', 9600)

# Function to send English character to Arduino
def send_character():
    english_char = entry.get().upper()  # Convert to uppercase
    if english_char:
        ser.write(english_char.encode())

# Create the main window
root = tk.Tk()
root.title("Braille Character Sender")

# Create GUI components
label = tk.Label(root, text="Enter English Character:")
label.pack(pady=5)

entry = tk.Entry(root, width=10)
entry.pack(pady=5)

send_button = tk.Button(root, text="Send to Arduino", command=send_character)
send_button.pack(pady=10)

# Run the main loop
root.mainloop()

### ⚡ Arduino Code – `braille_arduino.ino`
```cpp
// Your full Arduino code goes here
#include <Arduino.h>

const int ledPins[] = {2, 4, 7, 8, 12, 13};

const bool brailleAlphabet[26][6] = {
  {1, 0, 0, 0, 0, 0}, // a
  {1, 1, 0, 0, 0, 0}, // b
  {1, 0, 0, 1, 0, 0}, // c
  {1, 0, 0, 1, 1, 0}, // d
  {1, 0, 0, 0, 1, 0}, // e
  {1, 1, 0, 1, 0, 0}, // f
  {1, 1, 0, 1, 1, 0}, // g
  {1, 1, 0, 0, 1, 0}, // h
  {0, 1, 0, 1, 0, 0}, // i
  {0, 1, 0, 1, 1, 0}, // j
  {1, 0, 1, 0, 0, 0}, // k
  {1, 1, 1, 0, 0, 0}, // l
  {1, 0, 1, 1, 0, 0}, // m
  {1, 0, 1, 1, 1, 0}, // n
  {1, 0, 1, 0, 1, 0}, // o
  {1, 1, 1, 1, 0, 0}, // p
  {1, 1, 1, 1, 1, 0}, // q
  {1, 1, 1, 0, 1, 0}, // r
  {0, 1, 1, 1, 0, 0}, // s
  {0, 1, 1, 1, 1, 0}, // t
  {1, 0, 1, 0, 0, 1}, // u
  {1, 1, 1, 0, 0, 1}, // v
  {0, 1, 0, 1, 1, 1}, // w
  {1, 0, 1, 1, 0, 1}, // x
  {1, 0, 1, 1, 1, 1}, // y
  {1, 0, 1, 0, 1, 1}  // z
};

void setup() {
  for (int i = 0; i < 6; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char c = tolower(Serial.read());
    if (c >= 'a' && c <= 'z') {
      const bool* braillePattern = brailleAlphabet[c - 'a'];
      for (int i = 0; i < 6; i++) {
        digitalWrite(ledPins[i], braillePattern[i] ? HIGH : LOW);
      }
      delay(1000);
      for (int i = 0; i < 6; i++) {
        digitalWrite(ledPins[i], LOW);
      }
      delay(1000);
    }
  }
}



