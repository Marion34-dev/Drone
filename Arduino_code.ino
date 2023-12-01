#include <SPI.h>
#include <WiFi101.h>
#include <math.h>
#include <config.h>

int keyIndex = 0; // network key Index number (needed only for WEP)
int status = WL_IDLE_STATUS;

WiFiServer server(23);
bool alreadyConnected = false;

float GPS_Latitude = 0.0;
float GPS_Longitude = 0.0;
float GPS_Altitude = 0.0;

char GPSBuffer[82];
byte GPSIndex = 0;

void setup()
{
    Serial1.begin(9600);
    pinMode(GPSENABLE, OUTPUT);
    digitalWrite(GPSENABLE, HIGH);

    if (WiFi.status() == WL_NO_SHIELD)
    {
        while (true)
            ;
    }

    while (status != WL_CONNECTED)
    {
        status = WiFi.begin(ssid, pass);
        delay(10000);
    }

    server.begin();
    printWiFiStatus();
}

void loop()
{
    WiFiClient client = server.available();

    CheckGPS();

    // String dataString = String(GPS_Latitude, 6) + "," + String(GPS_Longitude, 6) + "," + String(GPS_Altitude, 6) + "\n";

    if (client)
    {
        if (!alreadyConnected)
        {
            client.flush();
            alreadyConnected = true;
        }

        if (client.available() > 0)
        {
            char thisChar = client.read();
            server.write(thisChar);
        }
        //  server.write(dataString.c_str(), dataString.length());
    }
    delay(1000);
}

void printWiFiStatus()
{
    IPAddress ip = WiFi.localIP();
}

void CheckGPS()
{
    int inByte;
    while (Serial1.available() > 0)
    {
        inByte = Serial1.read();
        if ((inByte == '$') || (GPSIndex >= 81))
        {
            GPSIndex = 0;
        }
        if (inByte != '\r')
        {
            GPSBuffer[GPSIndex++] = inByte;
        }
        if (inByte == '\n')
        {
            ProcessGPSLine();
            GPSIndex = 0;
        }
    }
}

void ProcessGPSLine()
{
    if ((GPSBuffer[1] == 'G') && (GPSBuffer[2] == 'N') && (GPSBuffer[3] == 'G') && (GPSBuffer[4] == 'G') && (GPSBuffer[5] == 'A'))
    {
        ProcessGNGGACommand();
    }
}

void ProcessGNGGACommand()
{
    server.write(GPSBuffer, GPSIndex);

    char *token = strtok(GPSBuffer, ",");
    int fieldIndex = 0;
    while (token != NULL)
    {
        // Update GPS data based on fieldIndex
        if (fieldIndex == 2) // Latitude
        {
            GPS_Latitude = atof(token);
        }
        else if (fieldIndex == 4) // Longitude
        {
            GPS_Longitude = atof(token);
        }
        else if (fieldIndex == 9) // Altitude
        {
            GPS_Altitude = atof(token);
        }

        token = strtok(NULL, ",");
        fieldIndex++;
    }
}
