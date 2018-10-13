#include <DHT.h>
#include "EmonLib.h"
#define control_A 5
#define control_B A0
char keyIn = {};
// Include Emon Library
EnergyMonitor emon1;                   // Create an instance
DHT dht(4, DHT22); 
bool status_A = false;
int status_B = 0;
void setup()
{  
    pinMode(control_A, OUTPUT);
    pinMode(control_B, INPUT);
    Serial.begin(9600);
    dht.begin();
    emon1.current(1, 36.58); // Current: input pin, calibration.
}

void loop()
{
  if (Serial.available() > 0) {
      keyIn = Serial.read();
//      Serial.println(keyIn);
      if(keyIn == 'A'){
          digitalWrite(control_A, HIGH);
          status_A = true;
      }
      else if(keyIn == 'Y'){
          digitalWrite(control_A, LOW);
          status_A = false;
      }
  }
   status_B = analogRead(control_B);
   float h = dht.readHumidity();
   float t = dht.readTemperature(); //read Humidity and Temperature 
   double Irms = emon1.calcIrms(1480);  // Calculate Irms only
/*  if (isnan(t) || isnan(h)) 
    {
        Serial.println("Failed to read from DHT");
    } 
    else 
    {*/
        Serial.print("{\"Humidity\":"); 
        Serial.print(h, 2);
        Serial.print(", \"Temperature\":"); 
        Serial.print(t, 2);
        Serial.print(", \"currents\":");
        Serial.print(Irms);
        Serial.print(", \"control_A\":");
        Serial.print(status_A);
        Serial.print(", \"control_B\":");
        Serial.print(status_B);
        Serial.println("}");
//    }
  delay(100);
}
