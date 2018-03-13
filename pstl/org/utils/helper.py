class Helper():
    """description of class"""

    @staticmethod
    def _merge_cls_attrs(cls, attrs = {}):
        """Given two dicts, merge them into a new dict as a shallow copy."""
        for k, v in attrs.items():
            setattr(cls, k, v)
        return cls

    @staticmethod
    def _bind_method(cls, func, method_name=None):
        """Adds func to class so it is an accessible method; use method_name to specify the name to be used for calling the method.
        The new method is accessible to any instance immediately."""
        func.im_class=cls
        func.im_func=func
        func.im_self=None
        if not method_name: method_name=func.__name__
        setattr(cls, method_name, func)
        return cls

    @staticmethod
    def _upper_first_letter(x):
        return x[0].upper() + x[1:]