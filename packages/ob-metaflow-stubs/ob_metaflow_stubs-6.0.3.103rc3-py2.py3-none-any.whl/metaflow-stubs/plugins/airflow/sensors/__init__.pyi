##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.22.1+obcheckpoint(0.0.11);ob(v1)                              #
# Generated on 2024-09-20T21:42:44.619582                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.airflow.sensors.base_sensor

class ExternalTaskSensorDecorator(metaflow.plugins.airflow.sensors.base_sensor.AirflowSensorDecorator, metaclass=type):
    def serialize_operator_args(self):
        ...
    def validate(self, flow):
        ...
    ...

class S3KeySensorDecorator(metaflow.plugins.airflow.sensors.base_sensor.AirflowSensorDecorator, metaclass=type):
    def validate(self, flow):
        ...
    ...

SUPPORTED_SENSORS: list

