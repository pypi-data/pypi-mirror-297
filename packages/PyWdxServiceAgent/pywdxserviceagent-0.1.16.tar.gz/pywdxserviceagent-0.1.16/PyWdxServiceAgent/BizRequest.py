class BizRequestFlags:
    _None = "None"
    Diagnostics = "Diagnostics"
    ServiceLog = "ServiceLog"


class BizRequest:

    def __init__(self):
        self.classId = ""
        self.methodId = ""
        self.clientIP = ""
        self.clientMachineName = ""
        self.clientMAC = ""
        self.serviceLogOption = False
        self.flags = BizRequestFlags._None
        self.parameters = {}
        self.enableLog = True
        self.executeId = ""
    
    def to_dict(self):
        return {
            'classId': self.classId,
            'methodId': self.methodId,
            'clientIP': self.clientIP,
            'clientMachineName': self.clientMachineName,
            'clientMAC': self.clientMAC,
            'serviceLogOption': self.serviceLogOption,
            'flags': self.flags,
            'parameters': self.parameters,
            'enableLog': self.enableLog,
            'executeId': self.executeId
        }

class BizRequestCollection():

    def __init__(self):
        self.serviceLogOption = False
        self.flags = BizRequestFlags._None
        self.items = []
        self.enableLog = True
        self.executeId = ""
        
    def to_dict(self):
        return {
            'serviceLogOption': self.serviceLogOption,
            'flags': self.flags,
            'items': [request.to_dict() for request in self.items],
            'enableLog': self.enableLog,
            'executeId': self.executeId
        }