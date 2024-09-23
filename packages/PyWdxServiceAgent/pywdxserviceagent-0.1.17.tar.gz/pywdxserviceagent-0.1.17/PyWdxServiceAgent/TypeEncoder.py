import json

class TypeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, int):
            return {"type": "int", "value": obj}
        elif isinstance(obj, float):
            return {"type": "float", "value": obj}
        elif isinstance(obj, str):
            return {"type": "str", "value": obj}
        elif isinstance(obj, bool):
            return {"type": "bool", "value": obj}
        elif obj is None:
            return {"type": "null", "value": None}
        else:
            # 기본적으로 처리할 수 없는 타입은 super로 처리
            return super().default(obj)