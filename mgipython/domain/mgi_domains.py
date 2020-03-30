from .base_serializer import Field, Serializer
import logging

logger = logging.getLogger("mgipython.domain")

class UserDomain(Serializer):
    __fields__ = [
      Field("_user_key"),
      Field("login"),
      Field("name"),
      Field("_usertype_key"),
      Field("_userstatus_key")
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

class MGIOrganism(Serializer):
    __fields__ = [
        Field("_organism_key"),
        Field("commonname"),
        Field("latinname"),
    ]
