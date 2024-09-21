##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.22.1+ob(v1)                                                   #
# Generated on 2024-09-20T00:12:02.912930                                        #
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

class MetaflowGSPackageError(metaflow.exception.MetaflowException, metaclass=type):
    ...

