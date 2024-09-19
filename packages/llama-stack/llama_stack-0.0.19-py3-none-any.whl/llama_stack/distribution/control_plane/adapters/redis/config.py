# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from llama_models.schema_utils import json_schema_type
from pydantic import BaseModel, Field


@json_schema_type
class RedisImplConfig(BaseModel):
    url: str = Field(
        description="The URL for the Redis server",
    )
    namespace: Optional[str] = Field(
        default=None,
        description="All keys will be prefixed with this namespace",
    )
