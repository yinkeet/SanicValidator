import pkgutil

from functools import wraps
from inspect import signature

from sanic.log import logger

class Dependencies(object):
    def __init__(self, app, loop):
        self.app = app
        self.loop = loop
        self.__components = {}
        self.app.dependencies = self

    def register_package(self, package):
        logger.debug('Register package \'' + package.__name__ + '\'')
        for importer, module_name, is_pkg in pkgutil.iter_modules(package.__path__, prefix=package.__name__ + "."):
            if not is_pkg:
                module = importer.find_module(module_name).load_module(module_name)
                for attr in dir(module):
                    instance = getattr(module, attr)
                    if(issubclass(type(instance), Register)):
                        logger.debug('Register component \'' + module.__name__ + '.' + attr + '\' as ' + instance.name)
                        self._register(instance)

    def register_module(self, module):
        for attr in dir(module):
            instance = getattr(module, attr)
            if(issubclass(type(instance), Register)):
                logger.debug('Register component \'' + module.__name__ + '.' + attr + '\' as ' + instance.name)
                self._register(instance)

    def register(self, name, object):
        logger.debug('Register component ' + name)
        self.__components[name] = object

    def get_component(self, name):
        logger.debug('Get component \'' + name + '\'')
        return self.__components[name]

    def exists(self, name):
        return name in self.__components

    def _register(self, instance):
        parameters = signature(instance.function).parameters
        if 'app' in parameters and 'loop' in parameters:
            self.__components[instance.name] = instance.function(self.app, self.loop)
        elif 'app' in parameters:
            self.__components[instance.name] = instance.function(self.app)
        elif 'loop' in parameters:
            self.__components[instance.name] = instance.function(self.loop)
        else:
            self.__components[instance.name] = instance.function()

class Register(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, function):
        self.function = function
        return self

def inject(function):
    @wraps(function)    
    async def wrapper(request, *args, **kwargs):
        for parameter in signature(function).parameters:
            dependencies = request.app.dependencies
            if dependencies.exists(parameter):
                kwargs[parameter] = dependencies.get_component(parameter)

        return await function(request, *args, **kwargs)
    return wrapper