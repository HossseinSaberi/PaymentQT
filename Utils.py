import dotenv
import os
from jdatetime import datetime as jdatetime
from PyQt5.QtWidgets import QStyledItemDelegate
from datetime import datetime


class ReadEnvFile:

    def __init__(self, env_file='.env'):
        dotenv.load_dotenv(env_file)

    @staticmethod
    def get_env(key, default=None):
        return os.getenv(key, default)



class JDateUtils:
    month_translator = {
        'Farvardin': 'فروردین ماه',
        'Ordibehesht': 'اردیبهشت ماه',
        'Khordad': 'خرداد ماه',
        'Tir': 'تیر ماه',
        'Mordad': 'مرداد ماه',
        'Shahrivar': 'شهریور ماه',
        'Mehr': 'مهر ماه',
        'Aban': 'آبان ماه',
        'Azar': 'آذر ماه',
        'Dey': 'دی ماه',
        'Bahman': 'بهمن ماه',
        'Esfand': 'اسفند ماه'
    }
    def __init__(self):
        pass

    @staticmethod
    def convert_to_jalali(gregorian_date):
        jalali_date_obj = jdatetime.fromgregorian(datetime=gregorian_date)
        jalali_date_str = jalali_date_obj.strftime('%Y/%m/%d')
        return jalali_date_str

    @staticmethod
    def convert_to_gregorian(jalali_date_str):
        year, month, day = map(int, jalali_date_str.split('/'))
        jalali_date = jdatetime(year, month, day).date()
        gregorian_date = jalali_date.togregorian()
        return gregorian_date

    @staticmethod
    def get_jmonth_name(jalali_date_str):
        date = jdatetime.strptime(jalali_date_str, '%Y/%m/%d')
        month_name = date.strftime('%B')
        return JDateUtils.month_translator[month_name]


class CustomItemDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(size.height() + 8)  # Adding top and bottom margin
        return size