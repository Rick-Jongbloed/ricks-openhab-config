import threading
from EasyRule import ItemRegistry, BusEvent

class Counter(object):
    def __init__(self, item_name, min = 0, max = None, start = None, postUpdate = True):
        """
        Thread-safe counter

        :param item_name: name of the item under which the counter will be found in item registry
        :param min: Maximum value of the counter
        :param max: Minimum value of the counter
        :param start: Start value of the counter, will be set when Initialize-Function is called (call manually!)
        :param postUpdate:  Update item with same name as counter with current value
        """
        self.item_name = item_name
        self.start = start
        self.min = min
        self.max = max
        self.val = 0
        self.__postUpdate = postUpdate
        self.__lock = threading.Lock()

        #return this counter instead of item
        ItemRegistry.AddCustomItem(item_name, self)

    def Initialize(self):

        _start = None
        #if start value not set try to get it from item registry
        if self.start is None:
            item = ItemRegistry.getItem(self.item_name, search_custom_items=False)
            if item.state is None:
                _start = 0
            else:
                assert isinstance(item.state, int), 'Item state has to be integer. Is: "{}"({})'.format(item.state, type(item.state))
                _start = item.state
        else:
            _start = self.start

        assert _start is not None
        self.__process(None, _start)
        return self.val

    def __process(self, add, set_to = None):
        if add is not None:
            assert isinstance(add, int), type(add)
        if set_to is not None:
            assert isinstance(set_to, int), type(set_to)

        try:
            self.__lock.acquire()

            if set_to is not None:
                self.val = set_to
            else:
                self.val += add

            #Check boundaries
            if self.min is not None:
                self.val = max( self.min, self.val)
            if self.max is not None:
                self.val = min( self.max, self.val)

            #Update item
            if self.__postUpdate:
                BusEvent.postUpdate(self.item_name, str(self.val))
        finally:
            self.__lock.release()

    def Increase(self, step = 1):
        assert step >= 0
        self.__process(step)
        return self.val

    def Decrease(self, step = 1):
        assert step >= 0
        self.__process(step * -1)
        return self.val