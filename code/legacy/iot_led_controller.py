import json
import time
import random
from paho.mqtt import client as mqtt

BROKER = "broker.mqtt-dashboard.com"
PORT = 1883

TOPIC_LDR = "XDing/ldr"
TOPIC_DHT = "XDing/dht"
TOPIC_CTL = "inTopic"   # Or you can use something like "XDing/ctl" to avoid interference from other users

LDR_BRIGHT_TH = 200
HUMID_TH = 30.0
TEMP_HIGH_TH = 30.0     # High temperature threshold -> Yellow LED (adjust as needed)

latest = {"raw": None, "h": None, "t": None}
last_led = None
last_fan = None

def decide_led(raw, h, t):
    # Red: bright environment AND high humidity
    if raw < LDR_BRIGHT_TH and h > HUMID_TH:
        return "R"
    # Yellow: high temperature OR high humidity
    if t > TEMP_HIGH_TH or h > HUMID_TH:
        return "Y"
    # Green: all other cases
    return "G"

def decide_fan(led_cmd):
    # Fan runs ONLY when LED is Red
    return "F" if led_cmd == "R" else "f"

def on_connect(client, userdata, flags, rc):
    print("Connected:", rc)
    client.subscribe(TOPIC_LDR)
    client.subscribe(TOPIC_DHT)
    print("Subscribed:", TOPIC_LDR, TOPIC_DHT)

    # After connecting, force the fan OFF first (non-retained, so it won't overwrite LED behavior)
    client.publish(TOPIC_CTL, "f", qos=0, retain=False)
    print("==> FAN OFF (on connect)")

def on_message(client, userdata, msg):
    global last_led, last_fan

    topic = msg.topic
    payload = msg.payload.decode("utf-8", errors="ignore")
    try:
        data = json.loads(payload)
    except Exception:
        print("Bad JSON:", topic, payload)
        return

    if topic == TOPIC_LDR:
        try:
            latest["raw"] = int(data.get("raw"))
        except Exception:
            print("Bad LDR:", data)
            return
        print(f"[LDR] raw={latest['raw']}")

    elif topic == TOPIC_DHT:
        try:
            latest["t"] = float(data.get("t"))
            latest["h"] = float(data.get("h"))
        except Exception:
            print("Bad DHT:", data)
            return
        print(f"[DHT] t={latest['t']} h={latest['h']}")

    # Only decide when all three values are available
    if latest["raw"] is None or latest["h"] is None or latest["t"] is None:
        return

    led = decide_led(latest["raw"], latest["h"], latest["t"])
    fan = decide_fan(led)

    # LED: publish the LED command (state behavior controlled by the ESP side)
    client.publish(TOPIC_CTL, led, qos=0, retain=False)
    last_led = led
    print(f"==> LED SEND {led}")

    # Fan: only publish when the fan command changes (Red -> ON, otherwise OFF)
    if fan != last_fan:
        client.publish(TOPIC_CTL, fan, qos=0, retain=False)
        last_fan = fan
        print(f"==> FAN SEND {fan}")

def main():
    client_id = f"pc-ctrl-{random.randint(0, 99999)}"
    c = mqtt.Client(client_id=client_id, clean_session=True)
    c.on_connect = on_connect
    c.on_message = on_message

    # Safety: if the program crashes / disconnects unexpectedly, the broker will publish "f" to stop the fan
    c.will_set(TOPIC_CTL, payload="f", qos=0, retain=False)

    c.connect(BROKER, PORT, keepalive=60)
    c.loop_start()

    print("Running... Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping... (send fan OFF)")
    finally:
        # Normal exit: also force the fan OFF before disconnecting
        try:
            c.publish(TOPIC_CTL, "f", qos=0, retain=False)
            time.sleep(0.2)
        except Exception:
            pass
        c.loop_stop()
        c.disconnect()

if __name__ == "__main__":
    main()
