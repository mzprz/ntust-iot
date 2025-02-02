/************************ INCLUDE LIBRARY ************************/
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Servo.h>
/*****************************************************************/

/********************** PIN CONFIGURATION ************************/
#define pinAlarm D5
#define pinServo1 D6
#define pinServo2 D7
/*****************************************************************/

/********************* VARIABEL WiFi & MQTT **********************/
const char* ssid = "SURAKARTAN"; // Nama WiFi
const char* password = "prasetyo12"; // Password WiFi
const char* mqtt_server = "192.168.43.242"; // IP address
const int mqtt_port = 1884; // Port MQTT
WiFiClient espClient;
PubSubClient client(espClient);
/*****************************************************************/

/************************* VARIABEL GLOBAL ***********************/
Servo myservo1;
Servo myservo2;

DynamicJsonDocument root(1024);
int pos = 0; // variable to store the servo position
int stateAlarm = 0;
bool clockwise = true;
/*****************************************************************/

/************************ DEKLARASI FUNGSI ***********************/
void setup_wifi();
void reconnect();
void callback(char* topic, byte* payload, unsigned int length);

/*****************************************************************/

void setup() {
        Serial.begin(115200);

        pinMode(pinAlarm, OUTPUT);

        setup_wifi();

        /***** Connnect MQTT *****/
        client.setServer(mqtt_server, mqtt_port);
        while (!client.connected()) {
                String connection_id = String(ESP.getChipId());
                client.connect(connection_id.c_str());
                Serial.print(".");
                delay(500);
        }

        Serial.println("\nConnected to MQTT");
        /************************/
        client.subscribe("dataAlert");
        client.setCallback(callback);
}

void loop() {
        if (!client.connected()) { // Koneksikan kembali apabila koneksi terputus
                reconnect();
                client.subscribe("dataAlert");
        }
        client.loop();

        // FUNGSI Alarm -------------------------------------------------------
        if(!stateAlarm) {
                myservo1.attach(pinServo1);
                myservo2.attach(pinServo2);
                myservo1.write(pos);
//                delay(10);
                myservo2.write((pos+180)/2);
                delay(10);
                if (clockwise) {
                        if (pos == 180){
                          pos--;
                          clockwise = false;
                        } else {
                          pos++;
                        }
                } else {
                        if (pos == 0){
                          pos++;
                          clockwise = true;
                          } else {
                            pos--;
                          }
                }
//                Serial.println(pos);
                digitalWrite(pinAlarm, LOW);
        }
        else if(stateAlarm) {
                myservo1.detach();
                myservo2.detach();
                digitalWrite(pinAlarm, HIGH);
        }
}

void setup_wifi() {
        // We start by connecting to a WiFi network
        Serial.println();
        Serial.print("Connecting to ");
        Serial.println(ssid);

        WiFi.begin(ssid, password);

        // Waiting until connected
        while (WiFi.status() != WL_CONNECTED) {
                delay(500);
                Serial.print(".");
        }
        randomSeed(micros());

        Serial.println("");
        Serial.println("WiFi connected");
        Serial.println("IP address: ");
        Serial.println(WiFi.localIP());
}

void reconnect() {
        // Loop until we're reconnected
        while (!client.connected()) {
                Serial.print("Attempting MQTT connection...");

                // Create a random client ID
                String clientId = "ESP8266Client-";
                clientId += String(random(0xffff), HEX);

                // Attempt to connect
                if (client.connect(clientId.c_str())) {
                        Serial.println("connected");
                } else {
                        Serial.print("failed, rc=");
                        Serial.print(client.state());
                        Serial.println(" try again in 2 seconds");

                        // Wait 2 seconds before retrying
                        delay(2000);
                }
        }
}

void callback(char* topic, byte* payload, unsigned int length) {
        Serial.print("Message received on topic ");
        Serial.print(topic);
        Serial.print(": ");
        String string_message;
        for (int i = 0; i < length; i++) {
                Serial.print((char)payload[i]);
                string_message += char(payload[i]);
        } Serial.println();

        deserializeJson(root, string_message);

        int area = root["area"];
        int status = root["status"];

        Serial.print("Area : ");
        Serial.print(area);
        Serial.print(", Status : ");
        Serial.print(status);

        if(area == 1 ) {
                stateAlarm = status;
                Serial.println("ZING " + String(status));
        }

}
