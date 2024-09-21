##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.22.1+obcheckpoint(0.0.10);ob(v1)                              #
# Generated on 2024-09-20T18:51:04.539536                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.client.core
    import metaflow.parameters
    import metaflow.graph
    import metaflow.events
    import metaflow.exception
    import metaflow.decorators
    import datetime
    import metaflow.metaflow_current

JSONType: metaflow.parameters.JSONTypeClass

class Run(metaflow.client.core.MetaflowObject, metaclass=type):
    def steps(self, *tags: str) -> typing.Iterator[metaflow.client.core.Step]:
        """
        [Legacy function - do not use]
        
        Returns an iterator over all `Step` objects in the step. This is an alias
        to iterating the object itself, i.e.
        ```
        list(Run(...)) == list(Run(...).steps())
        ```
        
        Parameters
        ----------
        tags : str
            No op (legacy functionality)
        
        Yields
        ------
        Step
            `Step` objects in this run.
        """
        ...
    @property
    def code(self) -> typing.Optional[metaflow.client.core.MetaflowCode]:
        """
        Returns the MetaflowCode object for this run, if present.
        Code is packed if atleast one `Step` runs remotely, else None is returned.
        
        Returns
        -------
        MetaflowCode, optional
            Code package for this run
        """
        ...
    @property
    def data(self) -> typing.Optional[metaflow.client.core.MetaflowData]:
        """
        Returns a container of data artifacts produced by this run.
        
        You can access data produced by this run as follows:
        ```
        print(run.data.my_var)
        ```
        This is a shorthand for `run['end'].task.data`. If the 'end' step has not yet
        executed, returns None.
        
        Returns
        -------
        MetaflowData, optional
            Container of all artifacts produced by this task
        """
        ...
    @property
    def successful(self) -> bool:
        """
        Indicates whether or not the run completed successfully.
        
        A run is successful if its 'end' step is successful.
        
        Returns
        -------
        bool
            True if the run completed successfully and False otherwise
        """
        ...
    @property
    def finished(self) -> bool:
        """
        Indicates whether or not the run completed.
        
        A run completed if its 'end' step completed.
        
        Returns
        -------
        bool
            True if the run completed and False otherwise
        """
        ...
    @property
    def finished_at(self) -> typing.Optional[datetime.datetime]:
        """
        Returns the datetime object of when the run finished (successfully or not).
        
        The completion time of a run is the same as the completion time of its 'end' step.
        If the 'end' step has not completed, returns None.
        
        Returns
        -------
        datetime, optional
            Datetime of when the run finished
        """
        ...
    @property
    def end_task(self) -> typing.Optional[metaflow.client.core.Task]:
        """
        Returns the Task corresponding to the 'end' step.
        
        This returns None if the end step does not yet exist.
        
        Returns
        -------
        Task, optional
            The 'end' task
        """
        ...
    def add_tag(self, tag: str):
        """
        Add a tag to this `Run`.
        
        Note that if the tag is already a system tag, it is not added as a user tag,
        and no error is thrown.
        
        Parameters
        ----------
        tag : str
            Tag to add.
        """
        ...
    def add_tags(self, tags: typing.Iterable[str]):
        """
        Add one or more tags to this `Run`.
        
        Note that if any tag is already a system tag, it is not added as a user tag
        and no error is thrown.
        
        Parameters
        ----------
        tags : Iterable[str]
            Tags to add.
        """
        ...
    def remove_tag(self, tag: str):
        """
        Remove one tag from this `Run`.
        
        Removing a system tag is an error. Removing a non-existent
        user tag is a no-op.
        
        Parameters
        ----------
        tag : str
            Tag to remove.
        """
        ...
    def remove_tags(self, tags: typing.Iterable[str]):
        """
        Remove one or more tags to this `Run`.
        
        Removing a system tag will result in an error. Removing a non-existent
        user tag is a no-op.
        
        Parameters
        ----------
        tags : Iterable[str]
            Tags to remove.
        """
        ...
    def replace_tag(self, tag_to_remove: str, tag_to_add: str):
        """
        Remove a tag and add a tag atomically. Removal is done first.
        The rules for `Run.add_tag` and `Run.remove_tag` also apply here.
        
        Parameters
        ----------
        tag_to_remove : str
            Tag to remove.
        tag_to_add : str
            Tag to add.
        """
        ...
    def replace_tags(self, tags_to_remove: typing.Iterable[str], tags_to_add: typing.Iterable[str]):
        """
        Remove and add tags atomically; the removal is done first.
        The rules for `Run.add_tag` and `Run.remove_tag` also apply here.
        
        Parameters
        ----------
        tags_to_remove : Iterable[str]
            Tags to remove.
        tags_to_add : Iterable[str]
            Tags to add.
        """
        ...
    def __iter__(self) -> typing.Iterator[metaflow.client.core.Step]:
        """
        Iterate over all children Step of this Run
        
        Yields
        ------
        Step
            A Step in this Run
        """
        ...
    def __getitem__(self, name: str) -> metaflow.client.core.Step:
        """
        Returns the Step object with the step name 'name'
        
        Parameters
        ----------
        name : str
            Step name
        
        Returns
        -------
        Step
            Step for this step name in this Run
        
        Raises
        ------
        KeyError
            If the name does not identify a valid Step object
        """
        ...
    def __getstate__(self):
        ...
    def __setstate__(self, state):
        ...
    @property
    def trigger(self) -> typing.Optional[metaflow.events.Trigger]:
        """
        Returns a container of events that triggered this run.
        
        This returns None if the run was not triggered by any events.
        
        Returns
        -------
        Trigger, optional
            Container of triggering events
        """
        ...
    ...

current: metaflow.metaflow_current.Current

def get_metadata() -> str:
    """
    Returns the current Metadata provider.
    
    If this is not set explicitly using `metadata`, the default value is
    determined through the Metaflow configuration. You can use this call to
    check that your configuration is set up properly.
    
    If multiple configuration profiles are present, this call returns the one
    selected through the `METAFLOW_PROFILE` environment variable.
    
    Returns
    -------
    str
        Information about the Metadata provider currently selected. This information typically
        returns provider specific information (like URL for remote providers or local paths for
        local providers).
    """
    ...

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

class MetaflowInternalError(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowNotFound(metaflow.exception.MetaflowException, metaclass=type):
    ...

ARGO_WORKFLOWS_UI_URL: None

KUBERNETES_NAMESPACE: str

SERVICE_VERSION_CHECK: bool

UI_URL: None

def load_token(token_prefix):
    ...

def new_token(token_prefix, prev_token = None):
    ...

def store_token(token_prefix, token):
    ...

class EnvironmentDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    def runtime_step_cli(self, cli_args, retry_count, max_user_code_retries, ubf_context):
        ...
    ...

class KubernetesDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    def __init__(self, attributes = None, statically_defined = False):
        ...
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        ...
    def package_init(self, flow, step_name, environment):
        ...
    def runtime_init(self, flow, graph, package, run_id):
        ...
    def runtime_task_created(self, task_datastore, task_id, split_index, input_paths, is_cloned, ubf_context):
        ...
    def runtime_step_cli(self, cli_args, retry_count, max_user_code_retries, ubf_context):
        ...
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_retries, ubf_context, inputs):
        ...
    def task_finished(self, step_name, flow, graph, is_task_ok, retry_count, max_retries):
        ...
    ...

def validate_tags(tags, existing_tags = None):
    """
    Raises MetaflowTaggingError if invalid based on these rules:
    
    Tag set size is too large. But it's OK if tag set is not larger
    than an existing tag set (if provided).
    
    Then, we validate each tag.  See validate_tag()
    """
    ...

class ArgoWorkflows(object, metaclass=type):
    def __init__(self, name, graph: metaflow.graph.FlowGraph, flow, code_package_sha, code_package_url, production_token, metadata, flow_datastore, environment, event_logger, monitor, tags = None, namespace = None, username = None, max_workers = None, workflow_timeout = None, workflow_priority = None, auto_emit_argo_events = False, notify_on_error = False, notify_on_success = False, notify_slack_webhook_url = None, notify_pager_duty_integration_key = None, enable_heartbeat_daemon = True, enable_error_msg_capture = False):
        ...
    def __str__(self):
        ...
    def deploy(self):
        ...
    @staticmethod
    def list_templates(flow_name, all = False):
        ...
    @staticmethod
    def delete(name):
        ...
    @classmethod
    def terminate(cls, flow_name, name):
        ...
    @staticmethod
    def get_workflow_status(flow_name, name):
        ...
    @staticmethod
    def suspend(name):
        ...
    @staticmethod
    def unsuspend(name):
        ...
    @classmethod
    def trigger(cls, name, parameters = None):
        ...
    def schedule(self):
        ...
    def trigger_explanation(self):
        ...
    @classmethod
    def get_existing_deployment(cls, name):
        ...
    @classmethod
    def get_execution(cls, name):
        ...
    def list_to_prose(self, items, singular):
        ...
    ...

unsupported_decorators: dict

class IncorrectProductionToken(metaflow.exception.MetaflowException, metaclass=type):
    ...

class RunIdMismatch(metaflow.exception.MetaflowException, metaclass=type):
    ...

class IncorrectMetadataServiceVersion(metaflow.exception.MetaflowException, metaclass=type):
    ...

class ArgoWorkflowsNameTooLong(metaflow.exception.MetaflowException, metaclass=type):
    ...

class UnsupportedPythonVersion(metaflow.exception.MetaflowException, metaclass=type):
    ...

def check_python_version(obj):
    ...

def check_metadata_service_version(obj):
    ...

def resolve_workflow_name(obj, name):
    ...

def make_flow(obj, token, name, tags, namespace, max_workers, workflow_timeout, workflow_priority, auto_emit_argo_events, notify_on_error, notify_on_success, notify_slack_webhook_url, notify_pager_duty_integration_key, enable_heartbeat_daemon, enable_error_msg_capture):
    ...

def resolve_token(name, token_prefix, obj, authorize, given_token, generate_new_token, is_project):
    ...

def validate_token(name, token_prefix, authorize, instructions_fn = None):
    """
    Validate that the production token matches that of the deployed flow.
    In case both the user and token do not match, raises an error.
    Optionally outputs instructions on token usage via the provided instruction_fn(flow_name, prev_user)
    """
    ...

def get_run_object(pathspec: str):
    ...

def get_status_considering_run_object(status, run_obj):
    ...

def validate_run_id(workflow_name, token_prefix, authorize, run_id, instructions_fn = None):
    """
    Validates that a run_id adheres to the Argo Workflows naming rules, and
    that it belongs to the current flow (accounting for project branch as well).
    """
    ...

def sanitize_for_argo(text):
    """
    Sanitizes a string so it does not contain characters that are not permitted in Argo Workflow resource names.
    """
    ...

def remap_status(status):
    """
    Group similar Argo Workflow statuses together in order to have similar output to step functions statuses.
    """
    ...

