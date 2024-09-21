from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class CommonQualities(BaseModel):
    model_config = ConfigDict(extra="allow", alias_generator=to_camel)

    label: str | None = None
    description: str | None = None
    ref: str | None = Field(None, alias="sdfRef")

    def get_extra(self) -> dict[str, Any]:
        return self.__pydantic_extra__
