# Arduino Uno Ultrasonic Sensor Display

A small Arduino Uno + Python/Pygame demo. The Arduino measures distance with an ultrasonic sensor, activates a buzzer when an object is within the configured threshold, and sends distance readings to a Python desktop window over serial.

## Hardware and pin map

| Part | Arduino Uno pin |
|---|---:|
| Ultrasonic sensor TRIG | D8 |
| Ultrasonic sensor ECHO | D9 |
| Additional digital sensor 1 | D3 |
| Additional digital sensor 2 | D4 |
| Buzzer | D13 |
| Serial link to computer | USB |

**Sensor assumption:** The original sketch checks D3 and D4 for `LOW`, so this corrected sketch preserves the assumption that the two additional sensors are active-LOW digital outputs. Confirm the output type and voltage of your actual sensors before powering the circuit. The sketch configures D3/D4 as `INPUT`; sensors that do not actively drive their outputs HIGH and LOW may need suitable pull-up/pull-down wiring or a different pin configuration.

## Arduino setup

1. Open `arduino/Ultrasonic_sensor1/Ultrasonic_sensor1.ino` in the Arduino IDE.
2. Connect your Arduino Uno and select **Arduino Uno** under **Tools → Board**.
3. Select the correct port under **Tools → Port**.
4. Upload the sketch.
5. If checking readings in Serial Monitor, set the baud rate to **9600**. Close Serial Monitor before starting the Python program because only one application can usually use the serial port at a time.

The sketch prints one distance value in centimeters per line. `-1` means no echo was received before the timeout. The buzzer is activated when the distance is 5 cm or less, or either active-LOW digital sensor is triggered.

## Python setup

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\activate
python -m pip install -r requirements.txt
python parking_display.py --port COM5
```

Replace `COM5` with your Arduino's actual port, such as `COM3`. To see detected ports, run `python -m serial.tools.list_ports -v`. On macOS/Linux, use the relevant device path, for example `/dev/ttyACM0` or `/dev/ttyUSB0`.

You can also set the `ARDUINO_PORT` environment variable and run `python parking_display.py`.

`car.py` and `python parking system.py` are compatibility entry points; both launch the shared `parking_display.py` program. The supplied `assets/car1.png` is used as a background. The original ZIP referenced a `Blind Walking PNG` image folder that was not included, so the missing animation has not been fabricated or claimed as included.

## GitHub upload checklist

- Commit the `arduino/Ultrasonic_sensor1/Ultrasonic_sensor1.ino` sketch, Python files, `assets/car1.png`, `requirements.txt`, `.gitignore`, and this README.
- Do not commit virtual environments, generated caches, passwords, or private credentials.
- Add your own wiring photos or missing animation assets only if you have permission to publish them.
- Test on the actual Uno and sensor circuit. A successful Python syntax check does not verify the hardware or Arduino behavior.

## Troubleshooting

- **Serial port cannot open:** select the correct port and close Arduino Serial Monitor/Plotter.
- **No distance reading:** check TRIG/ECHO wiring, sensor power, common ground, and selected port/baud rate.
- **Buzzer is always on/off:** confirm that D3/D4 sensors really output active-LOW digital signals and are not floating.
- **Distance shows `No echo detected`:** check the ultrasonic sensor's power, wiring, target, and orientation.
