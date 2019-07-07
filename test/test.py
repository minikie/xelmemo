class C(object):
    def __init__(self, keys, values):
        for (key, value) in zip(keys, values):
            self.__dict__[key] = value


keys = ['a','b']
values = [1,2]
c = C(keys, values)

print c.a