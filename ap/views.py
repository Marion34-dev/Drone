import asyncio
import telnetlib
import json
from django.http import JsonResponse, StreamingHttpResponse
from django.views import View
from django.shortcuts import render



HOST = "192.168.1.149"
""" 
class ReceiveDataView(View):
    async def get_data(self):
        loop = asyncio.get_event_loop()

        try:
            tn = telnetlib.Telnet(HOST)
            database_result = await loop.run_in_executor(None, tn.read_until, b"\n", 1.1)
            return {"data": database_result.decode("utf-8")}
        
        except Exception as e:
            return {"error": str(e)}

    async def get(self, request):
        data = await self.get_data()
        return JsonResponse(data)

 """
""" 
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
        while True:
            data = await self.get_data()
            print("Continuous Execution:", data)
            await asyncio.sleep(1)  # Adjust the sleep duration as needed

    async def get(self, request):
        # Start the continuous execution in the background
        asyncio.create_task(self.continuous_execution())

    
        data = await self.get_data()
        return JsonResponse(data) """

"""CURRENTLY STREAMS DATA"""
class ReceiveDataView(View):
    async def get_data(self):
        try:
            tn = telnetlib.Telnet(HOST)
            database_result = await asyncio.to_thread(tn.read_until, b"\n", 1.1)
            tn.close()
            return {"data": database_result.decode("utf-8")}
        except Exception as e:
            return {"error": str(e)}
        
# DISPLAYING OLD VALUES AND NEW VALUES IN BROWSER
    """ async def continuous_execution(self):
        while True:
            data = await self.get_data()
            print("Continuous Execution:", data)
            if 'data' in data and data['data']:
                yield f"{data['data']}\n\n"
            await asyncio.sleep(1)  """
    
    async def continuous_execution(self):
        current_data = None
        
        while True:
            data = await self.get_data()
            print("Continuous Execution:", data)
            
            if 'data' in data and data['data']:
                # Only send the latest data
                if data['data'] != current_data:
                    current_data = data['data']
                    yield f"{current_data}\n\n"
            
            await asyncio.sleep(1)

    def get(self, request):
        return StreamingHttpResponse(self.continuous_execution(), content_type="text/event-stream")
    

class LocationView(View):
    def get(self, request):
        lat = request.GET.get('latitude', 0.0)
        lng = request.GET.get('longitude', 0.0)

        # Return the values as JSON
        data = {'latitude': lat, 'longitude': lng}
        return render(request, 'map.html', {'latitude': lat, 'longitude': lng})
    