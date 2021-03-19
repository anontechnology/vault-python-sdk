class VaultResponseException(Exception):

    def __init__(self, message, status):
        error_message = f'Error {status}: {message}'
        self.code = status
        Exception.__init__(self, error_message)

    def __str__(self):
        return repr(self.code)
