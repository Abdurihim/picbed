# -*- coding: utf-8 -*-
"""
    utils._compat
    ~~~~~~~~~~~~~

    A module providing tools for cross-version compatibility.

    :copyright: (c) 2019 by staugur.
    :license: BSD 3-Clause, see LICENSE for more details.
"""

from sys import version_info
from os import getenv

PY2 = version_info[0] == 2

if PY2:  # pragma: nocover

    def iteritems(d):
        return d.iteritems()

    def itervalues(d):
        return d.itervalues()

    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)
    from urllib import urlencode
    from urllib2 import Request, urlopen
    from urlparse import urlparse, urlsplit

else:  # pragma: nocover

    def iteritems(d):
        return iter(d.items())

    def itervalues(d):
        return iter(d.values())

    text_type = str
    string_types = (str,)
    integer_types = (int, )
    from urllib.parse import urlencode, urlparse, urlsplit
    from urllib.request import Request, urlopen


class Properties(object):

    def __init__(self, fileName, from_env=False):
        #: 读取配置文件
        self.fileName = fileName
        #: 使用get方法查询无果时，是否从环境变量读取
        self.from_env = from_env
        self.properties = {}
        self._getProperties()

    def __getDict(self, strName, dictName, value):

        if(strName.find('.') > 0):
            k = strName.split('.')[0]
            dictName.setdefault(k, {})
            return self.__getDict(strName[len(k)+1:], dictName[k], value)
        else:
            dictName[strName] = value
            return

    def _getProperties(self):
        try:
            pro_file = open(self.fileName, 'Ur')
            for line in pro_file.readlines():
                line = line.strip().replace('\n', '')
                if line.find("#") != -1:
                    line = line[0:line.find('#')]
                if line.find('=') > 0:
                    strs = line.split('=')
                    strs[1] = line[len(strs[0])+1:]
                    self.__getDict(
                        strs[0].strip(),
                        self.properties, strs[1].strip()
                    )
        except IOError:
            pass
        else:
            pro_file.close()
        return self.properties

    def get(self, k, default_value=None):
        if not self.properties:
            self._getProperties()
        v = self.properties.get(k)
        if self.from_env is True:
            if not v:
                v = getenv(k)
        return v or default_value
