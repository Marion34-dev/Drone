import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import telnetlib
HOST =  "192.168.1.149" #UPDATE


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
                        latitude, longitude, altitude = tuple(f'{float(x):.6f}' for x in (latitude_str, longitude_str, altitude_str))

                        await self.send(text_data=json.dumps({
                            'coordinates': f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}",
                        }))

            await asyncio.sleep(1.1)

    async def get_data(self):
        try:
            tn = telnetlib.Telnet(HOST)
            database_result = await asyncio.to_thread(tn.read_until, b"\n", 1.1)
            tn.close()
            return {"data": database_result.decode("utf-8")}
        except Exception as e:
            return {"error": str(e)}
