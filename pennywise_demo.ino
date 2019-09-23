#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

uint8_t servonum = 0;
uint8_t eyecounter = 0;
uint8_t headcounter = 0;

#define EYE_SERVO_MIN 200
#define EYE_SERVO_MAX 400

void setup() {
  pinMode(2, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60);
}

void loop() {
  for( int loopcounter = 0; loopcounter <= 1; loopcounter++ ) {
    // EYES CENTER = ~320
    // EYES move right to left (viewer perspective)
    // LEFT EYE = I2C 15
    // RIGHT EYE = I2C 1
    // HEAD = I2C 0

//    for( int angle = 0; angle < 181; angle++ ){
//      angleToPulse(angle);
//      pwm.setPWM(15, 0, angleToPulse(90));  
//    }
    digitalWrite(2, HIGH);
    digitalWrite(10, HIGH);
    digitalWrite(11, HIGH);
    digitalWrite(12, HIGH);
    
    for(eyecounter; eyecounter <= 4; eyecounter++){
      delay(2000);
      pwm.setPWM(0, 250, 400);
      delay(2000);
        pwm.setPWM(15, 0, 200);
        pwm.setPWM(1, 0, 200);
        delay(100);     
        pwm.setPWM(15, 0, 250);
        pwm.setPWM(1, 0, 250);
      pwm.setPWM(0, 0, 200);
        delay(100);
        pwm.setPWM(15, 0, 300);
        pwm.setPWM(1, 0, 300);
        delay(100);
        pwm.setPWM(15, 0, 350);
        pwm.setPWM(1, 0, 350);
        delay(2000);
      pwm.setPWM(0, 0, 400);
        delay(100);
        pwm.setPWM(15, 0, 400);
        pwm.setPWM(1, 0, 400);
        delay(100);
    }
  }
  //angleToPulse(0);
  pwm.setPWM(0, 0, 280);
  pwm.setPWM(15, 0, 320);
  pwm.setPWM(1, 0, 320);
  exit(0);
}

int angleToPulse(int ang){
  int pulse = map(ang, 0, 180, EYE_SERVO_MIN, EYE_SERVO_MAX);
  return(pulse);
}