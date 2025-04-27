// Arduino main code for ESP32#include <WiFi.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <BluetoothSerial.h>
#include <esp_wifi.h>        // << BU satır eksikti!
#include "model.h"


#define TRIG_PIN 5
#define ECHO_PIN 18
#define LED_PIN 2

const char* ssid = "...";
const char* password = "1234567890";
const char* mqtt_server = "test.mosquitto.org";

WiFiClient espClient;
PubSubClient client(espClient);
BluetoothSerial SerialBT;

// Bluetooth MAC whitelist (izinli cihazlar)
String allowedMACs[] = { "AA:BB:CC:DD:EE:FF" };

// Global değişkenler
int packetSize = 0;
int rssiValue = -100;
int deviceCount = 1;

void setup_wifi() {
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi bağlandı!");
}

void mqttReconnect() {
  while (!client.connected()) {
    Serial.print("MQTT bağlanıyor...");
    if (client.connect("ESP32Client")) {
      Serial.println("Bağlandı!");
    } else {
      Serial.print("Hata: ");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void sendAlert(const char* msg) {
  if (!client.connected()) mqttReconnect();
  client.loop();
  client.publish("aiot-nids/alert", msg);
  Serial.println("MQTT uyarısı gönderildi.");
}

long readDistanceCM() {
  digitalWrite(TRIG_PIN, LOW); delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH);
  return duration * 0.034 / 2;
}

bool isBluetoothAuthorized() {
  // Bluetooth taraması bu versiyonda sadece dummy örnek
  // Gerçek tarama için ileri düzey BLE scan gerekir
  return true; // Şimdilik herkes izinli gibi çalışır
}

void packetSniffer(void *buf, wifi_promiscuous_pkt_type_t type) {
  wifi_promiscuous_pkt_t *pkt = (wifi_promiscuous_pkt_t *)buf;
  rssiValue = pkt->rx_ctrl.rssi;
  packetSize = pkt->rx_ctrl.sig_len;
  deviceCount++; // Basit sayaç (her paket = bir cihaz varsayımı)
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  setup_wifi();
  client.setServer(mqtt_server, 1883);

  SerialBT.begin("AIoT-NIDS");

  WiFi.mode(WIFI_STA);
  esp_wifi_set_promiscuous(true);
  esp_wifi_set_promiscuous_rx_cb(&packetSniffer);
}

void loop() {
  long distance = readDistanceCM();
  bool proximity = distance < 100;
  bool btOk = isBluetoothAuthorized();

  float features[] = { (float)packetSize, (float)rssiValue, (float)deviceCount };
  int prediction = clf.predict(features);

  if ((proximity && !btOk) || prediction == ANOMALY) {
    digitalWrite(LED_PIN, HIGH);
    sendAlert("AIoT-NIDS: Tehdit Algılandı!");
  } else {
    digitalWrite(LED_PIN, LOW);
  }

  deviceCount = 1; // her döngüde sıfırla
  delay(2000);
}
