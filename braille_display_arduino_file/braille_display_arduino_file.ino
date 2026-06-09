#include <Arduino.h>

// === Pin Definitions ===
int solenoids[6] = {2, 3, 4, 5, 6, 7};             // Solenoid output pins (Braille dots 1–6)
int brailleButtons[6] = {A0, A1, A2, A3, A4, A5};   // Input buttons for Braille keyboard
int modeSwitch = 10;                               // Mode switch: LOW = Display, HIGH = Keyboard
int charTypeSwitch = 9;                            // Character type switch: LOW = Alphabet, HIGH = Number

bool prevMode = LOW;
bool prevType = LOW;

// === Braille Alphabet Map (A–Z) ===
const bool alphabetMap[26][6] = {
  {1,0,0,0,0,0}, // A
  {1,1,0,0,0,0}, // B
  {1,0,0,1,0,0}, // C
  {1,0,0,1,1,0}, // D
  {1,0,0,0,1,0}, // E
  {1,1,0,1,0,0}, // F
  {1,1,0,1,1,0}, // G
  {1,1,0,0,1,0}, // H
  {0,1,0,1,0,0}, // I
  {0,1,0,1,1,0}, // J
  {1,0,1,0,0,0}, // K
  {1,1,1,0,0,0}, // L
  {1,0,1,1,0,0}, // M
  {1,0,1,1,1,0}, // N
  {1,0,1,0,1,0}, // O
  {1,1,1,1,0,0}, // P
  {1,1,1,1,1,0}, // Q
  {1,1,1,0,1,0}, // R
  {0,1,1,1,0,0}, // S
  {0,1,1,1,1,0}, // T
  {1,0,1,0,0,1}, // U
  {1,1,1,0,0,1}, // V
  {0,1,0,1,1,1}, // W
  {1,0,1,1,0,1}, // X
  {1,0,1,1,1,1}, // Y
  {1,0,1,0,1,1}  // Z
};

// === Braille Number Map (0–9) ===
// Note: In Braille, numbers are represented by same patterns as A–J but preceded by a number sign.
// We're using direct mapping for simplicity.
const bool numberMap[10][6] = {
  {0,1,0,1,1,0}, // 0 (J)
  {1,0,0,0,0,0}, // 1 (A)
  {1,1,0,0,0,0}, // 2 (B)
  {1,0,0,1,0,0}, // 3 (C)
  {1,0,0,1,1,0}, // 4 (D)
  {1,0,0,0,1,0}, // 5 (E)
  {1,1,0,1,0,0}, // 6 (F)
  {1,1,0,1,1,0}, // 7 (G)
  {1,1,0,0,1,0}, // 8 (H)
  {0,1,0,1,0,0}  // 9 (I)
};

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 6; i++) {
    pinMode(solenoids[i], OUTPUT);
    pinMode(brailleButtons[i], INPUT_PULLUP);
  }
  pinMode(modeSwitch, INPUT_PULLUP);
  pinMode(charTypeSwitch, INPUT_PULLUP);
  prevMode = digitalRead(modeSwitch);
  prevType = digitalRead(charTypeSwitch);
  Serial.println("🔁 System Ready");
}

void loop() {
  bool mode = digitalRead(modeSwitch);         // HIGH = Keyboard
  bool charMode = digitalRead(charTypeSwitch); // HIGH = Number

  if (mode != prevMode || charMode != prevType) {
    Serial.print("🟢 Mode: ");
    Serial.print(mode == HIGH ? "Keyboard" : "Display");
    Serial.print(" | Type: ");
    Serial.println(charMode == HIGH ? "Number" : "Alphabet");
    prevMode = mode;
    prevType = charMode;
  }

  if (mode == HIGH) {
    // === Keyboard Mode ===
    byte value = readBrailleButtons();
    if (value != 0) {
      if (charMode == LOW) handleAlphabetInput(value);
      else handleNumberInput(value);
      Serial.println();
    }
  } else {
    // === Display Mode ===
    if (Serial.available()) {
      char c = Serial.read();
      c = toupper(c);
      const bool* dots = getBraillePattern(c, charMode);
      if (dots != nullptr) {
        updateSolenoids(dots);
        delay(1000);
        resetSolenoids();
      }
    }
  }

  delay(1000);
}

byte readBrailleButtons() {
  byte value = 0;
  for (int i = 0; i < 6; i++) {
    if (!digitalRead(brailleButtons[i])) {
      value |= (1 << i);
    }
  }
  return value;
}

void handleAlphabetInput(byte pattern) {
  for (int i = 0; i < 26; i++) {
    byte b = 0;
    for (int j = 0; j < 6; j++) {
      if (alphabetMap[i][j]) b |= (1 << j);
    }
    if (b == pattern) {
      Serial.print((char)('A' + i));
      return;
    }
  }
}

void handleNumberInput(byte pattern) {
  for (int i = 0; i < 10; i++) {
    byte b = 0;
    for (int j = 0; j < 6; j++) {
      if (numberMap[i][j]) b |= (1 << j);
    }
    if (b == pattern) {
      Serial.print((char)('0' + i));
      return;
    }
  }
}

const bool* getBraillePattern(char c, bool numberMode) {
  if (numberMode && c >= '0' && c <= '9') return numberMap[c - '0'];
  if (!numberMode && c >= 'A' && c <= 'Z') return alphabetMap[c - 'A'];
  return nullptr;
}

void updateSolenoids(const bool* pattern) {
  for (int i = 0; i < 6; i++) {
    digitalWrite(solenoids[i], pattern[i] ? LOW : HIGH);  // Adjust to LOW if using active-low solenoids
  }
}

void resetSolenoids() {
  for (int i = 0; i < 6; i++) {
    digitalWrite(solenoids[i], LOW);  // All OFF
  }
}
