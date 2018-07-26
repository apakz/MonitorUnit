# coding=utf-8
import time
import numpy as np
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_DHT
import os #DS18B20
import glob #DS18B20
import Adafruit_CharLCD as LCD
import urllib2
import RPi.GPIO as GPIO

# LEDsetup
GPIO.setmode(GPIO.BCM)
LED_pin = 12
GPIO.setup(LedPin, GPIO.OUT)
t_blink = 0.25 # Time to blink LED

# Place your API Code here
API_code = 'YOUR API CODE'
t_delay = 15 # Time between readings

#LCD Pin Config:
lcd_rs        = 25
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 18
lcd_d7        = 22
lcd_backlight = 2
# 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2
# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)
lcd.message('Monitor')

# MCP3008 Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#Set up DHT22
dht_pin = 6
dht_sensor = Adafruit_DHT.DHT22

#Set up DS18B20 to read external temperature from pin 4
os.system('modprobe w1-gpio')  # Turns on the GPIO module
os.system('modprobe w1-therm') # Turns on the Temperature module
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
def read_temp_raw():
  f = open(device_file, 'r') # Opens the temperature device file
  lines = f.readlines() # Returns the text
  f.close()
  return lines
def read_temp():
  lines = read_temp_raw() # Read the temperature 'device file'
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
   if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    return temp_c

#Current monitor Initial values
R_burden=18.2
CT_ratio=2000
number_of_samples = 2230
mains_voltage = 230
supply_voltage = 3.3

#Set up current monitor
ADC_counts = 1024
offset_I = 511
ICAL = CT_ratio/R_burden

while True:
        n = 0
        sum_I = 0
        sample_I = 512
        filtered_I = 0
        while  n < number_of_samples:
            lastsample_I = sample_I
            sample_I = mcp.read_adc(0)
            lastfiltered_I = filtered_I
            # Digital high pass filter
            filtered_I = 0.996 * (lastfiltered_I + sample_I - lastsample_I)
            sq_I = filtered_I * filtered_I

            sum_I = sum_I+sq_I # sum for one sample
            n =+ 1
        I_ratio = ICAL*(supply_voltage/ADC_counts)
        Irms = I_ratio * np.sqrt(sum_I/number_of_samples)
        
        # Compute final sensor readings
        Power= Irms*mains_voltage
        humidity, int_temp = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
        ext_temp = read_temp()
        
        # Print to terminal
        print(Power, 'Watts', humidity, '%', int_temp, 'degrees', ext_temp, 'degrees')
        # Send to LCD
        lcd.clear()
        text = 'Pwr='+str(Power)+'Hum='+str(humidity)+'\nIT='+str(int_temp)+' ET='+str(ext_temp)
        lcd.message(text)
        #Send values to ThingSpeak
        baseURL = 'https://api.thingspeak.com/update?api_key='+API_code
        f = urllib2.urlopen(baseURL+'&field1='+str(Power)+'&field2='+str(humidity)+'&field3='
                            +str(int_temp)+'&field4='+str(ext_temp))
        print f.read()
        f.close()
        
        #Blink LED everytime sensors are read
        GPIO.output(LedPin, GPIO.LOW)
        time.sleep(t_blink)
        #Pause between readings
        time.sleep(t_delay-t_blink)





