#include <SPI.h>
#include <Ethernet.h>
#include <stdio.h> 
#include <stdlib.h> 
#include <time.h> 

const int B = 4275;               // B value of the thermistor
const int R0 = 100000;            // R0 = 100k
const int pinTemperature = A0;     // Grove - Temperature Sensor connect to A0

const int pinNoise = A1;   // sound sensor

const int pinLight = A2;   // light sensor


// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = {
  0x90, 0xA2, 0xDA, 0x10, 0xA7, 0xE1
};

IPAddress ip(192, 168, 10, 1);

// Initialize the Ethernet server library
// with the IP address and port you want to use
// (port 80 is default for HTTP):
EthernetServer server(80);

void setup() {
  // You can use Ethernet.init(pin) to configure the CS pin
  //Ethernet.init(10);  // Most Arduino shields
  //Ethernet.init(5);   // MKR ETH shield
  //Ethernet.init(0);   // Teensy 2.0
  //Ethernet.init(20);  // Teensy++ 2.0
  //Ethernet.init(15);  // ESP8266 with Adafruit Featherwing Ethernet
  //Ethernet.init(33);  // ESP32 with Adafruit Featherwing Ethernet

  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.println("Ethernet WebServer Example");

  // start the Ethernet connection and the server:
  Ethernet.begin(mac, ip);

  // Check for Ethernet hardware present

 // I am commenting from here 
  /*
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
    while (true) {
      delay(1); // do nothing, no point running without Ethernet hardware
    }
  }
  if (Ethernet.linkStatus() == LinkOFF) {
    Serial.println("Ethernet cable is not connected.");
  }
*/
 // until here

  // start the server
  server.begin();
  Serial.print("server is at ");
  Serial.println(Ethernet.localIP());
  srand(time(0)); 
}


void loop() {
  // listen for incoming clients
  EthernetClient client = server.available();
  if (client) {
    Serial.println("new client");
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    while (client.connected()) {
      //Serial.println("I am in While loop");
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        Serial.println("I read the request");
        //Serial.println(c);
        // if you've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so you can send a reply
        if (c == '\n' && currentLineIsBlank) {
          Serial.println("I am responsing");
          // send a standard http response header
          /*
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println("Connection: close");  // the connection will be closed after completion of the response
          client.println("Refresh: 5");  // refresh the page automatically every 5 sec
          client.println();
          client.println("<!DOCTYPE HTML>");
          client.println("<html>");
          // output the value of each analog input pin
          client.println(300);
          /*for (int analogChannel = 0; analogChannel < 6; analogChannel++) {
            int sensorReading = analogRead(analogChannel);
            client.print("analog input ");
            client.print(analogChannel);
            client.print(" is ");
            client.print(sensorReading);
            client.println("<br />");
          }
          client.println("</html>");*/
        // ++++++++++++++++++++++From here only my comments ++++++++++++++++++++++++++++
        // measuring temperature ========================================================================================
        int status_sensor = 0;
        int a = analogRead(pinTemperature);
        float R = 1023.0/a-1.0;
        R = R0*R;
        float temperature = 1.0/(log(R/R0)/B+1/298.15)-273.15; // convert to temperature via datasheet
        if(16 <= temperature && temperature <= 22){
        status_sensor = 1;
        }else if((10 <= temperature && temperature <= 15) || (23 <= temperature && temperature <= 26)){
        status_sensor = 2;
        }else{
        status_sensor = 3;  
        }
        Serial.println(temperature);
        
        // measuring noise ==============================================================================================
        long sum = 0;
        for(int i=0; i<5; i++)
        {
            sum += analogRead(pinNoise);
        }
        float noise = sum/5;
        Serial.println(noise);
        if(noise <= 600){
        noise = map(noise, 0, 600, 0, 40);
        }else if(noise <= 800){
        noise = map(noise, 601, 800, 41, 70);
        }else{
        noise = map(noise, 801, 1023, 71, 100);  
        }
        Serial.println(noise);
      
        // measuring light ==============================================================================================
        int light_sensed = analogRead(pinLight);
        Serial.println(light_sensed);
        double light = exp(light_sensed/80);
        Serial.println(light);

        // measuring light ==============================================================================================
        int co2 = 0;
        if(status_sensor == 1){
        co2 = (rand()%(800 - 0 + 1)) + 0;   
        }else if(status_sensor == 2){
        co2 = (rand()%(2000 - 801 + 1)) + 801;  
        }else{
        co2 = (rand()%(3000 - 2001 + 1)) + 2001;
        }
        Serial.println(co2);
        Serial.println(status_sensor);

        // measuring light ==============================================================================================
        int humidity = 0;
        if(status_sensor == 1){
        humidity = (rand()%(60 - 30 + 1)) + 30;   
        }else if(status_sensor == 2){
        humidity = (rand()%(29 - 25 + 1)) + 25;  
        }else{
        humidity = (rand()%(24 - 0 + 1)) + 0;
        }
        Serial.println(humidity);

          // sending data to the raspberry pi server
          client.print(temperature);
          client.print(":");
          client.print(noise);
          client.print(":");
          client.print(light);
          client.print(':');
          client.print(co2);
          client.print(':');
          client.print(humidity);
          break;
        // ++++++++++++++++++++++ Until here only my comments ++++++++++++++++++++++++++++
        }
        if (c == '\n') {
          // you're starting a new line
          currentLineIsBlank = true;
        } else if (c != '\r') {
          // you've gotten a character on the current line
          currentLineIsBlank = false;
        }
      }
    }
    // give the web browser time to receive the data
    delay(1);
    // close the connection:
    client.stop();
    Serial.println("client disconnected");
  }
}
