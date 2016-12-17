class Point(object):
    def __init__(self, x, y, value='', modifiable=False):
        self._x = x
        self._y = y
        self._value = value if value.strip() else ''
        self._modifiable = modifiable

    # getters
    def get_x(self):
        return self._x
    def get_y(self):
        return self._y
    def get_value(self):
        return self._value
    def get_modifiable(self):
        return self._modifiable

    # setters
    def set_x(self, x):
        self._x = x
    def set_y(self, y):
        self._y = y
    def set_value(self, value):
        self._value = value
    def set_modifiable(self, modifiable):
        self._modifiable = modifiable

    def __repr__(self):
        return "{} {} = {}".format(self._x, self._y, self._value)

def main():
    p = Point(5, 6, 'X')
    print p

if __name__ == '__main__':
    main()
