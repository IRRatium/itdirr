from __future__ import annotations

from typing import Any
from pydantic import Field, model_validator

from .base import ITDBaseModel
from .comment import Comment
from .pagination import Pagination


class Comments(ITDBaseModel):
    comments: list[Comment] = Field(default_factory=list)
    pagination: Pagination | None = None

    @model_validator(mode="before")
    @classmethod
    def normalize_structure(cls, payload: Any) -> Any:
        if not isinstance(payload, dict):
            return {"comments": []}

        if "replies" in payload:
            return {
                "comments": payload.get("replies", []),
                "pagination": payload.get("pagination"),
            }


        if "comments" in payload:
            return payload

        return {"comments": []}

Comments.model_rebuild()