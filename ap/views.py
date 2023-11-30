"""import asyncio
import telnetlib
from django.http import StreamingHttpResponse
from django.views import View

HOST =  "192.168.1.149" #UPDATE
# HACKSPACE "192.168.1.58"

class ReceiveDataView(View):
    async def get_data(self):
        try:
            tn = telnetlib.Telnet(HOST)
            database_result = await asyncio.to_thread(tn.read_until, b"\n", 1.1)
            tn.close()
            return {"data": database_result.decode("utf-8")}
        except Exception as e:
            return {"error": str(e)}
        
    
    async def continuous_execution(self):
        current_data = None
        
        while True:
            data = await self.get_data()
            print("Continuous Execution:", data)
            
            if 'data' in data and data['data'] is not None:
                # Only send the latest data
                if data['data'] != current_data:
                    current_data = data['data']

                #latitude, longitude, altitude = [f'{float(x):.6f}' for x in current_data.split(',')]
                    gngga_values = current_data.split(',')[1:]

                    if len(gngga_values) >= 10:
                    # Extract latitude, longitude, and altitude
                        latitude_str, longitude_str, altitude_str = gngga_values[1], gngga_values[3], gngga_values[8]

                            # Check if the strings are not empty before converting to float
                        if latitude_str and longitude_str and altitude_str:
                            latitude, longitude, altitude = tuple(f'{float(x):.6f}' for x in (latitude_str, longitude_str, altitude_str))

                            yield f"The drone's current location is:\t Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}\n\n"
                          
                 #   yield f"{current_data}\n\n"
            
            await asyncio.sleep(1.1)

    def get(self, request):
        response = StreamingHttpResponse(self.continuous_execution(), content_type="text/event-stream") 
        return response """

"""class LocationView(View):
    def get(self, request):
        lat = request.GET.get('latitude', 0.0)
        lng = request.GET.get('longitude', 0.0)

        # Return the values as JSON
        data = {'latitude': lat, 'longitude': lng}
        return render(request, 'map.html', {'latitude': lat, 'longitude': lng})
"""

from django.shortcuts import render
from django.views import View

class ReceiveDataView(View):
    template = 'index.html'

    def get(self, request):
        return render(request, self.template)


