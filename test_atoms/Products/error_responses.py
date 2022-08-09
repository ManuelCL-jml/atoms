from dataclasses import dataclass, field
from typing import List, Dict, Any, ClassVar, Union

from rest_framework.status import HTTP_400_BAD_REQUEST


# Clase que estandariza una respuesta cuando ocurre un error
@dataclass
class MyHttpError:
    message: str
    real_error: Union[str, None]
    error_desc: Union[str, None] = None
    code: int = HTTP_400_BAD_REQUEST

    def detail(self) -> List[Dict]:
        return [
            {
                "field": None,
                "data": self.real_error,
                "message": self.message,
                "desc": self.error_desc
            }
        ]

    def standard_error_responses(self) -> Dict[str, Any]:
        return {
            "code": [self.code],
            "status": ["ERROR"],
            "detail": self.detail()
        }

    def object_does_not_exist(self) -> Dict[str, Any]:
        return self.standard_error_responses()

    def multi_value_dict_key_error(self) -> Dict[str, Any]:
        return self.standard_error_responses()