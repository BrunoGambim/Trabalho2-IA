class HashTable(object):
    def __init__(self):
        self.table = {}

    def insert(self, item_id, item):
        key = hash(item_id)
        if self.table.get(key) == None:
            self.table[key] = [(item_id, item)]
        else:
            self.table[key].append((item_id, item))

    def get(self, item_id):
        key = hash(item_id)

        for tp in self.table[key]:
            if tp[0] == item_id:
                return tp[1]