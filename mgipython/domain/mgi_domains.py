from base_serializer import Field, Serializer
import logging

logger = logging.getLogger("mgipython.domain")

class UserDomain(Serializer):
    __fields__ = [
      Field("_user_key"),
      Field("login"),
      Field("name"),
    ]
class PropertyDomain(Serializer):
    __fields__ = [
      Field("_property_key"),
      Field("name"),
      Field("value"),
    ]

class NoteDomain(Serializer):
    __fields__ = [
      Field("_note_key"),
      Field("text"),
    ]
