import pickle
from base64 import b64encode, b64decode

class Serializer:
    @staticmethod
    def serialize(obj):
        return b64encode(pickle.dumps(obj)).decode('utf-8')
    
    @staticmethod
    def deserialize(obj):
        return pickle.loads(b64decode(obj.encode('utf-8')))