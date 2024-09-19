class BizResponse:
    def __init__(self):
        self.success = None
        self.message = ""
        self.serverIP = ""
        self.diagnostics = False
        self.result = None
        self.serviceLog = ""
        self.flags = None
        self.parameters = None
        self.extraData = None


        
class BizResponseCollection:
    def __init__(self):
        self.success = None
        self.serviceLog = ""
        self.flags = None
        self.items = []