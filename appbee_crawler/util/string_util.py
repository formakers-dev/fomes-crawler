import re

class StringUtil(object):

    @staticmethod
    def parseNumber(string):
        pattern = r'[ ,\t\n\r]'
        str = re.sub(pattern, '', string)
        return int(str)