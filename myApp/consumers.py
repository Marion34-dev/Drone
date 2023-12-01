import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import telnetlib
from django.conf import settings

HOST = settings.IP_ADDRESS

class YourConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

        while True:
            data = await self.get_data()
            print("Continuous Execution:", data)

            if 'data' in data and data['data'] is not None:
                gngga_values = data['data'].split(',')[1:]

                if len(gngga_values) >= 10:
                    latitude_str, longitude_str, altitude_str = gngga_values[1], gngga_values[3], gngga_values[8]

                    if latitude_str and longitude_str and altitude_str:
                        latitude, longitude, altitude = map(float, (latitude_str, longitude_str, altitude_str))

                        # Convert latitude to decimal degrees
                        latitude_degrees = int(latitude // 100) + (latitude % 100) / 60

                        # Convert longitude to decimal degrees, considering west
                        longitude_degrees = -(int(longitude // 100) + (longitude % 100) / 60)

                        # Format the values
                        latitude_formatted = f"{latitude_degrees:.6f}"
                        longitude_formatted = f"{longitude_degrees:.6f}"
                        altitude_formatted = f"{float(altitude):.6f}"

                        await self.send(text_data=json.dumps({
                            'coordinates': f"Latitude: {latitude_formatted} degrees, Longitude: {longitude_formatted} degrees, Altitude: {altitude_formatted} meters",
                        }))


                        """ latitude, longitude, altitude = tuple(f'{float(x):.6f}' for x in (latitude_str, longitude_str, altitude_str))

                        await self.send(text_data=json.dumps({
                            'coordinates': f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude} meters",
                        })) """

            await asyncio.sleep(1.1)

    async def get_data(self):
        try:
            tn = telnetlib.Telnet(HOST)
            database_result = await asyncio.to_thread(tn.read_until, b"\n", 1.1)
          #  tn.close()
            return {"data": database_result.decode("utf-8")}
        except Exception as e:
            return {"error": str(e)}
