##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.22                                                            #
# Generated on 2024-09-20T00:45:49.668832                                        #
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

