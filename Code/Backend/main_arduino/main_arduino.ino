// library variabelen

#include <HX711_asukiaaa.h>

int pinsDout[] = {A0};
const int numPins = sizeof(pinsDout) / sizeof(pinsDout[0]);
int pinSlk = 9;
HX711_asukiaaa::Reader reader(pinsDout, numPins, pinSlk);

#define LOAD_CELL_RATED_VOLT 0.00037f
#define LOAD_CELL_RATED_GRAM 50000.0f

#define HX711_R1 20000.0
#define HX711_R2 8200.0

HX711_asukiaaa::Parser parser(LOAD_CELL_RATED_VOLT, LOAD_CELL_RATED_GRAM, HX711_R1, HX711_R2);
float offsetGrams[numPins];

// declaratie variabelen

String serialData = "Def: 0";
String val;

int volume;
int id;
int value;
int len;
int indexSerial;

float delayt;
float volumePerSec = 38;
float arrayRecipe[5];

bool stateButton = 0;
bool prevStateButton = 0;
bool glassPresent = 0;
bool finRequest = 0;
bool waitForNewGlass = 0;
bool systemReady = false;

// declaratie pinnen

int pinsPumps[] = {2,3,4,5,6,7};
int pinButton = 8;
int pinsSensors[] = {};




void setup() {
  Serial.begin(9600);
  Serial.println("Serial Started");
  
  for (int i = 0; i < 6; i++) {
    pinMode(pinsPumps[i],OUTPUT);
    digitalWrite(pinsPumps[i],HIGH);
  }

  pinMode(pinButton,INPUT_PULLUP);

  Serial.println("Starting load cells");
  reader.begin();
  for (int i = 0; i < reader.doutLen; ++i) {
    offsetGrams[i] = parser.parseToGram(reader.values[i]);
  }

}

void makeCocktail(int id, float volume) {
  delay(500);
  digitalWrite(pinsPumps[id-1],LOW);
  delayt = volume*1000/volumePerSec;
  Serial.println(delayt);
  delay(delayt);
  digitalWrite(pinsPumps[id-1],HIGH);
}

void sendWeights() {
  auto readState = reader.read();
  Serial.println("ReadState: " + HX711_asukiaaa::getStrOfReadState(readState));
  if (readState == HX711_asukiaaa::ReadState::Success) {
    String tempText = "";
    for (int i = 0; i < reader.doutLen; ++i) {
      float gram = parser.parseToGram(reader.values[i]) - offsetGrams[i];
      tempText += String(i) + ":" + String(gram/1000);
      Serial.print("Sensor:" + String(i) + ": " + String(gram/1000));
      Serial.println("");
    }
    Serial.println("");
    Serial.println("Sen:" + tempText);
  }
}

void loop() {
  // Serial.println("Sending Data"); // To send data 
    stateButton = digitalRead(pinButton);
    //Serial.println(stateButton);
    
    if (stateButton != prevStateButton) {
      if (stateButton == 1) {
        Serial.println("Glass removed");
        glassPresent = 0;
      }
      if (stateButton == 0) {
        Serial.println("New Glass put down");
        glassPresent = 1;
        if (systemReady == false) {
          Serial.println("First glass put down");
          systemReady = true;
        }
      }
      
    }
    
  
    
    if (Serial.available() > 0) {
      serialData = Serial.readStringUntil('\n'); // receiving data
      // Serial.print("Arduino Acknowledges receiving following data: ");
      //Serial.println(serialData);
      /*
      if (serialData.indexOf("Sen:") == 0) {
        val = serialData[4];
        id = val.toInt();
        value = 1023;
        Serial.println("Sen:"+ String(id) + "/Val:" + String(value));
      }*/

      if (serialData.indexOf("Act:") == 0) {
        if (serialData == "Act:Start") {
        Serial.println("Starting cocktailprocess");
        } else if (serialData == "Act:Fin") {
          finRequest = 1;
          Serial.println("Waiting until glass is removed...");       
        } else {
      serialData.remove(0,4);
      val = serialData[0];
      id = val.toInt();
      serialData.remove(0,2);
      volume = serialData.toFloat();
      Serial.print(id + String(":"));
      Serial.println(volume);
      makeCocktail(id,volume);
        } 
      }

      if (serialData.indexOf("Sen:") == 0) {
        sendWeights();
      }
    }

    if (finRequest == 1) {
      if ((waitForNewGlass == 0) && (glassPresent == 0)) {
        waitForNewGlass = 1;
        Serial.println("Waiting for new glass...");
      }
      if ((waitForNewGlass == 1) && (glassPresent == 1)) {
        Serial.println("Finished cocktailprocess"); 
        finRequest = 0;
        waitForNewGlass = 0;
      }
    }
    
    prevStateButton = stateButton;
}