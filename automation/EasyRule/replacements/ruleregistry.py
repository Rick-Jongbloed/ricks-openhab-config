import EasyRule
rules = EasyRule.openhab.jsr223.scope.rules

class RuleRegistry(object):

    @staticmethod
    def setEnabled( rule_name, is_enabled):
        assert isinstance(rule_name, str),  type(rule_name)
        assert isinstance(is_enabled, bool),  type(is_enabled)

        rules.setEnabled(unicode(rule_name), is_enabled)

    @staticmethod
    def remove( rule_name):
        assert isinstance(rule_name, str), type(rule_name)
        rules.remove(unicode(rule_name))

    @staticmethod
    def getAll():
        return rules.getAll()