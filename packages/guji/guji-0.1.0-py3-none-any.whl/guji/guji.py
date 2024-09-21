import pytz
from datetime import datetime
from pytz import timezone

def now():
    korea = datetime.now(pytz.timezone('Asia/Seoul'))
    guji_time = korea.strftime('%Y-%m-%d %H:%M:%S')

    return guji_time

now()
