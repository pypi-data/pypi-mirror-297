class TransactionOption:
    TxLocal = "TxLocal"
    TxDist = "TxDist"
    TxNone = "TxNone"
    TxSerializable = "TxSerializable"

class ExecutionOption:
        ExecNone      = "None"
        '''
        요청이 ExecuteDataSet 메서드를 수행함
        '''
        ExecuteDataSet      = "ExecuteDataSet"
        '''
        요청이 ExecuteNonQuery 메서드를 수행함
        '''
        ExecuteNonQuery     = "ExecuteNonQuery"
        '''
        요청이 ExecuteScalar 메서드를 수행함
        '''
        ExecuteScalar       = "ExecuteScalar"

class QueryRequestFlags:
        FlagNone      = "None"
        '''
        진단 호출
        '''
        Diagnostics         = "Diagnostics",
        '''
        서버측 출력 메시지(오라클의 dbms_output 등) 반환하도록 요청
        '''
        DbmsOutput          = "DbmsOutput",
        '''
        서비스 측 로그 메시지를 반환하도록 요청
        '''
        ServiceLog          = "ServiceLog",

class QueryRequest:

    def __init__(self):
        self.mapperName = ""
        self.queryId = ""
        self.clientIP = ""
        self.clientMachineName = ""
        self.clientMAC = ""
        self.commandTimeout = 0
        self.transactionTimeout = 600
        self.transactionOption = TransactionOption.TxNone
        self.executionOption = ExecutionOption.ExecNone
        self.dbmsOutputOption = False
        self.serviceLogOption = False
        self.flags = QueryRequestFlags.FlagNone
        self.parameters = {}
        self.dataSet = None
        self.enableLog = True
        self.executeId = ""
    
    def to_dict(self):
        return {
            'mapperName': self.mapperName,
            'queryId': self.queryId,
            'clientIP': self.clientIP,
            'clientMachineName': self.clientMachineName,
            'clientMAC': self.clientMAC,
            'commandTimeout': self.commandTimeout,
            'transactionTimeout': self.transactionTimeout,
            'transactionOption': self.transactionOption,
            'executionOption': self.executionOption,
            'dbmsOutputOption': self.dbmsOutputOption,
            'serviceLogOption': self.serviceLogOption,
            'flags': self.flags,
            'parameters': self.parameters,
            'dataSet': self.dataSet,
            'enableLog': self.enableLog,
            'executeId': self.executeId
        }

class QueryRequestCollection():
    def __init__(self):
        self.mapperName = ""
        self.transactionOption = TransactionOption.TxNone
        self.transactionTimeout = 600
        self.serviceLogOption = False
        self.flags = QueryRequestFlags.FlagNone
        self.items = []
        self.enableLog = True
        self.executeId = ""

    def to_dict(self):
        return {
            'mapperName': self.mapperName,
            'transactionTimeout': self.transactionTimeout,
            'transactionOption': self.transactionOption,
            'serviceLogOption': self.serviceLogOption,
            'flags': self.flags,
            'items': self.items,
            'enableLog': self.enableLog,
            'executeId': self.executeId
        }