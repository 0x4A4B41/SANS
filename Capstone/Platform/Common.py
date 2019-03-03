"""
Common Objects
"""


class Printable:
    def __repr__(self):
        from pprint import pformat
        # return "<" + type(self).__name__ + "> " + pformat(vars(self), indent=4, width=1)
        return str(self.__class__) + '\n' + '\n'.join(
            ('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))
