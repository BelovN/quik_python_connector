from collections.abc import MutableSequence


class TemplateList(MutableSequence):
    type_value: type

    def __len__(self) -> int:
        return len(self._items)

    def insert(self, index: int, value) -> None:
        if not isinstance(value, self.type_value):
            raise ValueError(f' value must be instance of {self.type_value} class. Not a ' + str(type(value)))
        self._items.insert(index, self.type_value)

    def copy(self):
        new_instance = self.__class__()
        new_instance._items = self._items
        return new_instance

    def __setitem__(self, index: int, value) -> None:
        if not isinstance(value, self.type_value):
            raise ValueError(f' value must be instance of {self.type_value} class. Not a ' + str(type(value)))
        self._items.__setitem__(index, value)

    def __getitem__(self, given):
        if isinstance(given, int):
            return self._items[given]
        elif isinstance(given, slice):
            sliced_items = self._items[given.start:given.stop:given.step]
            new_instance = self.copy()
            new_instance._items = sliced_items
            return new_instance
        else:
            return None

    def __delitem__(self, index: int) -> None:
        self._items.__delitem__(index)
