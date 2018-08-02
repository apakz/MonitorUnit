# MonitorUnit
Raspberry Pi project that utilises a Current Transformer via an MCP3008, DHT22 and DS18B20 to output Power, internal Humidity, internal Temperature and external Temperature. To the send the data to ThingSpeak integrating it into the Internet of Things (IoT) and show values on a 16x2 LCD screen.

## Prerequisites
Core Required components:
* Raspberry Pi w/ power cable & internet connection
* Jumper leads (male-male and female-male)
* Optional (but recommended): RPi breakout board
* Optional: LED & 220 ohm resistor
Tested with Raspbian on RPi 3. For installation of each component, please see the links below in the Acknowledgements % Resources section

### Power monitor 
* SCT-013-000 Current Transformer
* MCP3008 Analogue-to-Digital convertor
* 18 ohm resistor
* 2x 4.7-10k ohm resistors
* 10uF capacitor

### DHT22
* DHT22 sensor
* 4.7-10k ohm resistor

### DS18B20
* DS18B20 sensor
* 4.7-10k ohm resistor

### LCD Screen
* LCD Screen
* Potentiometer

### ThingSpeak
Sign up for free via https://thingspeak.com/users/sign_up. Lots of tutorials and guides on their site.

## Acknowledgements % Resources
* DHT22 and ThingSpeak - https://www.hackster.io/adamgarbo/raspberry-pi-2-iot-thingspeak-dht22-sensor-b208f4
* DS18B20 - https://thepihut.com/blogs/raspberry-pi-tutorials/18095732-sensors-temperature-with-the-1-wire-interface-and-the-ds18b20
* MCP3008 - https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
* LCD Screen - https://pimylifeup.com/raspberry-pi-lcd-16x2/

## Known Issues
After about 30 entries, there is a HTTP bad gateway error

## Future developments
* Streamline code (break up into components)
