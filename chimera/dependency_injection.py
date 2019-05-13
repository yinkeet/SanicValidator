import pkgutil

from sanic.log import logger


class Dependencies(object):
    __instance = None
    def __new__(cls):
        if Dependencies.__instance is None:
            Dependencies.__instance = object.__new__(cls)
            Dependencies.__components = {}
        return Dependencies.__instance

    def register_package(self, package):
        logger.debug('Register package \'' + package.__name__ + '\'')
        for importer, module_name, is_pkg in pkgutil.iter_modules(package.__path__, prefix=package.__name__ + "."):
            if not is_pkg:
                module = importer.find_module(module_name).load_module(module_name)
                for attr in dir(module):
                    instance = getattr(module, attr)
                    if(issubclass(type(instance), Register)):
                        logger.debug('Register component \'' + module.__name__ + '.' + attr + '\' as ' + instance.name)
                        if instance.register_return:
                            self.__components[instance.name] = instance.function()
                        else:
                            self.__components[instance.name] = instance.function

    def register_module(self, module):
        for attr in dir(module):
            instance = getattr(module, attr)
            if(issubclass(type(instance), Register)):
                logger.debug('Register component \'' + module.__name__ + '.' + attr + '\' as ' + instance.name)
                if instance.register_return:
                    self.__components[instance.name] = instance.function()
                else:
                    self.__components[instance.name] = instance.function

    def register(self, name, object):
        logger.debug('Register component ' + name)
        self.__components[name] = object

    def get_component(self, name):
        logger.debug('Get component \'' + name + '\'')
        return self.__components[name]

    def exists(self, name):
        return name in self.__components

class Register(object):
    def __init__(self, name, register_return=False):
        self.name = name
        self.register_return = register_return

    def __call__(self, function):
        self.function = function
        return self

def inject(function):
    def wrapper(*args, **kwargs):
        from inspect import signature
        for parameter in signature(function).parameters:
            if Dependencies().exists(parameter):
                kwargs[parameter] = Dependencies().get_component(parameter)

        return function(*args, **kwargs)

    return wrapper