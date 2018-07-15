import collections

import EasyRule
from EasyRule import ItemRegistry, BusEvent


class FiFo(collections.Sequence):
    def __init__(self, item_name, len):
        assert isinstance(item_name, str), type(item_name)
        assert isinstance(len, int) and len > 0, '{} : {}'.format( type(len), len)

        self.__data = []
        self.__len = len
        self.__item_names = []

        for i in range(self.__len):
            self.__item_names.append('{:s}{:d}'.format(item_name, i))
            self.__data.append(None)

        #return this FiFo
        ItemRegistry.AddCustomItem(item_name, self)

        #if the items already exist
        if ItemRegistry.ItemExists(self.__item_names[0]):
            self.Initialize()

    @EasyRule.log_traceback
    def Initialize(self):

        for i, name in enumerate(self.__item_names):
            item = ItemRegistry.getItem(name, search_custom_items=False)
            if item.state is not None:
                self.__data[i] = item.state

    @EasyRule.log_traceback
    def push(self, value):
        """
        Pushes all values one step further and the inserts the value at first position
        :param value:
        :return:
        """

        #push everything one further
        for k in reversed(range(self.__len - 1)):
            self.__data[k+1] = self.__data[k]
        self.__data[0] = value

        #push to items
        for i in range(self.__len):
            if self.__data[i] is not None:
                BusEvent.postUpdate( self.__item_names[i], self.__data[i])


    def __getitem__(self, index):
        assert isinstance(index, int)
        return self.__data[index]

    def __setitem__(self, index, value):
        assert isinstance(index, int)
        self.__data[index] = value
        BusEvent.postUpdate(self.__item_names[index], value)

    def __iter__(self):
        for __item in self.__data:
            yield __item

    def __len__(self):
        return self.__len


    def __delitem__(self, key):
        raise NotImplementedError('Deleting an item makes no sense!')

    def insert(self, index, value):
        raise NotImplementedError('Inserting an item is not supported!')