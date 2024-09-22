class ProtectedClass:
    def __setattr__(self, name, value):
        cls = type(self)
        if name.startswith("_"):
            super().__setattr__(name, value)
            return
        if isinstance(getattr(cls, name, None), property):
            super().__setattr__(name, value)
            return
        e = "%r object has no property %r"
        e %= (cls.__name__, name)
        raise AttributeError(e)
