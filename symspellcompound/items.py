from copy import copy


class SuggestItem(object):
    def __init__(self, term="", distance = 0, count = 0):
        self.term = term
        self.distance = distance
        self.count = count

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(self, other.__class__):
            return self.term == other.term
        return False

    def __str__(self):
        return self.term + ":" + str(self.count) + ":" + str(self.distance)

    def getCount(self):
        return self.count

    def get_hash_code(self):
        return hash(self.term)

    def shallow_copy(self):
        return copy(self)

class DictionaryItem:
    def __init__(self):
        self.suggestions = []
        self.count = 0

