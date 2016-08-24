import re
import sys
from mgipython.error import DateFormatError
from dateutil import parser

class DateHelper():

    def validate_date(self, date):
        """
        This supports multiple formats
        """
        try:
            if ">=" in date:
                parser.parse(re.sub('>=', '', date).strip())
            elif "<=" in date:
                parser.parse(re.sub('<=', '', date).strip())
            elif "<" in date:
                parser.parse(re.sub('<', '', date).strip())
            elif ">" in date:
                parser.parse(re.sub('>', '', date).strip())
            elif ".." in date:
                [date1, date2] = date.split("..")
                parser.parse(date1.strip())
                parser.parse(date2.strip())
            else:
                parser.parse(date.strip())
        except:
            e = sys.exc_info()[0]
            raise DateFormatError("Invalid Date format: %s" % str(e))
