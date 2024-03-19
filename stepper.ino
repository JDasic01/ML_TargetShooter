#include <AccelStepper.h>

#define STEP_PIN_1 2
#define DIR_PIN_1 3
#define STEP_PIN_2 4
#define DIR_PIN_2 5
#define STEPS_PER_REV 200
#define SPEED 1000

AccelStepper stepper1(AccelStepper::DRIVER, STEP_PIN_1, DIR_PIN_1);
AccelStepper stepper2(AccelStepper::DRIVER, STEP_PIN_2, DIR_PIN_2);

void setup() {
  Serial.begin(9600);  // Same baud rate as Python program
  stepper1.setMaxSpeed(SPEED);
  stepper1.setAcceleration(1000);
  stepper2.setMaxSpeed(SPEED);
  stepper2.setAcceleration(1000);
}

void loop() {
  if (Serial.available() > 0) {
    char incomingData[10];
    Serial.readBytesUntil('\n', incomingData, sizeof(incomingData));
    
    char *token = strtok(incomingData, ",");
    int x = atoi(token);
    token = strtok(NULL, ",");
    int y = atoi(token);

    moveSteppers(x, y);
  }
}

void moveSteppers(int x, int y) {
  int center_x = 320;
  int center_y = 240;

  int dx = x - center_x;
  int dy = y - center_y;

  int step_size = 10;

  if (abs(dx) > 20) {
    if (dx > 0) {
      stepper1.move(step_size);
    } else {
      stepper1.move(-step_size);
    }
  }

  if (abs(dy) > 20) {
    if (dy > 0) {
      stepper2.move(step_size);
    } else {
      stepper2.move(-step_size);
    }
  }

  stepper1.run();
  stepper2.run();
}
