##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.22.1+obcheckpoint(0.0.10);ob(v1)                              #
# Generated on 2024-09-20T19:26:01.407140                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow.plugins.airflow.sensors.base_sensor
    import metaflow.decorators

class AirflowSensorDecorator(metaflow.decorators.FlowDecorator, metaclass=type):
    def __init__(self, *args, **kwargs):
        ...
    def serialize_operator_args(self):
        """
        Subclasses will parse the decorator arguments to
        Airflow task serializable arguments.
        """
        ...
    def create_task(self):
        ...
    def validate(self, flow):
        """
        Validate if the arguments for the sensor are correct.
        """
        ...
    def flow_init(self, flow, graph, environment, flow_datastore, metadata, logger, echo, options):
        ...
    ...

class SensorNames(object, metaclass=type):
    @classmethod
    def get_supported_sensors(cls):
        ...
    ...

class AirflowException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

AIRFLOW_STATES: dict

class ExternalTaskSensorDecorator(metaflow.plugins.airflow.sensors.base_sensor.AirflowSensorDecorator, metaclass=type):
    def serialize_operator_args(self):
        ...
    def validate(self, flow):
        ...
    ...

