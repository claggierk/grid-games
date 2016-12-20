class PointXY(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash("{}{}".format(self.x, self.y))

class Point(object):
    def __init__(self, row, column, value='', modifiable=False, group=None, visible=False):
        self._row = row
        self._column = column
        if value:
            self._value = value if value.strip() else ''
        else:
            self._value = value
        self._modifiable = modifiable
        self._group = group
        self._visible = visible

    # getters
    def get_row(self):
        return self._row
    def get_column(self):
        return self._column
    def get_value(self):
        return self._value
    def get_modifiable(self):
        return self._modifiable
    def get_group(self):
        return self._group
    def get_visible(self):
        return self._visible

    # setters
    def set_row(self, row):
        self._row = row
    def set_column(self, column):
        self._column = column
    def set_value(self, value):
        self._value = value
    def set_modifiable(self, modifiable):
        self._modifiable = modifiable
    def set_group(self, group):
        self._group = group
    def set_visible(self, visible):
        self._visible = visible

    def __repr__(self):
        return "{} {} = {}".format(self._row, self._column, self._value)

def main():
    p = Point(row=5, column=6, value='X')
    print p

if __name__ == '__main__':
    main()
