import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import telnetlib
from django.conf import settings

HOST = settings.IP_ADDRESS

class YourConsumer(AsyncWebsocketConsumer):

    async def connect(self): # Websocket connection established
        await self.accept() # 'Accept' the WebSocket connection
        asyncio.create_task(self.send_continuous_data())

    async def send_continuous_data(self):
        while True:
            data = await self.get_data()
            print("Continuous Execution:", data)

            # if 'data' in data and data['data'] is not None:
            if 'data' in data: # Check data has the 'data' key

                gngga_values = data['data'].split(',')[1:]

                if len(gngga_values) >= 10:
                    latitude_str, longitude_str, altitude_str = gngga_values[1], gngga_values[3], gngga_values[8]

                    if latitude_str and longitude_str and altitude_str:
                        latitude, longitude, altitude = map(float, (latitude_str, longitude_str, altitude_str))

                        # Convert latitude to decimal degrees
                        latitude_degrees = int(latitude // 100) + (latitude % 100) / 60

                        # Convert longitude to decimal degrees, converting to west for Google Maps
                        longitude_degrees = -(int(longitude // 100) + (longitude % 100) / 60)

                        # Format the values
                        latitude_formatted = f"{latitude_degrees:.6f}"
                        longitude_formatted = f"{longitude_degrees:.6f}"
                        altitude_formatted = f"{float(altitude):.6f}"

                        await self.send(text_data=json.dumps({
                            'coordinates': f"Latitude: {latitude_formatted} degrees, Longitude: {longitude_formatted} degrees, Altitude: {altitude_formatted} meters",
                        }))

            await asyncio.sleep(1.1)

    # Obtain data from Telnet connection
    async def get_data(self):
        try:
            # Establish a Telnet connection to the specified host
            tn = telnetlib.Telnet(HOST)
            # Read data until a newline char or 1.1 seconds have passed
            database_result = await asyncio.to_thread(tn.read_until, b"\n", 1.1)
            # Return the data in a dictionary format
            return {"data": database_result.decode("utf-8")}
            
        except Exception as e:
            # Return error message in a dictionary format
            return {"error": str(e)}
