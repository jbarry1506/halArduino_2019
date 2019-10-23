#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
int incomingByte;  // variable to read incoming serial data 

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(115200);
  pinMode(9,OUTPUT);
}

void loop() {
  if(Serial.available() > 0){
    incomingByte = Serial.read();
    switch(incomingByte){
      case 'L':
//        for (pos = 0; pos <= 59; pos += 1) { // goes from 0 degrees to 180 degrees
//          // in steps of 1 degree
//          myservo.write(pos);              // tell servo to go to position in variable 'pos'
//          delay(50);                       // waits 15ms for the servo to reach the position
//        }
//        for (pos = 59; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
//          myservo.write(pos);              // tell servo to go to position in variable 'pos'
//          delay(50);                       // waits 15ms for the servo to reach the position
//        }
        myservo.write(30);
        break;
      case 'M':
//        for (pos = 60; pos <= 119; pos += 1) { // goes from 0 degrees to 180 degrees
//          // in steps of 1 degree
//          myservo.write(pos);              // tell servo to go to position in variable 'pos'
//          delay(50);                       // waits 15ms for the servo to reach the position
//        }
//        for (pos = 119; pos >= 60; pos -= 1) { // goes from 180 degrees to 0 degrees
//          myservo.write(pos);              // tell servo to go to position in variable 'pos'
//          delay(50);                       // waits 15ms for the servo to reach the position
//        }
        myservo.write(90);
        break;        
      case 'R':
//        for (pos = 120; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
//          // in steps of 1 degree
//          myservo.write(pos);              // tell servo to go to position in variable 'pos'
//          delay(50);                       // waits 15ms for the servo to reach the position
//        }
//        for (pos = 180; pos >= 120; pos -= 1) { // goes from 180 degrees to 0 degrees
//          myservo.write(pos);              // tell servo to go to position in variable 'pos'
//          delay(50);                       // waits 15ms for the servo to reach the position
//        }
        myservo.write(150);
      default:
        break;       
    }
  }
}