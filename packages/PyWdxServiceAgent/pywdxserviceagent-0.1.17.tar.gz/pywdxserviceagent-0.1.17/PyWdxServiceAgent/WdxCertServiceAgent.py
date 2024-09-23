import httpx
import json
import pandas as pd
import os

class WdxCertServiceAgent:

    def __init__(self,client_appid, userid, client_dns, service_appid, service_id):
        self.service_appid = service_appid;
        self.client_appid = client_appid;
        self.userid = userid;
        self.client_dns = client_dns;
        self.service_id = service_id;
        # .env 파일 로드(end point 주소를 가져오자!!)
        from dotenv import load_dotenv
        load_dotenv()

    def default(obj):
        print(obj)
        if obj is None:
            return
        return obj
    
    def GetJwtToken(self):

        endpoint_url = os.environ['WDX_JWTTOKEN_ENDPOINT']

        certService_endpoint = endpoint_url + '/GetSecurityKey'

        headers = {
            'Content-Type': 'application/json; charset=utf-8' ,
            'Accept':'appliction/json'
            }
        
        jwt_gen_request = { 
            "clientappid": self.client_appid,
            "userid": self.userid, 
            "clientdns": self.client_dns,
            "securitykey": "",
            "serviceid": self.service_id ,
            "appid": self.service_appid,
            }

        jwt_gen_request_json = json.dumps(jwt_gen_request, default=self.default)

        print(jwt_gen_request_json)

        resp = httpx.post(certService_endpoint, headers=headers, data=jwt_gen_request_json)

        print(f"http code => {resp.status_code}")

        json_string = resp.content.decode('utf-8')

        securityKey = json.loads(json_string)

        jwt_gen_request['securitykey'] = securityKey
        
        certService_endpoint = endpoint_url + '/GenerateToken'

        jwt_gen_request_json = json.dumps(jwt_gen_request, default=self.default)

        print(jwt_gen_request_json)

        resp = httpx.post(certService_endpoint, headers=headers, data=jwt_gen_request_json)

        print(f"http code => {resp.status_code}")

        data = resp.content.decode('utf-8').replace('"','')

        return data


