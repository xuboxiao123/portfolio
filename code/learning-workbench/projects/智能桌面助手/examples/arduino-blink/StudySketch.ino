#if defined(LED_BUILTIN)
const int outputPin = LED_BUILTIN;
#else
// Generic ESP32 teaching pin: verify your board and wiring before uploading.
const int outputPin = 2;
#endif
void setup(){pinMode(outputPin,OUTPUT);}
void loop(){digitalWrite(outputPin,HIGH);delay(500);digitalWrite(outputPin,LOW);delay(500);}
