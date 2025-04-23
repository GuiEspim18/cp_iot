#define BUZZER_PIN 7

void setup() {
    pinMode(BUZZER_PIN, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read();
        if (command == '1') {
            digitalWrite(BUZZER_PIN, HIGH);
        } 
        if (command == '0') {
            digitalWrite(BUZZER_PIN, LOW);
        }
    }
}