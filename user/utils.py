import os
from datetime import datetime


def upload_to(instance, filename):
    today_date = datetime.now().strftime('%d-%m-%Y')
    return os.path.join(today_date, filename)
