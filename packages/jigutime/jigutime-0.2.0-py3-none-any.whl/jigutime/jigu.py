import pytz
from datetime import datetime
from pytz import timezone

def now():
    korea = datetime.now(pytz.timezone('Asia/Seoul'))
    jigu_time = korea.strftime('%Y-%m-%d %H:%M:%S')

    return jigu_time

now()
