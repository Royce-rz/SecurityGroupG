#include <ICM_20948.h>
#include <Base64.h>
#include <AESLib.h>
#include <SPI.h>
#include <WiFiNINA.h>
#include <WiFiSSLClient.h>
#include <WiFiClient.h>
#include <ArduinoHttpClient.h>
#include <Wire.h>

const char ssid[] = "TALKTALKE5A7F3"; // WiFi/Hotspot name
const char pass[] = "E83CHHMT"; // WiFi/Hotspot password

const String deviceId = "IoT_devices_data"; // name the ID of this IoT device

const char serverAddress[] = "192.168.1.196"; // Flask address
int serverPort = 443; // Flask port

ICM_20948_I2C icm; 
WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverAddress, serverPort); // use http method

String dataBuffer = ""; // buffer area of collected data
const int bufferSize = 60; // maximum of data packet
int dataCount = 0; // number of data collected

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

void sendData() {
  // Include the device ID in the data sent to the server
  String postData = "device_id=" + deviceId + "&data=" + dataBuffer;
  Serial.println(postData);

  // Send data to the server
  Serial.println("Sending batch data to server...");
  client.post("/data", "application/x-www-form-urlencoded", postData);
  Serial.println(client.responseBody());
}

void initializeSensors() {
  if (!initializeICM()) {
    Serial.println("ICM-20948 initialization successfully");
  } else {
    Serial.println("ICM-20948 initialized failed");
  }
}

bool initializeICM() {
  bool status = icm.begin(Wire, 0x68); // initialization of device
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
  Serial.println("WiFi connected!");

  initializeSensors();
}

void loop() {
  accumulateSensorData();
  if (dataCount >= bufferSize) {
    sendData();
    dataBuffer = ""; // clean the buffer area
    dataCount = 0; // reset the region
  }

  delay(10); 
}







