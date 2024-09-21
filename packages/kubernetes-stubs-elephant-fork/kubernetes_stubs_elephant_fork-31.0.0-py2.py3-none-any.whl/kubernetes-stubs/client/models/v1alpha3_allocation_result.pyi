import datetime
import typing

import kubernetes.client

class V1alpha3AllocationResult:
    controller: typing.Optional[str]
    devices: typing.Optional[kubernetes.client.V1alpha3DeviceAllocationResult]
    node_selector: typing.Optional[kubernetes.client.V1NodeSelector]
    
    def __init__(self, *, controller: typing.Optional[str] = ..., devices: typing.Optional[kubernetes.client.V1alpha3DeviceAllocationResult] = ..., node_selector: typing.Optional[kubernetes.client.V1NodeSelector] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3AllocationResultDict:
        ...
class V1alpha3AllocationResultDict(typing.TypedDict, total=False):
    controller: typing.Optional[str]
    devices: typing.Optional[kubernetes.client.V1alpha3DeviceAllocationResultDict]
    nodeSelector: typing.Optional[kubernetes.client.V1NodeSelectorDict]
