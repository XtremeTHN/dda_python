#!/usr/bin/python3
import sys


class PyConfigError(Exception):
    pass


class pyconfig:
    def create_settings(file_name):
        open(file_name,'x').close()
        txt_object = open(file_name, 'a+')
        return txt_object

    def set_settings(text_object, dict_settings):
        try:
            for x in dict_settings:
                text_object.write(f"{x} = '{dict_settings[x]}'")
                text_object.write("""
""")
        except:
            log = sys.exc_info()
            raise PyConfigError(log[0])

    def get_text_object(file_name):
        text_object = open(file_name, 'a+')
        return text_object

    def close(text_object):
        text_object.close()
