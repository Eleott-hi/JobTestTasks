class TreeStore:
    def __init__(self, items):
        self.items = items
        self.item_map = {item["id"]: item for item in items}
        self.children_map = {}

        for item in items:
            parent = item["parent"]
            if parent not in self.children_map:
                self.children_map[parent] = []
            self.children_map[parent].append(item)

    def getAll(self):
        return self.items

    def getItem(self, id):
        return self.item_map.get(id)

    def getChildren(self, id):
        return self.children_map.get(id, [])

    def getAllParents(self, id):
        parents = []
        current = self.item_map.get(id)
        while current and current["parent"] != "root":
            parent_id = current["parent"]
            parent = self.item_map.get(parent_id)
            if parent:
                parents.append(parent)
            current = parent
        if current and current["parent"] == "root":
            parents.append(current)
        return parents


items = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None},
]

ts = TreeStore(items)

print(ts.getAll())
print(ts.getItem(7))
print(ts.getChildren(4))
print(ts.getChildren(5))
print(ts.getAllParents(7))
