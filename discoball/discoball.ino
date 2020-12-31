#include <Servo.h> 
#include <Adafruit_NeoPixel.h>

#define SPEED_SLIDER A0
#define TILT_SLIDER A1
#define CW_SPEED 6
#define CCW_SPEED 5
#define LED_PIN    2
#define LED_BI_PIN 3
#define LED_COUNT 3
#define REVERSE_BUTTON_PIN 4
#define RUN_BUTTON_PIN 7
#define WOBBLE_BUTTON_PIN 8

int speed = 0;
float tilt_angle = 0, wobble_offset = 0;
int wobble_speed = 0, wobble_amount = 0;
bool cw = true;
bool reverse_button = false;
bool last_reverse_button = false;
bool reverse_button_pushed = false;
bool run = false;
bool run_button = false;
bool last_run_button = false;
bool run_button_pushed = false;
bool wobble = false;
bool wobble_button = false;
bool last_wobble_button = false;
bool wobble_button_pushed = false;
bool wobble_up = true;

Servo tilt;
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
uint32_t color = strip.Color(0, 0, 0);

void setup() { 
  Serial.begin(9600);
  tilt.attach(9);
  strip.begin();
  strip.show(); 
  pinMode(REVERSE_BUTTON_PIN, INPUT);
  digitalWrite(LED_BI_PIN, 0);
  wobble_amount = 30;
  wobble_speed = 30;
} 

void loop() {
  delay(30);

  run_button = digitalRead(RUN_BUTTON_PIN);
  if (run_button && last_run_button && !run_button_pushed) {
    run_button_pushed = true;
    run = !run;
  }
  if (!run_button && !last_run_button && run_button_pushed) {
    run_button_pushed = false;
  }
  last_run_button = run_button;

  reverse_button = digitalRead(REVERSE_BUTTON_PIN);
  if (reverse_button && last_reverse_button && !reverse_button_pushed) {
    reverse_button_pushed = true;
    cw = !cw;
  }
  if (!reverse_button && !last_reverse_button && reverse_button_pushed) {
    reverse_button_pushed = false;
  }
  last_reverse_button = reverse_button;

  speed = int(float(1023-analogRead(SPEED_SLIDER)) / 1023 * 255);
  //Serial.print("speed=");
  //Serial.println(speed);

  if(cw && run) {
    analogWrite(CCW_SPEED, 0);
    analogWrite(CW_SPEED, speed);
  }
  else if(!cw && run) {
    analogWrite(CW_SPEED, 0);
    analogWrite(CCW_SPEED, speed);
  }
  else {
    analogWrite(CW_SPEED, 0);
    analogWrite(CCW_SPEED, 0);
  }
  
  //color = strip.Color(0, 255, 0);
  //strip.fill(color);
  strip.setPixelColor(0, 255, 100, 255);
  strip.setPixelColor(1, 100, 255, 100);
  strip.setPixelColor(2, 100, 100, 255);
  strip.show(); 

  tilt_angle = float(1023-analogRead(TILT_SLIDER)) / 1023 * 180;
  //Serial.print("tilt=");
  //Serial.println(tilt_angle);

  wobble_button = digitalRead(WOBBLE_BUTTON_PIN);
  if (wobble_button && last_wobble_button && !wobble_button_pushed) {
    wobble_button_pushed = true;
    wobble = !wobble;
    Serial.print("wobble=");
    Serial.println(wobble);
  }
  if (!wobble_button && !last_wobble_button && wobble_button_pushed) {
    wobble_button_pushed = false;
  }
  last_wobble_button = wobble_button;

  if (wobble) {
    //Serial.println(float(wobble_offset));
    if ((wobble_offset < float(wobble_amount)/2) && wobble_up ) {
      wobble_offset = wobble_offset + float(wobble_amount) * float(wobble_speed) / (60 * 30);
      //Serial.println("wobble up");
    }
    else if ((wobble_offset > float(-wobble_amount)/2) && !wobble_up ) {
      wobble_offset = wobble_offset - float(wobble_amount) * float(wobble_speed) / (60 * 30);   
      //Serial.println("wobble down");
    }
    else {
      wobble_up = !wobble_up;
    }
  }
  else {
    wobble_offset = 0;
  }
  tilt.write(tilt_angle + wobble_offset);
} 
