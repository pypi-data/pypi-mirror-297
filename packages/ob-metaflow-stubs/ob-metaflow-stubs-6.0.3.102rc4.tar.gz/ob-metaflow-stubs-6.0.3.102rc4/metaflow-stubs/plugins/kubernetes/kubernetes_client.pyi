##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.22.1+obcheckpoint(0.0.10);ob(v1)                              #
# Generated on 2024-09-20T19:06:14.548322                                        #
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

KUBERNETES_NAMESPACE: str

CLIENT_REFRESH_INTERVAL_SECONDS: int

class KubernetesClientException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class KubernetesClient(object, metaclass=type):
    def __init__(self):
        ...
    def get(self):
        ...
    def list(self, flow_name, run_id, user):
        ...
    def kill_pods(self, flow_name, run_id, user, echo):
        ...
    def job(self, **kwargs):
        ...
    def jobset(self, **kwargs):
        ...
    ...

