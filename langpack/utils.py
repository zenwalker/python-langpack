class safedict(dict):
    def __missing__(self, key):
        return '{' + key + '}'


def flatten_dict(data, result=None, prevpath=None):
    if result is None:
        result = {}

    if prevpath is None:
        prevpath = []

    for key, value in data.items():
        nextpath = prevpath.copy()
        nextpath.append(key)

        if isinstance(value, dict):
            flatten_dict(value, result, nextpath)
        else:
            result['.'.join(nextpath)] = value

    return result


def safe_format(source, **kwargs):
    return source.format_map(safedict(**kwargs))
