class MissingEventData(Exception):
    def __init__(self, message="Could not retrieve event data."):
        self.message = message
        super().__init__(self.message)


class InvalidEventUrl(Exception):
    def __init__(self, message="Url is not a valid event url."):
        self.message = message
        super().__init__(self.message)


class MissingEventFMID(Exception):
    def __init__(self, message=f"FMID could not be found."):
        self.message = message
        super().__init__(self.message)
