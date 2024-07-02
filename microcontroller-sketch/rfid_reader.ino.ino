/**
 * Title: Sketch UniVersoMe MIFARE RFID Card Reader
 * Author: Gianluca Carbone
 * Date: 2023-02-18 
 * Version: 1.0.2
 * Tags: MFRC522 module
 */

#include <RTClib.h>   // Library for Date and Time Module
#include <Wire.h>     // Library for communication with I2C
#include <SPI.h>      // Library for Serial Peripheral Interface
//#include <ArduinoJson.h> - https://arduinojson.org/ 
#include <MFRC522.h>  // Library for the RFID Reader
#include <Stepper.h>  // Library for Stepper Motor

// =====[ RFID READER ]=====
#define SS_PIN  10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::StatusCode status;
MFRC522::MIFARE_Key currentKey;

// Init array that will store new NUID 
byte nuidPICC[4];

//#define NR_AUTH_KEYS   10
//MFRC522::MIFARE_Key masterKey = {0x07, 0x91, 0xb0, 0x93, 0x00, 0x00};
//MFRC522::MIFARE_Key currentKey;
//MFRC522::MIFARE_Key authorizedKeys[NR_AUTH_KEYS];

// =====[ STEPPER MOTOR ]=====
const int stepsPerRevolution = 2048;  // change this to fit the number of steps per revolution
const int rolePerMinute = 15;  // RPM
//Stepper stepmotor(stepsPerRevolution, A3, A1, A2, A0);

String sendMessage;
String receivedMessage;

bool handshake;

// =====[ SYSTEM SETUP ]=====
void setup() {
  Serial.begin(115200);                 // Initialize the Serial monitor (USB) for debugging. Baudrate value
  handshake=false;
  //Serial.setTimeout(100);
  while(!Serial);                       // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
  SPI.begin();                          // Init SPI bus

  //pinMode(LED_BUILTIN, OUTPUT);       // set LED pin as output
  //digitalWrite(LED_BUILTIN, LOW);     // switch off LED pin

  mfrc522.PCD_Init();
  delay(4);				                      // Optional delay. Some board do need more time after init to be ready
  //stepmotor.setSpeed(rolePerMinute);
  
  Serial.println("UniVersoMe - Smart Card Access Control System");
  mfrc522.PCD_DumpVersionToSerial();	// Show details of PCD - MFRC522 Card Reader details
  Serial.println("---------------------------------------------");
}

// =====[ SYSTEM LOOP ]=====
void loop() {
  // Serial Handshake
  if ( !handshake && Serial.available() > 0 ) {
    String message = Serial.readStringUntil('\n');
    Serial.println("[DEBUG] - Serial message" + message);
    if ( message.equals("Hello") ) {
      Serial.println("H4NDSH4K3");
      handshake = true;
    }
  }
  if ( !mfrc522.PICC_IsNewCardPresent() ) { delay(50); return; };
  if ( !mfrc522.PICC_ReadCardSerial() ) { delay(50); return; };
  
  // Dump debug info about the card; PICC_HaltA() is automatically called
	//mfrc522.PICC_DumpToSerial(&(mfrc522.uid));
  
  // [LOG] - Chip Type
  MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
  Serial.print(mfrc522.PICC_GetTypeName(piccType));
  Serial.print(F(", "));

  // Check is the PICC of Classic MIFARE type
  if ( piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&
       piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
       piccType != MFRC522::PICC_TYPE_MIFARE_4K ) {
    Serial.println(F("Your tag is not of type MIFARE Classic."));
    return;
  }

  //Serial.print("[DEBUG] - UID Size: "); Serial.print(mfrc522.uid.size); 
  printHex(mfrc522.uid.uidByte, mfrc522.uid.size);
  Serial.println(F(""));

  // Store NUID into nuidPICC array
  /*for (byte i = 0; i < mfrc522.uid.size; i++) {
    nuidPICC[i] = mfrc522.uid.uidByte[i];

    // [LOG] - Chip UID
    Serial.print(nuidPICC[i]);
  }
  Serial.println(F("")); 
  */

  //if (Serial.available() > 0) {

  // Send Card UID to Serial
  // Implement Switch state to wait on RX signal from the Raspberry
  /* if (Serial.available() > 0) {
    //String message = Serial.readString();
    String message = Serial.readStringUntil('\n');
    message = "TIME" + " " + message;
    Serial.println(message)
  } 
  */
  
  // Halt PICC
  mfrc522.PICC_HaltA();

  // Stop encryption on PCD
  mfrc522.PCD_StopCrypto1();

  delay(2000);
}

/**
 * Helper routine to dump a byte array as hex values to Serial. 
 */
void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    //Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i] < 0x10 ? "0" : "");
    Serial.print(buffer[i], HEX);
  }
}

/**
 * Helper routine to dump a byte array as dec values to Serial.
 */
void printDec(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(' ');
    Serial.print(buffer[i], DEC);
  }
}

/* Issues
  * - Skip MOTD Serial print setup
*/

/* Useful links
 1. https://github.com/miguelbalboa/rfid/blob/master/examples/ReadNUID/ReadNUID.ino
 2. https://forum.arduino.cc/t/how-to-read-bytes-from-a-rfid-card-and-convert-them-into-an-integer/1158246
 3. Arduino JSON: https://arduinojson.org/ 
 */

/* Updates:
  * v1.0.1
  * ? - Arduino sends data via Serial in JSON format: https://www.youtube.com/watch?v=-3swby4ryU4 
  *
  * v1.0.0 ---------
  * 
  * MFRC522.h class from https://github.com/miguelbalboa/rfid
*/