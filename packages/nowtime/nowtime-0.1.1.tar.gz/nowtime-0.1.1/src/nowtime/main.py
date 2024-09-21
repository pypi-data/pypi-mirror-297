import pytz
from datetime import datetime

def now():
    now_time = datetime.now(pytz.tmezone("Asia/Seoul")
    return now_time
