from datetime import datetime


base_classes = [int, str, float, bool, datetime]


class Model:
    def to_dict(self) -> dict:
        """Returns object attributes as a dictionary.

        Returns:
            dict: Dictionary of objects attributes.
        """

        return self.__dump_object(self)

    def __dump_object(self, object):
        to_return = {}
        for key, value in object.__dict__.items():
            to_return[key] = self.__get_value(value)
        return to_return

    def __get_value(self, object):
        object_type = type(object)
        if object_type in base_classes or object == None:
            # If simple object or None return its value.
            return object
        elif object_type == list or object_type == tuple:
            object_list = []
            # If a list or tuple we run this function for each item and return a list.
            for item in object:
                object_list.append(self.__dump_object(item))
            return object_list
        elif object_type == dict:
            object_dict = {}
            for key, value in object.items():
                object_dict[key] = self.__dump_object(value)
            return object_dict
        else:
            # If a custom object we start the process over
            return self.__dump_object(object)
