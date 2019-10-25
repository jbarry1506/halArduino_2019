/* 
This is the Arduino Duemillanove ATMEGA 328p 
file to control the Pennywise servo, LED eyes,
and whatever other electronics are involved.
AUTHOR:     Jim Barry
DATE:       9/15/2019
*/ 

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

uint8_t servonum = 0;
uint8_t eyecounter = 0;
uint8_t headcounter = 0;

int HEAD = 0; //I2C HEAD SERVO
int LEFT = 15; //I2C LEFT EYE SERVO
int RIGHT = 1; //I2C RIGHT EYE SERVO 
char incomingByte; // variable to read incoming serial data
int pos = 0; // variable to store the servo position
    
    // EYES CENTER = ~320
    // EYES LEFT = 250
    // EYES RIGHT = 400

    // 180 degrees for head
#define HEAD_SERVO_MIN 210
#define HEAD_SERVO_MAX 390

    // 90 degrees for eyes
#define LEFT_EYE_SERVO_MIN 260
#define LEFT_EYE_SERVO_MAX 340
#define RIGHT_EYE_SERVO_MIN 260
#define RIGHT_EYE_SERVO_MAX 340 


void setup() {
  pinMode(2, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  
  Serial.begin(115200);
  pwm.begin();
  pwm.setPWMFreq(60);
}

void loop() {
  // read serial data and move the head
  if(Serial.available() > 0){
    incomingByte = Serial.read();
    if(incomingByte >= '0' && incomingByte <= '9'){
      pos = (pos * 10) + (incomingByte - '0');  
    }
    else if(incomingByte == 's'){
      // Serial.println(pos);
      // move head
      pwm.setPWM(0, 0, pos);
      pos = 0;  
    }
    else if(incomingByte == 'e'){
      // Serial.println(pos);
      // move eyes
      pwm.setPWM(15, 0, pos);
      pwm.setPWM(1, 0, pos);      
      pos = 0;  
    }    
  }
}
