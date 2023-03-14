
class User(dict):
    handle: str

    def __init__(self, handle):
        self.handle = handle
        dict.__init__(self, handle=handle)