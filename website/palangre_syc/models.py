from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, str):
            return str(obj)
        return super().default(obj)
    
    