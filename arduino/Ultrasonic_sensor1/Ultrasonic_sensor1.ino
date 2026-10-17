/*
  Arduino Uno + ultrasonic distance sensor + two active-LOW digital sensors + buzzer

  Ultrasonic TRIG: D8
  Ultrasonic ECHO: D9
  Active-LOW sensor inputs: D3 and D4
  Buzzer: D13
  Serial output: distance in cm, one value per line, 9600 baud

  IMPORTANT: This keeps the original sketch's assumption that each extra sensor
  outputs LOW when active. If your sensors have different output behavior, adjust
  sensorIsActive() and/or the wiring notes in README.md.
*/

const byte TRIG_PIN = 8;
const byte ECHO_PIN = 9;
const byte SENSOR_1_PIN = 3;
const byte SENSOR_2_PIN = 4;
const byte BUZZER_PIN = 13;

const unsigned long ECHO_TIMEOUT_US = 30000UL;
const int DANGER_DISTANCE_CM = 5;

bool sensorIsActive(byte pin) {
  // Preserves the original code's active-LOW sensor assumption.
  return digitalRead(pin) == LOW;
}

long readDistanceCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);  // Standard trigger pulse for common HC-SR04 modules
  digitalWrite(TRIG_PIN, LOW);

  unsigned long duration = pulseIn(ECHO_PIN, HIGH, ECHO_TIMEOUT_US);
  if (duration == 0) {
    return -1;  // No echo/timeout; do not treat it as zero-centimeter distance
  }
  return (long)(duration * 0.0343 / 2.0);
}

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(SENSOR_1_PIN, INPUT);
  pinMode(SENSOR_2_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(TRIG_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);
}

void loop() {
  long distanceCm = readDistanceCm();

  bool extraSensorTriggered = sensorIsActive(SENSOR_1_PIN) ||
                              sensorIsActive(SENSOR_2_PIN);
  bool ultrasonicTriggered = distanceCm >= 0 &&
                             distanceCm <= DANGER_DISTANCE_CM;

  digitalWrite(BUZZER_PIN, (extraSensorTriggered || ultrasonicTriggered)
                               ? HIGH
                               : LOW);

  // Python display reads one numeric distance per line. -1 means no echo.
  Serial.println(distanceCm);
  delay(50);  // Allows the ultrasonic echo to settle between readings
}
