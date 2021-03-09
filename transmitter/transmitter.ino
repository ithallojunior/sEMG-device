/*
SENDER which uses the pre-calibrated OSCCAL from EEPROM.

This code is for multiple channel transmission and reception. In order
to differentiate the devices they are marked with white dots, so
they are called 2SEMG, 1SEMG, (this naming follows historical reasons) 
and so on. This is because of the 40 bit nature
of the pipe name (5 Bytes). They  can just differ on the first byte.
*/

#include <EEPROM.h>
#include "nRF24L01.h"
#include "RF24.h"

#define DEVICE1 // if commented it activates the second device

#define CSN_PIN 4
#define CE_PIN 5 //reset pin
#define ANALOG_PIN 3 //PB3, pin 2
#define CHANNEL 76//0x4c

#define BUFFER_SIZE 1 //max 255, real buffer size

#define SAMPLING_FREQUENCY 2000 //HZ
#define DELTA 1000000/SAMPLING_FREQUENCY


// setting the name of the transmitter
#ifdef DEVICE1
  const unsigned char pipe[6] = "2SEMG";
#else
  const unsigned char pipe[6] = "1SEMG";
#endif

uint16_t data[BUFFER_SIZE]; 
unsigned int i=0;
unsigned long int t=0;
unsigned char value;

RF24 radio(CE_PIN, CSN_PIN);

void setup() {

  //loading calibrated OSCCAL
  EEPROM.get(0, value);
  OSCCAL = value;

  radio.begin(); 
  radio.setChannel(CHANNEL);
  radio.setAddressWidth(5);

  radio.setAutoAck(false);
  radio.setPayloadSize(sizeof(data)); // 2 x buffer size
  radio.setRetries(0,0);
  radio.setDataRate(RF24_2MBPS); //more than enough
  
  radio.stopListening();
  radio.openWritingPipe(pipe);
  
  analogReference(INTERNAL); // sets attiny85 reference voltage to 1v1

}


void loop(void){  
    
    // fill the buffer
    for(i=0;i < BUFFER_SIZE;i++){ 

      data[i] = analogRead(ANALOG_PIN);
      
      while( (micros() - t) <= DELTA);
      t += DELTA;

    }
   
 //send data 
 radio.writeFast(&data, sizeof(data) );

 }
 

