"""
vocabulary related domain objects
"""
from base_serializer import Field, Serializer
import logging

logger = logging.getLogger("mgipython.domain")


class VocTermChoice(Serializer):
    """
    Represents a choice in a vocabulary select list
    """    
    __fields__ = [
      Field("_term_key"),
      Field("term")
    ]
    
class VocTermChoiceList(Serializer):
    """
    Represents the full choice list for a vocabulary
    """
    __fields__ = [
      Field("choices", conversion_class=VocTermChoice)
    ]
    
    def __init__(self):
        super(VocTermChoiceList, self).__init__()
        self.choices = []
    
