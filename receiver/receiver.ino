 /* 
 * Receiver
 */
#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"

#define CSN_PIN 7
#define CE_PIN 8
#define CHANNEL 76//0x4c
#define BUFFER_SIZE 1 //abs max per transmission 32 Bytes
#define COMPUTER_BUFFER_SIZE 1
#define DEVICES 1

//#define WAIT_ALL_DEVICES // if enabled, waits for signals from all devices


RF24 radio(CE_PIN, CSN_PIN);

const unsigned char pipes[][6] = {"2SEMG", "1SEMG"};
uint16_t receiver_buffer[DEVICES][COMPUTER_BUFFER_SIZE] = { 0 };

uint8_t pipe = 0;
uint8_t previous_pipe = 0;
uint8_t pipe_count = 0;

void receiver() {

  pipe_count = 0;
  previous_pipe = DEVICES + 1; // in order to be different for only one device
  while(pipe_count < DEVICES){
    
    if (radio.available(&pipe)){

      radio.read(&receiver_buffer[pipe-1], sizeof(uint16_t));
      
      #ifdef WAIT_ALL_DEVICES
        if (pipe != previous_pipe){
          pipe_count += 1;
          previous_pipe = pipe;
        }
      #else
        pipe_count += 1;
        previous_pipe = pipe;
      #endif  
    }
  
  }
  
  for (int i=0;i<COMPUTER_BUFFER_SIZE;i++){  
    
    for (int j=0; j<DEVICES; j++){
    
      Serial.write(receiver_buffer[j][i]/256);
      Serial.write(receiver_buffer[j][i]%256);
    }
  
  }

}


void setup() {
 
  Serial.begin(115200);
  delay(1000);
    
  radio.begin(); 
  radio.setChannel(CHANNEL);
  radio.setAddressWidth(5);
  //radio.enableAckPayload();
  
  radio.setAutoAck(false);
  radio.setRetries(0,0); 
  //radio.setCRCLength(RF24_CRC_16);
  radio.setDataRate(RF24_2MBPS); //more than enough
  radio.setPayloadSize(BUFFER_SIZE * sizeof(uint16_t)); // 2 x buffer size
  

  for (int i=0; i<DEVICES; i++){
  
    radio.openReadingPipe(i+1, pipes[i]);
    delay(250);
  }

  //start
  radio.startListening();
 
}


void loop(void){
  receiver();
}
 


