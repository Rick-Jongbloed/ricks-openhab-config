from org.eclipse.smarthome.model.persistence.extensions import PersistenceExtensions as pe


class PersistenceExtensions(object):

    @staticmethod
    def persist( item, serviceName = None):
        return pe.persist(item, serviceName) if serviceName is not None else pe.persist(item)

    @staticmethod
    def previousState( item, skipEqual = False, serviceName = None):
        return pe.previousState(item, skipEqual, serviceName) if serviceName is not None else pe.previousState(item, skipEqual)

    @staticmethod
    def lastUpdate( item, serviceName = None):
        return pe.lastUpdate(item, serviceName) if serviceName is not None else pe.lastUpdate(item)


    #-------------------------------------------------------------------------------
    # Timestamp functions
    @staticmethod
    def averageSince( item, timestamp, serviceName = None):
        return pe.averageSince(item, timestamp, serviceName) if serviceName is not None else pe.averageSince(item, timestamp)

    @staticmethod
    def changedSince( item, timestamp, serviceName = None):
        return pe.changedSince(item, timestamp, serviceName) if serviceName is not None else pe.changedSince(item, timestamp)

    @staticmethod
    def deltaSince( item, timestamp, serviceName = None):
        return pe.deltaSince(item, timestamp, serviceName) if serviceName is not None else pe.deltaSince(item, timestamp)

    @staticmethod
    def evolutionRate( item, timestamp, serviceName = None):
        return pe.evolutionRate(item, timestamp, serviceName) if serviceName is not None else pe.evolutionRate(item, timestamp)

    @staticmethod
    def historicState( item, timestamp , serviceName = None):
        return pe.historicState(item, timestamp, serviceName) if serviceName is not None else pe.historicState(item, timestamp)

    @staticmethod
    def maximumSince( item, timestamp, serviceName = None):
        return pe.maximumSince(item, timestamp, serviceName) if serviceName is not None else pe.maximumSince(item, timestamp)

    @staticmethod
    def minimumSince( item, timestamp, serviceName = None):
        return pe.minimumSince(item, timestamp, serviceName) if serviceName is not None else pe.minimumSince(item, timestamp)

    @staticmethod
    def updatedSince( item, timestamp, serviceName = None):
        return pe.updatedSince(item, timestamp, serviceName) if serviceName is not None else pe.updatedSince(item, timestamp)