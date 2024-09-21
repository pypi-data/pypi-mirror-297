import datetime
import typing

import kubernetes.client

class V1alpha3DeviceRequestAllocationResult:
    device: str
    driver: str
    pool: str
    request: str
    
    def __init__(self, *, device: str, driver: str, pool: str, request: str) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceRequestAllocationResultDict:
        ...
class V1alpha3DeviceRequestAllocationResultDict(typing.TypedDict, total=False):
    device: str
    driver: str
    pool: str
    request: str
