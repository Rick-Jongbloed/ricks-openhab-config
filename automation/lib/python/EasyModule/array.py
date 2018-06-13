import collections
from EasyRule import ItemRegistry, BusEvent

class Array(collections.Sequence):
    def __init__(self, item_name, len):
        assert isinstance(item_name, str), type(item_name)
        assert isinstance(len, int) and len > 0, '{} : {}'.format( type(len), len)

        self.__len = len
        self.__item_names = []

        _name = item_name + '{:d}'

        for i in range(self.__len):
            self.__item_names.append(_name.format(i))

        #return this counter instead of item
        ItemRegistry.AddCustomItem(item_name, self)


    def __getitem__(self, index):
        assert isinstance(index, int)
        return ItemRegistry.getItem(self.__item_names[index]).state

    def __setitem__(self, index, value):
        assert isinstance(index, int)
        BusEvent.postUpdate(self.__item_names[index], value)

    def __iter__(self):
        for __item in self.__item_names:
            yield ItemRegistry.getItem(__item).state

    def __len__(self):
        return self.__len


    def __delitem__(self, key):
        raise NotImplementedError('Deleting an item makes no sense!')

    def insert(self, index, value):
        raise NotImplementedError('Inserting an item is not supported!')