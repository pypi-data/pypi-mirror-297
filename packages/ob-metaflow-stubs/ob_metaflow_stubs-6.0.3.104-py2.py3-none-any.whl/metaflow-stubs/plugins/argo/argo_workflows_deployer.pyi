##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.22.1+obcheckpoint(0.0.11);ob(v1)                              #
# Generated on 2024-09-20T21:46:07.402561                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.graph
    import metaflow.runner.deployer
    import metaflow.runner.subprocess_manager

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

class DeployerImpl(object, metaclass=type):
    def __init__(self, flow_file: str, show_output: bool = True, profile: typing.Optional[str] = None, env: typing.Optional[typing.Dict] = None, cwd: typing.Optional[str] = None, file_read_timeout: int = 3600, **kwargs):
        ...
    def __enter__(self) -> metaflow.runner.deployer.DeployerImpl:
        ...
    def create(self, **kwargs) -> metaflow.runner.deployer.DeployedFlow:
        """
        Create a deployed flow using the deployer implementation.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments to pass to `create` corresponding to the
            command line arguments of `create`
        
        Returns
        -------
        DeployedFlow
            DeployedFlow object representing the deployed flow.
        
        Raises
        ------
        Exception
            If there is an error during deployment.
        """
        ...
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Cleanup resources on exit.
        """
        ...
    def cleanup(self):
        """
        Cleanup resources.
        """
        ...
    ...

class DeployedFlow(object, metaclass=type):
    def __init__(self, deployer: metaflow.runner.deployer.DeployerImpl):
        ...
    ...

class TriggeredRun(object, metaclass=type):
    def __init__(self, deployer: metaflow.runner.deployer.DeployerImpl, content: str):
        ...
    def wait_for_run(self, timeout = None):
        """
        Wait for the `run` property to become available.
        
        Parameters
        ----------
        timeout : int, optional
            Maximum time to wait for the `run` to become available, in seconds. If None, wait indefinitely.
        
        Raises
        ------
        TimeoutError
            If the `run` is not available within the specified timeout.
        """
        ...
    @property
    def run(self):
        """
        Retrieve the `Run` object for the triggered run.
        
        Note that Metaflow `Run` becomes available only when the `start` task
        has started executing.
        
        Returns
        -------
        Run, optional
            Metaflow Run object if the `start` step has started executing, otherwise None.
        """
        ...
    ...

def get_lower_level_group(api, top_level_kwargs: typing.Dict, _type: typing.Optional[str], deployer_kwargs: typing.Dict):
    """
    Retrieve a lower-level group from the API based on the type and provided arguments.
    
    Parameters
    ----------
    api : MetaflowAPI
        Metaflow API instance.
    top_level_kwargs : Dict
        Top-level keyword arguments to pass to the API.
    _type : str
        Type of the deployer implementation to target.
    deployer_kwargs : Dict
        Keyword arguments specific to the deployer.
    
    Returns
    -------
    Any
        The lower-level group object retrieved from the API.
    
    Raises
    ------
    ValueError
        If the `_type` is None.
    """
    ...

def handle_timeout(tfp_runner_attribute, command_obj: metaflow.runner.subprocess_manager.CommandManager, file_read_timeout: int):
    """
    Handle the timeout for a running subprocess command that reads a file
    and raises an error with appropriate logs if a TimeoutError occurs.
    
    Parameters
    ----------
    tfp_runner_attribute : NamedTemporaryFile
        Temporary file that stores runner attribute data.
    command_obj : CommandManager
        Command manager object that encapsulates the running command details.
    file_read_timeout : int
        Timeout for reading the file.
    
    Returns
    -------
    str
        Content read from the temporary file.
    
    Raises
    ------
    RuntimeError
        If a TimeoutError occurs, it raises a RuntimeError with the command's
        stdout and stderr logs.
    """
    ...

def suspend(instance: metaflow.runner.deployer.TriggeredRun, **kwargs):
    """
    Suspend the running workflow.
    
    Parameters
    ----------
    **kwargs : Any
        Additional arguments to pass to the suspend command.
    
    Returns
    -------
    bool
        True if the command was successful, False otherwise.
    """
    ...

def unsuspend(instance: metaflow.runner.deployer.TriggeredRun, **kwargs):
    """
    Unsuspend the suspended workflow.
    
    Parameters
    ----------
    **kwargs : Any
        Additional arguments to pass to the unsuspend command.
    
    Returns
    -------
    bool
        True if the command was successful, False otherwise.
    """
    ...

def terminate(instance: metaflow.runner.deployer.TriggeredRun, **kwargs):
    """
    Terminate the running workflow.
    
    Parameters
    ----------
    **kwargs : Any
        Additional arguments to pass to the terminate command.
    
    Returns
    -------
    bool
        True if the command was successful, False otherwise.
    """
    ...

def status(instance: metaflow.runner.deployer.TriggeredRun):
    """
    Get the status of the triggered run.
    
    Returns
    -------
    str, optional
        The status of the workflow considering the run object, or None if the status could not be retrieved.
    """
    ...

def production_token(instance: metaflow.runner.deployer.DeployedFlow):
    """
    Get the production token for the deployed flow.
    
    Returns
    -------
    str, optional
        The production token, None if it cannot be retrieved.
    """
    ...

def delete(instance: metaflow.runner.deployer.DeployedFlow, **kwargs):
    """
    Delete the deployed flow.
    
    Parameters
    ----------
    **kwargs : Any
        Additional arguments to pass to the delete command.
    
    Returns
    -------
    bool
        True if the command was successful, False otherwise.
    """
    ...

def trigger(instance: metaflow.runner.deployer.DeployedFlow, **kwargs):
    """
    Trigger a new run for the deployed flow.
    
    Parameters
    ----------
    **kwargs : Any
        Additional arguments to pass to the trigger command, `Parameters` in particular
    
    Returns
    -------
    ArgoWorkflowsTriggeredRun
        The triggered run instance.
    
    Raises
    ------
    Exception
        If there is an error during the trigger process.
    """
    ...

class ArgoWorkflowsDeployer(metaflow.runner.deployer.DeployerImpl, metaclass=type):
    def __init__(self, deployer_kwargs, **kwargs):
        """
        Initialize the ArgoWorkflowsDeployer.
        
        Parameters
        ----------
        deployer_kwargs : dict
            The deployer-specific keyword arguments.
        **kwargs : Any
            Additional arguments to pass to the superclass constructor.
        """
        ...
    ...

