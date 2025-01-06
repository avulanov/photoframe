#include <Arduino.h>
#include "../lib/device_controller/device_controller.h"

// put function declarations here:



void setup() {
  // put your setup code here, to run once:
  SetupSD();
  SetupDisplay();

}

void loop() {
  // put your main code here, to run repeatedly:
  RunDisplay();
  while(1); 
}
