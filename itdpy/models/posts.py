from __future__ import annotations

from typing import Any
from pydantic import Field, model_validator

from .base import ITDBaseModel
from .post import Post
from .pagination import Pagination


class Posts(ITDBaseModel):
    posts: list[Post] = Field(default_factory=list)
    pagination: Pagination | None = None

    @model_validator(mode="before")
    @classmethod
    def parse_structure(cls, data: Any) -> Any:
        if isinstance(data, dict) and "data" in data:
            data = data["data"]

        if isinstance(data, list):
            return {"posts": data}

        if isinstance(data, dict):
            return {
                "posts": data.get("posts") or data.get("items") or [],
                "pagination": data.get("pagination"),
            }

        return {"posts": []}

    def __iter__(self):
        return iter(self.posts)

    def __getitem__(self, item):
        return self.posts[item]

    def __len__(self):
        return len(self.posts)

    def __repr__(self):
        return f"<Posts count={len(self.posts)}>"
