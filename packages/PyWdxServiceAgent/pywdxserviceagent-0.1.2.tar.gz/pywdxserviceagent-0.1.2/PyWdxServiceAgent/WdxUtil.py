import pandas as pd
import uuid
import hashlib

class WdxUtil:

    @staticmethod
    def ConvertToDataframe(rows):
        # Convert rows to DataFrame
        return pd.DataFrame(rows)


    @staticmethod
    def GetGuid():
        return str(uuid.uuid4())
    

    @staticmethod
    def MD5(input_string, encodingName="ascii"):
        encoded_string = input_string.encode(encodingName)

        md5_hash = hashlib.md5(encoded_string).hexdigest()

        return md5_hash