from uuid import UUID


class DictMap(dict):
    def __init__(self, *args, **kwargs):
        super(DictMap, self).__init__(*args, **kwargs)
        # self.update(*args, **kwargs)
        for k, v in self.items():
            self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            value = DictMap(value)
        elif isinstance(value, str) or isinstance(value, bytes):
            pass
        elif hasattr(value, "__iter__"):
            value = [self.normalize_iterable(i) for i in value]
        super(DictMap, self).__setitem__(key, value)
        # print(f'setitem: [{key, value}]')

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(DictMap, self).__delitem__(key)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.update(d)

    def normalize_iterable(self, v):
        value = v
        if isinstance(v, dict):
            value = DictMap(v)
        elif isinstance(v, UUID):
            value = str(v)
        return value

    def exclude(self, keys):
        return {k: self[k] for k in self.keys() if k not in keys}

    def del_keys(self, keys):
        for k in keys:
            if k in self.keys():
                del self[k]

    def dig(self, *keys, **kwargs):
        item = self
        for key in keys:
            if isinstance(item, dict) and key in item:
                item = item[key]
            elif isinstance(item, (list, tuple)) and isinstance(key, int):
                item = item[key]
            else:
                if "fail" in kwargs and kwargs["fail"] is True:
                    if isinstance(item, dict):
                        raise KeyError
                    else:
                        raise IndexError
                else:
                    return None

        return item


def trim_object(item, max=512, exc_fields=None):
    if exc_fields is None:
        exc_fields = []
    if isinstance(item, str):
        return item[:max]
    elif isinstance(item, dict):
        return {
            k: v[:max] if isinstance(v, str) else str(v)
            for k, v in item.items()
            if k not in exc_fields
        }
    else:
        return item
