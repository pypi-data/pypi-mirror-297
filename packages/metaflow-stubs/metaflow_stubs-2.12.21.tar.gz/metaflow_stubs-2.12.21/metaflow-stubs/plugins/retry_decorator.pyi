##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.21                                                            #
# Generated on 2024-09-19T17:04:54.871424                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

MAX_ATTEMPTS: int

class RetryDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        ...
    def step_task_retry_count(self):
        ...
    ...

