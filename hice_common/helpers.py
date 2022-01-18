from datetime import datetime, date
from decimal import Decimal
from typing import Any, Union, Dict, List


def to_json_serializable(
        data: Any
) -> Union[Dict[str, Any], List[Dict[str, Any]], List[str], str]:
    if isinstance(data, (datetime, date)):
        return data.isoformat()
    elif isinstance(data, Decimal):
        return str(data)
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = to_json_serializable(data[i])
        return data
    elif isinstance(data, dict):
        for key in data:
            data[key] = to_json_serializable(data[key])
        return data
    return data
