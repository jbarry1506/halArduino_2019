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
    // LEFT EYE = I2C 15
    // RIGHT EYE = I2C 1
    // HEAD = I2C 0
        
    // EYES CENTER = ~320
    // EYES LEFT = 250
    // EYES RIGHT = 400

//    for( int angle = 0; angle < 181; angle++ ){
//      angleToPulse(angle);
//      pwm.setPWM(15, 0, angleToPulse(90));  
//    }

    // LED Eyes, interior=yellow, exterior=white
    digitalWrite(2, HIGH);
    digitalWrite(10, HIGH);
    digitalWrite(11, HIGH);
    digitalWrite(12, HIGH);

    // Eye and head movement
    for(eyecounter; eyecounter <= 4; eyecounter++){
      // left eye
      pwm.setPWM(15, 0, 320);
      // right eye
      pwm.setPWM(1, 0, 320);
      delay(1000);
          // left eye look left
      pwm.setPWM(15, 0, 250);
          // right eye look left
      pwm.setPWM(1, 0, 250);
      delay(1000);
          // left eye look right
      pwm.setPWM(15, 0, 400);
          // right eye look right
      pwm.setPWM(1, 0, 400);
      delay(1000);
          // left eye look left
      pwm.setPWM(15, 0, 250);
          // right eye look left
      pwm.setPWM(1, 0, 250);
      delay(1000);
      // sweep eyes left to middle slowly
      for(uint16_t pulselen = 250; pulselen < 320; pulselen++){
            // move left eye
        pwm.setPWM(15, 0, pulselen);
            // move right eye
        pwm.setPWM(1, 0, pulselen);
        delay(100);        
      }
      // sweep head from middle to right
      for(uint16_t headlen = 260; headlen > 180; headlen--){
            // move head
        pwm.setPWM(0, 0, headlen); 
        delay(50);       
      }
//      delay(2000);
//      int left = 250;
//      int middle = 320;
//      int right = 400;
//      for(uint16_t pulselen = left; pulselen < right; pulselen++){
//        pwm.setPWM(0, 0, pulselen);
//        delay(200);
//          pwm.setPWM(15, 0, 200);
//          pwm.setPWM(1, 0, 200);
//      }
//      delay(1000);     
//      pwm.setPWM(15, 0, 250);
//      pwm.setPWM(1, 0, 250);
    }
  }
  //angleToPulse(0);
  pwm.setPWM(0, 0, 240);
  pwm.setPWM(15, 0, 320);
  pwm.setPWM(1, 0, 320);
  exit(0);
}

// angle to pulse conversion function
int angleToPulse(int ang){
  int pulse = map(ang, 0, 180, EYE_SERVO_MIN, EYE_SERVO_MAX);
  return(pulse);
}