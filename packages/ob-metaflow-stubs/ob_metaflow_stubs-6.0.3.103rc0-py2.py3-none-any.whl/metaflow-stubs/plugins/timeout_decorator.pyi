##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.22.1+obcheckpoint(0.0.10);ob(v1)                              #
# Generated on 2024-09-20T18:44:03.677872                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow.decorators

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

UBF_CONTROL: str

DEFAULT_RUNTIME_LIMIT: int

class TimeoutException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class TimeoutDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    def __init__(self, *args, **kwargs):
        ...
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        ...
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_user_code_retries, ubf_context, inputs):
        ...
    def task_post_step(self, step_name, flow, graph, retry_count, max_user_code_retries):
        ...
    ...

def get_run_time_limit_for_task(step_decos):
    ...

