#include <Base64.h>
#include <AESLib.h>
#include <SPI.h>
#include <WiFiNINA.h>
#include <ArduinoHttpClient.h>
#include <Wire.h>
#include <ICM_20948.h>

const char ssid[] = "yourwifi_name"; // WiFi/Hotspot name
const char pass[] = "yourwifi_password"; // WiFi/Hotspot password

const String deviceId = "IoT_devices_data"; // name the ID of this IoT device

const char serverAddress[] = "yourIP_address"; // Flask address
int serverPort = 80; // Flask port

ICM_20948_I2C icm; 
AESLib aesLib;
WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverAddress, serverPort);

String dataBuffer = ""; // buffer area of collected data
const int bufferSize = 60; // maximum of data packet
int dataCount = 0; // number of data collected

byte key[] = "securitygroupg12";  // 16 bytes AES KEY
byte iv[] = "securitygroupg12";   // 16 bytes AES IV

void accumulateSensorData() {

  if (icm.dataReady()) {
    icm.getAGMT(); // sensor reading
    if (dataBuffer.length() > 0) {
      dataBuffer += ","; // add symbol between each data
    }
    dataBuffer += "0:" + String(icm.accX()) + "," + String(icm.accY()) + "," + String(icm.accZ()) + ","  + String(icm.gyrX()) + "," + String(icm.gyrY()) + "," + String(icm.gyrZ());
    dataCount++;
  }
}

void encryptAndSendData() {
  String postData = "device_id=" + deviceId + "&data=" + dataBuffer;
  const char* inputString = postData.c_str();
  Serial.println(postData);
  Serial.println(); 

  //char inputString[] = dataBuffer;
  int inputStringLength = strlen(inputString);
  Serial.println("Encryption start.");
  Serial.print("Original data is:\t");
  Serial.print(inputString);
  Serial.println(); 

  byte encryptedData[5120]; // Adjust size according to your needs
  memset(encryptedData, 0, sizeof(encryptedData));
  aesLib.set_paddingmode((paddingMode)0);
  int encryptedLength = aesLib.encrypt((byte*)inputString, inputStringLength, encryptedData, key, 128, iv);

  // calculate the length of encrypted information
  Serial.println("Encoding start.");
  int encodedLength = Base64.encodedLength(encryptedLength);
  char encodedString[encodedLength]; // restore the encoded data string
  Base64.encode(encodedString, (char*)encryptedData, encryptedLength);
  Serial.print("Encoded string is:\t");
  Serial.println(encodedString);
  Serial.println();

  Serial.print("Post string is:\t");
  Serial.println(String(encodedString));
  Serial.println();

  // Send data to the server
  Serial.println("Sending encrypted and encoded data to server...");
  client.post("/data", "text/plain", encodedString);
}

void initializeSensors() {// initialization of device
  if (!initializeICM()) {
    Serial.println("ICM-20948 initialization successfully");
  } else {
    Serial.println("ICM-20948 initialized failed");
  }
}

bool initializeICM() {
  bool status = icm.begin(Wire, 0x68); 
  delay(100); 
  return status;
}

void setup() {
  Serial.begin(9600);
  Wire.begin();
  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println("WiFi connection secussful");

  initializeSensors();
}

void loop() {
  accumulateSensorData();
  
  if (dataCount >= bufferSize) { 
    encryptAndSendData();
    //dataBuffer = ""; 
    //dataCount = 0; 
  }
  
  delay(10); 
}

