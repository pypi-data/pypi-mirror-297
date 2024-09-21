##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.21                                                            #
# Generated on 2024-09-19T17:04:54.917010                                        #
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

