class VaultResponseException(Exception):

    def __init__(self, message, status):
        self.message = f'Error {status}: {message}'
        self.code = status
        Exception.__init__(self, self.message)

    def __str__(self):
        return self.message
