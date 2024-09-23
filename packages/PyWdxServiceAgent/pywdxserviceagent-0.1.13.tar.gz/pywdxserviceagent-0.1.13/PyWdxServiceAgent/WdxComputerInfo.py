import socket
import uuid
import platform

class WdxComputerInfo:

    @staticmethod
    def GetComputerInfo():
        if WdxComputerInfo._isGetComputerInfo == False:
            WdxComputerInfo._computer_name = socket.gethostname()
            WdxComputerInfo._ip_address = socket.gethostbyname(WdxComputerInfo._computer_name)
            WdxComputerInfo._mac_address = ''.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                                for elements in range(0,8*6,8)][::-1]).upper()
            WdxComputerInfo._os_platform = platform.system()
            WdxComputerInfo._isGetComputerInfo = True

    _isGetComputerInfo = False
    _computer_name = ""
    _ip_address = ""
    _mac_address = ""
    _os_platform = ""

    @staticmethod
    def get_info():
        WdxComputerInfo.GetComputerInfo()
        return {
            "Computer Name": WdxComputerInfo.MachineName(),
            "IP Address": WdxComputerInfo.IPAddress(),
            "MAC Address": WdxComputerInfo.MACAddress(),
            "OS Platform": WdxComputerInfo.OSVersion()
        }
    
    @staticmethod
    def MachineName():
        WdxComputerInfo.GetComputerInfo()
        return WdxComputerInfo._computer_name

    @staticmethod
    def IPAddress():
        WdxComputerInfo.GetComputerInfo()
        return WdxComputerInfo._ip_address
    
    @staticmethod
    def MACAddress():
        WdxComputerInfo.GetComputerInfo()
        return WdxComputerInfo._mac_address

    @staticmethod
    def OSVersion():
        WdxComputerInfo.GetComputerInfo()
        return WdxComputerInfo._os_platform