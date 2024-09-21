def enforce(obj, cls, debug=False):
    if not isinstance(obj, cls):
        if debug:
            print(f"Blocked: {obj}")
        raise TypeError(f"Expected type: <{cls.__name__}> but got <{type(obj).__name__}>")
    if debug:
        print(f"Passed: {obj}")


class Person():
    def __init__(self):
        self.name = "Person name"

person = Person()

enforce(person, int, debug=True)