import abc, inspect


class Subscribable(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(Subscribable, self).__init__()
        self.__notification_targets = []
        self.__class_functions = {}

    def _set_notification_target(self, _class, func):
        """
        Possibility to specify which functions a class should call

        :param _class: Class
        :param func: Function which instances of the class have to call
        :return: None
        """
        assert _class.__name__ not in self.__class_functions, 'Redefinition of notification target for {}'.format(_class.__name__)
        assert len(inspect.getargspec(func).args) == 2, 'Notification fcuntion takes exactly 2 parameters! Provided: {}'.format( inspect.getargspec(func).args)
        self.__class_functions[_class.__name__] = func

    def notify(self, value):
        """
        Notify all listeners
        """
        for target_func in self.__notification_targets:
            target_func(self, value)
        return 0

    @abc.abstractmethod
    def notification(self, obj, value):
        raise NotImplementedError('')


    def __add_notification_target(self, obj):
        assert isinstance(obj, Subscribable)

        #custom function
        name = self.__class__.__name__
        func = obj.__class_functions.get(name, obj.notification)

        if not func in self.__notification_targets:
            self.__notification_targets.append(func)

    def subscribe(self, obj):
        """
        Subscribe to the Target Changes
        :param obj: target
        """
        assert isinstance(obj, Subscribable)
        obj.__add_notification_target(self)