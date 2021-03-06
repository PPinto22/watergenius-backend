
#include "FS.h"
#include <ESP8266WiFi.h>
#include <Wire.h> 
#include <DS3231.h>
#include <ArduinoJson.h>

#define DEBUG true

//THIS NODE CONFIG
#define NODEID /*NODEID*/
#define SENSORID /*SENSORID*/
#define MAXCONNECTIONTRY 5
#define SSIDCONNECT /*SSID*/
#define SSIDPW /*PW*/
#define SERVERIP /*SERVERIP*/
#define SERVERPORT 5000
#define SERVERTIMEOUT 10000
#define TIMERATE /*TIMERATE*/
#define thetaWP 0.37
#define P 0.4
#define Zr 0.4
bool connectedNework = false;
bool serverAvailable = false;


//ERROR 
#define LOGFILE "/LOG"
#define NONETWORK 1
#define NOSERVERCONNECTION 2
#define NOSERVERRESPONSE 3
#define NOWATER 3

//PINOUT
#define ON false
#define OFF true
#define WATERMESUREPOWER D1
#define WATERMESURE 12
#define WATERVALVE 15
#define TURNON D2
#define SOILSENSOR A0
volatile unsigned long  FlowPulse;
float calibrationFactor = 4.5;

void ICACHE_RAM_ATTR rpm ()
{ 
  //Serial.println("PULSE");
  FlowPulse++;
} 

bool sendError(String record ){
  WiFiClient client;
  record.replace(" ","_");
  String url = String("/sensorProblem/") + String(NODEID) + String('/')+ record;
  if (!client.connect(SERVERIP, SERVERPORT)) {
     if (DEBUG) Serial.println("connection failed");
    return false;
  }
  if(DEBUG) Serial.println("URL: "+url);
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + SERVERIP + "\r\n" + 
               "Connection: close\r\n\r\n");
  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > SERVERTIMEOUT) {
      if (DEBUG) Serial.println(">>> Client Timeout !");
      //client.stop();
      return false;
    }
  }
  bool response = false;
  for(int s=0;s<5 && !response;s++){
    while(client.available()){
      char c = client.read();
      //String line = client.readStringUntil('\0');
      if(DEBUG) Serial.print(c);
       if(c=='}'){
        response = true;
       }
    }
    if(!response) delay(10000);
  }
  //client.stop();
  return true;
}



void logUnsentErrors(String strs[], bool sent[], int len){
  File f = SPIFFS.open(LOGFILE, "a+");
  if (!f) {
    if(DEBUG) Serial.println("file open failed UNSENT");
    return;
  }
  for(int i = 0; i<len;i++){
    if(!sent[i]) f.println(strs[i]);
  }
  
  f.close();
}

void sendError(){
  File f = SPIFFS.open(LOGFILE, "r");
   if (!f) {
    if(DEBUG) Serial.println("file open failed READ");
    return;
  }
  String erros[100];
  bool sent[100];
  int totErros =0 ;
  String leftData = f.readStringUntil('\0');;
  f.close();
  SPIFFS.remove(LOGFILE);
  while(leftData.length()>5 && totErros<100){
    int splitpos = leftData.indexOf('\n');
    erros[totErros] = leftData.substring(0,splitpos);
    leftData = leftData.substring(splitpos+1,leftData.length());
    totErros++;
    
  }
  for(int i =0;i<totErros;i++){
    sent[i]= sendError(erros[i]);
  }
  logUnsentErrors(erros,sent,totErros);
}

void logError(int erroCode, String message){
  long now = millis();
  File f = SPIFFS.open(LOGFILE, "a+");
  if (!f) {
    if(DEBUG) Serial.println("file open failed");
    return;
  }
  String error = String(erroCode)+ "/" + String(1)+"/"+ message+ "/"+ String(now);
  f.println(error);
  f.close();
}


void setupGPIO(){

  pinMode(WATERVALVE, OUTPUT);
  digitalWrite(WATERVALVE, OFF);
  pinMode(WATERMESUREPOWER,OUTPUT);
  digitalWrite(WATERMESUREPOWER, OFF);
  pinMode(TURNON, OUTPUT);
  digitalWrite(TURNON, OFF);
  pinMode(SOILSENSOR, INPUT);
  pinMode(WATERMESURE,INPUT_PULLUP);
  closeWater();
  
}

bool connectNetwork(){
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSIDCONNECT, SSIDPW);
  int timetry =50;
  while (WiFi.status() != WL_CONNECTED) {
      if (timetry==0) {
        return false;
      }
      delay(100);
      timetry--;
  }
  if(DEBUG){
    Serial.println("WiFi connected");
    Serial.println(WiFi.localIP());
  }
  
  return true;
}


void openWater(){FlowPulse=0;digitalWrite(WATERVALVE,ON);}
void closeWater(){digitalWrite(WATERVALVE,OFF);FlowPulse=0;}
void turnONWaterPower(){digitalWrite(WATERMESUREPOWER,ON);}
void turnOFFWaterPower(){digitalWrite(WATERMESUREPOWER,OFF);}

float readWaterQuantity(){
  unsigned long  pulsCalc = 0 ;
  delay(75);
  detachInterrupt(digitalPinToInterrupt(WATERMESURE));
  noInterrupts();
  pulsCalc = FlowPulse;
  attachInterrupt(digitalPinToInterrupt(WATERMESURE), rpm, RISING);
  interrupts();
  return (100.0*pulsCalc)/45;
}

float readHumiditySoil(){
  int soil  = analogRead(SOILSENSOR);
  if (DEBUG) Serial.println("SOIL ANALOG " + String(soil));
  //soil = constrain(soil, 485, 1023);
  soil = map(soil, 854, 423, 0, 100);
  if (DEBUG) Serial.println("SOIL Humidity " + String(soil));
  //return 10.0;
  return soil*1.0;
  //return (soil-thetaWP)*P*Zr*1000;
}

int doIrrigation(long mlsQuantiy){
  float totalDone =0;
  float readLastMin[60];
  int timeRun=0;
  //turnSensorsON();
  turnONWaterPower();
  openWater();
  FlowPulse =0;
  attachInterrupt(digitalPinToInterrupt(WATERMESURE), rpm, RISING);
  interrupts();
  while(totalDone<mlsQuantiy){
    delay(1000);
    int pos = timeRun%60;
    totalDone=readWaterQuantity();
    readLastMin[pos]= totalDone;
    if(DEBUG) Serial.println("QUANTIDADE " +String(totalDone));
    if(timeRun>60 && readLastMin[(pos+1)%60]>=readLastMin[pos]){
      closeWater();
      turnOFFWaterPower();
      detachInterrupt(digitalPinToInterrupt(WATERMESURE));
      noInterrupts();
      logError(NOWATER,"WATHER READINGS NOT UPDATED WHEN IS TURN ON IN LAST MINUTE");
      return -1;
    } 
    timeRun++;
  }
  detachInterrupt(digitalPinToInterrupt(WATERMESURE));
  noInterrupts();
  turnOFFWaterPower();
  closeWater();
  return 0;
}

long sendSoilData(int humidity ){
  WiFiClient client;
  if (!client.connect(SERVERIP, SERVERPORT)) {
     if (DEBUG) Serial.println(String("NO CONNECTION TO ") + String(SERVERIP)+String(":")+ String(SERVERPORT));
     logError(NONETWORK,String("NO CONNECTION TO ") + String(SERVERIP)+String(":")+ String(SERVERPORT));
     serverAvailable=false;
    return -3;
  }

  String url = String("/sensorRead/") + String(SENSORID) + '/' + String(humidity);
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + SERVERIP + "\r\n" + 
               "Connection: close\r\n\r\n");
  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > SERVERTIMEOUT) {
      if (DEBUG) Serial.println(">>> Client Timeout !");
      serverAvailable=false;
      //client.stop();
      logError(NOSERVERRESPONSE,String("NO RESPONSE FROM ") + String(SERVERIP)+String(":")+ String(SERVERPORT));
      return -2;
    }
  }
  //Serial.println("Recieved Answer");
  bool response =false;
  long retValue = -1;
  StaticJsonBuffer<500> jsonBuffer;
  for(int s=0;s<5 && !response;s++){
    while(client.available()){
      String line = client.readStringUntil('\r');
      if(DEBUG) Serial.println(line);
      if(line.indexOf("quantidade")>0){
        JsonObject& root = jsonBuffer.parseObject(line);
        retValue = root["quantidade"];
        response = true;
        //break;
      }
      
    }
    if(!response) delay(10000);
  }
  //client.stop();
  if (DEBUG){
    Serial.print("IRRIGATION ");
    Serial.println(retValue);
  }
  if(!response) logError(NOSERVERRESPONSE,String("INVALID RESPONSE FROM ") + String(SERVERIP)+String(":")+ String(SERVERPORT));
  //return 10000;
  return retValue*1000;
}

void disconnectNetwork(){
  WiFi.disconnect();
  connectedNework =false;
  serverAvailable=false;
}

void turnSensorsOFF(){digitalWrite(TURNON,false);closeWater();turnOFFWaterPower();}

void turnSensorsON(){digitalWrite(TURNON,true);}

void turnOff(int minutes){
  turnSensorsOFF();
  disconnectNetwork();
  if (DEBUG) Serial.println("Will sleep for " + String(minutes));
  ESP.deepSleep(minutes*60e6);
}

void attemptConnectNetwork(){
  int trie =0;
  while(trie <MAXCONNECTIONTRY && !connectedNework){
    if (DEBUG){
      Serial.print("Reconect to ");
      Serial.print(SSIDCONNECT);
      Serial.print(" ");
      Serial.println(SSIDPW);
    }
    trie++;
    connectedNework = connectNetwork();
    delay(100);
  }
  if(trie>=MAXCONNECTIONTRY){
    logError(NONETWORK,String("FAIL CONNECT ")+String(SSIDCONNECT ));
    turnOff(TIMERATE);
  }
  serverAvailable=true;
}
void turnON(){
  attemptConnectNetwork();
  turnSensorsON();
  delay(1000);
}

void setup() {
  SPIFFS.begin();
  if (DEBUG){
    Serial.begin(9600);
    Serial.print("SETUP ");
  }
  setupGPIO();
  closeWater();
  turnON();
  float soil  = readHumiditySoil();
  turnSensorsOFF();
  long irrigationNeed = sendSoilData(soil);
  if(irrigationNeed>0){
    doIrrigation(irrigationNeed);
  }else{
  }
  if(serverAvailable){
    sendError();
  }
  turnOff(TIMERATE);
}

void loop() {
}



