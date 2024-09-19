class QueryResponse:
    def __init__(self):
        self.success = None
        self.message = ""
        self.serverIP = ""
        self.affectedRows = None
        self.scalarValue = None
        self.dbmsOutput = ""
        self.serviceLog = ""
        self.flags = None
        self.parameters = None
        self.dataSet = None
        self.extraData = None

class QueryResponseCollection:
    def __init__(self):
        self.success = None
        self.serviceLog = ""
        self.flags = None
        self.items = []