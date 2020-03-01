class KasparovGet:
    """
    This object holds all the required data to handle a Kasparov GET request.
    """
    def __init__(self, url, parameters):
        self.url = url
        self.parameters = parameters

    def append_to_url(self, text_to_append):
        self.url = self.url + text_to_append


class KasparovPost:
    """
    This object holds all the required data to handle a Kasparov POST request.
    """
    def __init__(self, request_url, raw_transaction):
        self.url = request_url
        self.headers = {"content-type": "application/json"}
        self.payload = {"rawTransaction": raw_transaction}
