import datetime
import typing

import kubernetes.client

class V1alpha1LeaseCandidate:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1alpha1LeaseCandidateSpec]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1alpha1LeaseCandidateSpec] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1LeaseCandidateDict:
        ...
class V1alpha1LeaseCandidateDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1alpha1LeaseCandidateSpecDict]
