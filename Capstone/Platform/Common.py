import io
import os
import re
import json

"""
Common Objects
"""


class Printable:
    def __repr__(self):
        from pprint import pformat
        # return "<" + type(self).__name__ + "> " + pformat(vars(self), indent=4, width=1)
        return str(self.__class__) + '\n' + '\n'.join(
            ('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))


class Common:

    def get_app_data_dir(self):
        return os.path.join(self.get_home_dir(), '.capstone_data')

    @staticmethod
    def write_to_file(filename, path, data):
        filename = os.path.join(path, filename)
        with io.open(filename, 'w', encoding='utf-8') as f:
            f.write(data)
            f.flush()
            f.close()

    @staticmethod
    def read_from_file(filename, path):
        filename = os.path.join(filename, path)
        with io.open(filename, 'r', encoding='utf-8') as f:
            data = f.readlines()
        return data

    @staticmethod
    def parse_oui_json(json_string):
        object_list = []
        json_objs = re.findall("({.*?})", json_string)
        for _object in json_objs:
            object_list.append(json.loads(_object))
        return object_list