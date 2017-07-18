import re

class StringUtil(object):

    def getPureNumber(self, string):
        pattern = r'[ ,\t\n\r]'
        str = re.sub(pattern, '', string)
        return str