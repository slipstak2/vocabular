import functools


def need_refresh(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.refresh()
        return result
    return inner

