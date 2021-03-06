SERIESRESISTOR 560  # the value of the 'other' resistor
SENSORPIN A0        # What pin to connect the sensor to
LOOP_DELAY 1000     # What pin to connect the sensor to
 
def setup(void)
    Serial.begin(9600);
 
def loop(void)
    float reading;
 
    reading = analogRead(SENSORPIN);
 
    Serial.print("Analog reading "); 
    Serial.println(reading);
 
    # convert the value to resistance
    reading = (1023 / reading)  - 1;
    reading = SERIESRESISTOR / reading;
    Serial.print("Sensor resistance "); 
    Serial.println(reading);
 
    delay(LOOP_DELAY);
