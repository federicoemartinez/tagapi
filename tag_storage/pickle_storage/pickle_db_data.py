from __future__ import annotations
from dataclasses import dataclass, field

from sortedcontainers import SortedDict, SortedSet


@dataclass
class PickleDbData:
    tags: SortedDict[str, SortedSet[str]] = field(default_factory=SortedDict)  # tag_name -> object_names
    objects: SortedDict[str, SortedSet[str]] = field(default_factory=SortedDict)  # object_name -> tag_names