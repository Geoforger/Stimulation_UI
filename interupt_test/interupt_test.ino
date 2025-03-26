#include <Arduino.h>

float stim_amplitude = 0.0;
float pulse_width = 0.0;
int comm_state = 0; // 0: User Mode, 1: PC Mode
int trigger_state = 0; // 0: External Trigger Off, 1: External Trigger On
int stim_state = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.startsWith("<A,")) {
      stim_amplitude = input.substring(3, input.length() - 1).toFloat();
      Serial.println("<ACK>");
    } else if (input.startsWith("<P,")) {
      pulse_width = input.substring(3, input.length() - 1).toFloat();
      Serial.println("<ACK>");
    } else if (input == "<T>") {
      comm_state ^= 1; // Toggle comm_state
      Serial.println("<ACK>");
    } else if (input == "<STOP>") {
      Serial.println("System Stop Initiated");
      Serial.println("<ACK>");
    } else if (input == "<EX>") {
      // Handle external trigger toggle
      trigger_state ^= 1; // Toggle trigger_state
      Serial.print("External Triggers Toggled: ");
      Serial.println(trigger_state);
      Serial.println("<ACK>");
    } else if (input == "<STIM>") {
      // Handle recording toggle
      stim_state ^= 1; // Toggle trigger_state
      Serial.print("Stimulation State Toggled: ");
      Serial.println(stim_state);
      Serial.println("<ACK>");
    }
  }

  if (comm_state == 1) {
    // Broadcasting state
    Serial.print("Stim Amplitude: ");
    Serial.print(stim_amplitude);
    Serial.print(" uA, Pulse Width: ");
    Serial.print(pulse_width);
    Serial.println(" ms");
    delay(1000); // Broadcast every second
  }
}
