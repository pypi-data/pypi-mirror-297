class QueryParameterCollection(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arrayBindCount(0)
        self.txCode([])
        self.txMessage("")
        self.fetchRowCount(0)
        self.txIsRollback(False)
        self.associativeArraySize(0)

    def arrayBindCount(self,count):
        self['$arrayBindCount'] = count

    def txCode(self,code):
        self['$txCode'] = code
        
    def txMessage(self,msg):
        self['$txMessage'] = msg
        
    def fetchRowCount(self,msg):
        self['$fetchRowCount'] = msg
        
    def txIsRollback(self,isRollback):
        self['$txIsRollback'] = isRollback
        
    def associativeArraySize(self,size):
        self['$associativeArraySize'] = size
