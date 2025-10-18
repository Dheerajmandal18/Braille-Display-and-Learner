# ♿ Braille Display and Learner

## 📘 Overview
This project presents a **low-cost refreshable Braille display** system designed to assist visually impaired individuals in reading digital text.  
The system uses **Arduino** to control solenoids representing Braille dots, while a **Python Tkinter GUI** sends English characters to be displayed in Braille.

---

## ⚙️ System Components
1. **Python GUI (Tkinter):**
   - Takes English character input.
   - Sends the character to Arduino through Serial Communication.
2. **Arduino Controller:**
   - Converts the received character into a 6-dot Braille pattern.
   - Activates solenoids corresponding to raised Braille dots.
3. **Solenoid Braille Display:**
   - Uses 6 solenoids to represent one Braille character at a time.

---

## 💻 Code Files

### 🐍 Python GUI – `braille_gui.py`
```python
import tkinter as tk
import serial

# Create a serial connection with the Arduino Uno
ser = serial.Serial('COM11', 9600)  # Replace 'COM11' with your Arduino port

# Function to send English character to Arduino
def send_character():
    english_char = entry.get().upper()  # Convert to uppercase
    ser.write(english_char.encode())

# Create the main window
root = tk.Tk()
root.title("Braille Character Sender")

# Create GUI components
label = tk.Label(root, text="Enter English Character:")
label.pack()

entry = tk.Entry(root)
entry.pack()

send_button = tk.Button(root, text="Send", command=send_character)
send_button.pack()

# Run the main loop
root.mainloop()


