import httpx
import json

from PyWdxServiceAgent.QueryResponse import QueryResponse
from PyWdxServiceAgent.WdxComputerInfo import WdxComputerInfo

class QueryServiceAgent:

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

        queryService_endpoint = self.endpoint_url + '/rest/queryservice'

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

        if type(request).__name__ == "QueryRequest":
            request.clientIP = WdxComputerInfo.IPAddress() if request.clientIP == "" else request.clientIP
            request.clientMachineName = WdxComputerInfo.MachineName() if request.clientMachineName == "" else request.clientMachineName
            request.clientMAC = WdxComputerInfo.MACAddress() if request.clientMAC == "" else request.clientMAC
        elif type(request).__name__ == "list":
            for req in request:
                req.clientIP = WdxComputerInfo.IPAddress() if req.clientIP == "" else req.clientIP
                req.clientMachineName = WdxComputerInfo.MachineName() if req.clientMachineName == "" else req.clientMachineName
                req.clientMAC = WdxComputerInfo.MACAddress() if req.clientMAC == "" else req.clientMAC

        if type(request).__name__ == "QueryRequest":
            query_request_json = json.dumps(request.to_dict(), default=self.default)
        else:
            query_request_json = json.dumps(request, default=self.default)

        print(query_request_json)

        resp = httpx.post(queryService_endpoint + "/" + operation, headers=headers, data=query_request_json)
        print(f"http code => {resp.status_code}")

        json_string = resp.content.decode('utf-8')
        print(f"http response=====\n{json_string}")

        data = json.loads(json_string)
        
        response = QueryResponse()
        response.success = data.get('success')
        response.message = data.get('message')
        response.serverIP = data.get('serverIP')
        response.affectedRows = data.get('affectedRows')
        response.scalarValue = data.get('scalarValue')
        response.dbmsOutput = data.get('dbmsOutput')
        response.serviceLog = data.get('serviceLog')
        response.flags = data.get('flags')
        response.parameters = data.get('parameters')
        response.dataSet = data.get('dataSet')
        response.extraData = data.get('extraData')

        return response


    def ExecuteDataset(self, request):
        return self._ExecuteCore(request=request, operation="Executedataset")


    def ExecuteNonquery(self, request):
        return self._ExecuteCore(request=request, operation="Executenonquery")

    def ExecuteScalar(self, request):
        return self._ExecuteCore(request=request, operation="Executescalar")

    def SaveDataTable(self, request):
        return self._ExecuteCore(request=request, operation="SaveDataTable")

    def ExecuteMultipleEach(self, requests):
        return self._ExecuteCore(request=requests, operation="ExecuteMultipleEach")

    def ExecuteFetchDataSet(self, requests):
        return self._ExecuteCore(request=requests, operation="ExecuteFetchDataSet")

    def ExecuteMultipleEachMapper(self, requests):
        return self._ExecuteCore(request=requests, operation="ExecuteMultipleEach")

