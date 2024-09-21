from datetime import datetime
import pytz

def now(time_format='%Y-%m-%d %H:%M:%S'):
    timezone = pytz.timezone('Asia/Seoul')
    korea_time = datetime.now(timezone)
    formatted_time = korea_time.strftime(time_format)
    return formatted_time
