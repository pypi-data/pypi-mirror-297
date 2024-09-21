from datetime import datetime
import pytz

def now():
    k_time = datetime.now(pytz.timezone('Asia/Seoul'))
    t = k_time.strftime('%Y-%m-%d %H:%M:%S')

    return t
