from copy import deepcopy
from typing import List, Any

from sendbee_api.fields import Field, ModelField, NumberField, TextField


class Model:
    """Abstract model class."""

    def __init__(self, item: Any):
        self.item = item
        self.attributes = {}

    def __getattr__(self, item):
        attr = self.attributes.get(item)
        if attr:
            return attr.value
        else:
            raise AttributeError(item)

    @classmethod
    def process(cls, data: list) -> List[object]:
        """Transform raw data into models."""

        model_list = []

        # iterate over formatted data from API call
        for item in data:

            # instantiate model with one row of data
            model_object = cls(item)

            # iterate over model properties
            for model_property in list(cls.__dict__):

                # invoke model property
                property_object = getattr(model_object,
                                          model_property)

                if isinstance(property_object, ModelField):

                    # recursion:
                    # if the instance of the field class is ModeClass
                    # run process on that model with only a portion of data
                    if isinstance(item[property_object.index], list):
                        models = property_object.model_cls.process(
                            item[property_object.index]
                        )
                    elif isinstance(item[property_object.index], dict):
                        models = property_object.model_cls.process(
                            [item[property_object.index]]
                        )[0]

                    setattr(model_object, model_property[1:], models)

                elif isinstance(property_object, Field):

                    # convert raw property data into corespondent
                    # data type defined by the Field class
                    property_object.convert_item(model_object)

                    # set model property value with formatted data
                    if property_object.value is None:
                        model_object.attributes[model_property[1:]] = None
                    else:
                        model_object.attributes[model_property[1:]] = \
                            deepcopy(property_object)

            model_list.append(model_object)

        return model_list


class Meta(Model):

    total = NumberField(index='total', desc="Total")
    items_to = NumberField(index='to', desc="Items To")
    items_from = NumberField(index='from', desc="Items From")
    per_page = NumberField(index='per_page', desc="Per Page")
    last_page = NumberField(index='last_page', desc="Last Page")
    current_page = NumberField(index='current_page', desc="Current Page")


class ServerMessage(Model):

    message = TextField(index='message', desc='Message from the server')
