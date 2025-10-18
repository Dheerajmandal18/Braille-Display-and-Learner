# ♿ Braille Display and Learner

## 📘 Overview
This project aims to design and implement a **low-cost refreshable Braille display** to help visually impaired individuals access digital information.  
It uses **Arduino** to control solenoids that form Braille characters, and a **Python-based GUI** to send text for conversion into Braille.

---

## ⚙️ System Overview
The system consists of three main modules:
1. **Python GUI:** Takes English text input and sends it to Arduino.
2. **Arduino Controller:** Converts characters into Braille patterns and activates solenoids.
3. **Solenoid Display:** Raises dots corresponding to each Braille character.

---

## 🔩 Hardware Components
- Arduino Uno  
- 6 Solenoids  
- MOSFETs for switching  
- Flyback diodes (1N4007)  
- Resistors (1kΩ)  
- External power supply  
- Jumper wires and breadboard  

---

## 💻 Software Components
- **Python** (Tkinter for GUI)
- **Arduino IDE**
- Serial communication via USB

---

## 🧠 Working Principle
1. User enters English text in the Python GUI.  
2. The text is sent to Arduino via serial communication.  
3. Arduino converts each letter to its Braille pattern.  
4. Corresponding solenoids are energized to display the character.  
5. Each character appears for one second, followed by a pause.

---

## 🌟 Features
- Low-cost hardware implementation  
- Easy to use and portable  
- One character refreshable Braille display  
- Potential to expand to multi-character display

---

## 🚀 Future Improvements
- Multi-character Braille display  
- Wireless communication using Bluetooth/Wi-Fi  
- Audio feedback integration for learners  

---

## 👨‍💻 Team Members
- **Piyush Lahot (2205027)**  
- **Dheeraj Kumar Mandal (2205018)**  

---

## 🧑‍🏫 Supervisor
**Mr. Manoj Kumar**  
Department of Instrumentation  
Bhaskaracharya College of Applied Sciences

---

## 🧾 References
- [Python Documentation](https://docs.python.org/3/)  
- [Tkinter Tutorials – TutorialsPoint](https://www.tutorialspoint.com/python/python_gui_programming.htm)  
- [Arduino Documentation](https://docs.arduino.cc/)  
- [GeeksforGeeks – Tkinter Widgets](https://www.geeksforgeeks.org/python-tkinter-widgets)

---

> 🩵 *Developed as part of the B.Sc. (Hons.) Instrumentation project at University of Delhi.*

