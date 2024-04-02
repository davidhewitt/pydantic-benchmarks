from __future__ import annotations

from datetime import datetime
from enum import Enum, IntEnum, auto
import json
from typing import Annotated, Literal
from pydantic import BaseModel
import timeit

import pydantic


class DataPointType(IntEnum):
    A = auto()
    B = auto()
    C = auto()


class DataPoint(BaseModel):
    x: int
    y: int
    type: DataPointType


class Samples(BaseModel):
    values: list[DataPoint]


data = {
    "values": [
        {"x": "1", "y": "5", "type": DataPointType.A},
        {"x": "2", "y": "4", "type": DataPointType.B},
        {"x": "3", "y": "3", "type": DataPointType.C},
        {"x": "4", "y": "2", "type": DataPointType.A},
        {"x": "5", "y": "1", "type": DataPointType.B},
    ]
    * 1_000
}

expression = "Samples.model_validate(data)"
if pydantic.__version__ < "2":
    expression = "Samples.validate(data)"

duration = timeit.timeit(
    expression,
    globals=globals(),
    number=1_000,
)

print("validate:", duration)

data_json = json.dumps(data)
expression = "Samples.model_validate_json(data_json)"
if pydantic.__version__ < "2":
    expression = "Samples.parse_raw(data_json)"

duration = timeit.timeit(
    expression,
    globals=globals(),
    number=1_000,
)

print("validate json:", duration)


# benchmark as per the same benchmark as msgspec uses
# # credit jcrist; see license in generate_data.py


class Permissions(Enum):
    READ = "READ"
    WRITE = "WRITE"
    READ_WRITE = "READ_WRITE"


class File(pydantic.BaseModel):
    type: Literal["file"] = "file"
    name: str
    created_by: str
    created_at: datetime
    updated_by: str | None = None
    updated_at: datetime | None = None
    nbytes: int
    permissions: Permissions


class Directory(pydantic.BaseModel):
    type: Literal["directory"] = "directory"
    name: str
    created_by: str
    created_at: datetime
    updated_by: str | None = None
    updated_at: datetime | None = None
    contents: list[Annotated[File | Directory, pydantic.Field(discriminator="type")]]


with open("data.json") as f:
    directory_data = f.read()

expression = "Directory.model_validate_json(directory_data)"
if pydantic.__version__ < "2":
    expression = "Directory.parse_raw(directory_data)"

duration = timeit.timeit(
    expression,
    globals=globals(),
    number=1_000,
)

print("msgspec validate benchmark", duration)
