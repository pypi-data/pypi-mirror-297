##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.22.1+obcheckpoint(0.0.10);ob(v1)                              #
# Generated on 2024-09-20T19:15:33.538406                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

class PyPIStepDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    def __init__(self, attributes = None, statically_defined = False):
        ...
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        ...
    def is_attribute_user_defined(self, name):
        ...
    ...

class PyPIFlowDecorator(metaflow.decorators.FlowDecorator, metaclass=type):
    def __init__(self, attributes = None, statically_defined = False):
        ...
    def flow_init(self, flow, graph, environment, flow_datastore, metadata, logger, echo, options):
        ...
    ...

