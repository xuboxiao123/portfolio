# Arduino and IoT source

[IoT case study](../../project-iot-monitor.md) · [Arduino sketch](environment_motor.ino) · [MQTT Python controller](iot_led_controller.py)

Two distinct historical exercises: the Arduino sketch reads a DHT11 and LDR and controls a motor; the Python controller belongs to the later ESP8266/MQTT proof of concept. They are not interchangeable firmware/controller halves. The Arduino humidity threshold is retained at its original 100% setting and requires calibration. The file named mqtt_esp8266.ino in the archive currently contains NFC-reader code, so it has not been mislabelled or included as matching MQTT firmware.
