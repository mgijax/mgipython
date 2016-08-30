import re
import sys
from sqlalchemy import Date, cast
from mgipython.error import DateFormatError
from dateutil import parser


#--  >  09/09/1995
#--  <  09/09/1995
#--  >= 09/09/1995
#--  <= 09/09/1995
#--  07/01/2005..07/06/2005 (between)  
#--  07/01/2005 (=)
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

    def build_query_with_date(self, query, field, date):
        if ">=" in date:
            query = query.filter(cast(field, Date) >= re.sub('>=', '', date).strip())
        elif "<=" in date:
            query = query.filter(cast(field, Date) <= re.sub('<=', '', date).strip())
        elif "<" in date:
            query = query.filter(cast(field, Date) < re.sub('<', '', date).strip())
        elif ">" in date:
            query = query.filter(cast(field, Date) > re.sub('>', '', date).strip())
        elif ".." in date:
            [date1, date2] = date.split("..")
            query = query.filter(field.between(date1.strip(), date2.strip()))
        else:
            query = query.filter(cast(field, Date) == date)

        return query
 
