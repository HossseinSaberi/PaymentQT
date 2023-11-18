import dotenv
import os
from jdatetime import datetime as jdatetime
from datetime import datetime


class ReadEnvFile:

    def __init__(self, env_file='.env'):
        dotenv.load_dotenv(env_file)

    @staticmethod
    def get_env(key, default=None):
        return os.getenv(key, default)



class JDateUtils:
    def __init__(self):
        pass

    @staticmethod
    def convert_to_jalali(gregorian_date):
        jalali_date_obj = jdatetime.fromgregorian(datetime=gregorian_date)
        jalali_date_str = jalali_date_obj.strftime('%Y/%m/%d')
        return jalali_date_str
