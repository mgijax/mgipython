class Field():
    """
    Serializeable Field
    
    Used to wrap field configuration for a Serializer implementing class
    
    e.g. __fields__ = [Field("col1"), Field("col2"), ... ]
    """

    def __init__(self, 
            field_name,
            conversion_class=None):

        self.field_name = field_name
        self.conversion_class = conversion_class


class Serializer():
    """
    A base class for creating serializable domain objects.
    
    They can be easily created from database models,
    and also input/output dictionaries for JSON serialization.
    
    e.g.
    class MarkerDomain(Serializer):
      __fields__ = [
        Field('_marker_key'),
        Field('symbol')
      ]
      
    Can be used as:
    d_marker = MarkerDomain()
    d_marker.load_from_model( sql_alchemy_marker_object )
    
    # these values will automatically be set
        d_marker._marker_key, d_marker.symbol
        
    Dictionary is created by calling serialize()
    d_marker.serialize()
    { 
      _marker_key: 1,
      symbol: 'Kit'
    }
    
    To recreate the domain object call
    d_marker.load_from_dict( json_dict )
    """
    
    # primary configuration to be declared in sub-class
    #  is-a: list of Field objects
    __fields__ = []

    def __init__(self):

        self.create_fields_as_attributes(self.__fields__)


    def create_fields_as_attributes(self, fields):
        for field in fields:

            setattr(self, field.field_name, None)


    def load_from_model(self, model):
        """
        Load this serializeable object from a model object
        based on __fields__ configuration

        populates attributes
        """
        
        for field in self.__fields__:

            value = self.get_model_value(model, field)

            if value:
                setattr(self, field.field_name, value)


    def get_model_value(self, model, field):

        # first check if we defined a getter
        value = self.get_field_value_from_getter(model, field)

        # second check for value from model attribute
        if not value:
            value = self.get_field_value_from_attr(model, field)


        # third check if value needs to be converted to a conversion_class
        if value and field.conversion_class:
            value = self.convert_value_to_class(value, field.conversion_class)


        return value


    def get_field_value_from_getter(self, model, field):
        """
        Look for method with the format
        get_field_name

        These override the default behavior of loading from
            the model attribute

        returns None if there is none
        """

        getter_attr = "get_" + field.field_name
        value = None
        if hasattr(self, getter_attr):
            value = getattr(self, getter_attr)(model)
        return value

    def get_field_value_from_attr(self, model, field):
        value = None
        if hasattr(model, field.field_name):
            value = getattr(model, field.field_name)

        return value
    

    def convert_value_to_class(self, value, conversion_class):

        if isinstance(value, list):
            value = self.convert_nested_list(value, conversion_class)
        
        else:
            value = self.convert_nested_object(value, conversion_class)

        return value

    def convert_nested_object(self, model, conversion_class):
        converted = conversion_class()
        converted.load_from_model(model)
        return converted

    def convert_nested_list(self, models, conversion_class):
        converted_objects = []
        for model in models:
            converted_object = conversion_class()
            converted_object.load_from_model(model)
            converted_objects.append(converted_object)

        return converted_objects


    def load_from_dict(self, json_dict):
        """
        Load this object from a dictionary 

        populates attributes if they match __fields__ configuration
        """

        for field in self.__fields__:

            if field.field_name in json_dict:

                value = json_dict[field.field_name]

                if field.conversion_class:
                    # convert to conversion_class
                    if isinstance(value, list):
                        for i in range(len(value)):
                            obj = field.conversion_class()
                            obj.load_from_dict(value[i])
                            value[i] = obj

                    else:
                        obj = field.conversion_class()
                        obj.load_from_dict(value)
                        value = obj

                setattr(self, field.field_name, value)



    def serialize(self):
        """
        returns serialized dictionary
        """

        output = {}
        for field in self.__fields__:

            value = getattr(self, field.field_name)

            # handle nested Serializer
            if isinstance(value, Serializer):
                value = value.serialize()

            # handle list of Serializers
            elif isinstance(value, list):
                for i in range(len(value)):
                    nested_item = value[i]
                    if isinstance(nested_item, Serializer):
                        value[i] = nested_item.serialize()
                    

            output[field.field_name] = value

        return output
    
    
# helper methods 
def convert_models(model, domain_class):
    """
    converts model or list of models into the domain_class
    by using domain_class.load_from_model(model)
    """
    instance = domain_class()
    return instance.convert_value_to_class(model, domain_class)

