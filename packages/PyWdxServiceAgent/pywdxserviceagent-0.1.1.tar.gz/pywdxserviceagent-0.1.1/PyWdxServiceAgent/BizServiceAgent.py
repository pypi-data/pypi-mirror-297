import httpx
import json

from BizResponse import BizResponse
from WdxComputerInfo import WdxComputerInfo

class BizServiceAgent:

    def __init__(self,useJwtToken = False,token=""):
        self.endpoint_url = ""
        self.useJwtToken = useJwtToken
        self.accessToken = "" if useJwtToken else token
        self.jwtToken = token if useJwtToken else ""

    def default(obj):
        print(obj)
        if obj is None:
            return
        return obj
    
    def _ExecuteCore(self, request, operation):

        bizService_endpoint = self.endpoint_url + '/rest/bizservice'

        if self.useJwtToken == False:
            headers = {
                'Content-Type': 'application/json; charset=utf-8' ,
                'Accept':'appliction/json',
                'HHIRest-Authenticate' : self.accessToken}
        else:
            headers = {
                'Content-Type': 'application/json; charset=utf-8' ,
                'Accept':'appliction/json',
                'Authorization' : "Bearer " + self.jwtToken}

        request.clientIP = WdxComputerInfo.IPAddress() if request.clientIP == "" else request.clientIP
        request.clientMachineName = WdxComputerInfo.MachineName() if request.clientMachineName == "" else request.clientMachineName
        request.clientMAC = WdxComputerInfo.MACAddress() if request.clientMAC == "" else request.clientMAC


        query_request_json = json.dumps(request.to_dict(), default=self.default)

        print(query_request_json)

        resp = httpx.post(bizService_endpoint + "/" + operation, headers=headers, data=query_request_json)
        print(f"http code => {resp.status_code}")

        json_string = resp.content.decode('utf-8')

        data = json.loads(json_string)
        
        response = BizResponse()
        response.success = data.get('success')
        response.message = data.get('message')
        response.serverIP = data.get('serverIP')
        response.diagnostics = data.get('diagnostics')
        response.result = data.get('result')
        response.serviceLog = data.get('serviceLog')
        response.flags = data.get('flags')
        response.parameters = data.get('parameters')
        response.extraData = data.get('extraData')

        return response


    def Execute(self, request):
        return self._ExecuteCore(request=request, operation="execute")


    def ExecuteMultiple(self, requests):
        return self._ExecuteCore(request=requests, operation="executeMultiple")