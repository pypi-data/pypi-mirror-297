import datetime
import typing

import kubernetes.client

class V1alpha3ResourceClaimSchedulingStatus:
    name: str
    unsuitable_nodes: typing.Optional[list[str]]
    
    def __init__(self, *, name: str, unsuitable_nodes: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3ResourceClaimSchedulingStatusDict:
        ...
class V1alpha3ResourceClaimSchedulingStatusDict(typing.TypedDict, total=False):
    name: str
    unsuitableNodes: typing.Optional[list[str]]
