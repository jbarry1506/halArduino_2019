/* 
This is the Arduino Duemillanove ATMEGA 328p 
file to control the Pennywise servo, LED eyes,
and whatever other electronics are involved.
AUTHOR:     Jim Barry
DATE:       9/15/2019
*/ 

int incomingByte;      // a variable to read incoming serial data into

void setup()
{
    Serial.begin(9600);
    pinMode(4, OUTPUT);
}

void loop() {
  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
    // if it's a capital H (ASCII 72), turn on the LED:
    if (incomingByte == 'H') {
      digitalWrite(4, HIGH);
    }
    // if it's an L (ASCII 76) turn off the LED:
    if (incomingByte == 'L') {
      digitalWrite(4, LOW);
    }
  }
}