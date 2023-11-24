import asyncio
import telnetlib
from django.http import StreamingHttpResponse
from django.views import View

HOST = "192.168.1.149"

"""STREAMING DATA"""
class ReceiveDataView(View):
    async def get_data(self):
        try:
            tn = telnetlib.Telnet(HOST)
            database_result = await asyncio.to_thread(tn.read_until, b"\n", 1.1)
            tn.close()
            return {"data": database_result.decode("utf-8")}
        except Exception as e:
            return {"error": str(e)}
        
# DISPLAYING OLD VALUES AS WELL AS NEW VALUES IN BROWSER
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
    