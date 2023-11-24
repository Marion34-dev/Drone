
#include <SPI.h>
#include <WiFi101.h>
#include <math.h>
#include "config.h"

int keyIndex = 0; // network key Index number (needed only for WEP)
int status = WL_IDLE_STATUS;

WiFiServer server(23);
bool alreadyConnected = false;

float GPS_Latitude = 0.0;
float GPS_Longitude = 0.0;
float GPS_Altitude = 0.0;

float prevLatitudeSeconds = 0.0;
float prevLongitudeSeconds = 0.0;
float prevAltitude = 0.0;

char GPSBuffer[82];
byte GPSIndex = 0;

void setup()
{
    Serial.begin(9600);
    while (!Serial)
    {
        // wait for serial port to connect
    }

    if (WiFi.status() == WL_NO_SHIELD)
    {
        Serial.println("WiFi shield not present");
        while (true)
            ;
    }

    while (status != WL_CONNECTED)
    {
        Serial.print("Attempting to connect to SSID: ");
        Serial.println(ssid);
        status = WiFi.begin(ssid, pass);
        delay(10000);
    }

    server.begin();
    printWiFiStatus();
}

void loop()
{
    WiFiClient client = server.available();

    // DUMMY DATA: server.write("GPS data 0.00 0.00\n");
    CheckGPS();
    float latitudeDifference = (GPS_Latitude * 3600) - prevLatitudeSeconds;
    float longitudeDifference = (GPS_Longitude * 3600) - prevLongitudeSeconds;
    float altitudeDifference = GPS_Altitude - prevAltitude;

    float distance = CalculateHaversineDistance(prevLatitudeSeconds, prevLongitudeSeconds, GPS_Latitude * 3600, GPS_Longitude * 3600);

    if (distance >= 100 || abs(altitudeDifference) >= 100)
    {
        GPS_Latitude = prevLatitudeSeconds / 3600;
        GPS_Longitude = prevLongitudeSeconds / 3600;
    }

    prevLatitudeSeconds = GPS_Latitude * 3600;
    prevLongitudeSeconds = GPS_Longitude * 3600;
    prevAltitude = GPS_Altitude;

    String dataString = "Latitude: " + String(GPS_Latitude, 6) +
                        " Longitude: " + String(GPS_Longitude, 6) +
                        " Altitude: " + String(GPS_Altitude, 6) + "\n";

    if (client)
    {
        if (!alreadyConnected)
        {
            client.flush();
            Serial.println("Connected via Telnet");
            client.println("Hello from Arduino!");
            alreadyConnected = true;
        }

        if (client.available() > 0)
        {
            // read the bytes incoming from the client:
            char thisChar = client.read();
            // echo the bytes back to the client:
            server.write(thisChar);
            // echo the bytes to the server as well:
            Serial.write(thisChar);
        }
        server.write(dataString.c_str(), dataString.length());
    }
    delay(1000);
}

void printWiFiStatus()
{
    //  Serial.print("SSID: ");
    //  Serial.println(WiFi.SSID());

    IPAddress ip = WiFi.localIP();
    Serial.print("IP Address: ");
    Serial.println(ip);
}

void CheckGPS()
{
    int inByte;
    while (Serial.available() > 0)
    {
        inByte = Serial.read();
        if ((inByte == '$') || (GPSIndex >= 80))
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
    char *token = strtok(GPSBuffer, ",");
    int fieldIndex = 0;
    while (token != NULL)
    {
        if (fieldIndex == 2)
        {
            float latitude = atof(token);
            char hemisphere = GPSBuffer[3];
            if (hemisphere == 'S')
            {
                latitude = -latitude;
            }
            GPS_Latitude = latitude / 100.0;
        }
        else if (fieldIndex == 4)
        {
            float longitude = atof(token);
            char hemisphere = GPSBuffer[5];
            if (hemisphere == 'W')
            {
                longitude = -longitude;
            }
            GPS_Longitude = longitude / 100.0;
        }
        else if (fieldIndex == 9)
        {
            float altitude = atoi(token);
            if (altitude >= 0)
            {
                GPS_Altitude = altitude;
            }
            else
            {
                altitude = GPS_Altitude;
            }
        }
        token = strtok(NULL, ",");
        fieldIndex++;
    }
}

float CalculateHaversineDistance(float lat1, float lon1, float lat2, float lon2)
{
    // Radius of the Earth in meters
    double earthRadius = 6371000.0;

    // Convert latitude and longitude from degrees to radians
    double lat1Rad = radians(lat1 / 3600);
    double lon1Rad = radians(lon1 / 3600);
    double lat2Rad = radians(lat2 / 3600);
    double lon2Rad = radians(lon2 / 3600);

    // Haversine formula
    double dlat = lat2Rad - lat1Rad;
    double dlon = lon2Rad - lon1Rad;
    double a = sin(dlat / 2) * sin(dlat / 2) + cos(lat1Rad) * cos(lat2Rad) * sin(dlon / 2) * sin(dlon / 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));
    double distance = earthRadius * c;

    return static_cast<float>(distance);
}
