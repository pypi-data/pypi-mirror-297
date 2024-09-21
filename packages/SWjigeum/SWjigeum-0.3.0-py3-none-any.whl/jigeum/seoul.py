from pytz import timezone
from datetime import datetime

def now():
    nt_time = datetime.now(timezone('Asia/Seoul'))
    t_time = nt_time.strftime('%Y-%m-%d %H:%M:%S')
    return t_time
