from OHImports import ChangedEventTrigger
from EasyRule import Rule
from EasyRule import ir

@Rule
class FiFo:
    def __init__(self, *args):

        self.items_anz  = 0
        self.items_list = []

        _len = len(args)
        if _len == 2 and isinstance(args[0], str) and isinstance(args[1], int):
            for k in range(args[1]):
                self.items_list.append( args[0].format(k))
        else:
            for i in range(_len):
                assert isinstance(args[i], str), "Arguments of FiFo must be Itemname as string!"
                self.items_list.append(args[i])

        self.items_anz = len(self.items_list)
        self.name = "FiFo({:s},{:d})".format(self.items_list[0], self.items_anz)


    def getEventTrigger(self):
        return [ ChangedEventTrigger(self.items_list[0])]

    def execute(self, event):

        #wir benoetigen mindestens zwei Items fuer ein Fifo!
        if self.items_anz < 2:
            return None

        for k in reversed( range(2, self.items_anz)):
            src = self.items_list[k-1]
            dst = self.items_list[k]
            ir.getItem(dst).postUpdate(ir.getItem(src).state)

        ir.getItem(self.items_list[1]).postUpdate(event.oldState)


    def Initialize(self):
        if self.items_anz < 2:
            self.logger.error( "Not enough items for a Fifo! Minimum 2, given: {}!".format(self.items_anz))

        for k in range(self.items_anz):
            item = self.items_list[k]
            if not ir.ItemExists(item):
                self.logger.error( "Item '{}' does not exist!".format(item))
                continue

            #wenn moeglich initialisieren
            if ir.getItem(item).state is None:
                if ir.getItem(self.items_list[0]).state is not None:
                    ir.getItem(item).postUpdate(ir.getItem(self.items_list[0]).state)