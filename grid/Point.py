class Point(object):
    def __init__(self, row, column, value='', modifiable=False):
        self._row = row
        self._column = column
        self._value = value if value.strip() else ''
        self._modifiable = modifiable

    # getters
    def get_row(self):
        return self._row
    def get_column(self):
        return self._column
    def get_value(self):
        return self._value
    def get_modifiable(self):
        return self._modifiable

    # setters
    def set_row(self, row):
        self._row = row
    def set_column(self, column):
        self._column = column
    def set_value(self, value):
        self._value = value
    def set_modifiable(self, modifiable):
        self._modifiable = modifiable

    def __repr__(self):
        return "{} {} = {}".format(self._row, self._column, self._value)

def main():
    p = Point(row=5, column=6, value='X')
    print p

if __name__ == '__main__':
    main()
