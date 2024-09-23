from datetime import datetime
import pytz                                                                                                                                                                                 
def jigeum_seoul_time():
    time = datetime.now(pytz.timezone('Asia/Seoul'))
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    return formatted_time