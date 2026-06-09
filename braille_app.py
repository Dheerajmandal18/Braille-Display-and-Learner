import sys, time, threading, datetime, queue, os
import serial
import pyttsx3
import pygame
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QLineEdit, QPushButton,
    QLabel, QVBoxLayout, QHBoxLayout, QCheckBox
)
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat, QFont
from PyQt5.QtCore import Qt, QTimer

# === CONFIG ===
PORT = 'COM2'  # Change to your Arduino port
BAUD = 9600
LOG_TO_FILE = True

# === Serial Setup ===
try:
    arduino = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)
except Exception as e:
    print(f"❌ Could not open port {PORT}: {e}")
    sys.exit()

# === TTS Setup ===
engine = pyttsx3.init()
engine.setProperty('rate', 150)
speech_queue = queue.Queue()

def speech_worker():
    while True:
        text = speech_queue.get()
        if text:
            try:
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")
        speech_queue.task_done()

threading.Thread(target=speech_worker, daemon=True).start()

# === Sound Setup ===
pygame.mixer.init()

# === PyQt5 App ===
class BrailleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⠃ Braille Display Dashboard")
        self.setStyleSheet("background-color: #1F1F1F; color: #ECECEC;")
        self.log_filename = f"log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.initUI()
        self.startReceiver()

    def initUI(self):
        layout = QVBoxLayout()

        self.modeLabel = QLabel("🔄 Mode: Unknown")
        self.modeLabel.setStyleSheet("font-size: 14px; padding: 4px;")
        layout.addWidget(self.modeLabel)

        self.outputBox = QTextEdit()
        self.outputBox.setReadOnly(True)
        self.outputBox.setFont(QFont("Consolas", 11))
        self.outputBox.setStyleSheet("background-color: #2A2A2A; border: 1px solid #444;")
        layout.addWidget(self.outputBox)

        inputLayout = QHBoxLayout()
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("Type a message to send...")
        self.inputField.setFont(QFont("Arial", 11))
        self.inputField.setStyleSheet("padding: 6px; border-radius: 4px;")
        self.inputField.returnPressed.connect(self.sendMessage)

        sendBtn = QPushButton("Send")
        sendBtn.setStyleSheet("background-color: #3A9BDC; color: white; font-weight: bold;")
        sendBtn.clicked.connect(self.sendMessage)

        inputLayout.addWidget(self.inputField)
        inputLayout.addWidget(sendBtn)

        layout.addLayout(inputLayout)

        optionsLayout = QHBoxLayout()
        self.logCheck = QCheckBox("📂 Auto-log to file")
        self.logCheck.setChecked(LOG_TO_FILE)

        self.soundCheck = QCheckBox("🔈 Enable sound")
        self.soundCheck.setChecked(True)

        self.ttsCheck = QCheckBox("🗣️ Enable TTS")
        self.ttsCheck.setChecked(True)

        clearBtn = QPushButton("🧹 Clear Log")
        clearBtn.clicked.connect(self.outputBox.clear)

        optionsLayout.addWidget(self.logCheck)
        optionsLayout.addWidget(self.soundCheck)
        optionsLayout.addWidget(self.ttsCheck)
        optionsLayout.addWidget(clearBtn)

        layout.addLayout(optionsLayout)
        self.setLayout(layout)

    def speak(self, text):
        if self.ttsCheck.isChecked():
            speech_queue.put(text)

    def play_sound(self, filename):
        if not self.soundCheck.isChecked():
            return
        if not os.path.exists(filename):
            print(f"⚠️ Sound file not found: {filename}")
            return
        def _play():
            try:
                sound = pygame.mixer.Sound(filename)
                sound.play()
            except Exception as e:
                print(f"Sound error: {e}")
        threading.Thread(target=_play, daemon=True).start()

    def startReceiver(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.serialListener)
        self.timer.start(100)  # check every 100ms

    def serialListener(self):
        if arduino.in_waiting:
            try:
                line = arduino.readline().decode(errors='ignore').strip()
                if line:
                    self.logAndDisplay(line, incoming=True)
                    self.checkMode(line)
                    self.speak(line)
                    self.play_sound("received.wav")
            except Exception as e:
                self.logAndDisplay(f"⚠️ Serial read error: {e}", color="#FF8888")

    def sendMessage(self):
        message = self.inputField.text().strip()
        if message:
            try:
                arduino.write((message + "\n").encode())
                self.logAndDisplay(message, incoming=False)
                self.inputField.clear()
                self.speak(message)
                self.play_sound("sent.wav")
            except Exception as e:
                self.logAndDisplay(f"⚠️ Error sending message: {e}", color="#FFAAAA")

    def logAndDisplay(self, msg, incoming=True, color=None):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        label = "📥" if incoming else "📝"
        full_msg = f"[{timestamp}] {label} {msg}"

        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color or ("#B6FFB6" if incoming else "#AAAAFF")))

        cursor = self.outputBox.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(full_msg + "\n", fmt)
        self.outputBox.setTextCursor(cursor)

        if self.logCheck.isChecked():
            try:
                with open(self.log_filename, "a", encoding="utf-8") as f:
                    f.write(full_msg + "\n")
            except Exception as e:
                print(f"Logging error: {e}")

    def checkMode(self, msg):
        if "Mode:" in msg:
            if "Keyboard" in msg:
                self.modeLabel.setText("🟢 Mode: Keyboard")
                self.modeLabel.setStyleSheet("color: #88FF99; padding: 4px;")
            elif "Display" in msg:
                self.modeLabel.setText("🔵 Mode: Display")
                self.modeLabel.setStyleSheet("color: #88CCFF; padding: 4px;")

# === Launch App ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrailleApp()
    window.resize(620, 460)
    window.show()
    sys.exit(app.exec_())
