import pytz
from datetime import datetime

def now():
    korea = datetime.now(pytz.timezone('Asia/Seoul'))
    request_time = korea.strftime('%Y-%m-%d %H:%M:%S')
    return request_time 
