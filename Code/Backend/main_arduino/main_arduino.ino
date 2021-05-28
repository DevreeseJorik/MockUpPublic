// declaratie variabelen

String serialData = "Def: 0";
String val;

int volume;
int id;
int value;
int len;
int indexSerial;
  float delayt;
// declaratie pinnen

int pinsPumps[] = {2,3,4,5,6,7};
float volumePerSec = 38;

float arrayRecipe[5];

void setup() {
  Serial.begin(9600);
  Serial.println("Serial Started");
  for (int i = 0; i < 6; i++) {
    pinMode(pinsPumps[i],OUTPUT);
    digitalWrite(pinsPumps[i],HIGH);
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

void loop() {
  // Serial.println("Sending Data"); // To send data 
  
    if (Serial.available() > 0) {
      serialData = Serial.readStringUntil('\n'); // receiving data
      // Serial.print("Arduino Acknowledges receiving following data: ");
      //Serial.println(serialData);
      if (serialData.indexOf("Sen:") == 0) {
        val = serialData[4];
        id = val.toInt();
        value = 1023;
        Serial.println("Sen:"+ String(id) + "/Val:" + String(value));
      }

      if (serialData.indexOf("Act:") == 0) {
        if (serialData == "Act:Start") {
        Serial.println("Starting cocktailprocess");
        } else if (serialData == "Act:Fin") {
          Serial.println("Waiting until glass is removed...");
          delay(5000);
          Serial.println("Finished cocktailprocess");        
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
    }
}


     
