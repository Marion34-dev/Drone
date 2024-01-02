#include <SPI.h>
#include <WiFi101.h>
#include <math.h>
#include <config.h>

int keyIndex = 0; // network key Index number (needed only for WEP)
int status = WL_IDLE_STATUS;

// WiFi server on port 23
WiFiServer server(23);
bool alreadyConnected = false;

float GPS_Latitude = 0.0;
float GPS_Longitude = 0.0;
float GPS_Altitude = 0.0;

// Buffer to store GPS data
char GPSBuffer[82];
byte GPSIndex = 0;

void setup()
{
   // Start serial communication with a GPS module
    Serial1.begin(9600);
    pinMode(GPSENABLE, OUTPUT);
    digitalWrite(GPSENABLE, HIGH);

    // Check if the WiFi shield is present
    if (WiFi.status() == WL_NO_SHIELD)
    {
        while (true)
            ;
    }

    // Connect to WiFi network
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
    // Check for a client connection
    WiFiClient client = server.available();

    CheckGPS();

    // String dataString = String(GPS_Latitude, 6) + "," + String(GPS_Longitude, 6) + "," + String(GPS_Altitude, 6) + "\n";

    if (client)
    {
        if (!alreadyConnected)
        {
            // Flush the client buffer if not already connected
            client.flush();
            alreadyConnected = true;
        }

        if (client.available() > 0)
        {
            // Read a character from the client and write it to the server
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
    // Process incoming GPS data
    int inByte;
    while (Serial1.available() > 0)
    {
        // Reset the GPS buffer index if the start of a new message is detected
        inByte = Serial1.read();
        if ((inByte == '$') || (GPSIndex >= 81))
        {
            GPSIndex = 0;
        }
        // Store the incoming character in the GPS buffer (except for carriage return)
        if (inByte != '\r')
        {
            GPSBuffer[GPSIndex++] = inByte;
        }
        // Trigger ProcessGPSLine when a newline character is received
        if (inByte == '\n')
        {
            ProcessGPSLine();
            GPSIndex = 0;
        }
    }
}

void ProcessGPSLine()
{
    // Check if the message is a GNGGA command
    if ((GPSBuffer[1] == 'G') && (GPSBuffer[2] == 'N') && (GPSBuffer[3] == 'G') && (GPSBuffer[4] == 'G') && (GPSBuffer[5] == 'A'))
    {
        ProcessGNGGACommand();
    }
}

void ProcessGNGGACommand()
{
    // Write the GPS data to the server
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
