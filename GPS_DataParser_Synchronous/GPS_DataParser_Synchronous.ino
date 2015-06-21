#include <SPI.h>
#include <SD.h>

//#define debugMode  // Comment out to disable informational serial prints

const char GPSDATASELECT = 'G';  // Choose data for parsing ('G' = GPGGA / 'R' = GPRMC)

char GPSDATANULL;

File logFile;

const int chipSelect = 10;

boolean programReset = false;

String serialString;

void setup() {
  Serial.begin(57600);

  if (GPSDATASELECT == 'G') GPSDATANULL = 'R';
  else if (GPSDATASELECT == 'R') GPSDATANULL = 'G';

#ifdef debugMode
  Serial.print("Initializing SD card...");
#endif
  if (!SD.begin(chipSelect)) {
#ifdef debugMode
    Serial.println("initialization failed!");
#endif
    return;
  }
#ifdef debugMode
  Serial.println("initialization done.");
  Serial.println(F("Ready to parse log. Waiting for start command."));
#endif
}

void loop() {
  if (programReset == true) {
    programReset = false;
    logFile = SD.open("COMPILED.txt");
    parseLog(logFile);
  }
  else if (Serial.available()) {
    char s = Serial.read();
    if (s == 'p') {
      logFile = SD.open("COMPILED.txt");
      parseLog(logFile);
    }
    else {
      Serial.println(F("Invalid character received. Waiting for valid start command."));
      return;
    }
  }
  delay(10);
}

/*void parseLog(File rawLog) {
 if (rawLog) {
 unsigned long startTime = millis();
 while (rawLog.available()) {
 Serial.write(rawLog.read());
 }
 rawLog.close();
 unsigned long totalDurationLong = millis() - startTime;
 int totalDurationSec = totalDurationLong / 1000;
 int totalDurationMin = totalDurationSec / 60;
 Serial.println();
 Serial.print(F("Parse duration: "));
 Serial.print(totalDurationSec);
 Serial.print(F(" seconds / "));
 Serial.print(totalDurationMin);
 Serial.println(F(" minutes"));
 }
 else Serial.println(F("Error opening log file for parsing."));
 }*/

void parseLog(File rawLog) {
  int lineCount = 0;
  boolean skipRead = false;
  boolean gpggaString = false;
  if (rawLog) {
    unsigned long startTime = millis();
    char c;
    while (rawLog.available()) {
      if (skipRead == false) c = rawLog.read();
      else skipRead = false;
      if (c == '$') {
        for (int x = 0; x < 3; x++) {
          c = rawLog.read();
        }
        if (c == GPSDATASELECT) {
          gpggaString = true;
          for (int x = 0; x < 3; x++) {
            c = rawLog.read();
          }
          for (unsigned long timeoutStart = millis(); (millis() - timeoutStart) < 5000; ) {
            c = rawLog.read();
            if (c == '$') {
              skipRead = true;
              if (!Serial.available()) {
                while (!Serial.available()) {
                  delay(1);
                }
              }
              char s = Serial.read();
              if (s == 'l') {
                Serial.println(serialString);
                Serial.flush();
                //delay(10);
                lineCount++;
                serialString = "";
                break;
              }
              else if (s == 'p') {
                programReset = true;
                rawLog.close();
                serialString = "";
                return;
              }
            }
            else serialString += c;
          }
        }
        else gpggaString = false;
      }
    }
    rawLog.close();
    unsigned long totalDurationLong = millis() - startTime;
    int totalDurationSec = totalDurationLong / 1000;
    if (gpggaString == true) totalDurationSec = totalDurationSec - 5;
    int totalDurationMin = totalDurationSec / 60;
    int extraDurationSec = totalDurationSec % 60;

#ifdef debugMode
    Serial.println();
    Serial.print(F("Parsed "));
    Serial.print(lineCount);
    Serial.print(F(" lines in "));
    Serial.print(totalDurationMin);
    Serial.print(F(" minutes and "));
    Serial.print(extraDurationSec);
    Serial.println(F(" seconds."));
#endif
    while (true) {
      delay(1000);
    }
  }
#ifdef debugMode
  else Serial.println(F("Error opening log file for parsing."));
#endif
}



