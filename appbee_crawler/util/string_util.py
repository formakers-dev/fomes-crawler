import re

import scrapy


class StringUtil(object):

    @staticmethod
    def parseNumber(string):
        pattern = r'[ ,\t\n\r]'
        str = re.sub(pattern, '', string)
        return int(str)

    @staticmethod
    def trim(obj):
        if type(obj) is str:
            trimmed_str = obj.strip(' \t\n\r\f\uFEFF')
            return trimmed_str

        elif type(obj) is list:
            trimmed_list = list()

            for item in obj:
                trimmed_list.append(StringUtil.trim(item))

            return trimmed_list

        elif type(obj) is dict or isinstance(obj, scrapy.Item):
            trimmed_dict = dict()

            for key in obj.keys():
                trimmed_dict[key] = StringUtil.trim(obj[key])

            return trimmed_dict
        else:
            print(str(obj) + ' cannot be stripped.')
            return obj
