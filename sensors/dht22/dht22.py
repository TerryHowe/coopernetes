import time
import datetime
import Adafruit_DHT
 

sensor = Adafruit_DHT.DHT22
pin = 18

while True:
    try:
        humidity, temperature_c = Adafruit_DHT.read_retry(sensor, pin)
    except Exception as e:
        import traceback 
        traceback.print_exc()
        print(e)
    else:
        temperature_f = temperature_c * (9 / 5) + 32
        result = '"timestamp": "{}", "temperature": {:.1f}, "humidity": {:.1f}'.format(
                    datetime.datetime.now(),
                    temperature_f,
                    humidity)
        print("{" + result + "}")
    time.sleep(60.0)
