class ComponentAttribute:
    def __init__(self, name: str, attribute_type, default_value: str):
        self.__name = name
        self.__attribute_type = attribute_type
        self.__value = default_value

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__attribute_type

    def get_value(self):
        return self.__value

    def set_value(self, value: str):
        self.__value = value
