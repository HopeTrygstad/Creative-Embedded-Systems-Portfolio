#include <Arduino.h>

// Touch pad pin mapping
#define RECORD_PIN T3   // record/stop
#define PAUSE_PIN  T9   // pause/resume
#define PLAY_PIN   T4   // play last recording
#define DELETE_PIN T5   // delete last recording
#define MODE_PIN   T2   // mode switch

const int THRESHOLD = 30;

// Previous touch states
bool wasRecordTouched = false;
bool wasPauseTouched  = false;
bool wasPlayTouched   = false;
bool wasDeleteTouched = false;
bool wasModeTouched   = false;

void checkPad(int pin, bool &wasTouched, const char* message) {
  int touchValue = touchRead(pin);
  bool isTouched = touchValue < THRESHOLD;

  if (isTouched && !wasTouched) {
    Serial.println(message);
    delay(200);   // small debounce
  }

  wasTouched = isTouched;
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("Touch controller ready");
}

void loop() {
  checkPad(RECORD_PIN, wasRecordTouched, "R");
  checkPad(PAUSE_PIN,  wasPauseTouched,  "P");
  checkPad(PLAY_PIN,   wasPlayTouched,   "Y");
  checkPad(DELETE_PIN, wasDeleteTouched, "D");
  checkPad(MODE_PIN,   wasModeTouched,   "M");

  delay(30);
}