import re
from datetime import datetime, timedelta
from typing import Optional

def parse_time(time_str: str) -> Optional[timedelta]:
    """Парсит строки вида '10m', '2h', '1d' в объект timedelta"""
    match = re.match(r"^(\d+)([mhds])$", time_str.lower())
    if not match:
        return None
        
    value, unit = int(match.group(1)), match.group(2)
    
    if unit == "m":
        return timedelta(minutes=value)
    elif unit == "h":
        return timedelta(hours=value)
    elif unit == "d":
        return timedelta(days=value)
    elif unit == "s":
        return timedelta(seconds=value)
    return None
