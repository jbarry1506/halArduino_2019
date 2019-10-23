#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
char incomingByte;  // variable to read incoming serial data 

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(115200);
  pinMode(9,OUTPUT);
}

void loop() {
  if(Serial.available() > 0){
    incomingByte = Serial.read();
    if(incomingByte >= '0' && incomingByte <= '9'){
      pos = (pos * 10) + (incomingByte - '0');
    }
    else if(incomingByte == 's'){
      Serial.println(pos);
      myservo.write(pos);
      pos = 0;
    }
  }
}