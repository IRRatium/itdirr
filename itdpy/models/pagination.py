from typing import Optional
from pydantic import Field
from .base import ITDBaseModel


class Pagination(ITDBaseModel):
    page: Optional[int] = 1
    limit: Optional[int] = 20
    total: Optional[int] = 0
    has_more: Optional[bool] = Field(False, alias="hasMore")

    def __repr__(self) -> str:
        return (
            f"<Pagination page={self.page} "
            f"limit={self.limit} total={self.total} "
            f"has_more={self.has_more}>"
        )
