class Task(object):

    """Documentation for class Task(object)."""

    def __init__(self, d):

        """__init__.

        Args:
            d (dict): dictionary with the attributes for self"""

        super(Task, self).__init__()
        self.__dict__ = d
