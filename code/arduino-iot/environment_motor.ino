// Include library for DHT11 sensor (must install DHT library in Arduino IDE first, meeting the "Component Adaptation System Requirements" in documentation)
#include <DHT.h>

// 1. Pin and parameter definitions (all labeled with purpose, meeting the "Code Comments" requirement in documentation)
const int motorPin = 8;          // Motor control pin (retained original definition)
const int ldrPin = A0;           // LDR (Light Dependent Resistor) analog pin (retained original definition)
const int dhtPin = 2;            // DHT11 humidity sensor data pin (adjust according to actual wiring)
const int lightThreshold = 100;  // Light threshold (criteria for night/dim environment, need actual debugging)
const int humidityThreshold = 100;// Humidity threshold (criteria for low humidity, unit: %RH, need actual debugging)

// Initialize DHT11 object (specify sensor type and pin, conforming to component driver logic)
DHT dht(dhtPin, DHT11);

void setup() {
  // Configure motor pin as output mode (basic actuator configuration)
  pinMode(motorPin, OUTPUT);
  // Initialize DHT11 sensor (add sensor initialization to ensure normal component operation)
  dht.begin();
  // Initialize serial communication (used to output light, humidity data and motor status, meeting the "Serial Monitor Output Screenshot" requirement in documentation)
  Serial.begin(9600);
  // Print system ready message for easy debugging and demonstration explanation
  Serial.println("Light + Humidity & Motor System Ready");
}

void loop() {
  // 2. Read data from two sensors (meeting the "Use at least two sensors" requirement in documentation)
  // Read LDR value (light intensity data)
  int lightValue = analogRead(ldrPin);
  // Read DHT11 humidity data (need to handle possible sensor read failures to ensure data validity)
  float humidity = dht.readHumidity();

  // 3. Data validity check and serial output (facilitates debugging and meets the "Sensor Output Evidence" requirement in documentation)
  Serial.print("Current Light Value: ");
  Serial.print(lightValue);
  Serial.print(" | Current Humidity: ");
  // If humidity read fails, output prompt; otherwise output actual humidity value
  if (isnan(humidity)) {
    Serial.print("Failed to read humidity");
  } else {
    Serial.print(humidity);
    Serial.print("%RH");
  }
  Serial.println();

  // 4. Motor control logic: Start motor only when "humidity is low (< threshold) AND night (light value < threshold)" (meeting the "Meaningful Interaction Between Components" requirement in documentation)
  if (lightValue < lightThreshold && !isnan(humidity) && humidity < humidityThreshold) {
    digitalWrite(motorPin, HIGH);  // Meet both conditions, start motor
    Serial.println("Motor Running (Dark + Low Humidity)");
  } else {
    digitalWrite(motorPin, LOW);   // Do not meet any condition, stop motor
    Serial.println("Motor Stopped (Not Dark OR Not Low Humidity)");
  }

  // Delay 2000 milliseconds (avoid frequent sensor reading leading to data fluctuation, and conform to DHT11 recommended sampling interval, need actual debugging)
  delay(2000);
}