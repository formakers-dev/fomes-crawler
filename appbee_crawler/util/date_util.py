import re
class DateUtil(object):

    @staticmethod
    def get_date_format(date):
        pattern = '(\d+)년[ ]*(\d+)월[ ]*(\d+)일'
        r = re.compile(pattern)
        match = r.search(date)
        return match.group(1) + match.group(2).zfill(2) + match.group(3).zfill(2)