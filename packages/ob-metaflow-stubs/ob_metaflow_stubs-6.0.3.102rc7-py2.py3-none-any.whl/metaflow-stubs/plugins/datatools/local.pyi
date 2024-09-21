##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.22.1+obcheckpoint(0.0.10);ob(v1)                              #
# Generated on 2024-09-20T19:26:01.347152                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

DATATOOLS_LOCALROOT: None

DATATOOLS_SUFFIX: str

class MetaflowLocalURLException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowLocalNotFound(metaflow.exception.MetaflowException, metaclass=type):
    ...

class LocalObject(object, metaclass=type):
    def __init__(self, url, path):
        ...
    @property
    def exists(self):
        """
        Does this key correspond to an actual file?
        """
        ...
    @property
    def url(self):
        """
        Local location of the object; this is the path prefixed with local://
        """
        ...
    @property
    def path(self):
        """
        Path to the local file
        """
        ...
    @property
    def size(self):
        """
        Size of the local file (in bytes)
        
        Returns None if the key does not correspond to an actual object
        """
        ...
    ...

class Local(object, metaclass=type):
    @classmethod
    def get_root_from_config(cls, echo, create_on_absent = True):
        ...
    def __init__(self):
        """
        Initialize a new context for Local file operations. This object is based used as
        a context manager for a with statement.
        """
        ...
    def __enter__(self):
        ...
    def __exit__(self, *args):
        ...
    def get(self, key = None, return_missing = False):
        ...
    def put(self, key, obj, overwrite = True):
        ...
    def info(self, key = None, return_missing = False):
        ...
    ...

