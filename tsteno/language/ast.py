class Node:
    __slots__ = ('head', 'childrens')

    def __init__(self, head, *childrens):
        self.head = head
        self.childrens = childrens

    def __repr__(self):
        if len(self.childrens) > 0:
            extra = '[{}]'.format(",".join(map(str, self.childrens)))
        else:
            extra = ''

        return "{}{}".format(self.head, extra)


class IdentifierToken:
    __slots__ = ('val')

    def __init__(self, val):
        self.val = val

    def get_value(self):
        return self.val

    def __repr__(self):
        return "`{}`".format(self.val)
