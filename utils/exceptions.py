
class OutOfCapacityException(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(OutOfCapacityException, self).__init__(message)

        # Now for your custom code...
        self.errors = 'Out of capacity on this edge.'
