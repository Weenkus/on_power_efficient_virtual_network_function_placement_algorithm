
class Assert(object):

    @staticmethod
    def is_instance(instance, instances_class):
        assert isinstance(instance, instances_class), '{0} should be an instance of class {1}'.format(
            instance.__name__, instances_class.__name__
        )
